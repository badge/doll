#!/usr/bin/env python
"""DoLL project"""
from setuptools import find_packages, setup

setup(name = 'DoLL',
    version = '0.1',
    description = "Database of Latin Lexicon.",
    long_description = "A database of the Latin lexicon, generated from the input files for Whitaker's Words.",
    author="Matthew Badger",
    url="https://github.com/badge/doll",
    license = "Apache",
    packages=find_packages()
    )