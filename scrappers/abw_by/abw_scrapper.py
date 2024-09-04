import re
import json
from datetime import timedelta, UTC, datetime

from random import choice

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
        """
        Select one user agent for headers.

        This method randomly selects a user agent from the predefined list
        of user agents to be used in HTTP requests. This helps in
        mimicking requests from different browsers or devices.

        :return: A dictionary containing a single key-value pair where
                 the key is "User-agent" and the value is a randomly
                 selected user agent string.
        """
        return {"User-agent": choice(self.user_agents)}

    def get_pages_list(self) -> int:
        """
        Retrieve the total number of pages from the API.

        This method sends a GET request to the API and parses the JSON
        response to extract the total number of pages available for
        navigation.

        :return: An integer representing the total number of pages.
        """
        response = get(self.SITE_API_URL)
        pages = response.json()["pagination"]["pages"]
        return pages

    def get_page_data(self, page: int) -> json:
        """
        Get data for a specific page from the API.

        This method sends a GET request to the API with the specified
        page number. If the request is successful, it returns the JSON
        data for that page.

        :param page: An integer representing the page number to retrieve.
        :return: A JSON object containing the data for the specified page
                 if the request is successful; otherwise, None.
        """
        response = get(self.SITE_API_URL, params={"page": page}, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_publication_date(string: str) -> datetime:
        """
        Convert a publication date string into a datetime object.

        This method takes a string representation of a date and attempts
        to parse it into a datetime object. It supports various formats,
        including "вчера" (yesterday). If the format is unrecognized,
        it defaults to the current date.

        :param string: A string representing the publication date.
        :return: A datetime object representing the parsed date.
        """
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
        """
        Parse a publication title string into structured data.

        This method splits a given title string into its components:
        brand, model, generation, and year. It returns an instance of
        PublicationTitleData containing this information.

        :param title: A string representing the publication title.
        :return: An instance of PublicationTitleData containing parsed data.
        """
        title_data_parts = title.split(" ")

        brand = title_data_parts[0]
        model = title_data_parts[1]
        generation = "".join(title_data_parts[2:(len(title_data_parts) - 1)])[:-1]
        year_part = title_data_parts[len(title_data_parts) - 1][:4]
        year = int(year_part) if len(year_part) == 4 else None
        title_data = PublicationTitleData(
            brand, model, generation, year
        )
        return title_data

    @staticmethod
    def parse_publication_other_data(other_data: str) -> PublicationOtherData:
        """
        Parse additional publication data from a string.

        This method extracts various attributes related to the vehicle
        from a given string, including engine type, horsepower,
        engine volume, transmission type, drive type, mileage, and
        body type. It uses regular expressions to find these attributes
        in the input string.

        :param other_data: A string containing additional information
                           about the vehicle.
        :return: An instance of PublicationOtherData containing the
                 extracted attributes.
        """
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
        """
        Retrieve and process publication data from multiple pages.

        This method iterates through the specified number of pages,
        retrieves publication data from each page, and processes each
        publication item. It extracts relevant information and saves
        it as instances of the Publication class.

        :param pages: An integer representing the total number of pages
                      to retrieve data from.
        """
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
        """
        Save a publication instance to the internal list.

        This method appends a given publication instance to the internal
        list of publications for later processing or storage.

        :param pub: An instance of the Publication class to be saved.
        """
        self.publications.append(pub)

    def save_json(self) -> None:
        """
        Save all collected publications to a JSON file.

        This method serializes the internal list of publications into JSON
        format and writes it to a file named "data.json".

        :return: None
        """
        with open("data.json", 'w') as file:
            data = json.dumps(self.publications, indent=4)
            file.write(data)

    def get_data(self) -> list:
        """
        Retrieve publication data and return a list of publications.

        This method calls the get_publications_data method to fetch
        publication data from the specified number of pages. After
        retrieving the data, it returns the internal list of
        publications.

        :return: A list of Publication instances containing the
                 retrieved publication data.
        """
        self.get_publications_data(pages=1)
        return self.publications
