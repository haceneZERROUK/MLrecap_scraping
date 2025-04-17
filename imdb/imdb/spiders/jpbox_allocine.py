import scrapy
import json
import re
from imdb.items import Jpbox_allocine_item



class JpboxAllocineSpider(scrapy.Spider):
    name = "jpbox_allocine"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/"]

    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            "fr_title_allocine", 
            "original_title_allocine", 
            "release_date_allocine", 
            "release_year_allocine", 
            "prod_year", 
            "duration", 
            "categories_allocine", 
            "writer_allocine", 
            "director_allocine", 
            "casting_allocine", 
            "press_note", 
            "classification", 
            "countries", 
            "distribution", 
            "total_entrances", 
            "box_office_week1", 
            "box_office_week2", 
            "societies_allocine", 
            "soundtrack_allocine", 
            "synopsis_allocine", 
            "url_allocine", 
        ],
        'FEEDS': { 
            'jpbox_allocine_FINAL.csv': { 
                'format': 'csv', 
                'encoding': 'utf8', 
                'store_empty': False, 
                'overwrite': True, 
                'delimiter': ';' 
            }, 
            'jpbox_allocine_FINAL.json': { 
                'format': 'json', 
                'encoding': 'utf8', 
                'store_empty': False, 
                'overwrite': True, 
            }, 
        } 
    } 


    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
        )


    def parse(self, response):
        
        # pages_number = int(response.css('div.pagination-item-holder span.button-md.item::text').getall()[-1])
        pages_number = 2
        
        for i in range(1, pages_number+1):
            next_url = self.start_urls[0] + "?page=" + str(i)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_movies_list)
            
            
    def parse_movies_list(self, response) : 
            
        list_movies = response.css("div.gd-col-middle > ul > li.mdl")

        for movie in list_movies:
            fr_title_allocine = movie.css("div > div.meta.meta-affintiy-score > h2.meta-title > a::text").get().strip().lower()
            original_title_allocine = movie.css("div > div.meta.meta-affintiy-score > div.meta-body > div.meta-body-item > span.dark-grey::text").get()
            if not original_title_allocine:
                original_title_allocine = fr_title_allocine
            original_title_allocine = original_title_allocine.strip().lower()

            url_allocine = response.urljoin(movie.css("div > div.meta.meta-affintiy-score > h2.meta-title > a::attr(href)").get())
            release_date_allocine = movie.css("div > div.meta > div.meta-body > div > span.date::text").get()
            if release_date_allocine : 
                release_year_allocine = int(release_date_allocine.split(" ")[-1])
            else : 
                release_year_allocine = None
                
            duration = response.css('div.meta-body-item.meta-body-info::text').re_first(r'\d+h\s*\d+min')

            meta = {
                "fr_title_allocine" : fr_title_allocine.strip() if fr_title_allocine else None,
                "original_title_allocine" : original_title_allocine.strip() if original_title_allocine else None,
                "url_allocine" : url_allocine,
                "release_date_allocine" : release_date_allocine,
                "release_year_allocine" : release_year_allocine, 
                "duration" : duration, 
            }

            yield response.follow(
                url = url_allocine,
                callback = self.parse_movie_page,
                meta = meta
            )

                
    def parse_movie_page(self, response) : 
        
        categories_allocine = response.css("div.meta-body-item.meta-body-info > span.dark-grey-link::text").getall()
        meta_body_items = response.css("div.meta-body-item.meta-body-direction.meta-body-oneline")
        writer_allocine = meta_body_items[1].css("span.dark-grey-link::text").getall() if len(meta_body_items) > 1 else []
        director_allocine = response.css("div.meta-body-item.meta-body-direction span.dark-grey-link::text").get(default=None)
        casting_allocine = response.css("div.meta-body-item.meta-body-actor span.dark-grey-link::text").getall()
        
        bloc_press_note = response.css("div.rating-item")
        try :
            press_note = bloc_press_note.css("div.stareval span.stareval-note::text").get(default=None)
        except AttributeError : 
            press_note = None
            
        press_note_label = bloc_press_note.css("div.rating-item-content span::text").get()
        if press_note_label and press_note_label.strip().lower() == "presse":
            press_note = bloc_press_note.css("div.stareval span.stareval-note::text").get()
        else:
            press_note = None

        synopsis_allocine = response.css("p.bo-p::text").get()
        classification = response.css("section[id='synopsis-details'] div.certificate span.certificate-text::text").get()
        countries = response.css("section.ovw.ovw-technical div.item span.that span.nationality::text").getall()
        
        technical_bloc = response.css("section.ovw.ovw-technical")
        
        total_entrances = None
        for item in technical_bloc.css("div.item"):
            total_entrances_label = item.css("span.what.light::text").get()
            if total_entrances_label and total_entrances_label.strip().lower() == "box office france" :
                total_entrances = item.css("span.that::text").get()
                break
            
        url_film = response.url
        box_office_url = url_film.replace("_gen_cfilm=", "-").replace(".html", "/box-office/")
        casting_url = url_film.replace("_gen_cfilm=", "-").replace(".html", "/casting/")
        
        dist_label = technical_bloc.css("div.item span.what.light::text").get() 
        if dist_label and dist_label.strip().lower() == "distributeur" :
            distribution = technical_bloc.css("span.blue-link::text").get()
        else:
            distribution = technical_bloc.css("span.blue-link::text").get()
            
        prod_year_label = technical_bloc.css("div.item span.what.light::text").get()
        if prod_year_label and prod_year_label.strip().lower() == "année de production" : 
            prod_year = technical_bloc.css("span.that::text").get()
        else : 
            prod_year = technical_bloc.css("span.that::text").get()
        
        meta = {
            **response.meta,
            "categories_allocine" : [c.strip() for c in categories_allocine] if categories_allocine else [],
            "writer_allocine" : [w for w in writer_allocine] if writer_allocine else [],
            "director_allocine" : director_allocine.strip() if director_allocine else None,
            "casting_allocine" : [c for c in casting_allocine] if casting_allocine else [],
            "press_note" : press_note.strip() if press_note else None,
            "synopsis_allocine" : synopsis_allocine.strip() if synopsis_allocine else None,
            "classification" : classification.strip() if classification else None,
            "countries" : [c for c in countries] if countries else [],
            "distribution" : distribution.strip() if distribution else None,
            "prod_year" : prod_year.strip() if prod_year else None,
            "url_casrting" : casting_url,
            "total_entrances" : int(re.sub(r"[^\d]", "", total_entrances)) if total_entrances else None,
            "total_entrances_label" : total_entrances_label,
        }
        
        yield response.follow(
            url = box_office_url,
            callback = self.parse_entrances,
            meta = meta
        )
            

    def parse_entrances(self, response):
        
        boxoffice = response.css("table.box-office-table tbody tr td.second-col::text").getall()
        box_office_week1 = boxoffice[0].strip() if len(boxoffice) > 0 else None
        box_office_week2 = boxoffice[1].strip() if len(boxoffice) > 1 else None       
         
        meta = {
            **response.meta,
            "box_office_week1" : box_office_week1,
            "box_office_week2" : box_office_week2
        }
        
        yield response.follow(
            url = response.meta["url_casrting"],
            callback = self.parse_casting,
            meta = meta
        )
    
    
    def parse_casting(self, response) : 
        
        societies_allocine = response.css("div.md-table-row > span.item.link.isnt-clickable::text").getall()
        if societies_allocine :
            societies_allocine = list(set(societies_allocine))
            
        soundtrack_elements = response.css("div.gd-col-left > div.section.casting-list-gql > div.md-table-row > span.item.link::text")
        soundtrack_allocine = soundtrack_elements[0].getall() if soundtrack_elements else []
    
        if (response.meta.get("total_entrances_label") and isinstance(response.meta["total_entrances_label"], str) and response.meta["total_entrances_label"].strip().lower() == "box office france") :
    
            yield Jpbox_allocine_item(
                fr_title_allocine = response.meta["fr_title_allocine"],
                original_title_allocine = response.meta["original_title_allocine"],
                url_allocine = response.meta["url_allocine"],
                release_date_allocine = response.meta["release_date_allocine"],
                release_year_allocine = response.meta["release_year_allocine"],
                duration = response.meta["duration"],
                categories_allocine = response.meta["categories_allocine"],
                writer_allocine = response.meta["writer_allocine"],
                director_allocine = response.meta["director_allocine"],
                casting_allocine = response.meta["casting_allocine"],
                press_note = response.meta["press_note"],
                synopsis_allocine = response.meta["synopsis_allocine"],
                classification = response.meta["classification"],
                countries = response.meta["countries"],
                distribution = response.meta["distribution"],
                prod_year = response.meta["prod_year"],
                total_entrances = response.meta["total_entrances"],
                box_office_week1 = response.meta["box_office_week1"],
                box_office_week2 = response.meta["box_office_week2"],
                societies_allocine = [s for s in societies_allocine] if societies_allocine else [],
                soundtrack_allocine = [s for s in soundtrack_allocine] if soundtrack_allocine else [],
            )

