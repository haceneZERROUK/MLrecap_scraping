#!/bin/bash

docker build -t mysql-custom -f Dockerfile.mysql .
docker tag mysql-custom mboumedineregistry.azurecr.io/mysql-custom:latest
docker push mboumedineregistry.azurecr.io/mysql-custom:latest

docker build -t init-airflow -f Dockerfile.airflow-init .
docker tag init-airflow mboumedineregistry.azurecr.io/init-airflow:latest
docker push mboumedineregistry.azurecr.io/init-airflow:latest

docker build -t scheduler-airflow -f Dockerfile.scheduler .
docker tag scheduler-airflow mboumedineregistry.azurecr.io/scheduler-airflow:latest
docker push mboumedineregistry.azurecr.io/scheduler-airflow:latest

docker build -t webserver-airflow -f Dockerfile.webserver .
docker tag webserver-airflow mboumedineregistry.azurecr.io/webserver-airflow:latest
docker push mboumedineregistry.azurecr.io/webserver-airflow:latest
