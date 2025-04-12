import scrapy
from scrap_movies.items import JpboxItem



class MoviesSPider(scrapy.Spider):


    name='moviesspider'
    start_urls = ['https://www.jpbox-office.com/v9_demarrage.php?view=2']
    

    def parse(self, response):


        films = response.css('tr')[3:-4]
        for f in films:
            url_movie = response.urljoin(f.css('td.col_poster_titre > h3 > a::attr(href)').get())
            meta = {
            'url_movie' : url_movie
            }

            yield response.follow(
                url = url_movie,
                callback = self.parse_movie_page, 
                meta = meta
            )



        next_page = response.css('div.pagination a::attr(href)').extract()[-1]

        if next_page is not None :
            yield response.follow(response.urljoin(next_page), callback = self.parse)
    


    def parse_movie_page(self, response):

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
        movie_infos_2 = response.css('td.texte_2022titre a::text').getall()
        if len(movie_infos) > 8:
            cat_movie = movie_infos[5]
        else:
            cat_movie = movie_infos_2[-1]
        url_home_movie = response.url.replace('&view=2', '')

        meta = {
        **response.meta,
        'fr_title': name,
        'original_title':original_name,
        'country':movie_infos[1],
        'category': cat_movie,
        'released_year': response.css('td.texte_2022titre > h3::text').get().replace("\r\n",'').replace('/', "").strip(), 
        'date': date,
        'classification':response.css('table.tablelarge1 div.bloc_infos_center.tablesmall1::text').extract()[-1].strip(),
        'duration':movie_infos[4].strip(),
        'total_entrances': data_result_clean[0],
        'weekly_entrances': data_result_clean[-1]
        
        }

        yield response.follow(
            url = url_home_movie,
            meta = meta,
            callback = self.parse_budget_movies
        )


    def parse_budget_movies(self, response):

        table_bloc = response.css("table.tablesmall.tablesmall1b")

        cell_title = table_bloc.css("tr td strong::text").get()
        if cell_title and cell_title.strip().lower() == "budget" : 
            budget = response.css("table.tablesmall.tablesmall1b tr td div strong::text").get()
        else : 
            budget = None

        cell_income_france = table_bloc.css("tr td em::text").get()
        if cell_income_france and cell_income_france.strip().lower() == "dont france" : 
            income_france = response.css("table.tablesmall.tablesmall1b tr td div em::text").get().replace(" ","")
        else : 
            income_france = None


        cell_income = table_bloc.css("tr td strong::text").getall()
        incomes_total = None
        for idx, text in enumerate(cell_income):
            if text.strip().lower() == "total salles":
                if idx + 1 < len(cell_income):
                    incomes_total = cell_income[idx + 1]
                break
        
        
        synopsis_list = response.css('div.bloc_infos.tablesmall5::text').getall()
        if len(synopsis_list) > 0:
            synopsis = synopsis_list[-1].strip()
        else:
            synopsis = None
        meta = {
            **response.meta,
            'budget' : budget,
            'incomes_total': incomes_total,
            'incomes_france': income_france,
            'synopsis' : synopsis
        }

        url_casting = f'{response.url}&view=7'

        yield response.follow(
            url = url_casting,
            meta = meta,
            callback = self.parse_casting
        )


    def parse_casting(self,response):

        directors = [a.strip() for a in response.css("td[itemprop='director'] h3 a::text").getall()]
        actors = [a.strip() for a in response.css("td[itemprop='actor'] h3 a::text").getall()]
        producers = [a.strip() for a in response.css("td[itemprop='producer'] h3 a::text").getall()]
        authors = [a.strip() for a in response.css("td[itemprop='author'] h3 a::text").getall()]
        compositors = [a.strip() for a in response.css("td[itemprop='compositor'] h3 a::text").getall()]
        

        yield JpboxItem(
            url_movie = response.meta['url_movie'],
            fr_title = response.meta['fr_title'],
            original_title = response.meta['original_title'],
            country = response.meta['country'],
            category = response.meta['category'],
            released_year = response.meta['released_year'],
            date = response.meta['date'],
            classification = response.meta['classification'],
            duration = response.meta['duration'],
            total_entrances = response.meta['total_entrances'],
            weekly_entrances = response.meta['weekly_entrances'],
            budget = response.meta['budget'],
            incomes_total = response.meta['incomes_total'],
            incomes_france = response.meta['incomes_france'],
            synopsis = response.meta['synopsis'],
            directors = directors,
            actors = actors,
            producers = producers,
            compositors = compositors,
            authors = authors,
        )
        


