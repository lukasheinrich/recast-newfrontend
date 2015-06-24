from setuptools import setup, find_packages

setup(
  name = 'recast-newfrontend',
  description = 'new frontend for the RECAST project',
  url = 'https://github.com/lukasheinrich/recast-newfrontend',
  author = 'Lukas Heinrich',
  author_email = 'lukas.heinrich@cern.ch',
  packages=find_packages(),
  include_package_data = True,
  install_requires = [
    'Flask',
    'Flask-Login',
    'Flask-SQLAlchemy',
    'click',
    'pyyaml',
    'celery',
    'redis',
    'IPython',
    'recast-database',
    'requests',
    'psycopg2'
  ],
  entry_points = {
    'console_scripts': [
      'recast-frontend = recastfrontend.frontendcli:frontendcli',
      'recast-frontend-admin = recastfrontend.admincli:admincli',
    ]
  },
  dependency_links = [
    'https://github.com/recast-hep/recast-database/tarball/master#egg=recast-database-0.0.1',
  ]
)
