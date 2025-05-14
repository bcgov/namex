import json
from datetime import datetime, timezone, timedelta
import uuid

from flask import current_app, request
from gcp_queue.logging import structured_log
from google.cloud.tasks_v2 import CloudTasksClient, HttpMethod
from google.protobuf import timestamp_pb2


# Singleton GCP Cloud Tasks Client
cloud_tasks_client = CloudTasksClient()


def schedule_or_reschedule_email(nr_num: str, option: str, cloud_event_payload: dict):
    """
    Cancel any in-flight email task for this nr number and schedule a new one 5 minutes out.
    This is only used for approved, conditional, and rejected emails that are not resends.
    """

    # Identify the queue
    remote_queue_path = cloud_tasks_client.queue_path(
        project=current_app.config["GCP_PROJECT"],
        location=current_app.config["GCP_REGION"],
        queue=current_app.config["CLOUD_TASKS_QUEUE_ID"],
    )
    # Create a timestamp 5 minutes in the future
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(datetime.now(timezone.utc) + timedelta(minutes=5))

    # 1) Remove any pending email tasks for this NR number
    for task in cloud_tasks_client.list_tasks(parent=remote_queue_path):
        existing_id = task.name.rsplit("/", 1)[-1]
        if existing_id.startswith(nr_num):
            structured_log(request, "INFO", f"Cancelled pending Cloud Tasks job '{existing_id}' for {nr_num}")
            cloud_tasks_client.delete_task(name=task.name)

    # 2) Generate a unique task ID for the NR number: 'NR_123456-APPROVED-43255d'
    task_id = f"{nr_num}-{option}-{uuid.uuid4().hex[:6]}"

    # 3) Build the full remote queue path including the task id
    task_name = cloud_tasks_client.task_path(
        project=current_app.config["GCP_PROJECT"],
        location=current_app.config["GCP_REGION"],
        queue=current_app.config["CLOUD_TASKS_QUEUE_ID"],
        task=task_id
    )

    # 4) Assemble the Cloud Task
    task = {
        "name":             task_name,
        "schedule_time":    timestamp,
        "http_request": {
            "http_method":  HttpMethod.POST,
            "url":          current_app.config["CLOUD_TASKS_HANDLER_URL"],
            "headers":      {"Content-Type": "application/json"},
            "body":         json.dumps(cloud_event_payload).encode("utf-8"),
            "oidc_token": {
                "service_account_email": current_app.config["CLOUD_TASKS_INVOKER_SERVICE_ACCOUNT"]
            }
        }
    }

    # 5) Enqueue the task to come back to the emailer at deliver_scheduled_email() endpoint in 5 minutes time
    cloud_tasks_client.create_task(parent=remote_queue_path, task=task)
