"""
Backward-compatible helper functions for existing tests.
This module provides the same interface as existing test helpers but with proper isolation.
"""
from .test_data_factory import TestDataFactory, TestNameRequestBuilder

# Global factory instance for convenience
_factory = TestDataFactory()


def add_test_user_to_db():
    """
    Create a unique test user (backward compatible with existing tests).
    This replaces the old add_test_user_to_db() function with proper isolation.
    """
    return _factory.create_test_user()


def create_draft_nr():
    """
    Create a draft name request with unique data (backward compatible).
    """
    builder = TestNameRequestBuilder(_factory)
    return builder.with_user().create_draft_nr()


def build_test_input_fields(**overrides):
    """
    Build test input fields with unique data (backward compatible).
    """
    return _factory.create_test_nr_data(**overrides)


def make_unique_name(suffix='LTD'):
    """
    Generate a unique company name.
    """
    return _factory.generate_unique_name(suffix)


def make_unique_draft_nr_data(**overrides):
    """
    Create unique draft NR data for API calls.
    """
    return _factory.create_test_nr_data(**overrides)


def ensure_test_user_exists(username=None):
    """
    Ensure a test user exists, creating one if needed.
    Returns the user.
    """
    if username:
        # Try to find existing user first
        from namex.models import User
        user = User.query.filter_by(username=username).first()
        if user:
            return user

    # Create new unique user
    return _factory.create_test_user(username=username)


def get_test_user():
    """
    Get or create a test user for the current test.
    """
    return ensure_test_user_exists()
