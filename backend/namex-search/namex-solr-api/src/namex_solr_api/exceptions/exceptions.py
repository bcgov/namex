# Copyright © 2023 Province of British Columbia
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
"""Application Specific Exceptions, to manage the business errors.

@log_error - a decorator to automatically log the exception to the logger provided

BusinessException - error, status_code - Business rules error
error - a description of the error {code / description: classname / full text}
status_code - where possible use HTTP Error Codes
"""
from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class BaseException(Exception):  # noqa: N818
    """Base exception class for custom exceptions."""

    error: str
    message: str = None
    status_code: HTTPStatus = None


@dataclass
class AuthorizationException(BaseException):
    """Authorization exception."""

    def __post_init__(self):
        """Return a valid AuthorizationException."""
        self.error = f"{self.error}, {self.status_code}"
        self.message = "Unauthorized access."
        self.status_code = HTTPStatus.UNAUTHORIZED


@dataclass
class BusinessException(BaseException):
    """Business rules exception."""

    def __post_init__(self):
        """Return a valid BusinessException."""
        if not self.message:
            self.message = "Business exception."


@dataclass
class DatabaseException(BaseException):
    """Database insert/update exception."""

    def __post_init__(self):
        """Return a valid DatabaseException."""
        self.message = "Database error while processing request."
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR


@dataclass
class ExternalServiceException(BaseException):
    """3rd party service exception."""

    def __post_init__(self):
        """Return a valid ExternalServiceException."""
        self.message = "3rd party service error while processing request."
        self.error = f"{self.error}, {self.status_code}"
        self.status_code = HTTPStatus.SERVICE_UNAVAILABLE


@dataclass
class SolrException(BaseException):
    """Solr search/update/delete exception."""

    def __post_init__(self):
        """Return a valid SolrException."""
        if self.status_code != HTTPStatus.SERVICE_UNAVAILABLE:
            self.error += f", {self.status_code}"
            self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.message = "Solr service error while processing request."
