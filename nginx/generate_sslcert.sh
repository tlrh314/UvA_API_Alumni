#!/bin/bash
set -e

STORAGE=${APIWEB_STORAGE-./storage/}certbot


echo "### Creating self-signed certificate for localhost ..."
mkdir -p "${STORAGE}/conf/live/api-alumni.nl"  # On the Docker host
LE_PATH="/etc/letsencrypt/live/api-alumni.nl"  # Inside the container
docker-compose -f docker-compose.yml run --rm --entrypoint "\
    openssl req -x509 -nodes -newkey rsa:1024 -days 1\
        -keyout '${LE_PATH}/privkey.pem' \
        -out '${LE_PATH}/fullchain.pem' \
        -subj '/CN=localhost'" certbot
echo
