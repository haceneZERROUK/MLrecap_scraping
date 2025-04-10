import scrapy
import json
import re
from imdb.items import Jpbox_allocine_item



class JpboxAllocineSpider(scrapy.Spider):
    name = "jpbox_allocine"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/"]


    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
        )


    def parse(self, response):
        with open("result-entrances.json") as file:
            self.movies_jpbox = json.load(file)
        
        pages_number = int(response.css('div.pagination-item-holder span.button-md.item::text').getall()[-1])
        
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

            url_allocine = response.urljoin(movie.css("div > div.meta.meta-affintiy-score > h2.meta-title > a::attr('href')").get())
            release_date_allocine = movie.css("div > div.meta > div.meta-body > div > span.date::text").get()
            if release_date_allocine : 
                release_year_allocine = release_date_allocine.split(" ")[-1]
            else : 
                release_year_allocine = ""
            
            jpbox_movie_infos = next((film for film in self.movies_jpbox if re.sub(r'\(.*?\)', '', film["original_title"]).strip().lower() == original_title_allocine or re.sub(r'\(.*?\)', '', film["fr_title"]).strip().lower() == fr_title_allocine), None)

            if jpbox_movie_infos:
                meta = {
                    "fr_title_jpbox": jpbox_movie_infos["fr_title"],
                    "original_title_jpbox": jpbox_movie_infos["original_title"],
                    "director_jpbox": jpbox_movie_infos["director"],
                    "country_jpbox": jpbox_movie_infos["country"],
                    "category_jpbox": jpbox_movie_infos["category"],
                    "released_year_jpbox": jpbox_movie_infos["released_year"],
                    "date_france_jpbox": jpbox_movie_infos["date"],
                    "PEGI_jpbox": jpbox_movie_infos["PEGI"],
                    "duration_jpbox": jpbox_movie_infos["duration"],
                    "total_entrances_jpbox": jpbox_movie_infos["total_entrances"],
                    "weekly_entrances_jpbox": jpbox_movie_infos["weekly_entrances"],
                }

                yield response.follow(
                    url=url_allocine,
                    callback=self.parse_movie_page,
                    meta={
                        **meta,
                        "fr_title_allocine" : fr_title_allocine,
                        "original_title_allocine" : original_title_allocine,
                        "url_allocine" : url_allocine,
                        "release_date_allocine" : release_date_allocine,
                        "release_year_allocine" : release_year_allocine
                    },
                )

                
    def parse_movie_page(self, response) : 
        
        categories_allocine = response.css("div.meta-body-item.meta-body-info > span.dark-grey-link::text").getall()
        meta_body_items = response.css("div.meta-body-item.meta-body-direction.meta-body-oneline")
        writer_allocine = meta_body_items[1].css("span.dark-grey-link::text").getall() if len(meta_body_items) > 1 else []
        director_allocine = response.css("div.meta-body-item.meta-body-direction span.dark-grey-link::text").get()
        casting_allocine = response.css("div.meta-body-item.meta-body-actor span.dark-grey-link::text").getall()
        
        bloc_press_note = response.css("div.rating-item")
        label = bloc_press_note.css("div.rating-item-content span::text").get()
        if label and label.strip().lower() == "presse":
            press_note = bloc_press_note.css("div.stareval span.stareval-note::text").get()
        else:
            press_note = None

        synopsis_allocine = response.css("p.bo-p::text").get()
        
        url_film = response.url        
        casting_url = url_film.replace("_gen_cfilm=", "-").replace(".html", "/casting/")
        
        distributor_bloc = response.css("section.ovw.ovw-technical")
        dist_label = distributor_bloc.css("div.item span.what.light::text").get()  # Extraire le texte du span.what.light
        if dist_label and dist_label.strip().lower() == "distributeur":
            distribution = distributor_bloc.css("span.blue-link::text").get()
        else:
            distribution = distributor_bloc.css("span.blue-link::text").get()  # Essaie toujours de récupérer le texte du blue-link
        
        yield Jpbox_allocine_item(
            fr_title_jpbox = response.meta["fr_title_jpbox"],
            original_title_jpbox = response.meta["original_title_jpbox"],
            director_jpbox = response.meta["director_jpbox"],
            country_jpbox = response.meta["country_jpbox"],
            category_jpbox = response.meta["category_jpbox"],
            released_year_jpbox = response.meta["released_year_jpbox"],
            released_date_jpbox = response.meta["date_france_jpbox"],
            PEGI_jpbox = response.meta["PEGI_jpbox"],
            duration_jpbox = response.meta["duration_jpbox"],
            total_entrances_jpbox = response.meta["total_entrances_jpbox"],
            weekly_entrances_jpbox = response.meta["weekly_entrances_jpbox"],
            
            fr_title_allocine = response.meta["fr_title_allocine"],
            original_title_allocine = response.meta["original_title_allocine"],
            release_date_allocine = response.meta["release_date_allocine"],
            release_year_allocine = response.meta["release_year_allocine"],
            url_allocine = response.meta["url_allocine"],
            categories_allocine = categories_allocine,
            writer_allocine = writer_allocine,
            director_allocine = director_allocine,
            casting_allocine = casting_allocine,
            press_note = press_note,
            synopsis_allocine = synopsis_allocine,
            distribution = distribution,
        )

        
    
    # def parse_casting(self, response) : 
        
    #     societies_allocine = response.css("div.md-table-row > span.item.link.isnt-clickable::text").getall()
    #     Soundtrack_allocine = response.css("div.gd-col-left > div.section.casting-list-gql > div.md-table-row > span.item.link::text")[0].getall()
                
    #     yield Jpbox_allocine_item(
    #         fr_title_jpbox = response.meta["fr_title_jpbox"],
    #         original_title_jpbox = response.meta["original_title_jpbox"],
    #         director_jpbox = response.meta["director_jpbox"],
    #         country_jpbox = response.meta["country_jpbox"],
    #         category_jpbox = response.meta["category_jpbox"],
    #         released_year_jpbox = response.meta["released_year_jpbox"],
    #         released_date_jpbox = response.meta["date_france_jpbox"],
    #         PEGI_jpbox = response.meta["PEGI_jpbox"],
    #         duration_jpbox = response.meta["duration_jpbox"],
    #         total_entrances_jpbox = response.meta["total_entrances_jpbox"],
    #         weekly_entrances_jpbox = response.meta["weekly_entrances_jpbox"],
            
    #         fr_title_allocine = response.meta["fr_title_allocine"],
    #         original_title_allocine = response.meta["original_title_allocine"],
    #         release_date_allocine = response.meta["release_date_allocine"],
    #         release_year_allocine = response.meta["release_year_allocine"],
    #         url_allocine = response.meta["url_allocine"],
    #         categories_allocine = response.meta["categories_allocine"],
    #         writer_allocine = response.meta["writer_allocine"],
    #         director_allocine = response.meta["director_allocine"],
    #         casting_allocine = response.meta["casting_allocine"],
    #         press_note = response.meta["press_note"],
    #         synopsis_allocine = response.meta["synopsis_allocine"],
    #         societies_allocine = societies_allocine,
    #         Soundtrack_allocine = Soundtrack_allocine
    #     )



        # yield scrapy.Request(
        #     url = casting_url,
        #     callback = self.parse_casting,
        #     meta = {
        #         **response.meta, 
        #         "categories_allocine" : categories_allocine,
        #         "writer_allocine" : writer_allocine,
        #         "director_allocine" : director_allocine,
        #         "casting_allocine" : casting_allocine,
        #         "press_note" : press_note,
        #         "synopsis_allocine" : synopsis_allocine
        #     }
        # )
