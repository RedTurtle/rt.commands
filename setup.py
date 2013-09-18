# -*- coding: utf-8 -*-
"""
rt.commands fabric stuff
"""
import os
from setuptools import setup, find_packages

version = '0.1.3'

def read(*rnames):
            return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGELOG.rst')
    + '\n'
    )

setup(name='rt.commands',
      version=version,
      description="Fabric scripts for RT",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author='RedTurtle developers',
      author_email='sviluppo@redturtle.it',
      url='http://www.redturtle.it',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', ]),
      include_package_data=True,
      namespace_packages=['rt'],
      zip_safe=False,
      install_requires=[
          # 'fabric'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
