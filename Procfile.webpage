web: pip install -e . && recast-frontend-admin mk_config -o herokuconf.yaml && recast-frontend rest_api --config herokuconf.yaml
worker: pip install -e . && recast-frontend-admin mk_config -o herokuconf.yaml && recast-frontend celery --config herokuconf.yaml
