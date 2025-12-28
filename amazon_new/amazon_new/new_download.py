import asyncio
import json
import re

import requests
from PIL import Image
from io import BytesIO
import os

from parsel import Selector


def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Image downloaded successfully: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")


def main():
    pdp_links = ["https://www.amazon.in/OMKAR-Snacks-Manglori-Mix-Preservative/dp/B0DCSMTCCH",
                 "https://www.amazon.in/Bikano-Aloo-Bhujia-1-kg/dp/B07NVS3FR1",
                 "https://www.amazon.in/Bhujialalji-Navratan-Mixture-favourite-Preservatives/dp/B0BC9DTZDQ",
                 "https://www.amazon.in/Parle-Chatkeens-Hot-Spicy-400/dp/B07QQYZ6HR/",
                 "https://www.amazon.in/Haldirams-Nagpur-Pancharatan-Mixture-150g/dp/B019BV5L5C"]

    cookies = {
        'session-id': '260-4198031-7496017',
        'i18n-prefs': 'INR',
        'ubid-acbin': '259-4958529-9696045',
        'session-token': 'Nax8Pfhf5qw6bg8euey72XRnbG/FD9HSqpnYzILQ3be+JglqyspBSlxdymKXrGtS728ilIbk/bVOb3VEc44yLgmKPC4r2E9atuKsULMAqQ0/suRoYjEYwpdqO++9tgod93XIgBNEpZM/+bgmA9L2IPxC6D12r+w+2ye96PnyH2+9WMYtEXglJroJgyd4cGKfV2LXslqRlsVKMUiKk5cNQOpF9GsMwEby6ihGzKw31PdushvUznePHiuSvJR6KEhPNqiRTgy8meBSzKVxRBgf/1BwObdHZAfOGraAQn3AKtBLcQINYe0by8bGIUJbmxwKTQlvCpxfvhhU/G6hbcvTiTBC3p5wEIfV',
        'session-id-time': '2082758401l',
        'csm-hit': 'tb:HV2TEZ9NBCEAT5A4X77F+s-HV2TEZ9NBCEAT5A4X77F|1741252118753&t:1741252118753&adb:adblk_no',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'device-memory': '8',
        'downlink': '1.25',
        'dpr': '1.2000000000000002',
        'ect': '3g',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'rtt': '300',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.2000000000000002',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '1600',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'viewport-width': '1600',
        # 'cookie': 'session-id=260-4198031-7496017; i18n-prefs=INR; ubid-acbin=259-4958529-9696045; session-token=Nax8Pfhf5qw6bg8euey72XRnbG/FD9HSqpnYzILQ3be+JglqyspBSlxdymKXrGtS728ilIbk/bVOb3VEc44yLgmKPC4r2E9atuKsULMAqQ0/suRoYjEYwpdqO++9tgod93XIgBNEpZM/+bgmA9L2IPxC6D12r+w+2ye96PnyH2+9WMYtEXglJroJgyd4cGKfV2LXslqRlsVKMUiKk5cNQOpF9GsMwEby6ihGzKw31PdushvUznePHiuSvJR6KEhPNqiRTgy8meBSzKVxRBgf/1BwObdHZAfOGraAQn3AKtBLcQINYe0by8bGIUJbmxwKTQlvCpxfvhhU/G6hbcvTiTBC3p5wEIfV; session-id-time=2082758401l; csm-hit=tb:HV2TEZ9NBCEAT5A4X77F+s-HV2TEZ9NBCEAT5A4X77F|1741252118753&t:1741252118753&adb:adblk_no',
    }

    image_url_list = []

    for url in pdp_links:
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
        )
        selector = Selector(text=response.text)
        image_url = selector.xpath("//div[@id='imgTagWrapperId']/img/@src").get()
        product_id = url.split('/dp/')[-1].replace('/', '')
        # print(product_id)
        print(image_url)
        save_location = f"F:\\Nirav\\Project_code\\amazon_new\\amazon_new\\downloaded_images\\{product_id}.jpg"
        download_image(image_url, save_location)


asyncio.run(main())
