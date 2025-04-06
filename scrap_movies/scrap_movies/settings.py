import random as rd

BOT_NAME = "scrap_movies"

SPIDER_MODULES = ["scrap_movies.spiders"]
NEWSPIDER_MODULE = "scrap_movies.spiders"

# Liste des User-Agents pour changer le User-Agent à chaque requête
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/91.0.864.59"
]

# Configure le middleware pour changer le User-Agent de manière aléatoire
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Désactive le middleware par défaut
    'scrap_movies.middlewares.RandomUserAgentMiddleware': 400,  # Activer notre middleware
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure la concurrence des requêtes (réduit la probabilité d'un blocage)
CONCURRENT_REQUESTS = 8  # Limiter à 8 requêtes simultanées
CONCURRENT_REQUESTS_PER_DOMAIN = 4  # Limiter à 4 requêtes simultanées par domaine
CONCURRENT_REQUESTS_PER_IP = 4  # Limiter à 4 requêtes simultanées par IP

# Configure un délai entre les requêtes (ex: 2 secondes)
DOWNLOAD_DELAY = 2  # Pauser entre chaque requête
# Activer AutoThrottle pour gérer dynamiquement les délais en fonction de la charge du serveur
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1  # Délai initial de 1 seconde
AUTOTHROTTLE_MAX_DELAY = 10  # Délai maximal de 10 secondes
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0  # Concurrence de 2 requêtes simultanées
AUTOTHROTTLE_DEBUG = True  # Afficher les logs pour voir les ajustements

# Activer la gestion des erreurs avec un nombre de tentatives
RETRY_TIMES = 3  # Réessayer 3 fois en cas d'échec
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]  # Réessayer lors de certains codes d'erreur

# Activer les cookies pour simuler un véritable utilisateur
COOKIES_ENABLED = True

# Ajouter des headers personnalisés pour simuler une requête normale d'un utilisateur
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'Connection': 'keep-alive',
}

# Configurer les paramètres de stockage des données
FEED_EXPORT_ENCODING = "utf-8"  # Utiliser l'encodage UTF-8

# Configuration de l'extension de logging pour faciliter le débogage
LOG_LEVEL = 'DEBUG'  # Activer les logs détaillés pour faciliter le débogage

# Optionnellement, tu peux désactiver les requêtes vers certains sites (si nécessaire)
# You can add specific IP or domains to avoid:
# RESTRICT_XHR = True
