# Author: Cuong Nguyen
#
# Build: docker build -t cuongnb14/swagger_ui:0.1 .
# Run: docker run -d -p 8080:8080 --name swagger_ui cuongnb14/swagger_ui:0.1 .
#

FROM ubuntu:16.04
MAINTAINER Cuong Nguyen "cuongnb14@gmail.com"


RUN apt-get update -qq

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip build-essential python3-dev \
        libmysqlclient-dev libxml2-dev libxslt1-dev libmysqlclient-dev libxml2-dev libxslt1-dev libssl-dev libffi-dev

RUN apt-get install locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip3 install -r requirements/local.txt

EXPOSE 8000

ENV C_FORCE_ROOT="true"
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

