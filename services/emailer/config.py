# Copyright © 2023 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the 'License');
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""All of the configuration for the service is captured here.

All items are loaded, or have Constants defined here that
are loaded into the Flask configuration.
All modules and lookups get their configuration from the
Flask config, rather than reading environment variables directly
or by accessing this configuration directly.
"""

import os

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())


def get_named_config(config_name: str = "production"):
    """Return the configuration object based on the name.

    :raise: KeyError: if an unknown configuration is requested
    """
    if config_name in ["production", "staging", "default"]:
        config = Production()
    elif config_name == "testing":
        config = Testing()
    elif config_name == "development":
        config = Development()
    else:
        raise KeyError(f"Unknown configuration: {config_name}")
    return config


class Config:
    """Base class configuration that should set reasonable defaults.

    Used as the base for all the other configurations.
    """

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    ENVIRONMENT = os.getenv("APP_ENV", "prod")

    NAMEX_LD_SDK_ID = os.getenv("NAMEX_LD_SDK_ID", None)

    # variables
    LEGISLATIVE_TIMEZONE = os.getenv("LEGISLATIVE_TIMEZONE", "America/Vancouver")
    TEMPLATE_PATH = os.getenv("TEMPLATE_PATH", None)
    REPORT_TEMPLATE_PATH = os.getenv("TEMPLATE_PATH", None)

    # API Endpoints
    NOTIFY_API_URL = os.getenv("NOTIFY_API_URL", "")
    NOTIFY_API_VERSION = os.getenv("NOTIFY_API_VERSION", "")
    NAMEX_API_URL = os.getenv("NAMEX_API_URL", "")
    NAMEX_API_VERSION = os.getenv("NAMEX_API_VERSION", "")
    LEGAL_API_URL = os.getenv("LEGAL_API_URL", "https://legal-api-dev.apps.silver.devops.gov.bc.ca")
    LEGAL_API_VERSION = os.getenv("LEGAL_API_VERSION", "/api/v1")

    NOTIFY_API_URL = f"{NOTIFY_API_URL + NOTIFY_API_VERSION}/notify"
    NAMEX_SVC_URL = f"{NAMEX_API_URL + NAMEX_API_VERSION}"
    ENTITY_SVC_URL = f"{LEGAL_API_URL + LEGAL_API_VERSION}"

    REPORT_SVC_URL = f"{os.getenv('REPORT_API_URL', None)}{os.getenv('REPORT_API_VERSION', None)}/reports"

    # service accounts
    ACCOUNT_SVC_AUTH_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL")
    ACCOUNT_SVC_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
    ACCOUNT_SVC_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
    ACCOUNT_SVC_TIMEOUT = os.getenv("KEYCLOAK_TIMEOUT")

    ENTITY_SVC_AUTH_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL")
    ENTITY_SERVICE_ACCOUNT_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
    ENTITY_SERVICE_ACCOUNT_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")

    NAME_REQUEST_URL = os.getenv("NAME_REQUEST_URL", "")
    DECIDE_BUSINESS_URL = os.getenv("DECIDE_BUSINESS_URL", "")
    BUSINESS_URL = os.getenv("BUSINESS_URL", "")
    COLIN_URL = os.getenv("COLIN_URL", "")
    CORP_FORMS_URL = os.getenv("CORP_FORMS_URL", "")
    SOCIETIES_URL = os.getenv("SOCIETIES_URL", "")
    AUTH_WEB_URL = os.getenv("AUTH_WEB_URL", "")
    BUSINESS_REGISTRY_URL = os.getenv("BUSINESS_REGISTRY_URL", "https://business-registry-dev.web.app/en-CA/")
    STEPS_TO_RESTORE_URL = os.getenv("STEPS_TO_RESTORE_URL", "")

    PAYMENT_SVC_AUTH_URL = os.getenv("KEYCLOAK_AUTH_TOKEN_URL", "")
    PAYMENT_SVC_AUTH_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "")
    PAYMENT_SVC_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

    NAMES_INFORMATION_URL = os.getenv(
        "NAMES_INFORMATION_URL",
        "https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/\
permits-licences/businesses-incorporated-companies/approval-business-name",
    )

    # Cloud Tasks
    GCP_PROJECT = os.getenv("GCP_PROJECT", "")
    GCP_REGION = os.getenv("GCP_REGION", "")
    CLOUD_TASKS_QUEUE_ID = os.getenv("CLOUD_TASKS_QUEUE_ID", "")
    CLOUD_TASKS_INVOKER_SERVICE_ACCOUNT = os.getenv("CLOUD_TASKS_INVOKER_SERVICE_ACCOUNT", "")
    CLOUD_TASKS_HANDLER_URL = os.getenv("CLOUD_TASKS_HANDLER_URL", "")


class Development(Config):
    """Creates the Development Config object."""

    TESTING = False
    DEBUG = True


class Testing(Config):
    """In support of testing only.

    Used by the py.test suite
    """

    DEBUG = True
    TESTING = True
    DEPLOYMENT_ENV = "testing"
    TEMPLATE_PATH = "src/namex_emailer/email_templates"


class Production(Config):
    """Production environment configuration."""

    TESTING = False
    DEBUG = False
