import re
import json
from calendar import month
from datetime import timedelta, UTC

from random import choice

from black import datetime
from requests import get
from time import sleep

import locale

from scrappers.data_classes import Publication, CarModel, PublicationOtherData, PublicationTitleData

locale.setlocale(locale.LC_ALL, '')


class AbwParser:
    SITE_URL = "https://abw.by"
    SITE_API_URL = "https://b.abw.by/api/v2/adverts/list/cars"
    publications: list = []
    user_agents: list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 Maxthon/5.3.8.2000",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 YaBrowser/20.12.2.105 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.60 YaBrowser/20.12.0.963 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 YaBrowser/20.9.0.933 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 YaBrowser/21.2.0.1097 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.1.112 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 OPR/74.0.3911.218",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 YaBrowser/21.2.2.101 Yowser/2.5 Safari/537.36",
    ]

    def get_headers(self) -> dict:
        return {"User-agent": choice(self.user_agents)}

    def get_pages_list(self) -> int:
        response = get(self.SITE_API_URL)
        pages = response.json()["pagination"]["pages"]
        return pages

    def get_page_data(self, page: int) -> json:
        response = get(self.SITE_API_URL, params={"page": page}, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_publication_date(string: str) -> datetime:
        month_now: int = datetime.now(UTC).strftime("%B")
        year_now: int = datetime.now(UTC).strftime("%Y")
        try:
            date = datetime.strptime(string, "%d %B %Y")
        except ValueError:
            if string.split(' ')[0] == "вчера":
                day_now = (datetime.now(UTC) - timedelta(days=1)).strftime("%d")
                month_now: int = (datetime.now(UTC) - timedelta(days=1)).strftime("%B")
            else:
                day_now = datetime.now(UTC).strftime("%d")
            date = datetime.strptime(f"{day_now} {month_now} {year_now}", "%d %B %Y")
        return date

    @staticmethod
    def parse_publication_title_data(title: str) -> PublicationTitleData:
        title_data_parts = title.split(" ")

        brand = title_data_parts[0]
        model = title_data_parts[1]
        generation = "".join(title_data_parts[2:(len(title_data_parts) - 1)])[:-1]
        year = int(title_data_parts[len(title_data_parts) - 1][:4])
        title_data = PublicationTitleData(
            brand, model, generation, year
        )
        return title_data

    @staticmethod
    def parse_publication_other_data(other_data: str) -> PublicationOtherData:
        engine_type = ""
        engine_hp = ""
        engine_volume = ""
        transmission_type = ""
        drive = ""
        mileage = ""
        body_type = ""

        if mileage_match := re.search(r'(\d+(\s\d+)?)\s*км', other_data):
            mileage = mileage_match.group(1)

        if engine_volume_match := re.search(r'(\d+(\.\d+)?)\s*л', other_data):
            engine_volume = engine_volume_match.group(1)

        if engine_hp_match := re.search(r'(\d+)\s*л\.с\.', other_data):
            engine_hp = engine_hp_match.group(1)

        if engine_type_match := re.search(r'(?<=\s)(бензин|дизель|электро|газ|гибрид|гидроген)(?=\s)', other_data):
            engine_type = engine_type_match.group(0)

        if transmission_type_match := re.search(r'(?<=\s)(автомат|механика|робот|вариатор)(?=\s)', other_data):
            transmission_type = transmission_type_match.group(0)

        if drive_match := re.search(r'(?<=\s)(полный|передний|задний)(?=\s)', other_data):
            drive = drive_match.group(0)

        pattern = re.compile(r'''
            (?<=\s)
            (внедорожник|кабриолет|купе|лимузин|
             лифтбек|микроавтобус/бус|минивен|пикап|
             универсал|седан|фургон|хэтчбек)
            (?=\s)
        ''', re.VERBOSE)
        if body_type_match := re.search(pattern, other_data):
            body_type = body_type_match.group(0)

        pub_other_data = PublicationOtherData(
            engine_type, engine_hp, engine_volume, transmission_type, drive, mileage, body_type
        )
        return pub_other_data

    def get_publications_data(self, pages: int) -> None:
        for p in range(1, pages + 1):
            data = self.get_page_data(p)
            for item in data["list"]:
                if isinstance(item["id"], int):
                    publication_id = item["id"]
                    publication_images = item["images"]
                    publication_price = int(item["price"]["usd"][:-4].replace(' ',''))
                    publication_link = f'{self.SITE_URL}{item["link"]}'
                    publication_description = item["text"]
                    publication_date = self.get_publication_date(item["date"])
                    title_data = self.parse_publication_title_data(item["title"])
                    other_data = self.parse_publication_other_data(item["description"])

                    car = CarModel(
                        brand=title_data.car_brand,
                        model=title_data.car_model,
                        generation=title_data.car_model_generation,
                    )

                    publication = Publication(
                        id=publication_id,
                        publication_date=publication_date,
                        link=publication_link,
                        images=publication_images,
                        description=publication_description,
                        engine_type=other_data.engine_type,
                        engine_hp=other_data.engine_hp,
                        engine_volume=other_data.engine_volume,
                        transmission_type=other_data.transmission_type,
                        car_drive=other_data.drive,
                        mileage=other_data.mileage,
                        car_year=title_data.car_year,
                        car_body_type=other_data.body_type,
                        price=publication_price,
                        car_model=car,
                        site_name="abw.by",
                        site_url=self.SITE_URL,
                    )
                    self.save_publication(publication)
            sleep(2)

    def save_publication(self, pub) -> None:
        self.publications.append(pub)

    def save_json(self) -> None:
        with open("data.json", 'w') as file:
            data = json.dumps(self.publications, indent=4)
            file.write(data)

    def get_data(self) -> list:
        self.get_publications_data(pages=2)
        return self.publications
