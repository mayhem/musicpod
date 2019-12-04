#!/bin/bash

CHECK_MUSICPOD=`docker ps | grep musicpod-dev`
if [ -z "$CHECK_MUSICPOD" ]; then
    echo "musicpod-dev container not running. start it with develop.sh first."
    exit -1
fi
docker exec -it musicpod-dev python3 -m musicpod.bin.manage $@
