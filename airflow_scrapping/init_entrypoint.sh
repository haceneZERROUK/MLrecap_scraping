#!/bin/bash
set -e

source deploiement_scripts/.env

airflow db migrate

airflow users create \
    --username $AIRFLOW_USER \
    --password $AIRFLOW_PASSWORD \
    --firstname admin \
    --lastname user --role Admin \
    --email admin@example.com

