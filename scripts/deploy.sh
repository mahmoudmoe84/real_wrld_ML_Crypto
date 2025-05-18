#!/bin/bash

# this script deploys the docker images to the kubernetes cluster
# given the enviroment variables
image_name=$1
env=$2
# check if user has provided the image names and env
if [ -z "$image_name" ]; then
    echo "No image namechas been provided."
    exit 1
fi 

if [ -z "$env" ]; then
    echo "No env provided. Exiting."
    exit 1
fi

# check if env is either dev or prod
if [ "$env" != "dev" ] && [ "$env" != "prod" ]; then
    echo " invalid, env must be either dev or prod"
    exit 1
fi 

cd deployments/${env}
# echo "KUBECONFIG=${KUBECONFIG}"

if [ "$env" == "dev" ]; then
    export KUBECONFIG=$HOME/.kube/config-rwml-dev
else 
    export KUBECONFIG=$HOME/.kube/rwml-production-test-kubeconfig.yaml
fi
echo $KUBECONFIG
if [ "$env" == "dev" ]; then
    echo " deploying image ${image_name} for dev"
    kubectl delete -f ${image_name}/${image_name}.yaml --ignore-not-found=true
	kubectl apply -f ${image_name}/${image_name}.yaml

else	
    echo " deploying image ${image_name} for prod"
    kubectl delete -f ${image_name}/${image_name}.yaml --ignore-not-found=true
	kubectl apply -f ${image_name}/${image_name}.yaml
fi 