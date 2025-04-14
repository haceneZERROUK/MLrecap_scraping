from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from allocine_affiche.spiders.films_affiche import FilmsAfficheSpider

def run():
    print(">>> Début de l'exécution du spider AlloCiné")
    process = CrawlerProcess(get_project_settings())
    process.crawl(FilmsAfficheSpider)
    process.start()
    print(">>> Fin de l'exécution")

if __name__ == "__main__":
    run()
