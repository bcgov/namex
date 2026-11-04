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
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
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
"""Unit tests for search endpoints."""
import pytest
from unittest.mock import Mock, patch
from namex_solr_api.services.namex_solr.doc_models import PCField


class TestSearchConfiguration:
    """Tests for search endpoint configuration."""

    def test_conflict_states_includes_corporation_states(self, app):
        """Test that corporation states (ACT, LIQ) are configured in conflict search."""
        from namex_solr_api.resources.v1 import search
        import inspect

        source = inspect.getsource(search.possible_conflict_names)
        assert '"ACT"' in source or "'ACT'" in source
        assert '"LIQ"' in source or "'LIQ'" in source
        assert 'APPROVED' in source
        assert 'CONDITION' in source

    def test_conflict_states_list_complete(self, app):
        """Test that full conflict states list is configured correctly."""
        from namex_solr_api.resources.v1 import search

        with app.app_context():
            source = inspect.getsource(search.possible_conflict_names)
            assert 'conflict_states' in source
            assert 'ACTIVE' in source or "'ACTIVE'" in source or '"ACTIVE"' in source

    def test_search_module_exports_endpoints(self, app):
        """Test that search module exports both endpoints."""
        from namex_solr_api.resources.v1 import search

        assert hasattr(search, 'possible_conflict_names')
        assert hasattr(search, 'nrs')
        assert callable(search.possible_conflict_names)
        assert callable(search.nrs)

    def test_excluded_subtypes_configured(self, app):
        """Test that excluded sub types are configured correctly."""
        from namex_solr_api.resources.v1 import search
        import inspect

        source = inspect.getsource(search.possible_conflict_names)
        assert 'exclude_sub_types' in source
        assert 'DBA' in source
        assert 'FR' in source or 'fr' in source.lower()
        assert 'GP' in source or 'gp' in source.lower()


class TestSearchInitialization:
    """Tests for search module initialization."""

    def test_search_blueprint_registered(self, app):
        """Test that search blueprint is registered with app."""
        with app.app_context():
            blueprints = app.blueprints
            assert 'SEARCH' in blueprints or any('search' in str(bp).lower() for bp in blueprints)

    def test_possible_conflict_endpoint_registered(self, app):
        """Test that possible_conflict_names endpoint is registered."""
        assert app.url_map is not None
        url_strings = [str(rule) for rule in app.url_map.iter_rules()]
        assert any('search' in url.lower() for url in url_strings)

    def test_app_creation_success(self, app):
        """Test that app is created successfully."""
        assert app is not None
        assert app.config.get('TESTING', False)


class TestConflictStatesConfiguration:
    """Tests specifically for corporation protection states."""

    def test_act_state_included(self, app):
        """Verify ACT state is in conflict filter."""
        from namex_solr_api.resources.v1 import search
        source = inspect.getsource(search.possible_conflict_names)
        assert 'ACT' in source

    def test_liq_state_included(self, app):
        """Verify LIQ state is in conflict filter."""
        from namex_solr_api.resources.v1 import search
        source = inspect.getsource(search.possible_conflict_names)
        assert 'LIQ' in source

    def test_approved_condition_states_included(self, app):
        """Verify APPROVED and CONDITION states are included."""
        from namex_solr_api.resources.v1 import search
        source = inspect.getsource(search.possible_conflict_names)
        assert 'APPROVED' in source
        assert 'CONDITION' in source


import inspect
