import scrapy
import json
import pandas as pd


class JpAlloNamesSpider(scrapy.Spider):
    name = "jp_allo_names"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/rechercher/?q="]


    def start_requests(self):
        
        with open("jpbox_fulldata.json") as file : 
            jpbox_movies = json.load(file) 
            

        pass

    def parse(self, response):
        
        pass









