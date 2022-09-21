docker build -t image-feature-vector-image .
docker run -d -p 5004:5004 --name image-feature-vector image-feature-vector-image:latest
docker update image-feature-vector --restart=always