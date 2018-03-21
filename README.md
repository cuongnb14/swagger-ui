Swagger Editor UI
==========

The interface to create swagger doc 

Install
--------

#### Build image: 

`docker-compose build`

#### Init database

`make d-migrate`

#### Create superuser

`make d-create-superuser`

#### Run 

`docker-compose up -d`

#### Create docs

http://localhost:8000

#### Get json doc

http://localhost:8000/docs/<doc-id>?format=json