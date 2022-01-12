# Copyright © c2021 Province of British Columbia
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
"""Name Request lookup values."""
from typing import Optional

from flask import Flask, current_app
from werkzeug.utils import cached_property

class NameRequestFilingActions:
    """Manages the mapping between NR types and the actions allowed in the target systems.

    This support the service signatures for Flask, but doesn't do anything special with it.
    """

    def __init__(self, app:Flask =None):
        """Initializer, supports setting the app context on instantiation."""
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Setup the extension.
        :param app: Flask app
        :return: naked
        """
        self.app = app
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        """Remove and cleanup after this service."""
        # the oracle session pool will clean up after itself
        # ctx = _app_ctx_stack.top
        # if hasattr(ctx, 'nro_oracle_pool'):


    # This is the raw mapping data.
    # This list will be collapsed to a dict type
    # multiple target systems is not supported
    # multiple filing actions per nr_type is supported
    # NR Type', 'LegalTypeCd', 'LegalTypeName', 'Filing Name', 'Target', 'entitiesFilingName', 'URL', 'learTemplate
    raw_nr_to_action_mapping =[
        ('CR', 'BC', 'B.C. Company', 'Incorporation', 'colin', None, None, None),
        ('CR', 'BC', 'B.C. Company', 'Amalgamation', 'colin', None, None, None),
        ('CCR', 'BC', 'B.C. Company', 'Change of Name', 'colin', None, None, None),
        ('CT', 'BC', 'B.C. Company', 'Continuation In', 'colin', None, None, None),
        ('RCR', 'BC', 'B.C. Company', 'Restoration', 'static', None, 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/permits-licences/businesses-incorporated-companies/forms-corporate-registry#information-packages', None),
        ('XCR', 'XP', 'Corporation (Foreign)', 'Extraprovincial Registration', 'colin', None, None, None),
        ('XCR', 'XP', 'Corporation (Foreign)', 'Extraprovincial Amalgamation', 'static', None, 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/permits-licences/businesses-incorporated-companies/forms-corporate-registry#forms', None),
        ('XCCR', 'XP', 'Corporation (Foreign)', 'Extraprovincial Change of Name', 'colin', None, None, None),
        ('XRCR', 'XP', 'Corporation (Foreign)', 'Extraprovincial Reinstatement', 'static', None, 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/permits-licences/businesses-incorporated-companies/forms-corporate-registry#information-packages', None),
        ('AS', 'XP', 'Corporation (Foreign)', 'Extraprovincial Assumed Name', 'static', None, 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/permits-licences/businesses-incorporated-companies/forms-corporate-registry#forms', None),
        ('LC', 'LLC', 'Extraprovincial Limited Liability Company', 'Extraprovincial Registration', 'static', None, 'https://www2.gov.bc.ca/assets/gov/employment-business-and-economic-development/business-management/permits-licences-and-registration/registries-packages/pack_33_xco_-_registration_statement_and_business_number_request.pdf', None),
        ('CLC', 'LLC', 'Extraprovincial Limited Liability Company', 'Extraprovincial Change of Name', 'static', None, 'https://www2.gov.bc.ca/assets/gov/employment-business-and-economic-development/business-management/permits-licences-and-registration/registries-forms/form_37_xco_-_name_change.pdf', None),
        ('RLC', 'LLC', 'Extraprovincial Limited Liability Company', 'Extraprovincial Reinstatement', 'static', None, 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/permits-licences/businesses-incorporated-companies/forms-corporate-registry#information-packages', None),
        ('AL', 'LLC', 'Extraprovincial Limited Liability Company', 'Extraprovincial Assumed Name', 'static', None, 'https://www2.gov.bc.ca/assets/gov/employment-business-and-economic-development/business-management/permits-licences-and-registration/registries-forms/form_37_xco_-_name_change.pdf', None),
        ('FR_FR', 'SP', 'Sole Proprietorship', 'Registration', 'lear', None, None, None),
        ('FR_DBA', 'SP', 'Sole Proprietorship (DBA)', 'Registration', 'lear', None, None, None),
        ('FR_GP', 'GP', 'General Partnership', 'Registration', 'lear', None, None, None),
        ('CFR_FR', 'CSP', 'Sole Proprietorship', 'Change of Name', 'lear', None, None, None),
        ('CFR_DBA', 'CSP', 'Sole Proprietorship (DBA)', 'Change of Name', 'lear', None, None, None),
        ('CFR_GP', 'CGP', 'General Partnership', 'Change of Name', 'lear', None, None, None),
        ('LL', 'LL', 'Limited Liability Partnership', 'Registration', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('CLL', 'LL', 'Limited Liability Partnership', 'Change of Name', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('XLL', 'XP', 'Extraprovincial Limited Liability Partnership', 'Registration', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('XCLL', 'XP', 'Extraprovincial Limited Liability Partnership', 'Change of Name', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('LP', 'LP', 'Limited Partnership', 'Registration', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('CLP', 'LP', 'Limited Partnership', 'Change of Name', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('XLP', 'XL', 'Extraprovincial Limited Partnership', 'Registration', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('XCLP', 'XL', 'Extraprovincial Limited Partnership', 'Change of Name', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('CP', 'CP', 'Cooperative', 'Incorporation', 'lear', 'incorporationApplication', None, "{'filing': {'header': {'name': {entitiesFilingName} }, '{entitiesFilingName}': {'nameRequest': {'nrNumber': '{nrNumber}', 'legalName': '{legalName}', 'legalType': '{legalType}'}}}}"),
        ('CP', 'CP', 'Cooperative', 'Amalgamation', 'lear', 'manual', None, None),
        ('CCP', 'CP', 'Cooperative', 'Change of Name', 'lear', 'changeOfName', None, "{'filing': {'header': {'name': {entitiesFilingName} }, '{entitiesFilingName}': {'nameRequest': {'nrNumber': '{nrNumber}', 'legalName': '{legalName}', 'legalType': '{legalType}'}}}}"),
        ('CTC', 'CP', 'Cooperative', 'Continuation In', 'lear', 'manual', None, None),
        ('RCP', 'CP', 'Cooperative', 'Restoration', 'lear', 'manual', None, None),
        ('XCP', 'XCP', 'Extraprovincial Cooperative', 'Incorporation', 'lear', 'manual', None, None),
        ('XCP', 'XCP', 'Extraprovincial Cooperative', 'Amalgamation', 'lear', 'manual', None, None),
        ('XCCP', 'XCP', 'Extraprovincial Cooperative', 'Change of Name', 'lear', 'manual', None, None),
        ('XRCP', 'XCP', 'Extraprovincial Cooperative', 'Restoration', 'lear', 'manual', None, None),
        ('CC', 'CCC', 'Community Contribution Co.', 'Incorporation', 'colin', None, None, None),
        ('CC', 'CCC', 'Community Contribution Co.', 'Amalgamation', 'colin', None, None, None),
        ('CCV', 'CCC', 'Community Contribution Co.', 'BC to CCC Conversion', 'colin', None, None, None),
        ('CCC', 'CCC', 'Community Contribution Co.', 'Change of Name', 'colin', None, None, None),
        ('CCCT', 'CCC', 'Community Contribution Co.', 'Continuation In', 'colin', None, None, None),
        ('RCC', 'CCC', 'Community Contribution Co.', 'Restoration', 'static', None, 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/permits-licences/businesses-incorporated-companies/forms-corporate-registry#information-packages', None),
        ('UL', 'ULC', 'Unlimited Liability Co.', 'Incorporation', 'colin', None, None, None),
        ('UL', 'ULC', 'Unlimited Liability Co.', 'Amalgamation', 'colin', None, None, None),
        ('UC', 'ULC', 'Unlimited Liability Co.', 'BC to ULC Conversion', 'colin', None, None, None),
        ('CUL', 'ULC', 'Unlimited Liability Co.', 'Change of Name', 'colin', None, None, None),
        ('ULCT', 'ULC', 'Unlimited Liability Co.', 'Continuation In', 'colin', None, None, None),
        ('RUL', 'ULC', 'Unlimited Liability Co.', 'Restoration', 'static', None, 'https://www2.gov.bc.ca/gov/content/employment-business/business/managing-a-business/permits-licences/businesses-incorporated-companies/forms-corporate-registry#information-packages', None),
        ('UA', 'A', 'Extraprovincial Unlimited Liability Company', 'Assumed', 'colin', None, None, None),
        ('XUL', 'A', 'Extraprovincial Unlimited Liability Company', 'Incorporation', 'colin', None, None, None),
        ('XCUL', 'A', 'Extraprovincial Unlimited Liability Company', 'Amalgamation', 'colin', None, None, None),
        ('XRUL', 'A', 'Extraprovincial Unlimited Liability Company', 'Restoration', 'colin', None, None, None),
        ('FI', 'FI', 'Financial Institution (BC)', 'Incorporation', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('CFI', 'FI', 'Financial Institution (BC)', 'Change of Name', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('RFI', 'FI', 'Financial Institution (BC)', 'Restoration', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('PA', 'PA', 'Private Act', 'Incorporation', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('PAR', 'PAR', 'Parish', 'Incorporation', 'static', None, 'https://www2.gov.bc.ca/gov/content/governments/organizational-structure/ministries-organizations/ministries/citizens-services/bc-registries-online-services', None),
        ('BC', 'BEN', 'BC Benefit Company Incorporation', 'Incorporation', 'lear', 'incorporationApplication', None, "{'filing': {'header': {'name': {entitiesFilingName} }, '{entitiesFilingName}': {'nameRequest': {'nrNumber': '{nrNumber}', 'legalName': '{legalName}', 'legalType': '{legalType}'}}}}"),
        ('BEAM', 'BEN', 'BC Benefit Company Incorporation', 'Amalgamation', 'lear', None, None, None),
        ('BEC', 'BEN', 'BC Benefit Company Incorporation', 'Change of Name', 'lear', 'alteration', None, "{'filing': {'header': {'name': {entitiesFilingName} }, '{entitiesFilingName}': {'nameRequest': {'nrNumber': '{nrNumber}', 'legalName': '{legalName}', 'legalType': '{legalType}'}}}}"),
        ('BECT', 'BEN', 'BC Benefit Company Incorporation', 'Continuation In', 'lear', None, None, None),
        ('BERE', 'BEN', 'BC Benefit Company Incorporation', 'Restoration', 'lear', None, None, None),
        ('BECV', 'BEN', 'BC Benefit Company Incorporation', 'Alteration', 'lear', 'alteration', None, "{'filing': {'header': {'name': {entitiesFilingName} }, '{entitiesFilingName}': {'nameRequest': {'nrNumber': '{nrNumber}', 'legalName': '{legalName}', 'legalType': '{legalType}'}}}}"),
        ('BECR', 'BEN', 'BC Benefit Company Incorporation', 'Convert to BC', 'lear', 'alteration', None, "{'filing': {'header': {'name': {entitiesFilingName} }, '{entitiesFilingName}': {'nameRequest': {'nrNumber': '{nrNumber}', 'legalName': '{legalName}', 'legalType': '{legalType}'}}}}"),
        ]

    @cached_property
    def get_dict(self) -> dict:
        """Return a dict of nr types to the target and filing actions.

        This takes the raw filing data and creates a dict."""
        current_app.logger.debug ('creating nr_filing_actions')
        d={}
        for (nr_type, legalType, legalTypeName, filingName, target, entitiesFilingName, URL, learTemplate) in self.raw_nr_to_action_mapping: # pylint: disable=W0612
            if nr_type not in d:
                d[nr_type] = {'legalType': legalType, 'target': target}

            actions = d[nr_type].get('actions', [])
            actions.append({'filingName': filingName, 'entitiesFilingName': entitiesFilingName, 'URL': URL, 'learTemplate': learTemplate})
            d[nr_type]['actions'] = actions

        current_app.logger.debug('completed creating nr_filing_actions')
        return d

    def get_actions(self, nr_type: str, entity_type_cd: str) -> Optional[dict]:
        """Return the target system and filing actions that a nr_type can be used for.

        Returns a dict with the following values:
        legalType: the short common legal types code, eg. 'BC', 'BEN'
        legalTypeName: convenience field with the legalType expanded
        filingName: common short filing name
        target: target system that provides the service
        actions: an Array of actions that the nr_type can be used for
            entitiesFilingName: business-schema name for the filing
            URL: the location of the service
            learTemplate: the templat that can be used to create a draft filing.
        """
        if nr_type in ['FR', 'CFR'] and entity_type_cd in ['FR', 'DBA', 'GP']:
            nr_type = nr_type + '_' + entity_type_cd

        return self.get_dict.get(nr_type)
