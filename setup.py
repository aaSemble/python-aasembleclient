#!/usr/bin/env python
#
#   Copyright 2015 aaSemble
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from setuptools import setup, find_packages

with open('requirements.txt', 'r') as fp:
    requirements = [x.strip() for x in fp]

setup(
    name='aasembleclient',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'aasemble = aasembleclient.main:main'
        ],
        'aasemble.client': [
            'repository-list = aasembleclient.repositories:List',
            'repository-source-list = aasembleclient.sources:ListByRepository',
            'source-list = aasembleclient.sources:List',
            'source-build-list = aasembleclient.builds:ListBySource',
            'build-list = aasembleclient.builds:List',
            'external-dependency-list = aasembleclient.external_dependencies:List',
        ],
    },

)
