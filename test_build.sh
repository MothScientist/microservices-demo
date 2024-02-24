#!/bin/env sh

echo ">> Building Docker Compose..."
docker-compose build

echo ">> Running Docker Compose..."
docker-compose up -d

# The -d flag is used to start services in the background,
# which allows you to continue working in the terminal without being tied to the process of running containers.

echo ">> sleep 5..."
sleep 5

echo ">> Checking the status of containers:"
docker ps -s
# The -s flag allows you to get information about the sizes of containers

echo ">> Stopping Docker Compose and removing containers..."
docker-compose down -v

echo ">> sleep 5"
sleep 5

echo ">> Checking the status of containers:"
docker-compose ps