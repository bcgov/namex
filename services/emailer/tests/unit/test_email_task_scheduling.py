import uuid
from http import HTTPStatus

import pytest
from simple_cloudevent import SimpleCloudEvent, to_queue_message

from namex_emailer.services import ce_cache
from namex_emailer.services.email_scheduler import cloud_tasks_client, schedule_or_reschedule_email


@pytest.fixture(autouse=True)
def configure_app(app):
    """Ensure all needed config keys are set to test the email scheduler."""
    app.config.update(
        {
            "GCP_PROJECT": "test-project",
            "GCP_REGION": "test-region",
            "CLOUD_TASKS_QUEUE_ID": "test-queue",
            "CLOUD_TASKS_HANDLER_URL": "https://example.com/tasks/handle-send",
            "CLOUD_TASKS_INVOKER_SERVICE_ACCOUNT": "sa-test@test.iam.gserviceaccount.com",
        }
    )
    yield
    ce_cache.clear()


def make_fake_task(nr_num: str, option: str):
    """Stub out the bare minimum of a CloudTasks Task for our tests."""

    class T:
        pass

    t = T()
    t.name = (
        "projects/test-project/locations/test-region/"
        f"queues/test-queue/tasks/{nr_num.replace(' ', '_')}-{option}-abc123"
    )
    return t


def make_fake_cloud_event(nr_num: str, option: str):
    """Example cloud event to be used for testing."""
    ce = SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source=f"/requests/{nr_num}",
        subject="namerequest",
        type="bc.registry.names.request",
        time="2025-06-09T12:00:00+00:00",
        data={"request": {"nrNum": nr_num, "option": option}},
    )
    return ce


def test_scheduler_creates_one_task_when_none_pending(monkeypatch, app):
    """
    Verify that when there are no existing tasks for a given NR number,
    schedule_or_reschedule_email schedules exactly one new Cloud Task
    using the correct queue, handler URL, and service account.
    """

    # Capture any tasks created
    created = []

    # 1) Required Monkeypatching
    monkeypatch.setattr(cloud_tasks_client, "list_tasks", lambda parent: [])
    monkeypatch.setattr(
        cloud_tasks_client, "delete_task", lambda *_: (_ for _ in ()).throw(AssertionError("should not delete"))
    )
    monkeypatch.setattr(cloud_tasks_client, "create_task", lambda parent, task: created.append((parent, task)))

    # 2) Invoke Cloud Tasks Scheduling
    with app.app_context():
        cloud_event = make_fake_cloud_event("NR 1234567", "APPROVED")
        schedule_or_reschedule_email(cloud_event)

    # 3) Extract data that cloud tasks used
    parent, task = created[0]
    prefix = f"projects/{app.config['GCP_PROJECT']}/locations/{app.config['GCP_REGION']}/queues/"
    req = task["http_request"]

    # 4) Assertions
    assert len(created) == 1
    assert parent.startswith(prefix)
    assert req["url"] == app.config["CLOUD_TASKS_HANDLER_URL"]
    assert req["oidc_token"]["service_account_email"] == app.config["CLOUD_TASKS_INVOKER_SERVICE_ACCOUNT"]


def test_scheduler_deletes_existing_then_creates(monkeypatch, app):
    """
    Verify that when an in-flight task already exists for a given NR number,
    schedule_or_reschedule_email cancels it before creating a fresh one
    with the correct name and scheduling parameters.
    """
    # Capture any tasks deleted & created
    deleted = []
    created = []

    # 1) Required Monkeypatching
    monkeypatch.setattr(cloud_tasks_client, "list_tasks", lambda parent: [make_fake_task("NR 1234567", "APPROVED")])
    monkeypatch.setattr(cloud_tasks_client, "delete_task", lambda name: deleted.append(name))
    monkeypatch.setattr(cloud_tasks_client, "create_task", lambda parent, task: created.append((parent, task)))

    # 4) Run the scheduler in the Flask app context
    with app.app_context():
        cloud_event = make_fake_cloud_event("NR 1234567", "REJECTED")
        schedule_or_reschedule_email(cloud_event)

    # 5) Assertions
    assert deleted == [make_fake_task("NR 1234567", "APPROVED").name]
    assert len(created) == 1
    assert "/tasks/NR_1234567-REJECTED-" in created[0][1]["name"]


def test_deliver_scheduled_email_success(client, monkeypatch):
    """
    Exercise the scheduled-email handler end-to-end, but spy on each
    key step so we can assert that:
      - process_email() is called with an event having the same ID,
      - get_bearer_token() is invoked,
      - send_email() is called with the right payload and token,
      - write_to_events() records the CloudEvent & email,
      - the handler returns 200, and
      - the CloudEvent ID is cached.
    """
    calls = {}

    # 1) Required Monkeypatching
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.process_email",
        lambda ce: (calls.setdefault("ce_for_email", ce), {"recipients": ["a@b.com"], "content": {"body": "ok"}})[1],
    )
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.get_bearer_token",
        lambda: (calls.setdefault("got_token", True), "fake-token-123")[1],
    )
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.send_email",
        lambda payload, token: (
            calls.setdefault("sent_email", {"payload": payload, "token": token}),
            type("FakeResp", (), {"status_code": HTTPStatus.OK})(),
        )[1],
    )
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.write_to_events",
        lambda ce, payload: calls.setdefault("wrote_event", {"ce": ce, "email": payload}),
    )

    # 2) Hit the endpoint
    cloud_event = make_fake_cloud_event("NR 1234567", "CONDITIONAL")
    body = to_queue_message(cloud_event)
    resp = client.post("/tasks/handle-send", data=body, content_type="application/json")

    # 3) Extract data that cloud tasks used
    sent = calls["sent_email"]
    wrote = calls["wrote_event"]

    # 4) Assertions
    assert resp.status_code == 200, resp.data.decode()
    assert cloud_event.id in ce_cache
    assert calls["ce_for_email"].id == cloud_event.id
    assert calls.get("got_token") is True
    assert sent["token"] == "fake-token-123"
    assert sent["payload"]["recipients"] == ["a@b.com"]
    assert sent["payload"]["content"]["body"] == "ok"
    assert wrote["ce"].id == cloud_event.id
    assert wrote["email"] == sent["payload"]


def test_deliver_scheduled_email_duplicate_skips(client, monkeypatch):
    """
    Verify that if an incoming CloudEvent has already been processed (its ID is
    cached), the handler:
      1) does NOT attempt to send the email again, and
      2) still returns HTTP 200 to acknowledge receipt.
    """

    # 1) Prepare the raw CloudEvent JSON body as Cloud Tasks would deliver it
    cloud_event = make_fake_cloud_event("NR 1234567", "CONDITIONAL")
    body = to_queue_message(cloud_event)

    # 2) Pre-mark this event ID in the cache to simulate a duplicate delivery
    ce_cache[cloud_event.id] = cloud_event

    # 3) Replace send_email() with a stub that fails if it's ever called
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.send_email",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("send_email() should not be called for duplicates")
        ),
    )

    # 4) Invoke the handler endpoint with the duplicate event
    resp = client.post("/tasks/handle-send", data=body, content_type="application/json")

    # 5) Handler should still return 200 but not attempt to send_email()
    assert resp.status_code == 200
