#!/bin/bash 

docker rm -f fast-text-rank
docker rmi -f fast-text-rank-image

docker rm -f google-translate-crack
docker rmi -f google-translate-crack-image

docker rm -f gtts
docker rmi -f gtts-image

docker rm -f paddle
docker rmi -f paddle-image

docker rm -f domain-parse-location
docker rmi -f domain-parse-location-image