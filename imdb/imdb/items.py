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

    fr_title_allocine = scrapy.Field()
    original_title_allocine = scrapy.Field()
    url_allocine = scrapy.Field()
    release_date_allocine = scrapy.Field()
    release_year_allocine = scrapy.Field()
    duration = scrapy.Field()
    categories_allocine = scrapy.Field()
    writer_allocine = scrapy.Field()
    director_allocine = scrapy.Field()
    casting_allocine = scrapy.Field()
    press_note = scrapy.Field()
    synopsis_allocine = scrapy.Field()
    classification = scrapy.Field()
    countries = scrapy.Field()
    distribution = scrapy.Field()
    prod_year = scrapy.Field()
    total_entrances = scrapy.Field()
    box_office_week1 = scrapy.Field()
    box_office_week2 = scrapy.Field()
    societies_allocine = scrapy.Field()
    soundtrack_allocine = scrapy.Field()
    
    
class AllocineFullItem(scrapy.Item) : 

    allocine_fr_title = scrapy.Field()
    allocine_original_title = scrapy.Field()
    allocine_url = scrapy.Field()
    allocine_release_date = scrapy.Field()
    allocine_release_year = scrapy.Field()
    allocine_duration = scrapy.Field()
    allocine_categories = scrapy.Field()
    allocine_writer = scrapy.Field()
    allocine_director = scrapy.Field()
    allocine_casting = scrapy.Field()
    allocine_press_note = scrapy.Field()
    allocine_synopsis = scrapy.Field()
    allocine_classification = scrapy.Field()
    allocine_countries = scrapy.Field()
    allocine_distribution = scrapy.Field()
    allocine_prod_year = scrapy.Field()
    allocine_total_entrances = scrapy.Field()
    allocine_box_office_week1 = scrapy.Field()
    allocine_box_office_week2 = scrapy.Field()
    allocine_societies = scrapy.Field()
    allocine_soundtrack = scrapy.Field()







