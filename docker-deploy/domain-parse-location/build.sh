docker build -t domain-parse-location-image .
docker run -d -p 5005:5005 --name domain-parse-location domain-parse-location-image:latest
docker update domain-parse-location --restart=always