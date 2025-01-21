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
"""Tests to assure the Flag Services.

Test-Suite to ensure that the Flag Service is working as expected.
"""
import pytest
from flask import Flask

from namex.models import User
from namex.services.flags import Flags


def test_flags_init():
    """Ensure that extension can be initialized."""
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = 'local'

    with app.app_context():
        flags = Flags(app)

    assert flags
    assert app.extensions['featureflags']


def test_flags_init_app():
    """Ensure that extension can be initialized."""
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = 'local'
    app.config['NAMEX_LD_SDK_ID'] = 'https://no.flag/avail'

    with app.app_context():
        flags = Flags()
        flags.init_app(app)
    assert app.extensions['featureflags']


def test_flags_init_app_production():
    """Ensure that extension can be initialized."""
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = 'production'
    app.config['NAMEX_LD_SDK_ID'] = 'https://no.flag/avail'

    with app.app_context():
        flags = Flags()
        flags.init_app(app)
    assert app.extensions['featureflags']


def test_flags_init_app_no_key_dev():
    """Assert that the extension is setup with a KEY, but in non-production mode."""
    app = Flask(__name__)
    app.config['NAMEX_LD_SDK_ID'] = None
    app.config['ENVIRONMENT'] = 'local'

    with app.app_context():
        flags = Flags()
        flags.init_app(app)
    assert app.extensions['featureflags']


def test_flags_init_app_no_key_prod():
    """Assert that prod with no key initializes, but does not setup the extension."""
    app = Flask(__name__)
    app.config['NAMEX_LD_SDK_ID'] = None
    app.config['ENVIRONMENT'] = 'production'

    with app.app_context():
        flags = Flags()
        flags.init_app(app)
        with pytest.raises(KeyError):
            client = app.extensions['featureflags']
            assert not client


def test_flags_bool_no_key_prod():
    """Assert that prod with no key initializes, but does not setup the extension."""
    app = Flask(__name__)
    app.config['NAMEX_LD_SDK_ID'] = None
    app.config['ENVIRONMENT'] = 'production'

    with app.app_context():
        flags = Flags()
        flags.init_app(app)
        on = flags.is_on('bool-flag')

    assert not on


def test_flags_bool():
    """Assert that a boolean (True) is returned, when using the local Flag.json file."""
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = 'local'
    app.config['NAMEX_LD_SDK_ID'] = 'https://no.flag/avail'

    with app.app_context():
        flags = Flags()
        flags.init_app(app)
        flag_on = flags.is_on('bool-flag')

        assert flag_on


def test_flags_bool_missing_flag(app):
    """Assert that a boolean (False) is returned when flag doesn't exist, when using the local Flag.json file."""
    from namex import flags
    app_env = app.config.get('ENVIRONMENT')
    try:
        with app.app_context():
            flag_on = flags.is_on('no flag here')

        assert not flag_on
    except:  # pylint: disable=bare-except; # noqa: B901, E722
        # for tests we don't care
        assert False
    finally:
        app.config['ENVIRONMENT'] = app_env


def test_flags_bool_using_current_app():
    """Assert that a boolean (True) is returned, when using the local Flag.json file."""
    from namex import flags
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = 'local'

    with app.app_context():
        flag_on = flags.is_on('bool-flag')

    assert flag_on


@pytest.mark.parametrize('test_name,flag_name,expected', [
    ('boolean flag', 'bool-flag', True),
    ('string flag', 'string-flag', 'a string value'),
    ('integer flag', 'integer-flag', 10),
    ('boolean flag', 'enable-won-emails', False),
])
def test_flags_bool_value(test_name, flag_name, expected):
    """Assert that a boolean (True) is returned, when using the local Flag.json file."""
    from namex import flags
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = 'local'

    with app.app_context():
        val = flags.value(flag_name)

    assert val == expected


def test_flag_bool_unique_user():
    """Assert that a unique user can retrieve a flag, when using the local Flag.json file."""
    app = Flask(__name__)
    app.config['ENVIRONMENT'] = 'local'
    app.config['NAMEX_LD_SDK_ID'] = 'https://no.flag/avail'

    user = User(username='username', firstname='firstname', lastname='lastname', sub='sub', iss='iss', idp_userid='123', login_source='IDIR')

    app_env = app.config['ENVIRONMENT']
    try:
        with app.app_context():
            flags = Flags()
            flags.init_app(app)
            app.config['ENVIRONMENT'] = 'local'
            val = flags.value('bool-flag', user)
            flag_on = flags.is_on('bool-flag', user)

        assert val
        assert flag_on
    except:  # pylint: disable=bare-except; # noqa: B901, E722
        # for tests we don't care
        assert False
    finally:
        app.config['ENVIRONMENT'] = app_env
