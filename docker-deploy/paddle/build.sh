docker build -t paddle-image .
docker run -d -p 5001:5001 --name paddle paddle-image:latest
docker update paddle --restart=always