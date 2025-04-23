# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UpcomingItem(scrapy.Item):
    fr_title = scrapy.Field() 
    original_title = scrapy.Field() 
    released_date = scrapy.Field() 
    released_year = scrapy.Field() 
    actor_1 = scrapy.Field() 
    actor_2 = scrapy.Field() 
    actor_3 = scrapy.Field() 
    directors = scrapy.Field() 
    writer = scrapy.Field() 
    distribution = scrapy.Field() 
    country = scrapy.Field() 
    category = scrapy.Field() 
    classification = scrapy.Field() 
    duration = scrapy.Field() 
    duration_minutes = scrapy.Field() 
    allocine_url = scrapy.Field()
    image_url = scrapy.Field()
    imdb_url = scrapy.Field()
    budget = scrapy.Field() 



