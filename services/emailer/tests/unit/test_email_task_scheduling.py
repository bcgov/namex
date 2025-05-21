import uuid

import pytest
from http import HTTPStatus
from simple_cloudevent import to_queue_message, SimpleCloudEvent

from namex_emailer.services.email_scheduler import schedule_or_reschedule_email, cloud_tasks_client
from namex_emailer.services import ce_cache


@pytest.fixture(autouse=True)
def configure_app(app):
    """Ensure all needed config keys are set to test the email scheduler."""
    app.config.update({
        "GCP_PROJECT":                               "test-project",
        "GCP_REGION":                                "test-region",
        "CLOUD_TASKS_QUEUE_ID":                      "test-queue",
        "CLOUD_TASKS_HANDLER_URL":                   "https://example.com/tasks/handle-send",
        "CLOUD_TASKS_INVOKER_SERVICE_ACCOUNT":       "sa-test@test.iam.gserviceaccount.com",
    })
    yield
    ce_cache.clear()


def make_fake_task(name: str):
    """
    Stub out the bare minimum of a CloudTasks Task for our tests.

    In production, list_tasks() returns a protobuf `Task` with many fields,
    but schedule_or_reschedule_email() only ever examines `task.name` to
    detect and cancel existing jobs. This stub gives us an object with
    exactly the `.name` attribute we need, without pulling in real GCP types.
    """
    class T: pass
    t = T()
    t.name = name
    return t


def test_schedule_creates_one_task_when_none_pending(monkeypatch, app):
    """
    Verify that when there are no existing tasks for a given NR number,
    schedule_or_reschedule_email schedules exactly one new Cloud Task
    using the correct queue, handler URL, and service account.
    """

    # Capture any tasks created
    created = []

    # 1) Simulate an empty queue: list_tasks() returns no tasks
    monkeypatch.setattr(cloud_tasks_client, "list_tasks", lambda parent: [])

    # 2) Ensure delete_task() is never called in this scenario
    monkeypatch.setattr(
        cloud_tasks_client,
        "delete_task",
        lambda name: (_ for _ in ()).throw(AssertionError("should not delete"))
    )

    # 3) Stub out create_task() to record its inputs instead of calling GCP
    def fake_create(parent, task):
        created.append((parent, task))
    monkeypatch.setattr(cloud_tasks_client, "create_task", fake_create)

    # 4) Invoke the scheduler within a Flask app context
    with app.app_context():
        schedule_or_reschedule_email("NR123", "APPROVED", {"foo": "bar"})

    # 5) Assert that exactly one task was created
    assert len(created) == 1
    parent, task = created[0]

    # 6) The queue path must use the configured project & region
    prefix = (
        f"projects/{app.config['GCP_PROJECT']}"
        f"/locations/{app.config['GCP_REGION']}/queues/"
    )
    assert parent.startswith(prefix), f"Queue path {parent} does not start with {prefix}"

    # 7) Inside the task payload, verify the HTTP request:
    req = task["http_request"]
    # The URL must match the configured handler endpoint
    assert req["url"] == app.config["CLOUD_TASKS_HANDLER_URL"]
    # The OIDC token must specify the configured service account
    assert (
        req["oidc_token"]["service_account_email"]
        == app.config["CLOUD_TASKS_INVOKER_SERVICE_ACCOUNT"]
    )


def test_schedule_deletes_existing_then_creates(monkeypatch, app):
    """
    Verify that when an in-flight task already exists for a given NR number,
    schedule_or_reschedule_email cancels it before creating a fresh one
    with the correct name and scheduling parameters.
    """
    # Prepare lists to capture calls
    deleted = []
    created = []

    # 1) Simulate an existing pending task in the queue for NR123
    fake_name = (
        "projects/test-project/locations/test-region/"
        "queues/test-queue/tasks/NR123-old-abc"
    )
    monkeypatch.setattr(
        cloud_tasks_client,
        "list_tasks",
        lambda parent: [make_fake_task(fake_name)]
    )

    # 2) Stub delete_task() to record which task name gets deleted
    monkeypatch.setattr(
        cloud_tasks_client,
        "delete_task",
        lambda name: deleted.append(name)
    )

    # 3) Stub create_task() to record the payload of the new task
    monkeypatch.setattr(
        cloud_tasks_client,
        "create_task",
        lambda parent, task: created.append(task)
    )

    # 4) Run the scheduler in the Flask app context
    with app.app_context():
        schedule_or_reschedule_email("NR123", "REJECTED", {"baz": "qux"})

    # 5) Assert the existing task was deleted exactly once
    assert deleted == [fake_name]

    # 6) Assert exactly one new task was created
    assert len(created) == 1

    # 7) Verify the new task’s name starts with "NR123-REJECTED-"
    new_task_name = created[0]["name"]
    assert "/tasks/NR123-REJECTED-" in new_task_name


@pytest.fixture
def example_ce():
    return SimpleCloudEvent(
        id=str(uuid.uuid4()),
        source="/requests/NR321",
        subject="namerequest",
        time="2025-05-14T12:00:00+00:00",
        type="bc.registry.names.request",
        data={"request": {"nrNum": "NR 321", "option": "APPROVED"}}
    )


def test_deliver_scheduled_email_success(client, monkeypatch, example_ce):
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
    body = to_queue_message(example_ce)
    calls = {}

    # 1) Spy on process_email()
    def fake_process_email(ce):
        calls['ce_for_email'] = ce
        return {"recipients": ["a@b.com"], "content": {"body": "ok"}}
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.process_email",
        fake_process_email
    )

    # 2) Spy on get_bearer_token()
    def fake_get_token():
        calls['got_token'] = True
        return "fake-token-123"
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.get_bearer_token",
        fake_get_token
    )

    # 3) Spy on send_email()
    class FakeResp:
        status_code = HTTPStatus.OK
    def fake_send_email(email_payload, token):
        calls['sent_email'] = {"payload": email_payload, "token": token}
        return FakeResp()
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.send_email",
        fake_send_email
    )

    # 4) Spy on write_to_events()
    def fake_write_to_events(ce, email_payload):
        calls['wrote_event'] = {"ce": ce, "email": email_payload}
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.write_to_events",
        fake_write_to_events
    )

    # 5) Hit the endpoint
    resp = client.post("/tasks/handle-send", data=body, content_type="application/json")
    assert resp.status_code == 200, resp.data.decode()
    assert example_ce.id in ce_cache

    # --- Now verify our spies ---

    # process_email got an event with the same ID
    assert calls['ce_for_email'].id == example_ce.id

    # get_bearer_token was called
    assert calls.get('got_token') is True

    # send_email saw the correct payload & token
    sent = calls['sent_email']
    assert sent["token"] == "fake-token-123"
    assert sent["payload"]["recipients"] == ["a@b.com"]
    assert sent["payload"]["content"]["body"] == "ok"

    # write_to_events saw an event with the same ID and the same payload
    wrote = calls['wrote_event']
    assert wrote["ce"].id == example_ce.id
    assert wrote["email"] == sent["payload"]


def test_deliver_scheduled_email_duplicate_skips(client, monkeypatch, example_ce):
    """
    Verify that if an incoming CloudEvent has already been processed (its ID is
    cached), the handler:
      1) does NOT attempt to send the email again, and
      2) still returns HTTP 200 to acknowledge receipt.
    """

    # 1) Prepare the raw CloudEvent JSON body as Cloud Tasks would deliver it
    body = to_queue_message(example_ce)

    # 2) Pre-mark this event ID in the cache to simulate a duplicate delivery
    ce_cache[example_ce.id] = example_ce

    # 3) Replace send_email() with a stub that fails if it's ever called
    #    (we expect the handler to skip sending for duplicates)
    monkeypatch.setattr(
        "namex_emailer.resources.scheduled_email_handler.send_email",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError(
            "send_email() should not be called for duplicates"
        ))
    )

    # 4) Invoke the handler endpoint with the duplicate event
    resp = client.post(
        "/tasks/handle-send",
        data=body,
        content_type="application/json"
    )

    # 5) Handler should still return 200 (to remove the task from the queue),
    #    but not attempt to send_email()
    assert resp.status_code == 200
