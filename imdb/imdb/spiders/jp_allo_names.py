import scrapy
import json
import re
from imdb.items import JpboxWithAllocineTitles


class JpAlloNamesSpider(scrapy.Spider):
    name = "jp_allo_names"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/rechercher/movie/?q="]


    def start_requests(self):
        
        with open("jpbox_fulldata.json") as file : 
            jpbox_movies = json.load(file) 
            
        for m in jpbox_movies : 
            jpbox_fr_title = m["fr_title"]
            cleaned_name = re.sub(r'\(.*?\)', '', jpbox_fr_title)
            jpbox_released_year = m["released_year"]
            
            url_search = f"{self.start_urls[0]}{cleaned_name}"
            
            meta = {
                "jpbox_fr_title" : jpbox_fr_title,
                "jpbox_released_year" : jpbox_released_year,
                "jpbox_original_title" : m["original_title"],
                "jpbox_actors" : m["actors"],
                "jpbox_producers" : m["producers"],
                "jpbox_authors" : m["authors"],
                "jpbox_compositors" : m["compositors"],
                "jpbox_directors" : m["directors"],
                "jpbox_country" : m["country"],
                "jpbox_category" : m["category"],
                "jpbox_released_date" : m["date"],
                "jpbox_classification" : m["classification"],
                "jpbox_duration" : m["duration"],
                "jpbox_total_entrances" : m["total_entrances"],
                "jpbox_weekly_entrances" : m["weekly_entrances"],
                "jpbox_incomes_total" : m["incomes_total"],
                "jpbox_incomes_france" : m["incomes_france"],
                "jpbox_budget" : m["budget"],
                "jpbox_url_movie" : m["url_movie"],
                "jpbox_synopsis" : m["synopsis"],
            }
            
            yield scrapy.Request(
                url = url_search,
                callback = self.parse,
                meta = meta
            )
  

    def parse(self, response):
        
        movie_results = response.css("section.movies-results ul li")

        if movie_results:
            for movie in movie_results:
                date_text = movie.css("div.meta-body-item.meta-body-info span.date::text").get()
                if date_text:
                    allocine_released_year = date_text.split(" ")[-1]

                    if allocine_released_year == response.meta["jpbox_released_year"]:
                        allocine_fr_title = movie.css("h2.meta-title span.meta-title-link::text").get()

                        yield JpboxWithAllocineTitles(
                            jpbox_fr_title = response.meta["jpbox_fr_title"],
                            jpbox_released_year = response.meta["jpbox_released_year"],
                            allocine_fr_title = allocine_fr_title,
                            allocine_released_year = allocine_released_year,
                            jpbox_original_title = response.meta["jpbox_original_title"],
                            jpbox_actors = response.meta["jpbox_actors"],
                            jpbox_producers = response.meta["jpbox_producers"],
                            jpbox_authors = response.meta["jpbox_authors"],
                            jpbox_compositors = response.meta["jpbox_compositors"],
                            jpbox_directors = response.meta["jpbox_directors"],
                            jpbox_country = response.meta["jpbox_country"],
                            jpbox_category = response.meta["jpbox_category"],
                            jpbox_released_date = response.meta["jpbox_released_date"],
                            jpbox_classification = response.meta["jpbox_classification"],
                            jpbox_duration = response.meta["jpbox_duration"],
                            jpbox_total_entrances = response.meta["jpbox_total_entrances"],
                            jpbox_weekly_entrances = response.meta["jpbox_weekly_entrances"],
                            jpbox_incomes_total = response.meta["jpbox_incomes_total"],
                            jpbox_incomes_france = response.meta["jpbox_incomes_france"],
                            jpbox_budget = response.meta["jpbox_budget"],
                            jpbox_url_movie = response.meta["jpbox_url_movie"],
                            jpbox_synopsis = response.meta["jpbox_synopsis"],
                        )
                        # Arrêter après avoir trouvé une correspondance
                        return

        # Vérifier s'il y a des pages suivantes
        try:
            page_number = int(response.css("nav.pagination.cf div.pagination-item-holder span.button.button-md.item::text").getall()[-1])
            current_page = 1
            if "page=" in response.url:
                current_page = int(response.url.split("page=")[1])

            # Ne passer à la page suivante que si nous n'avons pas trouvé de correspondance
            if current_page < page_number:
                next_page = current_page + 1
                next_url = response.url.split("?")[0] + f"?page={next_page}"
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    meta=response.meta
                )
        except (IndexError, ValueError):
            pass
    



