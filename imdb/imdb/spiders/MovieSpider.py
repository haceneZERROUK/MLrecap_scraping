import scrapy
import scrapy.selector


class MovieSpider(scrapy.Spider):
    name = "MovieSpider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/fr/search/title/?title_type=feature"]

    
    def start_requests(self):
        pass
        
    
    
    
    def parse(self, response):
        
        selector = scrapy.selector(self.start_urls[0])
        list_movies = selector.css(".ipc-metadata-list.ipc-metadata-list--dividers-between.sc-e22973a9-0.khSCXM.detailed-list-view.ipc-metadata-list--base")
        movies = list_movies.css("li.ipc-metadata-list-summary-item").getall()
        for m in movies : 
            url = m.css("a.ipc-title-link-wrapper::attr(href)").get()
            url_movie = response.urljoin(url)
            yield response.follow(url_movie, callback=self.parse_movie_page,meta={"url_movie" : url_movie})
            
        
    def parse_movie_page(self, response) : 
        
        original_title = response.css("span.sc-ec65ba05-1.fUCCIx::text").get()
        fr_title = response.css("span.hero__primary-text::text").get()
        if not original_title : 
            original_title = fr_title
        release_year = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(1) > a::text").get()
        certification = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(2) > a::text").get()
        duration = response.css("div.sc-70a366cc-0.bxYZmb > ul > li:nth-child(3)::text").get()
        score = response.css("span.sc-d541859f-1.imUuxf::text").get()
        metascore = response.css("span.score > span.sc-b0901df4-0::text").get()
        voters_number = response.css("div.sc-d541859f-3::text").get()
        description = response.css("span.sc-42125d72-2.mmImo::text").get()
        genre = response.css("div.ipc-chip-list__scroller > a > span::text").getall()
        languages = response.css("li[data-testid='title-details-languages'] > div > ul > li > a::text").getall()
        prod_cies = response.css("li[data-testid='title-details-companies'] > div > ul > li > a::text").getall()
        countries = response.css("li[data-testid='title-details-origin'] > div > ul > li > a::text").getall()
        actors = list(set(response.css("div[role='presentation'] > ul > li:nth-child(3) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        directors = list(set(response.css("div[role='presentation'] > ul > li:nth-child(1) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        writers = list(set(response.css("div[role='presentation'] > ul > li:nth-child(2) > div.ipc-metadata-list-item__content-container > ul[role='presentation'] > li > a::text").getall()))
        budget = response.css("div[data-testid='title-boxoffice-section'] > ul > li[data-testid='title-boxoffice-budget'] div > ul > li > span::text").get().replace("\u202f", "").replace("\xa0", "").replace("$US (estimé)", "")
        


        
        
        
        pass
        
        
        


