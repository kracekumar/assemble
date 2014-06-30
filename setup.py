#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = open('requirements.txt').read().splitlines()

test_requirements = list(requirements) + open('test_requirements.txt').read().splitlines()[1:]

setup(
    name='assemble',
    version='0.1.0',
    description='Make like build tool written in Python',
    long_description=readme + '\n\n' + history,
    author='Kracekumar Ramaraju',
    author_email='me@kracekumar.com',
    url='https://github.com/kracekumar/assemble',
    packages=[
        'assemble',
    ],
    package_dir={'assemble':
                 'assemble'},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'assemble = assemble.assemble:main',
        ]
    },
    license="BSD",
    zip_safe=False,
    keywords='assemble',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
