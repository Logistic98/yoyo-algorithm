docker build -t google-translate-crack-image .
docker run -d -p 5002:5002 --name google-translate-crack google-translate-crack-image:latest
docker update google-translate-crack --restart=always