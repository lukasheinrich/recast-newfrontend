#!/usr/bin/sh

source VENV/bin/activate

heroku pg:reset HEROKU_POSTGRESQL_SILVER_URL --confirm recast-frontend

pip uninstall recast-database -y

pip install -e . --process-dependency-links

recast-frontend fill_db --config myconfig.yaml
