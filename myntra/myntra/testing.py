import requests
from requests import Session


def _chrome(product_id):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }
    # Todo: Make Session
    _session = Session()
    _session.headers = headers
    _session.get("https://www.myntra.com")
    product_url =f"https://www.myntra.com/gateway/v2/product/https://www.myntra.com/{product_id}/related"
    response = _session.get(product_url)

    print(response.status_code)


def _edge(url):
    pass


if __name__ == '__main__':
    product_id = '29875024'
    # product_url = f"https://www.myntra.com/gateway/v2/product/{product_id}/related"
    _chrome(product_id)
    _edge(product_id)
