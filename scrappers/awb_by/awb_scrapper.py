import json
from datetime import timedelta

from random import choice

from black import datetime
from requests import get
from time import sleep

import locale
locale.setlocale(locale.LC_ALL, '')

SITE_URL = "https://abw.by"
SITE_API_URL = "https://b.abw.by/api/v2/adverts/list/cars"


class AbwParser:
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

    def get_headers(self):
        return {"User-agent": choice(self.user_agents)}

    @staticmethod
    def get_pages_list():
        response = get(SITE_API_URL)
        pages = response.json()["pagination"]["pages"]
        return pages

    def get_page_data(self, page: int):
        response = get(SITE_API_URL, params={"page": page}, headers=self.get_headers())
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_publication_date(string: str) -> float:
        month_now: int = datetime.now().strftime("%B")
        year_now: int = datetime.now().strftime("%Y")

        try:
            date = datetime.strptime(string, "%d %B %Y")
        except ValueError:
            if string.split(' ')[0] == "вчера":
                day_now = (datetime.now() - timedelta(days=1)).strftime("%d")
            else:
                day_now = datetime.now().strftime("%d")
            date = datetime.strptime(f"{day_now} {month_now} {year_now}", "%d %B %Y")
        # print(date)
        return date

    def get_items(self, pages: int):
        for p in range(1, pages + 1):
            data = self.get_page_data(p)
            for item in data["list"]:
                if isinstance(item["id"], int):
                    publication_other_data = item["description"].split(" / ")
                    publication_title = item["title"].split(" ")

                    car_brand = publication_title[0]
                    car_model = publication_title[1]
                    car_model_generation = "".join(publication_title[2:(len(publication_title) - 1)])[:-1]
                    car_year = publication_title[len(publication_title) - 1]

                    publication_id = item["id"]
                    publication_images = item["images"]

                    publication_price = int(item["price"]["usd"][:-4].replace(' ',''))

                    publication_link = f'{SITE_URL}{item["link"]}'
                    publication_description = item["text"]
                    publication_date = self.get_publication_date(item["date"]),

                    if len(publication_other_data) >= 7:
                        if publication_other_data[2] != "электро":
                            car_engine_type = publication_other_data[3]
                            car_engine_hp = publication_other_data[2].replace(" л.с.","")
                            car_engine_volume = publication_other_data[1].replace(" л","")
                            car_transmission_type = publication_other_data[4]
                            car_drive = publication_other_data[5]
                            car_mileage = publication_other_data[0].replace(" км","")
                            car_body_type = publication_other_data[6]
                        else:
                            car_engine_type = publication_other_data[2]
                            car_engine_hp = publication_other_data[1].replace(" л.с.","")
                            car_engine_volume = None
                            car_transmission_type = publication_other_data[4]
                            car_drive = publication_other_data[5]
                            car_mileage = publication_other_data[0].replace(" км","")
                            car_body_type = publication_other_data[6]
                    else:
                        print(f"{item["id"]} NOT FULL DATA\n{SITE_URL}{item["link"]}")
                        continue

                    self.publications.append(
                        {
                            "id": publication_id,
                            "publication_date": publication_date[0],
                            "link": publication_link,
                            "images": publication_images,
                            "description": publication_description,
                            "engine_type": car_engine_type,
                            "engine_hp": car_engine_hp,
                            "engine_volume": car_engine_volume,
                            "transmission_type": car_transmission_type,
                            "car_drive": car_drive,
                            "mileage": car_mileage,
                            "car_year": car_year,
                            "car_body_type": car_body_type,

                            "price": publication_price,

                            "car_model": {
                                "brand": car_brand,
                                "model": car_model,
                                "generation": car_model_generation,
                            },

                            "site_name": "awb.by",
                            "site_url": SITE_URL,

                        }
                    )
            sleep(2)

    def save_items(self):
        with open("data.json", "w") as file:
            data = json.dumps(self.publications, indent=4)
            file.write(data)


    def get_data(self):
        self.get_items(1)
        return self.publications


if __name__ == "__main__":
    abw = AbwParser()
    # pages = get_pages_list()
    # get_items(pages)
    # abw.get_items(1)
    # abw.save_items()
    print(abw.get_data())
    # abw.get_publication_date("16 Августа 2024")
    # abw.get_publication_date("вчера в 20:23")
    # abw.get_publication_date("сегодня в 20:23")
