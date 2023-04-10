#!/bin/bash
# Stop the existing container if it's running
container_id=$(docker ps -aqf "name=comp7940chatbot")
if [ -n "$container_id" ]; then
  docker stop "$container_id"
  docker rm "$container_id"
fi
