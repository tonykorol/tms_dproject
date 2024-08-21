import datetime
import json

from requests import request
from time import sleep

SITE_URL = "https://abw.by"
SITE_API_URL = "https://b.abw.by/api/v2/adverts/list/cars"

publications = []


def get_pages_list():
    req = request("GET", SITE_API_URL)
    pages = req.json()["pagination"]["pages"]
    return pages


def get_page_data(page):
    req = request("GET", SITE_API_URL, params={"page": page})
    if req.status_code == 200:
        return req.json()


def get_items(pages):
    for p in range(1, pages+1):
        data = get_page_data(p)
        for item in data["list"]:
            if type(item["id"]) == int:
                publication_other_data = item["description"].split(" / ")
                publication_title = item["title"].split(" ")

                car_brand = publication_title[0]
                car_model = publication_title[1]
                car_model_generation = publication_title[2]
                car_year = publication_title[3]

                publication_id = item["id"]
                publication_images = item["images"]
                publication_price = item["price"]["usd"]
                publication_link = f'{SITE_URL}{item["link"]}'
                publication_description = item["text"]

                car_engine_type = publication_other_data[3]
                car_engine_hp = publication_other_data[2]
                car_engine_volume = publication_other_data[1]
                car_transmission_type = publication_other_data[4]
                car_drive = publication_other_data[5]
                car_mileage = publication_other_data[0]
                # car_body_type = publication_other_data[6]

                publications.append(
                    {
                        publication_id:{
                            "publication_link": publication_link,
                            "publication_images": publication_images,
                            "publication_price": publication_price,
                            "publication_description": publication_description,
                            "car_model": {
                                "car_brand": car_brand,
                                "car_model": car_model,
                                "car_model_generation": car_model_generation,
                                "car_year": car_year,
                            },
                            "publication_data": {
                                "car_engine_type": car_engine_type,
                                "car_engine_hp": car_engine_hp,
                                "car_engine_volume": car_engine_volume,
                                "car_transmission_type": car_transmission_type,
                                "car_drive": car_drive,
                                "car_mileage": car_mileage,
                                # "car_body_type": car_body_type,
                            },
                        }
                    }
                )
        sleep(2)
    with open("data.json", "w") as file:
        data = json.dumps(publications, indent=4)
        file.write(data)


if __name__ == "__main__":
    # pages = get_pages_list()
    # get_items(pages)
    get_items(1)