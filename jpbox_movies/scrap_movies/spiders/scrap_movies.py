import scrapy
import json




class MoviesSPider(scrapy.Spider):
    """
    Spider pour extraire les informations des films à partir du site jpbox-office.com.
    
    Il scrute la page des films, extrait le nom, l'année, les entrées hebdomadaires et l'URL du film,
    puis suit les liens de pagination pour extraire les informations de pages suivantes.
    """


    name='moviesscrap'
        
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

        with open('list_movies.json', 'r', encoding='utf-8') as json_data:
            data = json.load(json_data)

        urls_list = [movie["url_movie"] for movie in data]

        for url in urls_list:
            yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        """
        Fonction de parsing pour extraire les informations sur les films depuis la page.
        
        Récupère les films de la page courante et génère un dictionnaire avec les informations suivantes :
        - name : Nom du film
        - original_name : Nom du film dans la langue originale
        - realisateur
        - annee : Année de sortie du film
        -category
        - weeklyentrance : Entrées hebdomadaires
        Ensuite, il suit le lien de la page suivante si disponible.
        """

        if response.status == 200:
            # Extraire les données
            print(f'Scrap du lien {response.css('tr > td.texte_2022titre > h1::text').get().strip()}')
        else:
            # Gérer les erreurs
            self.logger.error(f"Erreur de récupération de la page {response.url}")

        name = response.css('tr > td.texte_2022titre > h1::text').get().strip()
        original_name = response.css('tr > td.texte_2022titre > h2::text').get()
        if original_name:
            original_name = original_name.strip()
        else:
            original_name = name

        director = response.css('table.table_2022titre td.texte_2022titre h4 a::text').get()

        if director:
            director = response.css('table.table_2022titre td.texte_2022titre h4 a::text').get().strip()
        else:
            director = 'no information'

        date = response.css('table.tablelarge1 tr td p a::text').get()

        if date:
            date = response.css('table.tablelarge1 tr td p a::text').get()
        else:
            date = 'no information'
            

        data_result = response.css('table.tablesmall.tablesmall2 td.col_poster_contenu_majeur').extract()
        data_result_clean = [clean_data.replace('<td colspan="2" class="col_poster_contenu_majeur">', '')
                                .replace(' ','')
                                .replace("</td>",'')
                            .replace('<tdclass=\"col_poster_contenu_majeur\">', '') for clean_data in data_result]

        movie_infos =  response.css('table.table_2022titre td.texte_2022titre h3 ::text').extract()
        
        
        yield{

        'fr_title': name,
        'original_title':original_name,
        'director': director,
        'country':movie_infos[1],
        'category':movie_infos[5],
        'released_year': response.css('td.texte_2022titre > h3::text').get().replace("\r\n",'').replace('/', "").strip(), 
        'date': date,
        'PEGI':response.css('table.tablelarge1 div.bloc_infos_center.tablesmall1::text').extract()[-1].strip(),
        'duration':movie_infos[4].strip(),
        'total_entrances': data_result_clean[0],
        'weekly_entrances': data_result_clean[-1]
        }
