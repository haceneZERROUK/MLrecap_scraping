import scrapy
import re
from imdb.items import AllocineFullItem

class AllocineAllSpider(scrapy.Spider):
    name = "allocine_all"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/"]
    

    def start_requests(self):

        yield scrapy.Request(
            url = self.start_urls[0],
            callback = self.parse
        )

        
    def parse(self, response):
        
        yield from self.parse_movies_list(response)
        
        pages_number = int(response.css('div.pagination-item-holder span.button-md.item::text').getall()[-1])
        # pages_number = 2
        
        for i in range(2, pages_number+1) :
            next_url = self.start_urls[0] + "?page=" + str(i)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_movies_list)


    def parse_movies_list(self, response) : 

        list_movies = response.css("div.gd-col-middle > ul > li.mdl")

        for movie in list_movies:
            allocine_fr_title = movie.css("div > div.meta.meta-affintiy-score > h2.meta-title > a::text").get().strip()
            allocine_original_title = movie.css("div > div.meta.meta-affintiy-score > div.meta-body > div.meta-body-item > span.dark-grey::text").get()
            if not allocine_original_title:
                allocine_original_title = allocine_fr_title
            allocine_original_title = allocine_original_title.strip()

            allocine_url = response.urljoin(movie.css("div > div.meta.meta-affintiy-score > h2.meta-title > a::attr(href)").get())
            allocine_release_date = movie.css("div > div.meta > div.meta-body > div > span.date::text").get()
            if allocine_release_date : 
                allocine_release_year = int(allocine_release_date.split(" ")[-1])
            else : 
                allocine_release_year = None
                
            allocine_duration = movie.css('div.meta-body-item.meta-body-info::text').re_first(r'\d+h\s*\d+min')


            meta = {
                "allocine_fr_title" : allocine_fr_title.strip() if allocine_fr_title else None,
                "allocine_original_title" : allocine_original_title.strip() if allocine_original_title else None,
                "allocine_url" : allocine_url,
                "allocine_release_date" : allocine_release_date,
                "allocine_release_year" : allocine_release_year, 
                "allocine_duration" : allocine_duration, 
            }

            yield response.follow(
                url = allocine_url,
                callback = self.parse_movie_page,
                meta = meta
            )
        
        
    def parse_movie_page(self, response) : 
        
        allocine_categories = response.css("div.meta-body-item.meta-body-info > span.dark-grey-link::text").getall()
        meta_body_items = response.css("div.meta-body-item.meta-body-direction.meta-body-oneline")
        allocine_writer = meta_body_items[1].css("span.dark-grey-link::text").getall() if len(meta_body_items) > 1 else []
        allocine_director = response.css("div.meta-body-item.meta-body-direction span.dark-grey-link::text").get(default=None)
        allocine_casting = response.css("div.meta-body-item.meta-body-actor span.dark-grey-link::text").getall()
        
        bloc_press_note = response.css("div.rating-item")           
        press_note_label = bloc_press_note.css("div.rating-item-content span::text").get()
        if press_note_label and press_note_label.strip().lower() == "presse":
            allocine_press_note = bloc_press_note.css("div.stareval span.stareval-note::text").get()
        else:
            allocine_press_note = None

        allocine_synopsis = response.css("p.bo-p::text").get()
        allocine_classification = response.css("section[id='synopsis-details'] div.certificate span.certificate-text::text").get()
        if not allocine_classification : 
            allocine_classification = response.css("div.label.kids-label.aged-default::text").get()
        allocine_countries = response.css("section.ovw.ovw-technical div.item span.that span.nationality::text").getall()
        
        technical_bloc = response.css("section.ovw.ovw-technical")
        
        allocine_total_entrances = None
        for item in technical_bloc.css("div.item"):
            total_entrances_label = item.css("span.what.light::text").get()
            if total_entrances_label and total_entrances_label.strip().lower() == "box office france" :
                allocine_total_entrances = item.css("span.that::text").get()
                break
            
        url_film = response.url
        casting_url = url_film.replace("_gen_cfilm=", "-").replace(".html", "/casting/")
        
        dist_label = technical_bloc.css("div.item span.what.light::text").get() 
        if dist_label and dist_label.strip().lower() == "distributeur" :
            allocine_distribution = technical_bloc.css("span.blue-link::text").get()
        else:
            allocine_distribution = technical_bloc.css("span.blue-link::text").get()
            
        prod_year_label = technical_bloc.css("div.item span.what.light::text").get()
        if prod_year_label and prod_year_label.strip().lower() == "année de production" : 
            allocine_prod_year = technical_bloc.css("span.that::text").get()
        else : 
            allocine_prod_year = technical_bloc.css("span.that::text").get()
        
        if not response.meta["allocine_release_date"]:
            date_str = response.css("div.entity-card-player-ovw div.meta div.meta-body div.meta-body-item.meta-body-info span.blue-link::text").get()
            if date_str:
                response.meta["allocine_release_date"] = date_str.strip()            
                
        if not response.meta["allocine_release_year"] and response.meta["allocine_release_date"]:
            try:
                response.meta["allocine_release_year"] = int(response.meta["allocine_release_date"].split(" ")[-1])
            except (ValueError, IndexError):
                response.meta["allocine_release_year"] = None      
        
        meta = {
            **response.meta,
            "allocine_categories" : [c.strip() for c in allocine_categories] if allocine_categories else [],
            "allocine_writer" : [w for w in allocine_writer] if allocine_writer else [],
            "allocine_director" : allocine_director.strip() if allocine_director else None,
            "allocine_casting" : [c for c in allocine_casting] if allocine_casting else [],
            "allocine_press_note" : allocine_press_note.strip() if allocine_press_note else None,
            "allocine_synopsis" : allocine_synopsis.strip() if allocine_synopsis else None,
            "allocine_classification" : allocine_classification.strip() if allocine_classification else None,
            "allocine_countries" : [c for c in allocine_countries] if allocine_countries else [],
            "allocine_distribution" : allocine_distribution.strip() if allocine_distribution else None,
            "allocine_prod_year" : allocine_prod_year.strip() if allocine_prod_year else None,
            "allocine_total_entrances" : int(re.sub(r"[^\d]", "", allocine_total_entrances)) if allocine_total_entrances else None,
        }
        
        yield response.follow(
            url = casting_url,
            callback = self.parse_casting,
            meta = meta
        )


    def parse_casting(self, response):
        allocine_societies = response.css("div.md-table-row > span.item.link.isnt-clickable::text").getall()
        if allocine_societies:
            allocine_societies = list(set(allocine_societies))
        else:
            allocine_societies = []

        soundtrack_elements = response.css("div.gd-col-left > div.section.casting-list-gql > div.md-table-row > span.item.link::text")
        if soundtrack_elements and len(soundtrack_elements) > 0:
            allocine_soundtrack = soundtrack_elements.getall()
            allocine_soundtrack = list(set(allocine_soundtrack))
        else:
            allocine_soundtrack = []

        item = AllocineFullItem(
            allocine_fr_title = response.meta["allocine_fr_title"],
            allocine_original_title = response.meta["allocine_original_title"],
            allocine_url = response.meta["allocine_url"],
            allocine_release_date = response.meta["allocine_release_date"],
            allocine_release_year = response.meta["allocine_release_year"],
            allocine_duration = response.meta["allocine_duration"],
            allocine_categories = response.meta["allocine_categories"],
            allocine_writer = response.meta["allocine_writer"],
            allocine_director = response.meta["allocine_director"],
            allocine_casting = response.meta["allocine_casting"],
            allocine_press_note = response.meta["allocine_press_note"],
            allocine_synopsis = response.meta["allocine_synopsis"],
            allocine_classification = response.meta["allocine_classification"],
            allocine_countries = response.meta["allocine_countries"],
            allocine_distribution = response.meta["allocine_distribution"],
            allocine_prod_year = response.meta["allocine_prod_year"],
            allocine_total_entrances = response.meta["allocine_total_entrances"],
            allocine_box_office_week1 = None,
            allocine_box_office_week2 = None,
            allocine_societies = allocine_societies,
            allocine_soundtrack = allocine_soundtrack,
        )

        box_office_url = response.url.replace("casting", "box-office")

        meta = {
            "item": item,
            "dont_filter": True  # Important: permet de suivre les redirections même vers des URLs déjà visitées
        }

        yield scrapy.Request(
            url=box_office_url,
            callback=self.parse_box_office,
            errback=self.handle_box_office_error,
            meta=meta,
            dont_filter=True  # Important: permet de suivre les redirections même vers des URLs déjà visitées
        )

    def parse_box_office(self, response):
        # Vérifier si nous sommes sur une page box-office ou si nous avons été redirigés
        if "box-office" not in response.url:
            # Nous avons été redirigés, donc pas de données box-office
            yield response.meta["item"]
            return

        # Nous sommes sur une vraie page box-office, extrayons les données
        item = response.meta["item"]

        boxoffice = response.css("table.box-office-table tbody tr td.second-col::text").getall()
        if boxoffice and len(boxoffice) > 0:
            item["allocine_box_office_week1"] = boxoffice[0].strip()
        if boxoffice and len(boxoffice) > 1:
            item["allocine_box_office_week2"] = boxoffice[1].strip()

        yield item

    def handle_box_office_error(self, failure):
        # En cas d'erreur, retourner l'item sans les données box-office
        yield failure.request.meta["item"]


