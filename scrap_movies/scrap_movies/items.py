# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import json




class MoviesSPider(scrapy.Spider):
    """
    Spider pour extraire les informations des films à partir du site jpbox-office.com.
    
    Il scrute la page des films, extrait le nom, l'année, les entrées hebdomadaires et l'URL du film,
    puis suit les liens de pagination pour extraire les informations de pages suivantes.
    """


    name='moviesscrap'
    
    # start_urls = ['https://www.jpbox-office.com/v9_demarrage.php?view=2']
    

    # Ouvre le fichier JSON
    with open('../list_movies.json', 'r', encoding='utf-8') as json_data:
        d = json.load(json_data)  # Utilise json.load() pour charger directement à partir du fichier

    # Extraction des URLs
    urls_list = [movie["url_movie"] for movie in d]


    def parse(self, response):
        """
        Fonction de parsing pour extraire les informations sur les films et gérer la pagination.
        
        Récupère les films de la page courante et génère un dictionnaire avec les informations suivantes :
        - name : Nom du film
        - annee : Année de sortie du film
        - weeklyentrance : Entrées hebdomadaires
        - url_movie : URL du film
        
        Ensuite, il suit le lien de la page suivante si disponible.
        """

        for url in self.urls_list:

            link = response.css(url)

            yield{

            'name': link.css('tr > td.texte_2022titre > h1::text').get().strip(),
            # 'annee': f.css('td.col_poster_contenu  a::text').get()[-4:],
            # 'weeklyentrance': f.css("td.col_poster_contenu_majeur::text").get(),
            # 'url_movie' : response.urljoin(f.css('td.col_poster_titre > h3 > a::attr(href)').get())
            }

        next_page = response.css('div.pagination a::attr(href)').extract()[-1]

        if next_page is not None :
            yield response.follow(response.urljoin(next_page), callback = self.parse)

