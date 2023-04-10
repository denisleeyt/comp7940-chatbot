#!/bin/bash

# Replace the following placeholders with your actual values
ECR_REGISTRY="053130898515.dkr.ecr.ap-southeast-1.amazonaws.com"
IMAGE_NAME="comp7940:latest"
CONTAINER_NAME="comp7940chatbot"

# Pull the latest Docker image from ECR
aws ecr get-login-password --region 'ap-southeast-1' | docker login --username AWS --password-stdin $ECR_REGISTRY
docker pull $ECR_REPOSITORY/$IMAGE_NAME:latest

# Stop and remove the old container if it's running
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true

# Start a new container with the updated image
docker run -d --name $CONTAINER_NAME -p 80:80 $ECR_REPOSITORY/$IMAGE_NAME:latest
