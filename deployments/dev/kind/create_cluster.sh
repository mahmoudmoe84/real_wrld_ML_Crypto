#!/bin/bash
# Steps:

# 1. Delete the cluster (if it exists, otherwise it will fail)
echo "Deleting the cluster..."
kind delete cluster --name rwml-34fa

# 2. Delete the docker network (if it exists, otherwise it will fail)
echo "Deleting the docker network..."
docker network rm rwml-34fa-network

# 3. Create the docker network
echo "Creating the docker network..."
docker network create --subnet 172.100.0.0/16 rwml-34fa-network

# 4. Create the cluster
echo "Creating the cluster..."
KIND_EXPERIMENTAL_DOCKER_NETWORK=rwml-34fa-network kind create cluster --config ./kind-with-portmapping.yaml

# install kafka 
chmod +x ./install_kafka.sh
./install_kafka.sh

# Install Kafka UI
chmod +x ./install_kafka_ui.sh
./install_kafka_ui.sh

# Install RisingWave
chmod +x ./install_risingwave.sh
./install_risingwave.sh

# Install Grafana
chmod +x ./install_grafana.sh
./install_grafana.sh