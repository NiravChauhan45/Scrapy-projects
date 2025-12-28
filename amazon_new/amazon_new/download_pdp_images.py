import asyncio
import aiohttp
import os
from parsel import Selector

# Define image save directory
SAVE_DIR = "F:\\Nirav\\Project_code\\amazon_new\\amazon_new\\downloaded_images"
os.makedirs(SAVE_DIR, exist_ok=True)


async def download_image(session, url, save_path):
    """Asynchronously downloads an image from a URL."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as file:
                    file.write(await response.read())
                print(f"Image downloaded: {save_path}")
            else:
                print(f"Failed to download {url}, Status: {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")


async def fetch_image_url(session, product_url):
    """Fetches product page and extracts the main image URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }

    async with session.get(product_url, headers=headers) as response:
        if response.status == 200:
            page_content = await response.text()
            selector = Selector(text=page_content)
            return selector.xpath("//div[@id='imgTagWrapperId']/img/@src").get()
        else:
            print(f"Failed to fetch {product_url}")
            return None


async def main():
    """Fetches product images from Amazon and downloads them asynchronously."""
    pdp_links = [
        "https://www.amazon.in/OMKAR-Snacks-Manglori-Mix-Preservative/dp/B0DCSMTCCH",
        "https://www.amazon.in/Bikano-Aloo-Bhujia-1-kg/dp/B07NVS3FR1",
        "https://www.amazon.in/Bhujialalji-Navratan-Mixture-favourite-Preservatives/dp/B0BC9DTZDQ",
        "https://www.amazon.in/Parle-Chatkeens-Hot-Spicy-400/dp/B07QQYZ6HR/",
        "https://www.amazon.in/Haldirams-Nagpur-Pancharatan-Mixture-150g/dp/B019BV5L5C"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in pdp_links:
            product_id = url.split('/dp/')[-1].split('/')[0]
            save_path = os.path.join(SAVE_DIR, f"{product_id}.jpg")

            image_url = await fetch_image_url(session, url)
            if image_url:
                tasks.append(download_image(session, image_url, save_path))

        await asyncio.gather(*tasks)


# Run the async function
asyncio.run(main())
