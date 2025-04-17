from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os

def run_allocine_affiche_spider(**kwargs):
    """
    Run the Allociné affiche spider; raise if it fails.
    """
    from run_spider import run
    if not run():
        raise RuntimeError("Spider execution failed")
    return "Spider executed successfully"

def ensure_data_directory(**kwargs):
    """
    Ensure the /opt/airflow/data directory exists.
    """
    path = "/opt/airflow/data"
    os.makedirs(path, exist_ok=True)
    return path

default_args = {
    "owner": "khadija",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

project_root = "/opt/airflow"
sys.path.insert(0, project_root)

with DAG(
    dag_id="allocine_affiche_dag",
    default_args=default_args,
    description="Retrieve Allociné film posters every Tuesday",
    start_date=datetime(2024, 4, 1),
    schedule_interval="0 6 * * 2",
    catchup=False,
    tags=["scraping", "allocine", "films"],
) as dag:
    create_data_dir = PythonOperator(
        task_id="ensure_data_directory",
        python_callable=ensure_data_directory,
    )
    scrape_task = PythonOperator(
        task_id="scrape_affiche",
        python_callable=run_allocine_affiche_spider,
    )
    check_output = BashOperator(
        task_id="check_output",
        bash_command='ls -lh /opt/airflow/data/ || echo "No files found"',
    )
    create_data_dir >> scrape_task >> check_output