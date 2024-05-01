#!/bin/env sh

echo ">> Assembling containers and launching them..."
bash run_prod.sh

# The -d flag is used to start services in the background,
# which allows you to continue working in the terminal without being tied to the process of running containers.

echo ">> sleep 5..."
sleep 5

echo ">> Stopping Docker Compose..."
docker compose down --volumes  # Stopping running containers
# --volumes - attached volumes are also deleted

echo ">> sleep 5"
sleep 5

echo ">> Checking the status of containers:"
docker ps