import scrapy
from datetime import date, timedelta, datetime
import re
from upcoming.upcoming.items import UpcomingItem


FRENCH_MONTHS = {
    "janvier": 1,
    "février": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "août": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "décembre": 12,
}


class UpcomesSpider(scrapy.Spider):
    name = "upcomes"
    allowed_domains = ["www.allocine.fr", "www.imdb.com"]
    start_urls = ["https://www.allocine.fr"]

    custom_settings = {
        "FEEDS": {
            "./data/films.json": {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
            }
        },
    }

    today = date.today()
    days_until_wednesday = (2 - today.weekday()) % 7
    next_wednesday = today + timedelta(days=days_until_wednesday)

    def start_requests(self):
        allocine_upcoming = f"https://www.allocine.fr/film/agenda/sem-{self.next_wednesday.strftime('%Y-%m-%d')}/"
        yield scrapy.Request(
            url=allocine_upcoming, callback=self.parse_allocine_upcoming
        )

    def parse_allocine_upcoming(self, response):

        movies = response.css("div.gd-col-left ul li.mdl")
        if not movies:
            movies = response.css("li.mdl")
        if not movies:
            movies = response.css("div.card-entity-list div.card")

        for m in movies:

            movie_url = response.urljoin(
                m.css(
                    "div.card.entity-card div.meta h2.meta-title a.meta-title-link::attr('href')"
                ).get()
            )
            synopsis = m.css("div.content-txt::text").get()

            meta = {"synopsis": synopsis}

            yield response.follow(
                url=movie_url, callback=self.parse_allocine_movie_page, meta=meta
            )

    def parse_allocine_movie_page(self, response):

        fr_title = response.css(
            "div.titlebar.titlebar-page div.titlebar-title.titlebar-title-xl::text"
        ).get()
        original_title = response.css(
            "div.meta-body div[class='meta-body-item'] span.dark-grey::text"
        ).get()
        if not original_title:
            original_title = fr_title

        # Raw date string, e.g. "23 avril 2025"
        raw_date = response.css(
            "div.meta-body div.meta-body-info span.date.blue-link::text"
        ).get()
        raw_date = (
            raw_date.strip() if raw_date else self.next_wednesday.strftime("%d %B %Y")
        )

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
        actors = (
            response.css("div.meta-body-actor span.dark-grey-link::text").getall() or []
        )
        actor_1 = actors[0] if len(actors) > 0 else "no_actor"
        actor_2 = actors[1] if len(actors) > 1 else "no_actor"
        actor_3 = actors[2] if len(actors) > 2 else "no_actor"

        # Director & Writer (both under .meta-body-direction)
        director_list = response.css(
            "div.meta-body-direction span.dark-grey-link::text"
        ).getall()
        directors = director_list[0] if director_list else "unknown"

        writer_list = response.css(
            "div.meta-body-direction span.dark-grey-link::text"
        ).getall()
        writer = writer_list[-1] if writer_list else "unknown"

        # Distribution, Country, Category
        distribution_str = response.css(
            "section.ovw.ovw-technical div.item span.blue-link::text"
        ).get()
        distribution = distribution_str if distribution_str else "unknown"

        country_str = response.css(
            "section.ovw.ovw-technical div.item span.that span.nationality::text"
        ).get()
        country = country_str if country_str else "unknown"
        country = country.replace("U.S.A", ("Etats-Unis"))

        category_str = response.css(
            "div.meta-body-info span.dark-grey-link::text"
        ).get()
        category = category_str if category_str else "unknown"

        list_categories = response.css(
            "div.meta-body-info span.dark-grey-link::text"
        ).getall()

        # Classification
        classification_kid = response.css(
            "div.label.kids-label.aged-default::text"
        ).get()
        if classification_kid:
            classification = classification_kid
        else:
            classification = response.css("span.certificate-text::text").get()
            if not classification:
                classification = "Tout public"

        # Duration
        duration = "".join(
            [
                e.strip()
                for e in response.css(
                    "div.card.entity-card div.meta div.meta-body div.meta-body-item::text"
                ).getall()
            ]
        ).replace(",", "")
        if duration:
            hours, minutes = duration.replace("h", "").replace("min", "").split(" ")
            duration_minutes = int(hours) * 60 + int(minutes)
        else:
            duration = "1h 00min"
            duration_minutes = 60

        image_url_scrap = response.css(
            "div.entity-card-player-ovw figure.thumbnail span img.thumbnail-img::attr('src')"
        ).get()
        if image_url_scrap:
            image_url = image_url_scrap
        else:
            image_url = response.css(
                "div.entity-card-overview figure span img::attr('src')"
            ).get()

        if not response.meta["synopsis"]:
            synopsis = (
                response.css("section.ovw-synopsis div.content-txt p.bo-p::text")
                .get()
                .strip()
            )
        else:
            synopsis = response.meta["synopsis"].strip()

        yield UpcomingItem(
            fr_title=fr_title,
            original_title=original_title,
            released_date=released_date,
            released_year=released_year,
            actors=actors,
            actor_1=actor_1,
            actor_2=actor_2,
            actor_3=actor_3,
            directors=directors,
            writer=writer,
            distribution=distribution,
            country=country,
            list_categories=list_categories,
            category=category,
            classification=classification,
            duration=duration,
            duration_minutes=duration_minutes,
            allocine_url=response.url,
            image_url=image_url,
            synopsis=synopsis,
        )
