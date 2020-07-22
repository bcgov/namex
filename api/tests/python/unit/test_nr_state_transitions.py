"""
Unit tests for Name Request state transitions.
"""

from namex.services.name_request.base_name_request import BaseNameRequest


def test_draft_to_reserved(client, jwt, app):
    instance = BaseNameRequest()
    pass


def test_draft_to_conditionally_reserved(client, jwt, app):
    pass


def test_conditionally_reserved_to_conditional(client, jwt, app):
    pass


def test_reserved_to_approved(client, jwt, app):
    pass


def test_conditional_to_hold(client, jwt, app):
    pass


def test_approved_to_hold(client, jwt, app):
    pass


def test_conditional_to_cancelled(client, jwt, app):
    pass


def test_approved_to_cancelled(client, jwt, app):
    pass


def test_conditional_to_rejected(client, jwt, app):
    pass


def test_approved_to_rejected(client, jwt, app):
    pass
