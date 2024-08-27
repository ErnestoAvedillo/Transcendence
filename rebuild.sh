DOCKER_COMPOSE_FILE=./docker-compose.yml
VOLUMES=./volumes

docker compose -f $DOCKER_COMPOSE_FILE down --volumes

sudo find . -type d -name 'migrations' -exec rm -r {} +
sudo find . -type d -name '__pycache__' -exec rm -r {} +

sudo find . -type f -name 'db.sqlite3' -exec rm {} +

sudo rm -rf $VOLUMES
make volumes
docker compose -f $DOCKER_COMPOSE_FILE up --build -d db usermanagement matches gateway

#psql -U ${DB_USER} -d ${DB_NAME}