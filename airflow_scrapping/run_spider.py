import os
import sys
import logging
from scrapy.utils.log import configure_logging

# Global logger setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/opt/airflow/logs/spider_run.log')
    ]
)
logger = logging.getLogger(__name__)

# Ensure project root and data directory exist
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_path)

data_dir = os.path.join(base_path, 'data')
os.makedirs(data_dir, exist_ok=True)
logger.info(f"Data directory: {data_dir}")

def run():
    """
    Configure Scrapy logging and start the UpcomesSpider.
    Returns True on success, False otherwise.
    """
    configure_logging(install_root_handler=False)
    logging.getLogger('scrapy').propagate = False

    try:
        logger.info(">>> Starting Allociné spider")
        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings
        from upcoming.upcoming.spiders.upcomes import UpcomesSpider

        settings = get_project_settings()
        settings.set('LOG_ENABLED', False)

        process = CrawlerProcess(settings)
        process.crawl(UpcomesSpider)
        process.start()

        logger.info(">>> Spider finished successfully")
        return True
    except Exception as e:
        logger.error(f">>> Spider error: {e}")
        return False

if __name__ == "__main__":
    run()