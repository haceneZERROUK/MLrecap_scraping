import scrapy

class MoviesBudget(scrapy.Spider):
    """
    Spider pour extraire les informations des films à partir du site jpbox-office.com.
    
    Il scrute la page des films, extrait le nom, l'année, les entrées hebdomadaires et l'URL du film,
    puis suit les liens de pagination pour extraire les informations de pages suivantes.
    """


    name='moviesbudget'
    start_urls = ['https://www.jpbox-office.com/budgets.php']
    

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

        films = response.css('tr')[2:]
        for f in films:
            
            result_movie = f.css('td.col_poster_contenu_majeur::text').getall()
            result_income = f.css('td.col_poster_contenu_majeur font::text').getall()

            yield{

            'name': f.css('td.col_poster_titre h3  a::text').get(),
            'budget': result_movie[0].strip().replace('$', '').replace(' ',''),
            'income_boxoffice' : result_movie[1].strip().replace('$', '').replace(' ',''),
            'profit':result_income[0].strip().replace('$', '').replace(' ',''),
            'profitability':result_income[1].strip().replace('%', '').replace(' ','')
            }

        next_page = response.css('div.pagination a::attr(href)').extract()[-1]

        if next_page is not None :
            yield response.follow(response.urljoin(next_page), callback = self.parse)
