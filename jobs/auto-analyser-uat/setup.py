# Copyright © 2020 Province of British Columbia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Installer and setup for this module."""
from setuptools import setup


def read_requirements(filename):
    """Get application requirements from the requirements.txt file."""
    with open(filename, 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements if r.find('git+') != 0]
    return install_requires


REQUIREMENTS = read_requirements('requirements.txt')

setup(
    name='auto_analyser_uat',
    py_modules=['auto_analyser_uat.py'],
    zip_safe=False,
    install_requires=REQUIREMENTS
)
