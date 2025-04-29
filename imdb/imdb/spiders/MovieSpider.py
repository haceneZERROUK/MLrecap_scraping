import scrapy
import scrapy.selector
from imdb.items import ImdbItem
import json
import re



class MovieSpider(scrapy.Spider):

    name = "MovieSpider"  # Nom du spider
    allowed_domains = ["www.imdb.com"]  # Domaine autorisé pour les requêtes
    start_urls = ["https://www.imdb.com/fr/search/title/?title_type=feature"]  # URL de départ pour la recherche de films
    
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            "original_title_imdb",
            "fr_title_imdb",
            "release_year_imdb",
            "certification_imdb",
            "duration_imdb",
            "score_imdb",
            "metascore_imdb",
            "voters_number_imdb",
            "description_imdb",
            "categories_imdb",
            "languages_imdb",
            "prod_cies_imdb",
            "countries_imdb",
            "actors_imdb",
            "directors_imdb",
            "writers_imdb",
            "budget_imdb",
            "url_imdb",
            
            "fr_title_jpbox",
            "original_title_jpbox",
            "director_jpbox",
            "country_jpbox",
            "category_jpbox",
            "released_year_jpbox",
            "date_jpbox",
            "PEGI_jpbox",
            "duration_jpbox",
            "total_entrances_jpbox",
            "weekly_entrances_jpbox",
            "duration_mins"
        ]
    }

    
    def start_requests(self):

        with open("result-entrances.json") as file : 
            movies = json.load(file) 
            original_titles = [movie["original_title"] for movie in movies]
            fr_title = [movie["fr_title"] for movie in movies]
            
        # deux condition : si titre original est le meme ou si titre francais est le meme

        for movie in movies :
            name_complete = movie["original_title"]
            name = re.sub(r'\(.*?\)', '', name_complete).replace(" ", "")
            hours, minutes = [int(i) for i in movie["duration"].replace("min", "").strip().split("h")]
            duration_mins = (hours*60) + minutes
            
            url_search = f"https://www.imdb.com/fr/find/?q={name}&s=tt&ttype=ft&ref_=fn_ttl_pop"
            
            meta = {
                "fr_title_jpbox" : movie["fr_title"],
                "original_title_jpbox" : movie["original_title"],
                "director_jpbox" : movie["director"],
                "country_jpbox" : movie["country"],
                "category_jpbox" : movie["category"],
                "released_year_jpbox" : movie["released_year"],
                "date_jpbox" : movie["date"],
                "PEGI_jpbox" : movie["PEGI"],
                "duration_jpbox" : movie["duration"],
                "total_entrances_jpbox" : movie["total_entrances"],
                "weekly_entrances_jpbox" : movie["weekly_entrances"], 
                "duration_mins" : duration_mins
            }
                        
            yield scrapy.Request(
                url = url_search,
                callback = self.parse, 
                meta=meta
            )
            
            
    def parse(self, response) :
        
        released_year_jpbox = response.meta["released_year_jpbox"]
        list_results = response.css("div.sc-b03627f1-2.gWHDBT > ul > li")

        for r in list_results : 
            released_year_imdb = r.css("div.ipc-metadata-list-summary-item__c > div.ipc-metadata-list-summary-item__tc > ul.ipc-metadata-list-summary-item__tl > li > span::text").get()
            url_movie = response.urljoin(r.css("div.ipc-metadata-list-summary-item__c > div > a::attr('href')").get())
            
            if released_year_imdb == released_year_jpbox : 
                # # debug 
                # print("#########################")
                # print(released_year_jpbox)
                # print(released_year_imdb)
                # print(url_movie)
                # print("#########################")

                yield scrapy.Request(
                    url = url_movie, 
                    callback = self.parse_movie_page, 
                    meta = {**response.meta, "url_movie_imdb": url_movie}
                ) 

        
    def parse_movie_page(self, response):
        
        original_title_imdb = response.css("div.sc-ec65ba05-1.fUCCIx::text").get()
        fr_title_imdb = response.css("span.hero__primary-text::text").get()
        if original_title_imdb : 
            original_title_imdb = response.css("div.sc-ec65ba05-1.fUCCIx::text").get().replace("Titre original :", "").strip()
        else : 
            original_title_imdb = fr_title_imdb
        release_year_imdb = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(1) > a::text").get()
        
        certification_imdb = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(2) > a::text").get()
        duration_imdb = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(3)::text").get()
        score_imdb = response.css("span.sc-d541859f-1.imUuxf::text").get()       # target leaking
        metascore_imdb = response.css("span.score > span.sc-b0901df4-0::text").get()
        voters_number_imdb = response.css("div.sc-d541859f-3::text").get()
        description_imdb = response.css("span.sc-42125d72-2.mmImo::text").get()
        
        categories_imdb = response.css("div.ipc-chip-list__scroller > a > span::text").getall()
        languages_imdb = response.css("li[data-testid='title-details-languages'] > div > ul > li > a::text").getall()
        prod_cies_imdb = response.css("li[data-testid='title-details-companies'] > div > ul > li > a::text").getall()
        countries_imdb = response.css("li[data-testid='title-details-origin'] > div > ul > li > a::text").getall()
        
        actors_imdb = list(set(response.css("div[role='presentation'] > ul > li:nth-child(3) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        directors_imdb = list(set(response.css("div[role='presentation'] > ul > li:nth-child(1) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        writers_imdb = list(set(response.css("div[role='presentation'] > ul > li:nth-child(2) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        
        budget_imdb = response.css("div[data-testid='title-boxoffice-section'] > ul > li[data-testid='title-boxoffice-budget'] div > ul > li > span::text").get()
        
        meta_final = response.meta
        
        yield ImdbItem(
            original_title_imdb = original_title_imdb,
            fr_title_imdb = fr_title_imdb,
            release_year_imdb = release_year_imdb,
            certification_imdb = certification_imdb,
            duration_imdb = duration_imdb,
            score_imdb = score_imdb,
            metascore_imdb = metascore_imdb,
            voters_number_imdb = voters_number_imdb,
            description_imdb = description_imdb,
            categories_imdb = categories_imdb,
            languages_imdb = languages_imdb,
            prod_cies_imdb = prod_cies_imdb,
            countries_imdb = countries_imdb,
            actors_imdb = actors_imdb,
            directors_imdb = directors_imdb,
            writers_imdb = writers_imdb,
            budget_imdb = budget_imdb,
            url_imdb = meta_final["url_movie_imdb"],
            fr_title_jpbox = meta_final["fr_title_jpbox"],
            original_title_jpbox = meta_final["original_title_jpbox"],
            director_jpbox = meta_final["director_jpbox"],
            country_jpbox = meta_final["country_jpbox"],
            category_jpbox = meta_final["category_jpbox"],
            released_year_jpbox = meta_final["released_year_jpbox"],
            date_jpbox = meta_final["date_jpbox"],
            PEGI_jpbox = meta_final["PEGI_jpbox"],
            duration_jpbox = meta_final["duration_jpbox"],
            total_entrances_jpbox = meta_final["total_entrances_jpbox"],
            weekly_entrances_jpbox = meta_final["weekly_entrances_jpbox"],
            duration_mins = meta_final["duration_mins"]
        )
