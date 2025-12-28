import re
from datetime import datetime

import requests
from parsel import Selector
import pandas as pd

df = pd.read_excel(r"D:\Nirav Live Projects\nuttygritties\data_layout_product.xlsx", sheet_name="Sheet3")
urls = df['urls']
cookies = {
    'secure_customer_sig': '',
    'localization': 'IN',
    '_tracking_consent': '%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INGJ%22%2C%22reg%22%3A%22%22%7D',
    '_shopify_y': '4a5e8623-061c-4232-914c-3b8f89f6d373',
    '_orig_referrer': 'https%3A%2F%2Fwww.google.com%2F',
    '_landing_page': '%2Fcollections%2Fraw-almonds',
    'refb': '1a23388f-75b5-4c3c-a786-f7550e84c971',
    '_gcl_au': '1.1.180090999.1727336878',
    '_fbp': 'fb.1.1727336877811.921836183436355982',
    '_scid': 'ZoMvkFkqFlHFx-d4FbhIKZGY6xqDpWa2',
    '_ScCbts': '%5B%5D',
    '_sctr': '1%7C1727289000000',
    '_ga_2PHZSTNB3L': 'deleted',
    '_cmp_a': '%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D',
    'receive-cookie-deprecation': '1',
    'ssid': '42a0ea9b-3307-457d-8a70-9ade90b2e698',
    '_clck': 'hf7jbs%7C2%7Cfpm%7C0%7C1730',
    '_gid': 'GA1.2.1697027214.1727678627',
    '_shopify_sa_p': '',
    '_gat': '1',
    '_scida': 'pm1KXoYjBhw_MphMO4-J9tNzBtjUTVEu',
    '_gat_gtag_UA_159962660_1': '1',
    '_ga_2PHZSTNB3L': 'GS1.1.1727682841.15.0.1727682841.0.0.0',
    '_clsk': 'qpngh%7C1727682842362%7C8%7C1%7Cx.clarity.ms%2Fcollect',
    'fsb_previous_pathname': '/collections/dates/products/copy-of-omani-dates-khajoor-35g-pack-of-20',
    '_shopify_s': '41ec0a89-760C-4819-6254-6096FF8440B5',
    '_shopify_sa_t': '2024-09-30T07%3A54%3A02.972Z',
    '_ga': 'GA1.1.284946748.1727336877',
    '_ga_2HQR80TZ5G': 'GS1.1.1727682840.12.1.1727682844.56.0.0',
    'keep_alive': '1eb99eca-50a4-4c5e-a486-5a1ac825c531',
}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'secure_customer_sig=; localization=IN; _tracking_consent=%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INGJ%22%2C%22reg%22%3A%22%22%7D; _shopify_y=4a5e8623-061c-4232-914c-3b8f89f6d373; _orig_referrer=https%3A%2F%2Fwww.google.com%2F; _landing_page=%2Fcollections%2Fraw-almonds; refb=1a23388f-75b5-4c3c-a786-f7550e84c971; _gcl_au=1.1.180090999.1727336878; _fbp=fb.1.1727336877811.921836183436355982; _scid=ZoMvkFkqFlHFx-d4FbhIKZGY6xqDpWa2; _ScCbts=%5B%5D; _sctr=1%7C1727289000000; _ga_2PHZSTNB3L=deleted; _cmp_a=%7B%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%7D; receive-cookie-deprecation=1; ssid=42a0ea9b-3307-457d-8a70-9ade90b2e698; _clck=hf7jbs%7C2%7Cfpm%7C0%7C1730; _gid=GA1.2.1697027214.1727678627; _shopify_sa_p=; _gat=1; _scida=pm1KXoYjBhw_MphMO4-J9tNzBtjUTVEu; _gat_gtag_UA_159962660_1=1; _ga_2PHZSTNB3L=GS1.1.1727682841.15.0.1727682841.0.0.0; _clsk=qpngh%7C1727682842362%7C8%7C1%7Cx.clarity.ms%2Fcollect; fsb_previous_pathname=/collections/dates/products/copy-of-omani-dates-khajoor-35g-pack-of-20; _shopify_s=41ec0a89-760C-4819-6254-6096FF8440B5; _shopify_sa_t=2024-09-30T07%3A54%3A02.972Z; _ga=GA1.1.284946748.1727336877; _ga_2HQR80TZ5G=GS1.1.1727682840.12.1.1727682844.56.0.0; keep_alive=1eb99eca-50a4-4c5e-a486-5a1ac825c531',
    'if-none-match': '"cacheable:3dbf6fdab1f4ab41bdd046069dc6b58c"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

for url in urls:
    url = 'https://nuttygritties.com' + url
    response = requests.get(url, cookies=cookies, headers=headers)

    selector = Selector(text=response.text)

    product_name = selector.xpath("//header[@class='product-title']/h1/span/text()").get()

    selling_price = selector.xpath(
        "//div[@class='prices']/span[@class='price on-sale']/text()").get().strip().replace(
        '₹ ',
        '').replace(',', '')

    mrp = selector.xpath("//div[@class='prices']/span[@class='compare-price']/text()").get().strip().replace('₹ ',
                                                                                                             '').replace(
        ',', '')

    # mrp = mrp if mrp is not None else mrp = selling_price
    discount_percentage = selector.xpath(
        "//div[@class='product-label']/strong[@class='label label-sale']/text()").get().replace('  -', '').replace('%',
                                                                                                                   '').strip()

    pattern = r'(\d+\s*(kg|g)|(\d+.\d*(kg)|(\d+.\d*\s(kg))|\d+.\d*(Kg)))\b'
    matches = re.findall(pattern, product_name)

    # quantity
    if matches:
        product_quantity = matches[-1][0]
        qunty = re.search(r'\d+(\.\d+)?', product_quantity).group(0)
        if "kg" in product_quantity or "kgs" in product_quantity or "Kgs" in product_quantity or "Kg" in product_quantity:
            quantity = float(qunty) * 1000
        else:
            quantity = float(qunty)
    else:
        print("Quantity not found.")

    if quantity > 0:  # NOTE: selling_price/product_quantity
        unit_price = float(selling_price) / float(quantity)
        # unit_price = selling_price / quantity  # this quantity contains only digit
        unit_price = int(unit_price * 100) / 100
    else:
        unit_price = None

    # stock
    try:
        stock = selector.xpath("//div[@class='product-label']/strong[@class='sold-out label']/text()").get().strip()
        stock = 0
    except Exception as e:
        stock = 1

    today_date = datetime.now().strftime("%d-%m-%Y")

    data_dict = {"platform": "Nutty Gritties", "date": today_date, "SKU": '', "Brand": "Nutty Gritties",
                 "Pincode": "NA",
                 "product_name: ": product_name}
    print("mrp: ", mrp)
    print("selling_price: ", selling_price)
    print("discount_percentage: ", discount_percentage)
    print("quantity: ", str(quantity).replace(' ', ''))
    print("unit_price: ", unit_price)
    print("stock: ", stock)
    print('url: ', url)
    print()
    print()
