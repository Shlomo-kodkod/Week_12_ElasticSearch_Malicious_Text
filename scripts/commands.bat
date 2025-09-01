docker build -t kodkod1docker/elastic-malicious-text-system:v1.0 .

docker network create elastic

docker run -d --name elasticsearch --network elastic -p 9200:9200  -e "discovery.type=single-node" -e "xpack.security.enabled=false"
docker.elastic.co/elasticsearch/elasticsearch:9.1.3

docker run -d --name elastic-system --network elastic -p 8085:8085 -e ES_HOST=elasticsearch -e ES_PORT=9200 -e ES_INDEX=iranian