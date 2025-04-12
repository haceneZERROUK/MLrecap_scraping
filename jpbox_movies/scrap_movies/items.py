# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class JpboxItem(scrapy.Item):

    url_movie = scrapy.Field()
    fr_title = scrapy.Field()
    original_title = scrapy.Field()
    country = scrapy.Field()
    category = scrapy.Field()
    released_year = scrapy.Field()
    date = scrapy.Field()
    classification = scrapy.Field()
    duration = scrapy.Field()
    total_entrances = scrapy.Field()
    weekly_entrances = scrapy.Field()
    budget = scrapy.Field()
    incomes_total = scrapy.Field()
    incomes_france = scrapy.Field()
    synopsis = scrapy.Field()
    directors = scrapy.Field()
    actors = scrapy.Field()
    producers = scrapy.Field()
    compositors = scrapy.Field()
    authors = scrapy.Field()
