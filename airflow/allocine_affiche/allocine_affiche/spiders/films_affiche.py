import scrapy

class FilmsAfficheSpider(scrapy.Spider):
    name = "films_affiche"
    start_urls = ['https://www.allocine.fr/film/aucinema/']

    def parse(self, response):
        films = response.css('div.card')
        for film in films:
            titre = film.css('h2.meta-title a::text').get(default='').strip()
            lien = film.css('a.meta-title-link::attr(href)').get()
            yield {
                'titre': titre,
                'lien': response.urljoin(lien)
            }
