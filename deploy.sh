#!/bin/bash

AWSID="123456789012"
REGION="ca-central-1"
IMAGE="lambda-telegram-macbook"

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWSID.dkr.ecr.$REGION.amazonaws.com    
aws ecr create-repository --repository-name $IMAGE --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
docker tag  $IMAGE:latest $AWSID.dkr.ecr.$REGION.amazonaws.com/$IMAGE:latest
docker push $AWSID.dkr.ecr.$REGION.amazonaws.com/$IMAGE:latest        
