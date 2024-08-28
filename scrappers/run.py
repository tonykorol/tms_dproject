from scrappers.abw_by.abw_scrapper import AbwParser
from scrappers.database_writers.writer import save_publications


if __name__ == "__main__":
    abw = AbwParser()
    abw_data = abw.get_data()
    save_publications(abw_data)
