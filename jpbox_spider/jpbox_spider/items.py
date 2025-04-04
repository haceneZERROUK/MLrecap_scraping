# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JpboxSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    titre_film = scrapy.Field()
    pass
