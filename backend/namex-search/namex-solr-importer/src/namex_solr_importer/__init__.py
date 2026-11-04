# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
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
"""The NameX Solr Importer service.

This module loads all the data necessary for the NameX Solr Search.
"""

import os

from flask import Flask

from namex_solr_api.services import auth, solr
from namex_solr_importer.config import (
    DevelopmentConfig,
    ProductionConfig,
    UnitTestingConfig,
)
from namex_solr_importer.services import lear_db, namex_db, oracle_db
from namex_solr_importer.version import __version__
from structured_logging import StructuredLogging


def _get_build_openshift_commit_hash():
    return os.getenv("OPENSHIFT_BUILD_COMMIT", None)


def get_run_version():
    """Return a formatted version string for this service."""
    commit_hash = _get_build_openshift_commit_hash()
    if commit_hash:
        return f"{__version__}-{commit_hash}"
    return __version__


def register_shellcontext(app: Flask):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"app": app}

    app.shell_context_processor(shell_context)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": UnitTestingConfig,
}


def create_app(
    config_name: str = os.getenv("DEPLOYMENT_ENV", "production") or "production",
):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, ProductionConfig))
    app.logger = StructuredLogging(app).get_logger()
    solr.init_app(app)
    auth.init_app(app)
    # Init relevant dbs
    if app.config["INCLUDE_COLIN_LOAD"]:
        oracle_db.init_app(app)
    if app.config["INCLUDE_LEAR_LOAD"]:
        lear_db.init_app(app)
    if app.config["INCLUDE_NAMEX_LOAD"] or app.config["INCLUDE_SYNONYM_LOAD"]:
        namex_db.init_app(app)

    register_shellcontext(app)

    return app
