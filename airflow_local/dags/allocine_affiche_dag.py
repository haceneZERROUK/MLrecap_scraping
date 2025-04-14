from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os

# Paramètres par défaut pour le DAG
default_args = {
    "owner": "khadija",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
}

# Ajouter le répertoire racine du projet au chemin Python
project_root = "/opt/airflow"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Fonction pour exécuter le spider
def run_allocine_affiche_spider(**kwargs):
    from run_spider import run
    success = run()
    if not success:
        raise Exception("Le spider a rencontré une erreur")
    return "Spider exécuté avec succès"

# Créer un répertoire data si nécessaire
def ensure_data_directory(**kwargs):
    data_dir = "/opt/airflow/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Répertoire créé: {data_dir}")
    else:
        print(f"Le répertoire {data_dir} existe déjà")
    return data_dir

with DAG(
    dag_id="allocine_affiche_dag",
    default_args=default_args,
    description="Récupère les affiches de films d'Allociné tous les mardis",
    start_date=datetime(2024, 4, 1),
    schedule_interval="0 6 * * 2",  # Tous les mardis à 6h
    catchup=False,
    tags=["scraping", "allocine", "films"],
) as dag:

    # Vérifier que le répertoire data existe
    create_data_dir = PythonOperator(
        task_id="ensure_data_directory",
        python_callable=ensure_data_directory,
    )
    
    # Exécuter le spider
    scrape_task = PythonOperator(
        task_id="scrape_affiche",
        python_callable=run_allocine_affiche_spider,
    )
    
    # Vérifier que le fichier a été créé
    check_output = BashOperator(
        task_id="check_output",
        bash_command='ls -lh /opt/airflow/data/ | grep films || echo "Aucun fichier trouvé"',
    )
    
    # Définir l'ordre des tâches
    create_data_dir >> scrape_task >> check_output