#!/bin/bash

# this script builds docker images for a given dockerfile and pushes them to a docker registry
# given the enviroment variables

image_name=$1
env=$2

# check if user has provided the image names and env
if [ -z "$image_name" ]; then
    echo "No image name provided. Exiting."
    exit 1
fi
    if [ -z "$env" ]; then
        echo "No env provided. Exiting."
        exit 1
    fi

#check if env is either dev or prod
if [ "$env" != "dev" ] && [ "$env" != "prod" ]; then
    echo "invalid, env must be either dev or prod"
    exit 1
fi
if [ "$env" == "dev" ]; then
    echo "Building image ${image_name} for dev"
    export KUBECONFIG=$HOME/.kube/config-rwml-dev
    echo "KUBECONFIG: $KUBECONFIG"
  	docker build -t ${image_name}:dev -f docker/${image_name}.dockerfile .
    kind load docker-image ${image_name}:dev --name rwml-34fa
else
    echo "Building image for prod"
    export KUBECONFIG=$HOME/.kube/rwml-production-test-kubeconfig.yaml
    echo "KUBECONFIG: $KUBECONFIG"
    docker buildx build --platform \
    linux/arm64,linux/amd64 -t \
    ghcr.io/mahmoudmoe84/${image_name}:0.1.6-beta.$(shell date +%s) \
    -f docker/${image_name}.dockerfile . --push
fi
 