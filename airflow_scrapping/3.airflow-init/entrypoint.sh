#!/bin/bash

airflow db migrate &&
airflow users create --username airflow --password airflow \
    --firstname admin --lastname user --role Admin \
    --email admin@example.com
