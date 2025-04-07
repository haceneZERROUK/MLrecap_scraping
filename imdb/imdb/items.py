# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    
    original_title = scrapy.Field()
    fr_title = scrapy.Field()
    release_year = scrapy.Field()
    certification = scrapy.Field()
    duration = scrapy.Field()
    score = scrapy.Field()
    metascore = scrapy.Field()
    voters_number = scrapy.Field()
    description = scrapy.Field()
    categories = scrapy.Field()
    languages = scrapy.Field()
    prod_cies = scrapy.Field()
    countries = scrapy.Field()
    actors = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    budget = scrapy.Field()
    
