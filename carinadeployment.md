###deploying the frontend on carina


#### directory structure
    \
     +- recast-flask-frontend
	 |	\- carina-compose.yml 
     +- recast-rest-api

#### deployment recipe

    carina create recastfrontend --wait
    eval $(carina env recastfrontend)
    docker volume create --name datavolume
    docker volume create --name configvolume
    docker run -it -v configvolume:/configvolume --name config busybox true
    docker cp carinaconfig.yml config:/configvolume/config.yml
    docker-compose -f carina-compose.yml build
    docker-compose -f carina-compose.yml up -d
    docker exec -it recastflaskfrontend_recastfrontend_1 recast-frontend-admin create_db -c /configvolume/config.yml
    docker exec -it recastflaskfrontend_recastfrontend_1 recast-frontend fill_db -c /configvolume/config.yml
    #edit /etc/hosts so that ip shown in `docker ps` matches carinarecast.com
