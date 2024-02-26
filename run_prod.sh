#!/bin/env sh

docker compose up --detach --build  # Assembling containers and launching them
# --detach run containers in the background
# --build build images before starting containers

docker ps --all --size  # Getting information about running containers with their size
# -s --size shows the amount of data (on disk) that is used for the writable layer of each container
# --no-trunc don't truncate output