#!/bin/bash

if [ "$1" = "build" ]
then
    docker build -f Dockerfile.tools -t metabrainz/musicpod .
    exit
fi

if [ "$1" = "up" ]
then
    if [ $# -ge 1 ] 
    then 
        docker run -d --name musicpod-host --restart unless-stopped -v $2:/music -v `pwd`:/code/musicpod metabrainz/musicpod python3 musicpod/_dummy_loop.py
    else
        docker run -d --name musicpod-host --restart unless-stopped -v `pwd`:/code/musicpod metabrainz/musicpod python3 musicpod/_dummy_loop.py
    fi
    exit
fi

if [ "$1" = "down" ]
then
    docker rm -f musicpod-host
    exit
fi

if [ "$1" = "shell" ]
then
    docker exec -it musicpod-host bash
    exit
fi

docker exec -it musicpod-host python3 $@
