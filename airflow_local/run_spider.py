import os
import sys
import logging
from datetime import datetime

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/opt/airflow/logs/spider_run.log')
    ]
)

logger = logging.getLogger(__name__)

# Ajouter le répertoire de base au chemin Python
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

# Assurer que le répertoire data existe
data_dir = os.path.join(base_path, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    logger.info(f"Répertoire data créé: {data_dir}")

def run():
    try:
        logger.info(">>> Début de l'exécution du spider AlloCiné")
        
        # Importer à l'intérieur de la fonction pour éviter les problèmes de chemin
        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings
        from allocine_affiche.spiders.films_affiche import FilmsAfficheSpider
        
        # Obtenir les paramètres du projet et créer le processus
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        
        # Lancer le spider
        process.crawl(FilmsAfficheSpider)
        process.start()
        
        logger.info(">>> Fin de l'exécution avec succès")
        return True
    except Exception as e:
        logger.error(f">>> Erreur lors de l'exécution du spider: {str(e)}")
        return False

if __name__ == "__main__":
    run()