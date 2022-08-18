docker build -t fast-text-rank-image .
docker run -d -p 5000:5000 --name fast-text-rank fast-text-rank-image:latest
docker update fast-text-rank --restart=always