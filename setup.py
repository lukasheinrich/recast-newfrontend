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
    'Flask==0.10.1',
    'Flask-Login',
    'Flask-SQLAlchemy',
    'Flask-WTF',
    'flask-api',
    'click',
    'pyyaml',
    'celery',
    'redis',
    'IPython',
    'recast-database',
    'recast-search',
    'requests',
    'boto3',
    'elasticsearch',
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
    'https://github.com/cbora/recast-search/tarball/master#egg=recast-search-0.0.1',
  ]
)
