#!/bin/env sh

docker ps --all --size  # Getting information about running containers with their size
# -s --size shows the amount of data (on disk) that is used for the writable layer of each container
# --no-trunc don't truncate output

# Stopping containers that were started using the docker 'compose up' command (attached volumes are also deleted)
docker compose down --volumes

# If there are other containers, then we stop them too
if [ -n "$(docker ps --quiet)" ]; then
    docker ps -q | xargs -I {} docker stop {}
else
    echo "All containers have already been stopped."
fi

# Removing all containers
if [ -n "$(docker ps --quiet --all)" ]; then
    docker ps -q -a | xargs -I {} docker rm {}
else
    echo "All containers have already been deleted."
fi

# Removing all images
if [ -n "$(docker images --quiet --all)" ]; then
    docker images -q -a | xargs -I {} docker image rm {}
else
    echo "All images have already been deleted."
fi

git pull  # Getting updates from the repository

# Removing all unnecessary files and directories
# -f, --force - ignore nonexistent files
# -r, --recursive - remove directories and their contents recursively
rm --recursive .github
rm --force LICENSE
rm --force test_build.sh
rm --force README.md
rm --force .gitignore

# Rebuilding containers after an update
bash run_prod.sh