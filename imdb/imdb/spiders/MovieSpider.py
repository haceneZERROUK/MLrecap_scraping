import scrapy
import scrapy.selector
from imdb.items import ImdbItem


class MovieSpider(scrapy.Spider):
    """
    Spider pour récupérer des informations sur les films à partir d'IMDb.
    Ce spider parcourt les pages de résultats de recherche de films et récupère
    des informations détaillées sur chaque film.
    """
    
    name = "MovieSpider"  # Nom du spider
    allowed_domains = ["www.imdb.com"]  # Domaine autorisé pour les requêtes
    start_urls = ["https://www.imdb.com/fr/search/title/?title_type=feature"]  # URL de départ pour la recherche de films
    
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            "original_title", 
            "fr_title", 
            "release_year", 
            "certification", 
            "duration", 
            "score", 
            "metascore", 
            "voters_number", 
            "description", 
            "categories", 
            "Languages", 
            "prod_cies", 
            "countries", 
            "actors", 
            "directors", 
            "writers", 
            "budget"
                ]
    }

    
    def start_requests(self):
        """
        Méthode de démarrage des requêtes. Pour l'instant, elle ne fait rien,
        mais peut être étendue pour envoyer des requêtes personnalisées.
        """
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse) 
        
    
    
    def parse(self, response):
        """
        Méthode principale pour analyser la page de résultats de recherche.
        Cette méthode extrait les films listés sur la page de résultats et
        envoie des requêtes pour récupérer les pages détaillées de chaque film.
        
        :param response: L'objet de réponse de la requête HTTP
        """
        
        # Initialisation du sélecteur pour la page de résultats
        selector = scrapy.selector.Selector(response)
        
        # Sélection de la liste des films sur la page
        list_movies = selector.css(".ipc-metadata-list.ipc-metadata-list--dividers-between.sc-e22973a9-0.khSCXM.detailed-list-view.ipc-metadata-list--base")
        
        # Extraction des éléments de film
        movies = list_movies.css("li.ipc-metadata-list-summary-item")
        
        # Parcours de chaque film pour obtenir l'URL de sa page
        for m in movies: 
            url = m.css("a.ipc-title-link-wrapper::attr(href)").get()
            url_movie = response.urljoin(url)  # Construction de l'URL complète du film
            
            # Envoi de la requête pour récupérer la page détaillée du film
            yield response.follow(url_movie, callback=self.parse_movie_page, meta={"url_movie": url_movie})
            
        
    def parse_movie_page(self, response):
        """
        Méthode pour analyser la page détaillée de chaque film.
        Elle extrait les informations spécifiques sur chaque film comme 
        le titre, l'année de sortie, la durée, le score, etc.
        
        :param response: L'objet de réponse de la requête HTTP pour la page du film
        """
        
        # Extraction du titre original et du titre en français
        original_title = response.css("span.sc-ec65ba05-1.fUCCIx::text").get()
        fr_title = response.css("span.hero__primary-text::text").get()
        if not original_title:  # Si le titre original n'est pas trouvé, on utilise le titre français
            original_title = fr_title
        
        # Extraction de l'année de sortie, de la certification, de la durée, etc.
        release_year = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(1) > a::text").get()
        certification = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(2) > a::text").get()
        duration = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(3)::text").get()
        score = response.css("span.sc-d541859f-1.imUuxf::text").get()
        metascore = response.css("span.score > span.sc-b0901df4-0::text").get()
        voters_number = response.css("div.sc-d541859f-3::text").get()
        description = response.css("span.sc-42125d72-2.mmImo::text").get()
        
        # Extraction des genres, des langues, des sociétés de production, etc.
        categories = response.css("div.ipc-chip-list__scroller > a > span::text").getall()
        languages = response.css("li[data-testid='title-details-languages'] > div > ul > li > a::text").getall()
        prod_cies = response.css("li[data-testid='title-details-companies'] > div > ul > li > a::text").getall()
        countries = response.css("li[data-testid='title-details-origin'] > div > ul > li > a::text").getall()
        
        # Extraction des acteurs, réalisateurs et scénaristes
        actors = list(set(response.css("div[role='presentation'] > ul > li:nth-child(3) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        directors = list(set(response.css("div[role='presentation'] > ul > li:nth-child(1) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        writers = list(set(response.css("div[role='presentation'] > ul > li:nth-child(2) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        
        # Extraction du budget du film
        budget = response.css("div[data-testid='title-boxoffice-section'] > ul > li[data-testid='title-boxoffice-budget'] div > ul > li > span::text").get().replace("\u202f", "").replace("\xa0", "").replace("$US (estimé)", "")
        
        yield ImdbItem(
            original_title = original_title,
            fr_title = fr_title,
            release_year = release_year,
            certification = certification,
            duration = duration,
            score = score,
            metascore = metascore,
            voters_number = voters_number,
            description = description,
            categories = categories,
            languages = languages,
            prod_cies = prod_cies,
            countries = countries,
            actors = actors,
            directors = directors,
            writers = writers,
            budget = budget
        )
