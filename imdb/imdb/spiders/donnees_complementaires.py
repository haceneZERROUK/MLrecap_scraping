import scrapy
import json
from imdb.items import ItemImdbComplement


class DonneesComplementairesSpider(scrapy.Spider):
    name = "donnees_complementaires"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/fr/search/title/?title=sinners&title_type=feature&release_date=2025-01-01,2025-12-31"]


    def start_requests(self):
        
        # with open ("dataset_nettoye/dataset_nettoye.json", "r") as file : 
        with open ("dataset_nettoye/dataset_nottoye.json", "r", encoding="utf-8") as file:

            movies = json.load(file)
        
        for m in movies : 
            title = m["allocine_fr_title"]
            released_year = m["jpbox_released_year"]
            
            jpbox_fr_title = m["jpbox_fr_title"]
            allocine_fr_title = m["allocine_fr_title"]
            jpbox_released_year = m["jpbox_released_year"]
            jpbox_actors = m["jpbox_actors"]
            jpbox_directors = m["jpbox_directors"]
            allocine_writer = m["allocine_writer"]
            allocine_distribution = m["allocine_distribution"]
            jpbox_country = m["jpbox_country"]
            jpbox_budget = m["jpbox_budget"]
            jpbox_category = m["jpbox_category"]
            jpbox_released_date = m["jpbox_released_date"]
            allocine_classification = m["allocine_classification"]
            jpbox_duration = m["jpbox_duration"]
            jpbox_weekly_entrances = m["jpbox_weekly_entrances"]
            duration_minutes = m["duration_minutes"]
            
            url_search = f"https://www.imdb.com/fr/search/title/?title={title}&title_type=feature&release_date={int(released_year)-1}-01-01,{int(released_year)+1}-12-31"
            
            meta = {
                "jpbox_fr_title" : jpbox_fr_title,
                "allocine_fr_title" : allocine_fr_title,
                "jpbox_released_year" : jpbox_released_year,
                "jpbox_actors" : jpbox_actors,
                "jpbox_directors" : jpbox_directors,
                "allocine_writer" : allocine_writer,
                "allocine_distribution" : allocine_distribution,
                "jpbox_country" : jpbox_country,
                "jpbox_budget" : jpbox_budget,
                "jpbox_category" : jpbox_category,
                "jpbox_released_date" : jpbox_released_date,
                "allocine_classification" : allocine_classification,
                "jpbox_duration" : jpbox_duration,
                "jpbox_weekly_entrances" : jpbox_weekly_entrances,
                "duration_minutes" : duration_minutes
            }
            
            yield scrapy.Request(
                url = url_search,
                callback = self.parse,
                meta = meta
            )
            

    def parse(self, response):
        
        movie_block = response.css("div.ipc-page-grid__item--span-2 ul.ipc-metadata-list li")
        movie_href = movie_block.css("div.sc-1c782bdc-1.jeRnfh.dli-parent div.sc-1c782bdc-0.kZFQUh div.sc-2bbfc9e9-0.jUYPWY div.ipc-title a::attr(href)").get()
        if not movie_href:
            self.logger.warning(f"Aucun lien de film trouvé pour l'URL : {response.url}")
            return
        movie_url = response.urljoin(movie_href)

        meta = {
            **response.meta,
            "imdb_url" : movie_url
        }
        
        yield response.follow(
            url = movie_url, 
            meta = meta, 
            callback = self.parse_movie_page
        )

    def parse_movie_page(self, response) : 
        
        imdb_title = response.css("span[data-testid='hero__primary-text']::text").get()
        imdb_released_year = response.css("ul.ipc-inline-list.ipc-inline-list--show-dividers.sc-ec65ba05-2.joVhBE.baseAlt li:nth-child(1) a::text").get()
        imdb_directors = response.css("div.sc-70a366cc-3.iwmAOx ul li:nth-child(1) div ul li a::text").get()               # realisation
        imdb_writer = response.css("div.sc-70a366cc-3.iwmAOx ul li:nth-child(2) div ul li a::text").get()                  # scenario
        imdb_actors = response.css("div.sc-70a366cc-3.iwmAOx ul li:nth-child(3) div ul li a::text").getall()               # casting principal
        imdb_distribution = response.css("li[data-testid='title-details-companies'] div ul li a::text ").get()             # Sociétés de production
        imdb_budget =  response.css("section[data-testid='BoxOffice'] div[data-testid='title-boxoffice-section'] ul li[data-testid='title-boxoffice-budget'] div ul li span::text").get()

        yield ItemImdbComplement(
            jpbox_fr_title = response.meta["jpbox_fr_title"], 
            allocine_fr_title = response.meta["allocine_fr_title"], 
            jpbox_released_year = response.meta["jpbox_released_year"], 
            jpbox_actors = response.meta["jpbox_actors"], 
            jpbox_directors = response.meta["jpbox_directors"], 
            allocine_writer = response.meta["allocine_writer"], 
            allocine_distribution = response.meta["allocine_distribution"], 
            jpbox_country = response.meta["jpbox_country"], 
            jpbox_budget = response.meta["jpbox_budget"], 
            jpbox_category = response.meta["jpbox_category"], 
            jpbox_released_date = response.meta["jpbox_released_date"], 
            allocine_classification = response.meta["allocine_classification"], 
            jpbox_duration = response.meta["jpbox_duration"], 
            jpbox_weekly_entrances = response.meta["jpbox_weekly_entrances"], 
            duration_minutes = response.meta["duration_minutes"], 
            imdb_url = response.meta["imdb_url"],
            imdb_title = imdb_title,
            imdb_released_year = imdb_released_year,
            imdb_directors = imdb_directors,
            imdb_writer = imdb_writer,
            imdb_actors = imdb_actors,
            imdb_distribution = imdb_distribution,
            imdb_budget = imdb_budget,
            
        )





