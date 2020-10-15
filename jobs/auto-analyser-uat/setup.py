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
import ast
import re
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')  # pylint: disable=invalid-name
with open('src/auto_analyser_uat/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(  # pylint: disable=invalid-name
        f.read().decode('utf-8')).group(1)))


def read_requirements(filename):
    """Get application requirements from the requirements.txt file."""
    with open(filename, 'r') as req:
        requirements = req.readlines()
    install_requires = [r.strip() for r in requirements if r.find('git+') != 0]
    return install_requires


REQUIREMENTS = read_requirements('requirements.txt')

setup(
    name='auto_analyser_uat',
    version=version,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS
)
