import os
import sys
import logging
from scrapy.utils.log import configure_logging

data_path = os.environ.get('DATA_PATH', '/mnt/airflow-files/data')

# Configuration globale du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/opt/airflow/logs/spider_run.log')
    ]
)
logger = logging.getLogger(__name__)

# Assure que le chemin de base du projet est dans sys.path
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)

# Assure que le dossier data existe
# data_dir = os.path.join(base_path, 'data')
data_dir = os.path.join("/mnt/airflow-files/data") 
os.makedirs(data_dir, exist_ok=True)
logger.info(f"Dossier data : {data_dir}")

def run():
    """
    Configure le logging de Scrapy et lance le spider UpcomesSpider.

    Retourne True si l'exécution se termine sans erreur, False sinon.
    """
    # Désactive l'installation du handler de logs par défaut de Scrapy
    configure_logging(install_root_handler=False)
    # Empêche la propagation des logs Scrapy vers d'autres handlers
    logging.getLogger('scrapy').propagate = False

    try:
        logger.info(">>> Démarrage du spider Allociné")
        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings
        from upcoming.upcoming.spiders.upcomes import UpcomesSpider

        # Récupère les settings du projet et désactive le logging interne
        settings = get_project_settings()
        settings.set('LOG_ENABLED', False)

        # Lance le crawler
        process = CrawlerProcess(settings)
        process.crawl(UpcomesSpider)
        process.start()
        
        from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
        from dotenv import load_dotenv, find_dotenv
        
        dot_env_path = find_dotenv()
        load_dotenv(dotenv_path=dot_env_path, override=True)

        account_name = os.getenv("BLOB_ACCOUNT_NAME")
        account_key = os.getenv("BLOB_ACCOUNT_KEY")
        container_name = os.getenv("BLOB_CONTAINER_NAME")
        saving_file = os.getenv("saving_file")


        blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)
        blob_client = blob_service_client.get_blob_client(container=container_name,blob=saving_file + ".json")

        scrapped_file_path = './data/films.json'
        # scrapped_file_path = '/opt/airflow-files/data/films.json'
        # scrapped_file_path = '/mnt/airflow-files/data/films.json'

        with open(scrapped_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(f"Fichier {scrapped_file_path} uploadé dans le blob Azure '{container_name}'.")

        logger.info(">>> Spider terminé avec succès")
        return True
    except Exception as e:
        logger.error(f">>> Erreur du spider : {e}")
        return False

# if __name__ == "__main__":
#     run()
