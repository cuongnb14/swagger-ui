all: up

build:
	docker build -t cuongnb14/swagger_ui:0.1 .

docker-push:
	docker push cuongnb14/swagger_ui:0.1

docker-pull:
	docker pull cuongnb14/swagger_ui:0.1

up:
	docker-compose up -d

