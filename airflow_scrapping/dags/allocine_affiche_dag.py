from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os
import logging

# Utilisez un logger pour déboguer
logger = logging.getLogger(__name__)

# Paramètres par défaut du DAG
default_args = {
    "owner": "khadija",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
    "email_on_retry": False,
    "start_date": datetime(2025, 4, 1),  # Date plus récente
}

# Ajoute le répertoire principal au chemin Python
project_root = "/opt/airflow"
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def run_allocine_affiche_spider(**kwargs):
    """
    Exécute le spider Allociné pour récupérer les affiches.
    Lève une exception si l'exécution échoue.
    """
    try:
        logger.info("Démarrage du spider Allociné via Airflow")
        # Import explicite avec gestion d'erreur
        try:
            from run_spider import run
            logger.info("Module run_spider importé avec succès")
        except ImportError as e:
            logger.error(f"Erreur d'import du module run_spider: {e}")
            raise
        
        # Exécution avec logging détaillé
        result = run()
        logger.info(f"Résultat de l'exécution du spider: {result}")
        
        if not result:
            logger.error("Le spider a retourné False")
            raise RuntimeError("Échec du spider Allociné")
        
        return "Spider exécuté avec succès"
    except Exception as e:
        logger.error(f"Exception lors de l'exécution du spider: {e}")
        raise

def ensure_data_directory(**kwargs):
    """
    Assure que le dossier de données existe.
    """
    path = "/mnt/airflow-files/data"
    logger.info(f"Création du dossier: {path}")
    os.makedirs(path, exist_ok=True)
    return path

with DAG(
    dag_id="allocine_affiche_dag",
    default_args=default_args,
    description="Récupère les affiches de films d'Allociné chaque mardi",
    schedule_interval="0 6 * * 2",
    catchup=False,
    tags=["scraping", "allocine", "films"],
) as dag:
    # Vérifie le dossier data
    create_data_dir = PythonOperator(
        task_id="ensure_data_directory",
        python_callable=ensure_data_directory,
    )
    
    # Lance le spider
    scrape_task = PythonOperator(
        task_id="scrape_affiche",
        python_callable=run_allocine_affiche_spider,
    )
    
    # Vérifie la présence des fichiers
    check_output = BashOperator(
        task_id="check_output",
        bash_command='ls -lah /mnt/airflow-files/data/ || echo "Aucun fichier trouvé"',
    )
    
    create_data_dir >> scrape_task >> check_output
