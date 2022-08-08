container_id=$(docker ps|grep reverse-proxy|awk {'print $1'})
docker exec -it $container_id nginx -s reload
