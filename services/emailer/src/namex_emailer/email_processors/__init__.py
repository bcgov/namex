# Copyright © 2019 Province of British Columbia
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
"""This module contains all of the Entity Email specific processors.

Processors hold the business logic for how an email is interpreted and sent.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Tuple

import requests
from flask import current_app, request
from gcp_queue.logging import structured_log


def substitute_template_parts(template_code: str) -> str:
    """Substitute template parts in main template.

    Template parts are marked by [[partname.html]] in templates.

    This functionality is restricted by:
    - markup must be exactly [[partname.html]] and have no extra spaces around file name
    - template parts can only be one level deep, ie: this rudimentary framework does not handle nested template
    parts. There is no recursive search and replace.
    """
    template_parts = ["nr-footer"]

    # substitute template parts - marked up by [[filename]]
    for template_part in template_parts:
        # src/namex_emailer/email_templates/common/nr-footer.html
        template_part_code = Path(
            f"{current_app.config.get('TEMPLATE_PATH')}/template-parts/name-request/{template_part}.html"
        ).read_text()
        template_code = template_code.replace("[[{}.html]]".format(template_part), template_part_code)

    return template_code


def get_main_template(request_action, template_name, status=None):
    """
    Retrieve the appropriate email template based on request action and status.

    The function first checks for a request-specific template.
    If not found, it looks for a status-based version.
    If still not found, it falls back to a common default template.

    Args:
        request_action (str): The category or type of request (e.g., "CNV", "AML").
        template_name (str): The name of the email template file (e.g., "NR-PAID.html").
        status (str, optional): The specific status subdirectory (e.g., "approved", "rejected"). Defaults to None.

    Returns:
        str: The content of the template if found, otherwise None.
    """
    base_path = Path(current_app.config.get("TEMPLATE_PATH", ""))

    # Check the request_action template first
    template_path = base_path / request_action / template_name
    if template_path.exists():
        return template_path.read_text()

    # Check the specific status-based template
    if status:
        template_path = base_path / request_action / status / template_name
        if template_path.exists():
            return template_path.read_text()

    structured_log(request, "DEBUG", f"Not Found the template from {request_action}/{status}/{template_name}")

    # Check the common template fallback
    common_template_path = base_path / "common" / template_name
    if common_template_path.exists():
        return common_template_path.read_text()

    # Check the status-based common template
    if status:
        common_template_path = base_path / "common" / status / template_name
        if common_template_path.exists():
            return common_template_path.read_text()

    # Log error if template not found
    structured_log(request, "ERROR", f"Failed to get {request_action}, {status}, {template_name} email template")
    return None
