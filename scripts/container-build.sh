#!/usr/bin/env bash

ENGINE=${ENGINE:-podman}
DOCKERHUB_USER=${DOCKERHUB_USER:-chevdor}
IMAGE=archery-competition-manager

$ENGINE build \
    -t $IMAGE \
    -t $DOCKERHUB_USER/$IMAGE \
    -t docker.io/$DOCKERHUB_USER/$IMAGE \
    .
$ENGINE images | grep $IMAGE
