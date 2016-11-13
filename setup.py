#!/usr/bin/env python
"""DoLL project"""
from setuptools import find_packages, setup

setup(name='doll',
      version='0.3',
      description="Database of Latin Lexicon.",
      long_description="A database of the Latin lexicon, generated from the input files for   Whitaker's Words.",
      author="Matthew Badger",
      url="https://github.com/badge/doll",
      license="Apache",
      entry_points={
          'console_scripts': [
              'doll = doll.__main__:main'
          ]},
      packages=find_packages()
      )
