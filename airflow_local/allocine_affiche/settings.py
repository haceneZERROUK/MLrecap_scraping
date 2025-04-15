BOT_NAME = 'allocine_affiche'

SPIDER_MODULES = ['allocine_affiche.spiders']
NEWSPIDER_MODULE = 'allocine_affiche.spiders'
ROBOTSTXT_OBEY = False

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15'

# Configure logs
LOG_LEVEL = 'INFO'
LOG_FILE = '/opt/airflow/logs/scrapy.log'  # Enregistrer les logs dans le répertoire logs d'Airflow

# Configure item pipelines
ITEM_PIPELINES = {
   # Vous pouvez ajouter des pipelines personnalisés ici
}

FEEDS = {
    '/opt/airflow/data/films.json': {
        'format': 'json',
        'encoding': 'utf8',
        'overwrite': True,
    }
}

# Éviter d'être bloqué par le site
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Middleware pour gérer les requêtes
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
}

# Paramètres de retry en cas d'erreur
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]