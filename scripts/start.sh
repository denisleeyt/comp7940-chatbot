#!/bin/bash
# Replace the variables below with your actual ECR registry and image name
ECR_REGISTRY="053130898515.dkr.ecr.ap-southeast-1.amazonaws.com"
IMAGE_NAME="comp7940:latest"

# Pull the latest image from ECR
docker pull "$ECR_REGISTRY/$IMAGE_NAME"

# Start a new container using the latest image
docker run -d --name comp7940chatbot -p 80:80 "$ECR_REGISTRY/$IMAGE_NAME"
