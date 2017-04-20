[![Build Status](https://travis-ci.org/recast-hep/recast-flask-frontend.svg?branch=master)](https://travis-ci.org/recast-hep/recast-flask-frontend)

# recast-newfrontend  
attempt at a new frontend for RECAST live at: http://recast-frontend.herokuapp.com/


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

deploying on Heroku
	
    mv Procfile.<x> Procfile 
    git add Procfile
    git commit -m 'bla'
    git push heroku master


##Docker instructions

	 docker-compose build
	 docker-compose up -d

create database

	docker-compose run recastfrontend recast-frontend-admin create_db

fill database with dummy data		  
     
     docker-compose run recastfrontend recast-frontend fill_db
     
     
