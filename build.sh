#!/bin/bash

docker build -t frontend_image -f Dockerfile.app .
docker build -t openssl_hsm -f Dockerfile.hsm .
