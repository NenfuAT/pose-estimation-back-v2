-include .env

build:
	docker compose build

up:
	docker compose up -d

down:
	docker-compose down

log:
	docker compose logs

go:
	docker exec -it $(GO_CONTAINER_HOST) /bin/sh