# Copyright © 2023 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Exception responses."""
from http import HTTPStatus

from flask import current_app, jsonify

from .exceptions import BaseException

QUERY_TOO_COMPLEX = "QUERY_TOO_COMPLEX"
QUERY_TOO_COMPLEX_MESSAGE = (
    "This name is too complex for conflict search. Remove a word and try again."
)


def is_query_too_complex(error: object) -> bool:
    text = str(error or "").lower()
    return "toomanyclauses" in text or "maxclausecount" in text


def bad_request_response(message: str, errors: list[dict[str, str]] | None = None):
    """Build generic bad request response."""
    return jsonify({"message": message, "details": errors or []}), HTTPStatus.BAD_REQUEST


def exception_response(exception: BaseException):
    """Build exception error response."""
    details = repr(exception)
    current_app.logger.error(details)
    error_text = getattr(exception, "error", None) or details
    if is_query_too_complex(error_text):
        return jsonify({
            "code": QUERY_TOO_COMPLEX,
            "message": QUERY_TOO_COMPLEX_MESSAGE,
        }), HTTPStatus.UNPROCESSABLE_ENTITY
    try:
        message = exception.message or "Error processing request."
        status_code = exception.status_code or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception:
        current_app.logger.warning("Uncaught exception.")
        message = "Error processing request."
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return jsonify({"message": message, "detail": details}), status_code
