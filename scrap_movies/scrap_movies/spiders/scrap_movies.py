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
    
    def start_requests(self):
        """
        Cette méthode est appelée par Scrapy au début de l'exécution du spider.
        
        Elle a pour rôle de charger un fichier JSON contenant une liste de films, d'extraire les URLs des pages de ces films,
        et d'envoyer une requête Scrapy pour chaque URL afin de récupérer les pages de films et les traiter dans la méthode `parse`.

        Le processus se déroule comme suit :
        1. Le fichier `list_movies.json` est ouvert en mode lecture avec un encodage UTF-8. Ce fichier doit contenir une liste d'objets JSON où chaque objet représente un film.
        2. Le contenu du fichier JSON est chargé dans la variable `data`, qui est une liste de dictionnaires représentant chaque film.
        3. Une liste `urls_list` est générée en extrayant la valeur de la clé `"url_movie"` pour chaque film dans la liste `data`. Cela permet de récupérer toutes les URLs des pages de films.
        4. Pour chaque URL dans `urls_list`, une requête Scrapy est envoyée à l'URL via `scrapy.Request()`. Chaque requête a comme callback la méthode `parse`, ce qui signifie que le contenu de chaque page sera ensuite traité par la méthode `parse`.

        Cette méthode est utilisée pour initialiser l'exécution du spider en envoyant les requêtes de base vers les pages des films.

        Args:
            None

        Yields:
            scrapy.Request: Une requête Scrapy pour chaque URL présente dans le fichier JSON. Le callback de chaque requête est défini sur la méthode `parse`, qui gérera la réponse.

        Exemples:
            Si le fichier JSON contient les données suivantes :
            [
                {"name": "Film 1", "url_movie": "https://www.example.com/film1"},
                {"name": "Film 2", "url_movie": "https://www.example.com/film2"}
            ]
            Alors, deux requêtes seront envoyées, une vers `https://www.example.com/film1` et une autre vers `https://www.example.com/film2`,
            et les réponses seront envoyées à la méthode `parse`.
        """
        # Ouvre le fichier JSON et charge les données
        with open('list_movies.json', 'r', encoding='utf-8') as json_data:
            data = json.load(json_data)

        # Extraction des URLs
        urls_list = [movie["url_movie"] for movie in data]

        # Envoi de la requête pour chaque URL
        for url in urls_list:
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        """
        Fonction de parsing pour extraire les informations sur les films depuis la page.
        
        Récupère les films de la page courante et génère un dictionnaire avec les informations suivantes :
        - name : Nom du film
        - annee : Année de sortie du film
        - weeklyentrance : Entrées hebdomadaires
        - url_movie : URL du film
        
        Ensuite, il suit le lien de la page suivante si disponible.
        """

        name = response.css('tr > td.texte_2022titre > h1::text').get().strip()
        original_name = response.css('tr > td.texte_2022titre > h2::text').get()
        if original_name:
            original_name = original_name.strip()
        else:
            original_name = name 


        yield{

        'name': name,
        'original_name':original_name,
        'year': response.css('table.tablelarge1 tr td p a::text').get().strip()
        }
