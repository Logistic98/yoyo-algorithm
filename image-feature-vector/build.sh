docker build -t image-feature-vector-image .
docker run -d -p 5004:5004 --name image-feature-vector -e TZ="Asia/Shanghai" image-feature-vector-image:latest
docker update image-feature-vector --restart=always