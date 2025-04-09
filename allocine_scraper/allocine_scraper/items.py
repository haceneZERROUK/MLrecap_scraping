from scrapy.item import Item, Field


class AllocineItem(Item):
    titre = Field()
    date_sortie = Field()
    duree = Field()
    genres = Field()
    realisateur = Field()
    acteurs = Field()
    numero_film = Field()
    distributeur = Field()
    recompenses = Field()
    annee_production = Field()
    budget = Field()
    pays = Field()
    producteur = Field()
    note_critique = Field()
    vues_bande_annonce = Field()
    box_office_france = Field()
    box_office_etats_unis = Field()