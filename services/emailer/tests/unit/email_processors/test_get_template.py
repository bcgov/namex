# Copyright © 2025 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Unit Tests for the pick up template."""
import base64
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

from flask import request
from sbc_common_components.utils.enums import QueueMessageTypes
from simple_cloudevent import SimpleCloudEvent

from namex_emailer.email_processors import get_main_template, nr_notification
from namex_emailer.services.helpers import as_legislation_timezone, format_as_report_string
from tests import MockResponse

from .. import helper_create_cloud_event

@pytest.mark.parametrize(
    ["test_name", "request_action", "status", "template_name", "response"],
    [
        ("get_main_template", "AML", "approved", "approved-modernized.md", "main"),
        ("get_main_template", "ASSUMED", None, "NR-EXPIRED.html", "main"),
        ("get_common_template", "INVALID", "approved", "approved-modernized.md", "common"),
        ("get_common_template", "INVALID", None, "NR-EXPIRED.html", "common"),
        ("no_template", "INVALID", None, "invalid_name.md", None)
    ],
)
@patch("gcp_queue.logging.structured_log")  # Mock logging
def test_nr_notification(
    app, mock_log, test_name, request_action, status, template_name, response
):
    """Assert that get the main template function."""
    result = get_main_template(request_action, template_name, status)
    if not response:
        assert result is None
        mock_log.assert_called_once_with(
            request, "ERROR", f"Failed to get {request_action}, {status}, {template_name} email template"
        )
    else:
        assert isinstance(result, str)
        if response == "common":
            mock_log.assert_called_once_with(
                request, "DEBUG", f"Not Found the template from {request_action}/{status}/{template_name}"
            )
