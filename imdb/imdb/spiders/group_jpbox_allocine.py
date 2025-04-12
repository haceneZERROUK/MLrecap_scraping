import scrapy
import json

class GroupJpboxAllocineSpider(scrapy.Spider):
    name = "group_jpbox_allocine"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/"]


    def start_requests(self):
        
        with open("jpbox_full_data_with_allocine_names.json") as file : 
            movies = json.load(file) 

        for m in movies : 
            allocine_fr_title = m["allocine_fr_title"]
            allocine_released_year = m["allocine_released_year"]
            
            meta = {
                "jpbox_fr_title" : m["jpbox_fr_title"],
                "jpbox_original_title" : m["jpbox_original_title"],
                "allocine_fr_title" : allocine_fr_title,
                "allocine_released_year" : allocine_released_year,
                "jpbox_actors" : m["jpbox_actors"],
                "jpbox_producers" : m["jpbox_producers"],
                "jpbox_authors" : m["jpbox_authors"],
                "jpbox_compositors" : m["jpbox_compositors"],
                "jpbox_directors" : m["jpbox_directors"],
                "jpbox_country" : m["jpbox_country"],
                "jpbox_category" : m["jpbox_category"],
                "jpbox_released_date" : m["jpbox_released_date"],
                "jpbox_classification" : m["jpbox_classification"],
                "jpbox_duration" : m["jpbox_duration"],
                "jpbox_total_entrances" : m["jpbox_total_entrances"],
                "jpbox_weekly_entrances" : m["jpbox_weekly_entrances"],
                "jpbox_incomes_total" : m["jpbox_incomes_total"],
                "jpbox_incomes_france" : m["jpbox_incomes_france"],
                "jpbox_budget" : m["jpbox_budget"],
                "jpbox_url_movie" : m["jpbox_url_movie"],
                "jpbox_synopsisjpbox_released_year" : m["jpbox_synopsisjpbox_released_year"],
            }



    def parse(self, response):
        
        pass


















