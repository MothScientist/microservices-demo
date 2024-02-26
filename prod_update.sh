#!/bin/env sh

docker ps --all --size --no-trunc  # Getting information about running containers with their size
# The "size" information shows the amount of data (on disk) that is used for the writable layer of each container

docker-compose down --volumes  # Stopping running containers (attached volumes are also deleted)

# Checking the absence of running containers in the system
if [ -n "$(docker ps --quiet)" ]; then
    docker ps -q | xargs -I {} docker stop {}
else
    echo "All containers were stopped successfully."
fi

# Removing all containers
if [ -n "$(docker ps --quiet --all)" ]; then
    docker ps -q -a | xargs -I {} docker rm {}
else
    echo "All containers were deleted successfully."
fi

# Delete all images
if [ -n "$(docker images --quiet --all)" ]; then
    docker images -q -a | xargs -I {} docker image rm {}
else
    echo "All images were deleted successfully."
fi

git pull  # Getting updates from the repository

# Removing unnecessary files and directories for work
rm -r .github
rm -f LICENSE
rm -f test_build.sh
rm -f README.md
rm -f .gitignore

# Rebuilding containers after an update
bash run_prod.sh