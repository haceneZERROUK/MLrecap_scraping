import scrapy
from datetime import date, timedelta, datetime
import locale
import re
from upcoming.items import UpcomingItem
import json



class UpcomesSpider(scrapy.Spider):
    name = "upcomes"
    allowed_domains = ["www.allocine.fr", "www.imdb.com"]
    start_urls = ["https://www.allocine.fr"]

    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    days_until_wednesday = (2 - today.weekday()) % 7
    next_wednesday = today + timedelta(days=days_until_wednesday)
    
    def start_requests(self):

        allocine_upcoming = f"https://www.allocine.fr/film/agenda/sem-{self.next_wednesday.strftime('%Y-%m-%d')}/"

        print("allocine_upcoming ######################")
        print(allocine_upcoming)
        print("DEBUG ######################")
        
        yield scrapy.Request(
            url = allocine_upcoming,
            callback = self.parse_allocine_upcoming
        )


    def parse_allocine_upcoming(self, response) :

        movies = response.css("div.gd-col-left ul li.mdl")
        if not movies:
            movies = response.css("li.mdl")
        if not movies:
            movies = response.css("div.card-entity-list div.card")
        print("Nombre de films ######################")
        print(len(movies))
        print(" ######################")
                            
        for m in movies :
            
            movie_url = response.urljoin(m.css("div.card.entity-card div.meta h2.meta-title a.meta-title-link::attr('href')").get())

            yield response.follow(
                url = movie_url,
                callback = self.parse_allocine_movie_page
            )


    def parse_allocine_movie_page(self, response) :

        fr_title = response.css("div.titlebar.titlebar-page div.titlebar-title.titlebar-title-xl::text").get()      # OK
        original_title = response.css("div.meta-body div[class='meta-body-item'] span.dark-grey::text").get()       # OK
        if not original_title : 
            original_title = fr_title       # OK
        
        released_date = response.css("div.meta-body div.meta-body-info span.date.blue-link::text").get()        # OK
        released_date = released_date.strip() if released_date else self.next_wednesday # OK
        
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
        if isinstance(released_date, str):
            date_obj = datetime.strptime(released_date, "%d %B %Y")
        else:
            date_obj = datetime.combine(released_date, datetime.min.time())  # convertit date en datetime
        released_date = date_obj.strftime("%d/%m/%Y")       # OK
        released_year = released_date.split("/")[-1] if released_date else date.today().year        # OK

        actors = response.css("div.meta-body-actor span.dark-grey-link::text").getall() or []
        actor_1 = actors[0] if len(actors) > 0 else "no_actor"      # OK
        actor_2 = actors[1] if len(actors) > 1 else "no_actor"      # OK
        actor_3 = actors[2] if len(actors) > 2 else "no_actor"      # OK
        
        director_list = response.css("div.meta-body-direction span.dark-grey-link::text").getall()        # de dans allocine (réalisateur)
        director = director_list[0] if director_list else "unknown"     # OK
        
        writer_list = response.css("div.meta-body-direction span.dark-grey-link::text").getall()         # scénariste (Par dans allocine)
        writer = writer_list[-1] if writer_list else "unknown"          # OK
        
        distribution_str = response.css("section.ovw.ovw-technical div.item span.blue-link::text").get()               # Distributeur
        distribution = distribution_str if distribution_str else "unknown"              # OK
        
        country_str = response.css("section.ovw.ovw-technical div.item span.that span.nationality::text").get() 
        country = country_str if country_str else "unknown"         # OK
        
        category_str = response.css("div.meta-body-info span.dark-grey-link::text").get() 
        category = category_str if category_str else "unknown"          # OK
        
        classification_kid = response.css("div.label.kids-label.aged-default::text").get() 
        if classification_kid :
            classification = classification_kid     # OK
        else :
            classification = response.css("span.certificate-text::text").get()
            if not classification :
                classification = "Tout public"      # OK
                
        duration = "".join([e.strip() for e in response.css("div.card.entity-card div.meta div.meta-body div.meta-body-item::text").getall()]).replace(",", "")
        if duration : 
            hours, minutes = duration.replace("h", "").replace("min", "").split(" ")
            duration_minutes = int(hours)*60 + int(minutes)
        else : 
            duration = "1h 00min"           # OK
            duration_minutes = 60           # OK

        image_url = response.css("div.entity-card-player-ovw figure.thumbnail span img.thumbnail-img::attr('src')").get()

        yield UpcomingItem(
            fr_title = fr_title,                        # OK
            original_title = original_title,            # OK
            released_date = released_date,              # OK
            released_year = released_year,              # OK
            actor_1 = actor_1,                          # OK
            actor_2 = actor_2,                          # OK
            actor_3 = actor_3,                          # OK
            director = director,                        # OK
            writer = writer,                            # OK
            distribution = distribution,                # OK
            country = country,                          # OK
            category = category,                        # OK
            classification = classification,            # OK
            duration = duration,                        # OK
            duration_minutes = duration_minutes,        # OK
            allocine_url = response.url,                # OK
            image_url = image_url,                      
        )




############################################################################################################


class Upcomes_imdb(scrapy.Spider):
    
    name = "Upcomes_imdb"
    allowed_domains = ["www.allocine.fr", "www.imdb.com"]
    start_urls = ["www.imdb.com"]
    
    def country_to_code(country):
        
        with open("pays_codes.json", "r", encoding="utf-8") as f:
            countries_codes = json.load(f)
            
        result = countries_codes[country]
        return result.upper()
        
        

    def start_requests(self):

        fr_title = ""
        country = ""
        released_year = ""
        
        imdb_search_url = "https://www.imdb.com/fr/find/?q=lahn%20mah&s=tt&exact=true&ref_=fn_ttl_ex"
        imdb_search_url = f"https://www.imdb.com/fr/search/title/?title={fr_title}&title_type=feature&release_date={released_year}-01-01,&countries={country}"
        
        meta = {
            
        }
        
        yield scrapy.Request(
            url = imdb_search_url,
            meta = meta,
            callback = self.parse_imdb_search_page
        )


    def parse_imdb_search_page(self, response) :

        movie_block = response.css("div.ipc-page-grid__item--span-2 ul.ipc-metadata-list li")
        movie_href = movie_block.css("div.sc-1c782bdc-1.jeRnfh.dli-parent div.sc-1c782bdc-0.kZFQUh div.sc-2bbfc9e9-0.jUYPWY div.ipc-title a::attr(href)").get()
        movie_url = response.urljoin(movie_href)

        # yield response.follow(
        #     url = movie_url,
        #     meta = response.meta,
        #     callback = self.parse_imdb_movie_page
        # )


    def parse_imdb_movie_page(self, response) :

        try:
            budget_element = response.css("section[data-testid='BoxOffice'] div[data-testid='title-boxoffice-section'] ul li[data-testid='title-boxoffice-budget'] div ul li span::text").get()
            if budget_element:
                budget_brut = budget_element.replace("(estimé)", "")
                budget = re.sub(r'[^\d]', '', budget_brut)
            else:
                budget = None
        except Exception as e:
            budget = None

        if response.meta["image_url"] :
            image_url = response.meta["image_url"]
        else :
            image_url = response.urljoin(response.css("div.sc-a59ac7fe-1.fKuiiE div.sc-a59ac7fe-4.jGHVHD div div.ipc-media img::attr('src')").get())

  
# ​Les nouveaux films à venir sont généralement publiés sur AlloCiné chaque mercredi. Cette pratique est ancrée dans l'industrie cinématographique française depuis les années 1930, le mercredi étant choisi pour maximiser la fréquentation des cinémas en milieu de semaine .​