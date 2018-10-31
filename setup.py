#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, 2018, Joshua Saxby <joshua.a.saxby@gmail.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import os

from pip.req import parse_requirements
from pypandoc import convert_text
from setuptools import find_packages, setup


def readme(filepath):
    """
    Utility function to convert the README file to RST format and return it.
    """
    return convert_text(
        open(os.path.join(os.path.dirname(__file__), filepath)).read(),
        'rst', format='md'
    )


def retrieve_deps(filepath):
    """
    Given a file path that points to a requirements file that pip can
    understand, parse it using pip's parser and return the requirements it
    contains as a list.
    """
    return [
        str(dep.req) for dep in parse_requirements(filepath, session=False)
    ]


setup(
    name='basest',
    version='0.7.0',
    description=(
        'Converts symbols from any number base to any other number base'
    ),
    long_description=readme('README.md'),
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
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
    packages=find_packages(),
    install_requires=retrieve_deps('python_requirements/base.txt'),
    extras_require={
        'test': retrieve_deps('python_requirements/test.txt'),
        'build': retrieve_deps('python_requirements/build.txt'),
    },
    package_data={
        '': ['README.md', 'LICENSE'],
    },
    zip_safe=False
)
