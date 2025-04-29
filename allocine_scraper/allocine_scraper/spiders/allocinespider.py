import scrapy
from allocine_scraper.items import AllocineItem
from urllib.parse import urlencode


class AllocineSpider(scrapy.Spider):
    name = "allocine"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/decennie-2020/"]

    def parse(self, response):
        # Récupérer le nombre de pages
        nombre_de_pages = response.css('div.pagination-item-holder span.button-md.item::text').getall()
        if nombre_de_pages:
            nombre_de_pages = int(nombre_de_pages[-1])
        else:
            nombre_de_pages = 1

        # Extraire les films de la page actuelle
        films = response.css('div.card.entity-card.entity-card-list.cf')
        for film in films:
            titre = film.css('a.meta-title-link ::text').get()
            date_sortie = film.css('div.meta-body-item.meta-body-info span.date::text').get()
            duree = film.css('div.meta-body-item.meta-body-info *::text').getall()
            duree = duree[4].strip() if len(duree) > 4 else None
            genres = film.css('div.meta-body-item.meta-body-info span.dark-grey-link::text').getall()
            realisateur = film.css('div.meta-body-item.meta-body-direction span.dark-grey-link::text').getall()
            acteurs = film.css('div.meta-body-item.meta-body-actor span.dark-grey-link::text').getall()
            url_film = film.css('a.meta-title-link').attrib['href']
            numero_film = ''.join([x for x in url_film if x.isdigit()])

            # Créer un item
            film_item = AllocineItem()
            film_item['titre'] = titre
            film_item['date_sortie'] = date_sortie
            film_item['duree'] = duree
            film_item['genres'] = genres
            film_item['realisateur'] = realisateur
            film_item['acteurs'] = acteurs
            film_item['numero_film'] = numero_film

            # Suivre le lien vers les détails du film
            yield response.follow(
                url=url_film,
                callback=self.parse_details_film,
                meta={'item': film_item}
            )

        # Pagination
        for i in range(2, nombre_de_pages + 1):
            params = {'page': i}
            url_page_suivante = f"{response.url.split('?')[0]}?{urlencode(params)}"
            yield response.follow(url_page_suivante, callback=self.parse)

    def parse_details_film(self, response):
        film_item = response.meta['item']
        producteurs = response.xpath('//div[contains(@class, "meta-body-oneline")]/span[contains(text(), "Par")]/following-sibling::span/text()').getall()
        recompenses = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Récompenses")]/following-sibling::span/text()').get(default="").strip()
        pays = response.css('section.ovw-technical span.nationality ::text').getall()
        distributeur = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Distributeur")]/following-sibling::span/text()').get()
        url_bande_annonce = response.css('a.trailer.roller-item::attr(href)').get()
        budget = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Budget")]/following-sibling::span/text()').get()
        annee_production = response.xpath('//div[contains(@class, "item")]/span[contains(text(), "Année de production")]/following-sibling::span/text()').get()
        note_critique = response.css('div.rating-holder.rating-holder-3 span.stareval-note ::text').get()

        film_item['distributeur'] = distributeur
        film_item['recompenses'] = recompenses
        film_item['annee_production'] = annee_production
        film_item['budget'] = budget
        film_item['pays'] = pays
        film_item['producteur'] = producteurs
        film_item['note_critique'] = note_critique

        # Suivre le lien vers la bande-annonce
        if url_bande_annonce:
            yield response.follow(
                url=url_bande_annonce,
                callback=self.parse_bande_annonce,
                meta={'item': film_item}
            )
        else:
            yield film_item

    def parse_bande_annonce(self, response):
        film_item = response.meta['item']
        vues_bande_annonce = response.css('div.media-info-item.icon.icon-eye ::text').get()
        if vues_bande_annonce:
            vues_bande_annonce = vues_bande_annonce.strip()
        film_item["vues_bande_annonce"] = vues_bande_annonce

        # Suivre le lien vers le box-office
        yield response.follow(
            url=f'https://www.allocine.fr/film/fichefilm-{film_item["numero_film"]}/box-office/',
            callback=self.parse_box_office,
            meta={'item': film_item}
        )

    def parse_box_office(self, response):
        film_item = response.meta['item']
        tables = response.css('section.section')

        box_office_france = None
        box_office_etats_unis = None

        for index, table in enumerate(tables):
            premiere_semaine = table.css('td.responsive-table-column.second-col.col-bg::text').get()
            if premiere_semaine:
                premiere_semaine_format = premiere_semaine.strip().replace(" ", "")
            else:
                premiere_semaine_format = ""

            if index == 1:
                box_office_france = premiere_semaine_format
            elif index == 2:
                box_office_etats_unis = premiere_semaine_format

        film_item['box_office_france'] = box_office_france
        film_item['box_office_etats_unis'] = box_office_etats_unis

        yield film_item