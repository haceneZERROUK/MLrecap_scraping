from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

default_args = {
    "owner": "khadija",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_allocine_affiche_spider():
    base_path = "/opt/airflow/allocine_affiche"
    if base_path not in sys.path:
        sys.path.insert(0, base_path)

    try:
        from run_spider import run
        run()
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"❌ run_spider.py introuvable dans {base_path}.\nErreur originale : {e}"
        ) from e

with DAG(
    dag_id="allocine_affiche_dag",
    default_args=default_args,
    start_date=datetime(2024, 4, 1),
    schedule_interval="0 6 * * 2",  # Tous les mardis à 6h
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="scrape_affiche",
        python_callable=run_allocine_affiche_spider,
    )
