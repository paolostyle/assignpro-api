#!/bin/bash
imageName=assignpro-api
containerName=api

docker build -t $imageName .

echo Delete old container...
docker rm -f $containerName

echo Run new container...
docker run -d -p 80:80 --name $containerName $imageName
