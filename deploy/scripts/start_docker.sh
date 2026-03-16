#!/bin/bash

# Log everything
exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging in to ECR..."

aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin 891377050051.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling Docker image..."

docker pull 891377050051.dkr.ecr.ap-south-1.amazonaws.com/spotify_recommender_system:latest

echo "Stopping existing container if running..."

if [ "$(docker ps -q -f name=spotify_recommender_system)" ]; then
    docker stop spotify_recommender_system
fi

echo "Removing existing container if present..."

if [ "$(docker ps -aq -f name=spotify_recommender_system)" ]; then
    docker rm spotify_recommender_system
fi

echo "Starting new container..."

docker run -d -p 80:8000 \
--name spotify_recommender_system \
-e DAGSHUB_USER_TOKEN=$DAGSHUB_USER_TOKEN \
891377050051.dkr.ecr.ap-south-1.amazonaws.com/spotify_recommender_system:latest

echo "Container started successfully."