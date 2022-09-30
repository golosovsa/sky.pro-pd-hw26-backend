docker system prune -f
# docker image prune --all -f

docker build . -t pg -f ./Dockers/my_postgresql/Dockerfile
docker build . -t api -f ./Dockers/api/Dockerfile


docker network create app_network

docker run --network app_network --network-alias hw_pg_host --name pg -e POSTGRES_USER=hw_pg -e POSTGRES_PASSWORD=hw_pg_password -e POSTGRES_DB=hw_db -d pg
docker run --network app_network -p 25000:25000 --name test_api -d api
