import scrapy
import logging

class FilmsAfficheSpider(scrapy.Spider):
    name = "films_affiche"
    start_urls = ['https://www.allocine.fr/film/sorties-semaine/']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
    }

    def parse(self, response):
        self.logger.info(f"Parsing: {response.url}")
        
        try:
            films = response.css('li.mdl')  # chaque film est dans un <li class="mdl">
            self.logger.info(f"Nombre de films trouvés: {len(films)}")
            
            for film in films:
                titre = film.css('h2.meta-title a::text').get(default='').strip()
                lien = film.css('a.meta-title-link::attr(href)').get()
                
                if titre and lien:
                    self.logger.info(f"Film trouvé: {titre}")
                    yield {
                        'titre': titre,
                        'lien': response.urljoin(lien),
                        'date_extraction': self.crawler.stats.get_value('start_time').strftime('%Y-%m-%d')
                    }
        except Exception as e:
            self.logger.error(f"Erreur lors du parsing: {str(e)}")