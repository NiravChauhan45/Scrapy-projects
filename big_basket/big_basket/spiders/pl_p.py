import gzip
import hashlib
import os
from datetime import datetime
import numpy as np
import pandas as pd
import mysql.connector
import requests
import json
from big_basket.config.database_config import ConfigDatabase # type: ignore

obj = ConfigDatabase(table="new_pdp_data", database="big_basket")


def pagesave(url, data):
    page_save_id = str(
        int(hashlib.md5(bytes(
            str(url), "utf8")).hexdigest(),
            16) % (
                10 ** 10))

    page_save = f"E:\\Nirav\\Project_page_save\\big_basket\\pdp\\10-07-2025\\"
    filepath = page_save + f"{page_save_id}.html.gz"
    # Todo: pagesave
    os.makedirs(page_save, exist_ok=True)
    with gzip.open(filepath, 'w') as f:
        json_data = json.dumps(data).encode('utf-8')
        f.write(json_data)


def make_requests(url):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'x-entry-context-id=100; x-entry-context=bb-b2c; _bb_locSrc=default; x-channel=web; _bb_bhid=; _bb_nhid=1723; _bb_vid=NjAxODYwNzE3NzczMTYxNzEw; _bb_dsevid=; _bb_dsid=; _bb_cid=1; _bb_aid=MzA4NTgxODk5Nw==; csrftoken=72c3iw7hIMyjNDicaFYRlzlfUX5yaqY3kio16EsIavpTFc4OJYhnRQjdlHYsjYAz; _bb_home_cache=25c6ea2a.1.visitor; _bb_bb2.0=1; is_global=1; _bb_addressinfo=; _bb_pin_code=; _bb_sa_ids=10654; _is_tobacco_enabled=0; _is_bb1.0_supported=0; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xMDY1NA==; is_integrated_sa=0; bb2_enabled=true; csurftoken=6K1dcg.NjAxODYwNzE3NzczMTYxNzEw.1739940895768.hprXzRh2drtoyZwg6JbRykIj891p47tTbYYhdhpXy2k=; bigbasket.com=2c1e1a3b-d098-40ab-bcac-cd102a6d1d3c; _gcl_au=1.1.1542882375.1739940768; jarvis-id=b76abe01-2491-455b-bd04-53c1d89c0c9e; _gid=GA1.2.52505219.1739940768; _fbp=fb.1.1739940767924.809745978442071696; adb=0; ufi=1; ts=2025-02-19%2010:25:22.545; _ga=GA1.2.271261501.1739940768; _ga_FRRYG5VKHX=GS1.1.1739940767.1.1.1739940862.60.0.0',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.bigbasket.com/ps/?q=namkeen&nc=as&page=3',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'x-channel': 'BB-WEB',
        'x-tracker': 'a7d5a183-47f5-4d9e-afc5-cf609efc37bb',
    }
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    pagesave(url, json_data)
    return json_data


main_df = []


def product_data(page_count):
    # slug = "namkeen"
    slug = "namkin"
    url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={slug}&page={page_count}"
    json_data = make_requests(url)
    for data in json_data.get('tabs'):
        for products_data in data.get('product_info').get('products'):
            item = {}
            item['product_id'] = products_data.get('id')
            item['product_name'] = products_data.get('desc')
            item['brand'] = products_data.get('brand').get('name')
            item['mrp'] = products_data.get('pricing').get('discount').get('mrp')
            item['price'] = products_data.get('pricing').get('discount').get('prim_price').get('sp')
            discount_percentage = ((int(float(item['mrp'])) - int(float(item['price']))) / int(float(item['mrp']))) * 100
            item['discount'] = "N/A" if discount_percentage == 0.0 else discount_percentage
            item['in_stock'] = True if "001" in products_data.get('availability').get(
                'avail_status') else False
            # item['tag'] = " | ".join([tag.get('label') for tag in products_data.get('additional_attr').get('info')])
            item['tag'] = "N/A"
            item['image'] = " | ".join([url.get('l') for url in products_data.get('images')])
            # item['product_url'] = "https://www.bigbasket.com" + products_data.get('absolute_url')
            item['avg_rating'] = products_data.get('rating_info').get('avg_rating')
            item['number_of_rating'] = products_data.get('rating_info').get('rating_count')
            main_df.append(item)
            print(item)
        if data.get('product_info').get('products'):
            page_count += 1
            product_data(page_count)


try:
    page_count = 1
    product_data(page_count)
except Exception as e:
    print(e)

# if __name__ == '__main__':
#     today_date = datetime.now().strftime("%d_%m_%Y")
#     df = pd.DataFrame(main_df)
#     excel_path = f"F:\\Nirav\\Project_export_data\\big_basket\\{today_date}\\"
#     os.makedirs(excel_path, exist_ok=True)
#     # excel_path = excel_path + f"big_basket_{today_date}_namkeen.xlsx"
#     excel_path = excel_path + f"big_basket_{today_date}_namkin.xlsx"
#     df = df.replace('', np.nan).fillna("N/A")
#     try:
#         df = df.drop_duplicates()
#     except:
#         df = df.applymap(lambda x: tuple(x) if isinstance(x, list) else x)
#     df.to_excel(excel_path, index=False, engine="xlsxwriter")
#     print(f"Your excel file has been generated, total count is: {df['product_id'].count()}")
