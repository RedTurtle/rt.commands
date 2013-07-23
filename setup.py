from setuptools import setup, find_packages

version = '0.1.3.dev0'

setup(name='rt.commands',
      version=version,
      description="Fabric scripts for RT",
      long_description="""\
""",
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
