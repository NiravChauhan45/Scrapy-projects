import json, random
from rss.settings import *


def get_decodo_proxy():
    px = json.loads(open(r'rss/decodo_proxy_list.json', 'r').read())
    return {"https": random.choice(px)}


def get_scraper_do_proxy():
    return {"https": f"http://{SCRAPERDO_KEY}:@proxy.scrape.do:8080"}


def get_scraper_do_url():
    return f"http://api.scrape.do/?token={SCRAPERDO_KEY}"