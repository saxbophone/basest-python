#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from pip.req import parse_requirements
from setuptools import setup


def read(filepath):
    """
    Utility function to read the README file.
    """
    return open(os.path.join(os.path.dirname(__file__), filepath)).read()


def retrieve_deps(filepath):
    """
    Given a file path that points to a requirements file that pip can
    understand, parse it using pip's parser and return the requirements it
    contains as a list.
    """
    return [str(dep.req) for dep in parse_requirements(filepath, session=False)]


setup(
    name='basest',
    version='0.1.0',
    description='Converts symbols from any number base to any other number base',
    long_description=read('README.md'),
    url='https://github.com/saxbophone/basest-python',
    author='Joshua Saxby',
    author_email='joshua.a.saxby@gmail.com',
    license='Copyright 2016 Joshua Saxby',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: Education',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords='number base encoder decoder conversion encoding decoding',
    packages=['basest', 'tests',],
    install_requires=retrieve_deps('python_requirements/base.txt'),
    extras_require={
        'test': retrieve_deps('python_requirements/test.txt')
    },
    package_data={
        '': ['README.md', 'LICENSE'],
    },
    zip_safe=False,
)
