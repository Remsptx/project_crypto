#!/bin/bash

docker network create secret_link
docker run --name openssl_container -d --network secret_link openssl_hsm
docker run --name frontend_container -d -p 3000:3000 --network secret_link frontend_image

echo "Containers have been created and started."
