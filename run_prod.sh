#!/bin/env sh

docker-compose up --detach --build  # Assembling containers and launching them
# Detached mode: Run containers in the background
# Build images before starting containers

docker ps --all --size --no-trunc  # Getting information about running containers with their size
# The "size" information shows the amount of data (on disk) that is used for the writable layer of each container