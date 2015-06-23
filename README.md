# recast-newfrontend
attempt at a new frontend for RECAST


#instructions


    virtualenv venv
    source venv/bin/activate
    git clone git@github.com:lukasheinrich/recast-newfrontend.git
    cd recast-newfrontend
    pip install -e . --process-dependency-links

go to runarea 

create db

    recast-frontend-admin create_db --config myconfig.yaml

add some entries (models and db are provided as local vars in IPython session)

    recast-frontend-admin dbshell --config myconfig.yaml

run server

    recast-frontend server --config myconfig.yaml

run redis

    redis-server

run async worker

    recast-frontend celery --config ../runserver/myconfig.yaml

run REST API server

	recast-frontend rest_api --config ../runserver/myconfig.yaml