import uuid
import json
import pytest
import base64
from http import HTTPStatus
from types import SimpleNamespace
from datetime import datetime, timezone
from simple_cloudevent import SimpleCloudEvent, to_queue_message

from namex_emailer.services.email_scheduler import (
    schedule_or_reschedule_email,
    cloud_scheduler_client,
)
from namex_emailer.services import ce_cache, queue
import namex_emailer.services.helpers as email_helpers
import namex_emailer.resources.worker as worker_module


@pytest.fixture(autouse=True)
def configure_app(app):
    app.config.update({
        "GCP_PROJECT": "test-project",
        "GCP_REGION": "test-region",
        "NAMEX_MAILER_TOPIC": "projects/test-project/topics/test-topic",
    })
    yield
    ce_cache.clear()


def make_dummy_job(full_name: str):
    class Stub: pass
    job = Stub()
    job.name = full_name
    return job


def make_dummy_ce(nr_num: str, option: str, scheduled=False):
    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f"/requests/{nr_num}",
        subject="namerequest",
        type="bc.registry.names.request",
        time="2025-06-09T12:00:00+00:00",
        data={"request": {"nrNum": nr_num, "option": option}}
    )
    if scheduled:
        ce.data["request"]["scheduled"] = True
    return ce


def make_dummy_pubsub_envelope(nr_num: str, option: str, scheduled: bool = False) -> dict:
    # 1) Build the CE
    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f"/requests/{nr_num}",
        subject="namerequest",
        type="bc.registry.names.request",
        time=datetime.now(timezone.utc).isoformat(),
        data={"request": {"nrNum": nr_num, "option": option}}
    )
    if scheduled:
        ce.data["request"]["scheduled"] = True

    # 2) Serialize & base64-encode
    raw = to_queue_message(ce)  # bytes
    b64 = base64.b64encode(raw).decode("utf-8")

    # 3) Wrap in the Pub/Sub push envelope
    return {
        "subscription": "projects/test-project/subscriptions/fake-sub",
        "message": {
            "data": b64,
        }
    }


def test_scheduler_creates_one_job_when_none_pending(monkeypatch, app):
    create_job_calls = []
    monkeypatch.setattr(cloud_scheduler_client, "list_jobs", lambda request: [])
    monkeypatch.setattr(cloud_scheduler_client, "delete_job", lambda request: pytest.fail("delete_job called"))
    monkeypatch.setattr(cloud_scheduler_client, "create_job", lambda request: create_job_calls.append(request))

    with app.app_context():
        dummy_ce = make_dummy_ce("NR 1234567", "APPROVED", scheduled=True)
        schedule_or_reschedule_email(dummy_ce)

    # Extract data that scheduler used to create the job
    scheduled_job = create_job_calls[0]["job"]
    scheduled_job_target = scheduled_job.pubsub_target
    scheduled_job_data = json.loads(scheduled_job_target.data.decode())

    # Assert that the scheduler used the proper params when creating the job
    assert len(create_job_calls) == 1
    assert create_job_calls[0]["parent"] == "projects/test-project/locations/test-region"
    assert "NR_1234567-APPROVED-" in scheduled_job.name
    assert scheduled_job_target.topic_name == app.config["NAMEX_MAILER_TOPIC"]
    assert scheduled_job_data["data"]["request"]["scheduled"] is True


def test_scheduler_deletes_then_creates_when_one_pending(monkeypatch, app):
    delete_job_calls = []
    create_job_calls = []
    existing_job_name = "projects/test-project/locations/test-region/jobs/NR_1234567-APPROVED-ecc041"
    monkeypatch.setattr(cloud_scheduler_client, "list_jobs", lambda request: [make_dummy_job(existing_job_name)])
    monkeypatch.setattr(cloud_scheduler_client, "delete_job", lambda request: delete_job_calls.append(request))
    monkeypatch.setattr(cloud_scheduler_client, "create_job", lambda request: create_job_calls.append(request))

    with app.app_context():
        dummy_ce = make_dummy_ce("NR 1234567", "REJECTED", scheduled=True)
        schedule_or_reschedule_email(dummy_ce)

    # Extract data that scheduler used to delete and create the job
    deleted_job = delete_job_calls[0]
    scheduled_job = create_job_calls[0]["job"]

    # Assert that the scheduler used the proper params when deleting and creating the job
    assert len(delete_job_calls) == 1
    assert len(create_job_calls) == 1
    assert deleted_job["name"] == existing_job_name
    assert "/jobs/NR_1234567-REJECTED-" in scheduled_job.name


def test_worker_immedietely_sends_scheduled_cloud_events(monkeypatch, client):
    create_job_calls = []
    sent_emails = []
    dummy_email = {
        "recipients": "user@example.com",
        "content": {
            "subject":   "NR 123 Approved",
            "body":      "<p>Your name request was approved.</p>",
            "attachments":[{"fileName":"NR_123_Approved.pdf","fileBytes":"cGRmYnl0ZXM=",
                            "fileUrl":"","attachOrder":"1"}]
        }
    }
    monkeypatch.setattr(worker_module, "process_email", lambda ce: dummy_email)
    monkeypatch.setattr(
        email_helpers, "send_email",
        lambda payload, token: sent_emails.append((payload, token)) or SimpleNamespace(status_code=HTTPStatus.OK)
    )
    monkeypatch.setattr(
        worker_module, "schedule_or_reschedule_email",
        lambda nr_num, option, cloud_event_payload: create_job_calls.append((nr_num, option))
    )
    monkeypatch.setattr(cloud_scheduler_client, "list_jobs",  lambda **_: [])
    monkeypatch.setattr(cloud_scheduler_client, "delete_job", lambda **_: None)

    resp = client.post("/", json=make_dummy_pubsub_envelope("NR 1234567", "CONDITIONAL", scheduled=True))
    assert resp.status_code == 200
    assert create_job_calls == []
    assert sent_emails, "Expected send_email to be called for scheduled CE"


def test_worker_skips_duplicate(monkeypatch, client):
    ce = make_dummy_ce("NR 1234567", "REJECTED", scheduled=False)
    ce_cache[ce.id] = ce
    monkeypatch.setattr(queue, "get_simple_cloud_event", lambda req: ce)

    # Neither scheduler nor send should be called
    never = lambda *args, **kw: (_ for _ in ()).throw(AssertionError("Should not be called"))
    monkeypatch.setattr(worker_module, "schedule_or_reschedule_email", never)
    monkeypatch.setattr(email_helpers, "send_email", never)

    resp = client.post("/", json={})
    assert resp.status_code == 200


def test_worker_schedules_and_caches(monkeypatch, client):
    ce = make_dummy_ce("NR 1234567", "CONDITIONAL", scheduled=False)
    create_job_calls = []
    monkeypatch.setattr(queue, "get_simple_cloud_event", lambda req: ce)
    monkeypatch.setattr(cloud_scheduler_client, "list_jobs",  lambda **_: [])
    monkeypatch.setattr(cloud_scheduler_client, "delete_job", lambda **_: None)

    monkeypatch.setattr(
        worker_module, "schedule_or_reschedule_email",
        lambda event: create_job_calls.append((
            event.data["request"]["nrNum"].replace(" ", "_"),
            event.data["request"]["option"]
        )) or "job-id"
    )

    resp = client.post("/", json={})
    assert resp.status_code == 200
    assert create_job_calls == [("NR_1234567", "CONDITIONAL")], "Expected one scheduling call"
    assert ce.id in ce_cache, "Expected CE ID to be stored in cache"
