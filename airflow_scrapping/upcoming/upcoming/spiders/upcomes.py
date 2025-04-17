import scrapy
from datetime import date, timedelta, datetime
import re
import json
from upcoming.upcoming.items import UpcomingItem


iFRENCH_MONTHS = {
    'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6,
    'juillet': 7, 'août': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
}

class UpcomesSpider(scrapy.Spider):
    name = "upcomes"
    allowed_domains = ["www.allocine.fr", "www.imdb.com"]
    start_urls = ["https://www.allocine.fr"]

    custom_settings = {
            'FEEDS': {
                '/opt/airflow/data/films.json': {
                    'format': 'json',
                    'encoding': 'utf8',
                    'overwrite': True,
                }
            },
        }

    today = date.today()
    days_until_wednesday = (2 - today.weekday()) % 7
    next_wednesday = today + timedelta(days=days_until_wednesday)

    def start_requests(self):
        allocine_upcoming = f"https://www.allocine.fr/film/agenda/sem-{self.next_wednesday.strftime('%Y-%m-%d')}/"
        yield scrapy.Request(
            url=allocine_upcoming,
            callback=self.parse_allocine_upcoming
        )

    def parse_allocine_upcoming(self, response):
        movies = response.css("div.gd-col-left ul li.mdl") or response.css("li.mdl") or response.css("div.card-entity-list div.card")
        for m in movies:
            rel = m.css("div.card.entity-card div.meta h2.meta-title a.meta-title-link::attr('href')").get()
            if rel:
                movie_url = response.urljoin(rel)
                yield response.follow(
                    url=movie_url,
                    callback=self.parse_allocine_movie_page
                )

    def parse_allocine_movie_page(self, response):
        fr_title = response.css(
            "div.titlebar.titlebar-page div.titlebar-title.titlebar-title-xl::text"
        ).get() or ""

        original_title = response.css(
            "div.meta-body div.meta-body-item span.dark-grey::text"
        ).get() or fr_title

        # Raw date string, e.g. "23 avril 2025"
        raw_date = response.css(
            "div.meta-body div.meta-body-info span.date.blue-link::text"
        ).get()
        raw_date = raw_date.strip() if raw_date else self.next_wednesday.strftime("%d %B %Y")

        # Parse manually using FRENCH_MONTHS mapping
        try:
            day_str, month_str, year_str = raw_date.split()
            day = int(day_str)
            month = FRENCH_MONTHS[month_str.lower()]
            year = int(year_str)
            date_obj = datetime(year, month, day)
        except Exception:
            date_obj = datetime.combine(self.next_wednesday, datetime.min.time())

        released_date = date_obj.strftime("%d/%m/%Y")
        released_year = str(date_obj.year)

        # Actors
        actors = response.css("div.meta-body-actor span.dark-grey-link::text").getall() or []
        actor_1 = actors[0] if len(actors) > 0 else "no_actor"
        actor_2 = actors[1] if len(actors) > 1 else "no_actor"
        actor_3 = actors[2] if len(actors) > 2 else "no_actor"

        # Director & Writer (both under .meta-body-direction)
        crew = response.css("div.meta-body-direction span.dark-grey-link::text").getall() or []
        director = crew[0] if crew else "unknown"
        writer = crew[-1] if crew else "unknown"

        # Distribution, Country, Category
        distribution = (
            response.css("section.ovw.ovw-technical div.item span.blue-link::text").get() 
            or "unknown"
        )
        country = (
            response.css("section.ovw.ovw-technical div.item span.that span.nationality::text").get()
            or "unknown"
        )
        category = (
            response.css("div.meta-body-info span.dark-grey-link::text").get()
            or "unknown"
        )

        # Classification
        classification = (
            response.css("div.label.kids-label.aged-default::text").get()
            or response.css("span.certificate-text::text").get()
            or "Tout public"
        )

        # Duration
        duration_str = "".join(
            [e.strip() for e in response.css(
                "div.card.entity-card div.meta div.meta-body div.meta-body-item::text"
            ).getall()]
        ).replace(",", "")
        if duration_str and "h" in duration_str:
            parts = duration_str.replace("h", "").replace("min", "").split()
            hours, mins = int(parts[0]), int(parts[1]) if len(parts) > 1 else 0
            duration_minutes = hours * 60 + mins
            duration = f"{hours}h {mins:02d}min"
        else:
            duration_minutes = 60
            duration = "1h 00min"

        image_url = response.css(
            "div.entity-card-player-ovw figure.thumbnail span img.thumbnail-img::attr('src')"
        ).get()

        yield UpcomingItem(
            fr_title=fr_title,
            original_title=original_title,
            released_date=released_date,
            released_year=released_year,
            actor_1=actor_1,
            actor_2=actor_2,
            actor_3=actor_3,
            director=director,
            writer=writer,
            distribution=distribution,
            country=country,
            category=category,
            classification=classification,
            duration=duration,
            duration_minutes=duration_minutes,
            allocine_url=response.url,
            image_url=image_url,
        )


class Upcomes_imdb(scrapy.Spider):
    name = "Upcomes_imdb"
    allowed_domains = ["www.allocine.fr", "www.imdb.com"]
    start_urls = ["https://www.imdb.com"]

    def country_to_code(country):
        with open("pays_codes.json", "r", encoding="utf-8") as f:
            countries_codes = json.load(f)
        return countries_codes.get(country, country).upper()

    def start_requests(self):
        fr_title = ""
        country = ""
        released_year = ""
        imdb_search_url = (
            f"https://www.imdb.com/fr/search/title/?title={fr_title}"
            f"&title_type=feature&release_date={released_year}-01-01,&countries={country}"
        )
        yield scrapy.Request(
            url=imdb_search_url,
            callback=self.parse_imdb_search_page
        )

    def parse_imdb_search_page(self, response):
        movie_href = (
            response.css("div.sc-1c782bdc-1.jeRnfh.dli-parent \
                          div.sc-1c782bdc-0.kZFQUh \
                          div.sc-2bbfc9e9-0.jUYPWY \
                          div.ipc-title a::attr(href)").get()
        )
        if movie_href:
            movie_url = response.urljoin(movie_href)
            # yield response.follow(url=movie_url, callback=self.parse_imdb_movie_page)

    def parse_imdb_movie_page(self, response):
        try:
            budget_element = response.css(
                "section[data-testid='BoxOffice'] \
                 li[data-testid='title-boxoffice-budget'] span::text"
            ).get()
            if budget_element:
                budget_brut = budget_element.replace("(estimé)", "")
                budget = re.sub(r'[^\d]', '', budget_brut)
            else:
                budget = None
        except Exception:
            budget = None

        image_url = response.meta.get("image_url") or response.urljoin(
            response.css("div.ipc-media img::attr('src')").get()
        )
        # process budget, image_url, etc.
