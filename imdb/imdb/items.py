# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    
    original_title_imdb = scrapy.Field()
    fr_title_imdb = scrapy.Field()
    release_year_imdb = scrapy.Field()
    certification_imdb = scrapy.Field()
    duration_imdb = scrapy.Field()
    score_imdb = scrapy.Field()
    metascore_imdb = scrapy.Field()
    voters_number_imdb = scrapy.Field()
    description_imdb = scrapy.Field()
    categories_imdb = scrapy.Field()
    languages_imdb = scrapy.Field()
    prod_cies_imdb = scrapy.Field()
    countries_imdb = scrapy.Field()
    actors_imdb = scrapy.Field()
    directors_imdb = scrapy.Field()
    writers_imdb = scrapy.Field()
    budget_imdb = scrapy.Field()
    url_imdb = scrapy.Field()
    
    fr_title_jpbox = scrapy.Field()
    original_title_jpbox = scrapy.Field()
    director_jpbox = scrapy.Field()
    country_jpbox = scrapy.Field()
    category_jpbox = scrapy.Field()
    released_year_jpbox = scrapy.Field()
    date_jpbox = scrapy.Field()
    PEGI_jpbox = scrapy.Field()
    duration_jpbox = scrapy.Field()
    total_entrances_jpbox = scrapy.Field()
    weekly_entrances_jpbox = scrapy.Field()
    duration_mins = scrapy.Field()
    

class Jpbox_allocine_item(scrapy.Item):

    fr_title_jpbox = scrapy.Field()
    original_title_jpbox = scrapy.Field()
    director_jpbox = scrapy.Field()
    country_jpbox = scrapy.Field()
    category_jpbox = scrapy.Field()
    released_year_jpbox = scrapy.Field()
    released_date_jpbox = scrapy.Field()
    PEGI_jpbox = scrapy.Field()
    duration_jpbox = scrapy.Field()
    total_entrances_jpbox = scrapy.Field()
    weekly_entrances_jpbox = scrapy.Field()
    
    fr_title_allocine = scrapy.Field()
    original_title_allocine = scrapy.Field()
    release_date_allocine = scrapy.Field()
    release_year_allocine = scrapy.Field()
    url_allocine = scrapy.Field()
    categories_allocine = scrapy.Field()
    writer_allocine = scrapy.Field()
    director_allocine = scrapy.Field()
    casting_allocine = scrapy.Field()
    press_note = scrapy.Field()
    synopsis_allocine = scrapy.Field()
    distribution = scrapy.Field()