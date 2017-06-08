all: up

build:
	docker build -t cuongnb14/swagger_ui:0.1 .

docker-push:
	docker push cuongnb14/swagger_ui:0.1

docker-pull:
	docker pull cuongnb14/swagger_ui:0.1

pull:
	git pull && make restart

up:
	docker-compose up -d

restart:
	docker-compose restart swagger_ui
