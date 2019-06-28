#!/usr/bin/env bash
echo "Reloading Nginx container ${NGINX_CONTAINER}"
docker container exec ${NGINX_CONTAINER} nginx -s reload
