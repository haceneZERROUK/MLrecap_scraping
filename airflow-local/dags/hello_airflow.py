from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG(
    dag_id="hello_airflow",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    def hello():
        print("Coucou Khadija, Airflow tourne bien !")

    task = PythonOperator(
        task_id="say_hello",
        python_callable=hello
    )
