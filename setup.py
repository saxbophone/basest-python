#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, 2018, Joshua Saxby <joshua.a.saxby@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from __future__ import absolute_import, division, print_function

import os

from setuptools import find_packages, setup


def parse_requirements(filepath):
    """
    Load requirements from a pip requirements file
    """
    lines = (line.strip() for line in open(filepath))
    return [line for line in lines if line and not line.startswith('#')]


setup(
    name='basest',
    version='0.7.3',
    description='Arbitrary base binary-to-text encoder (any base to any base)',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.md')
    ).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/saxbophone/basest-python',
    author='Joshua Saxby',
    author_email='joshua.a.saxby@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
        'Topic :: Education',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',  # noqa
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords='number base encoder decoder conversion encoding decoding',
    packages=find_packages(exclude=['tests']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    install_requires=[],
    package_data={
        '': ['README.md', 'LICENSE'],
    },
    zip_safe=False
)
