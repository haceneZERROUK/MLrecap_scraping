import scrapy
from datetime import date
import re


class UpcomesSpider(scrapy.Spider):
    name = "upcomes"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr"]


    def start_requests(self):
        
        week = "2025-04-23"     # date today + 1jour
        
        allocine_upcoming = f"https://www.allocine.fr/film/agenda/sem-{week}/"
        
        yield scrapy.Request(
            url = allocine_upcoming,
            callback = self.parse_allocine_upcoming
        )
    
        
    def parse_allocine_upcoming(self, response) : 
        
        movies = response.css("div.gd-col-left ul li.mdl")
        for m in movies : 
            movie_url = response.urljoin(m.css("div.card.entity-card div.meta h2.meta-title a.meta-title-link::attr('href')").get())
            
            yield response.follow(
                url = movie_url,
                callback = self.parse_allocine_movie_page
            )
        

    def parse_allocine_movie_page(self, response) : 
        
        """
            jpbox_fr_title              OK  OK
            original_title              OK  OK
            released_date               OK  OK
            jpbox_released_year         OK  OK
            jpbox_actors                OK  OK
            jpbox_directors             OK  OK
            allocine_writer             OK  OK
            allocine_distribution       OK  OK
            jpbox_country               OK  OK
            jpbox_category              OK  OK
            allocine_classification     OK  OK
            jpbox_duration              OK  OK
            duration_minutes            OK  OK
            jpbox_budget                
            jpbox_weekly_entrances      
        """
        
        fr_title = response.css("div.titlebar.titlebar-page div.titlebar-title.titlebar-title-xl::text").get()
        original_title = response.css("div.meta-body div[class='meta-body-item'] span.dark-grey::text").get()
        released_date = response.css("div.meta-body div.meta-body-info span.date.blue-link::text").get().strip()
        released_year = released_date.split(" ")[-1]
        actors = response.css("div.meta-body-actor span.dark-grey-link::text").getall()
        director = response.css("div.meta-body-direction span.dark-grey-link::text").getall()[0]        # de dans allocine (réalisateur)
        writer = response.css("div.meta-body-direction span.dark-grey-link::text").getall()[-1]         # scénariste (Par dans allocine)
        distribution = response.css("section.ovw.ovw-technical div.item span.blue-link::text").get()               # Distributeur
        country = response.css("section.ovw.ovw-technical div.item span.that span.nationality::text").get()
        category = response.css("div.meta-body-info span.dark-grey-link::text").get()
        classification_kid = response.css("div.label.kids-label.aged-default::text").get()
        
        # lien de l'image dans le scraping des sorties
        image_url = ""
        
        if classification_kid : 
            classification = classification_kid
        else : 
            classification = response.css("span.certificate-text::text").get()
            
        duration_text = ''.join(response.css('div.meta-body-item.meta-body-info ::text').getall())
        duration = re.search(r'(\d+h\s+\d+min)', duration_text).group(1)
        hours, minutes = duration.replace("h", "").replace("min", "").split(" ")
        duration_minutes = int(hours)*60 + int(minutes)
        
        meta = {
            "fr_title" : fr_title, 
            "original_title" : original_title, 
            "released_date" : released_date, 
            "released_year" : released_year, 
            "actors" : actors, 
            "director" : director, 
            "writer" : writer, 
            "distribution" : distribution, 
            "country" : country, 
            "category" : category, 
            "classification" : classification, 
            "duration" : duration,
            "duration_minutes" : duration_minutes
        }
        
        imdb_search_url = f"https://www.imdb.com/fr/search/title/?title={fr_title}&title_type=feature&release_date={int(released_year)-1}-01-01,"
        
        
        yield response.follow(
            url = imdb_search_url,
            meta = meta, 
            callbask = self.parse_imdb_search_page
        )
        



# prendre les sorties allociné chaque mercredi
# si on toutes les infos allociné Ok - sinon compléter les infos manquantes sur imdb

# ​Les nouveaux films à venir sont généralement publiés sur AlloCiné chaque mercredi. Cette pratique est ancrée dans l'industrie cinématographique française depuis les années 1930, le mercredi étant choisi pour maximiser la fréquentation des cinémas en milieu de semaine .​