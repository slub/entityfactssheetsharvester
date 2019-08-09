"""
A commandline command (Python3 program) that retrieves EntityFacts sheets from a given CSV with GND identifiers and returns them as line-delimited JSON records.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='entityfactssheetsharvester',
      version='0.0.1',
      description='a commandline command (Python3 program) that retrieves EntityFacts sheets from a given CSV with GND identifiers and returns them as line-delimited JSON records',
      url='https://github.com/slub/entityfactssheetsharvester',
      author='Bo Ferri',
      author_email='zazi@smiy.org',
      license="Apache 2.0",
      packages=[
          'entityfactssheetsharvester',
      ],
      package_dir={'entityfactssheetsharvester': 'entityfactssheetsharvester'},
      install_requires=[
          'argparse>=1.4.0',
          'requests>=2.22.0',
          'rx>=3.0.1'
      ],
      entry_points={
          "console_scripts": ["entityfactssheetsharvester=entityfactssheetsharvester.entityfactssheetsharvester:run"]
      }
      )
