from scrappers.abw_by.abw_scrapper import AbwParser
from scrappers.database_writers.writer import save_publications


async def run():
    abw = AbwParser()
    abw_data = abw.get_data()
    await save_publications(abw_data)
