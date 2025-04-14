BOT_NAME = 'allocine_affiche'

SPIDER_MODULES = ['allocine_affiche.spiders']
NEWSPIDER_MODULE = 'allocine_affiche.spiders'
ROBOTSTXT_OBEY = False

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15'

FEEDS = {
    'data/films_affiche.json': {
        'format': 'json',
        'encoding': 'utf8',
        'overwrite': True
    }
}

