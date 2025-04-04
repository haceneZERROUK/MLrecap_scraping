import scrapy

class MoviesSPider(scrapy.Spider):
    name='films'
    start_urls = ['https://www.jpbox-office.com/v9_demarrage.php?view=2']
    

    def parse(self, response):
        # films = response.css('td h3 a::text').getall()
        # entrance_stats = response.css('td.col_poster_contenu_majeur ::text').getall()
        # url_link = response.css('td > h3 >  a::attr(href)').getall()

        films = response.css('tr')[3:-4]
        for f in films:

            yield{

            'name': f.css('td.col_poster_titre > h3 > a::text').get(),
            'original_name':
            'annee': f.css('td.col_poster_contenu  a::text').get()[-4:],
            'weeklyentrance': f.css("td.col_poster_contenu_majeur::text").get(),
            'url_movie' : response.urljoin(f.css('td.col_poster_titre > h3 > a::attr(href)').get())
            }

