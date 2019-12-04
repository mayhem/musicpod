#!/bin/bash

MUSIC_DIR=`echo "import config; print(config.MUSIC_DIR)" | python3 `
export MUSIC_DIR

if [ "$1" = "build" ]
then
    docker-compose -f docker-compose.dev.yml build
    exit
fi

if [ "$1" = "up" ]
then
    docker-compose -f docker-compose.dev.yml up -d
    exit
fi

if [ "$1" = "down" ]
then
    docker-compose -f docker-compose.dev.yml down
    exit
fi

docker-compose -f docker-compose.dev.yml up
