import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def get_page(session, url):
    async with session.get(url) as r:
        if r.status == 200:
            return await r.text()
        else:
            print(f"Failed to fetch {url}, status: {r.status}")
            return ""


async def get_all(session, urls):
    tasks = [asyncio.create_task(get_page(session, url)) for url in urls]
    return await asyncio.gather(*tasks)


async def main(urls):
    async with aiohttp.ClientSession() as session:
        return await get_all(session, urls)


def parse(results):
    for html in results:
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No title found"
            print(title)


if __name__ == '__main__':
    urls = [
        "https://books.toscrape.com/catalogue/page-1.html",
        "https://books.toscrape.com/catalogue/page-2.html",
        "https://books.toscrape.com/catalogue/page-3.html"
    ]
    results = asyncio.run(main(urls))
    parse(results)
