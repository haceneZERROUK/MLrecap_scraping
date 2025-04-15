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

class JpboxWithAllocineTitles(scrapy.Item) : 

    jpbox_fr_title = scrapy.Field()
    jpbox_released_year = scrapy.Field()
    allocine_fr_title = scrapy.Field()
    allocine_released_year = scrapy.Field()
    jpbox_original_title = scrapy.Field()
    jpbox_actors = scrapy.Field()
    jpbox_producers = scrapy.Field()
    jpbox_authors = scrapy.Field()
    jpbox_compositors = scrapy.Field()
    jpbox_directors = scrapy.Field()
    jpbox_country = scrapy.Field()
    jpbox_category = scrapy.Field()
    jpbox_released_date = scrapy.Field()
    jpbox_classification = scrapy.Field()
    jpbox_duration = scrapy.Field()
    jpbox_total_entrances = scrapy.Field()
    jpbox_weekly_entrances = scrapy.Field()
    jpbox_incomes_total = scrapy.Field()
    jpbox_incomes_france = scrapy.Field()
    jpbox_budget = scrapy.Field()
    jpbox_url_movie = scrapy.Field()
    jpbox_synopsis = scrapy.Field()
    
    
class ItemImdbComplement(scrapy.Item) : 
    jpbox_fr_title = scrapy.Field()
    allocine_fr_title = scrapy.Field()
    jpbox_released_year = scrapy.Field()
    jpbox_actors = scrapy.Field()
    jpbox_directors = scrapy.Field()
    allocine_writer = scrapy.Field()
    allocine_distribution = scrapy.Field()
    jpbox_country = scrapy.Field()
    jpbox_budget = scrapy.Field()
    jpbox_category = scrapy.Field()
    jpbox_released_date = scrapy.Field()
    allocine_classification = scrapy.Field()
    jpbox_duration = scrapy.Field()
    jpbox_weekly_entrances = scrapy.Field()
    duration_minutes = scrapy.Field()
    imdb_url = scrapy.Field()
    imdb_title = scrapy.Field()
    imdb_released_year = scrapy.Field()
    imdb_directors = scrapy.Field()
    imdb_writer = scrapy.Field()
    imdb_actors = scrapy.Field()
    imdb_distribution = scrapy.Field()
    imdb_budget = scrapy.Field()





