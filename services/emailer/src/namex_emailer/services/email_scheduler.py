import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import uuid

from flask import current_app, request
from google.cloud.scheduler_v1 import CloudSchedulerClient, Job, PubsubTarget
from namex_emailer.constants.notification_options import DECISION_OPTIONS, Option
from gcp_queue.logging import structured_log
from simple_cloudevent import to_structured


# Singleton GCP Cloud Scheduler Client
cloud_scheduler_client = CloudSchedulerClient()


def is_scheduled_cloud_event(ce) -> bool:
    return bool(ce.data.get("request", {}).get("scheduled", False))


def is_schedulable(ce) -> bool:
    option = ce.data.get("request", {}).get("option")
    return Option(option) in DECISION_OPTIONS if option else False


def cleanup_scheduled_job(ce):
    nr_num = ce.data["request"]["nrNum"].replace(" ", "_")
    parent = f"projects/{current_app.config['GCP_PROJECT']}/locations/{current_app.config['GCP_REGION']}"

    # Remove any pending jobs for this NR number
    for job in cloud_scheduler_client.list_jobs(request={"parent": parent}):
        existing_id = job.name.rsplit("/", 1)[-1]
        if existing_id.startswith(nr_num):
            cloud_scheduler_client.delete_job(request={"name": job.name})
            structured_log(request, "INFO", f"Cancelled scheduled email job '{existing_id}'")


def schedule_or_reschedule_email(ce):
    """
    Cancel any in-flight email job for this nr number and schedule a new one 5 minutes out.
    This is only used for approved, conditional, and rejected emails that are not resends.
    """
    # Scheduler constants
    payload = to_structured(ce)
    scheduler_parent = f"projects/{current_app.config["GCP_PROJECT"]}/locations/{current_app.config["GCP_REGION"]}"
    pubsub_topic = current_app.config["NAMEX_MAILER_TOPIC"]
    nr_num = payload["data"]["request"]["nrNum"].replace(" ", "_")
    option = payload["data"].get("request", {}).get("option")

    # Create a cron 5 minutes in the future
    fire_time = datetime.now(tz=ZoneInfo("America/Vancouver")) + timedelta(minutes=5)
    cron = f"{fire_time.minute} {fire_time.hour} {fire_time.day} {fire_time.month} *"

    # 1) Remove any pending jobs for this NR number
    for job in cloud_scheduler_client.list_jobs(request={"parent": scheduler_parent}):
        existing_id = job.name.rsplit("/", 1)[-1]
        if existing_id.startswith(nr_num):
            cloud_scheduler_client.delete_job(request={"name": job.name})
            structured_log(request, "INFO", f"Cancelled scheduled email job '{existing_id}'")

    # 2) Tag and prepare Pub/Sub target
    payload.setdefault("data", {}).setdefault("request", {})["scheduled"] = True
    target = PubsubTarget(
        topic_name=pubsub_topic,
        data=json.dumps(payload).encode()
    )

    # 3) build and create the job
    job_id = f"{nr_num}-{option}-{uuid.uuid4().hex[:6]}"
    job = Job(
        name=f"{scheduler_parent}/jobs/{job_id}",
        pubsub_target=target,
        schedule=cron,
        time_zone="America/Vancouver"
    )
    cloud_scheduler_client.create_job(request={"parent": scheduler_parent, "job": job})
    structured_log(request, "INFO", f"Scheduled email job '{job_id}'")
