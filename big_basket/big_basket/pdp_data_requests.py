import gzip
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Thread
import os
from mysql.connector import pooling
import loguru
import mysql.connector
import requests
from parsel import Selector

from big_basket.config.database_config import ConfigDatabase

try:
    connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=32, host="localhost",
                                                  user="root",
                                                  password="actowiz",
                                                  database="big_basket"
                                                  )
except Exception as e:
    print(e)

def fetch_data(id, product_id, conn, cur):
    url = f"https://www.bigbasket.com/pd/{product_id}"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'bigbasket.com=d3079b5b-945e-4598-b16c-c2142bed38cf; x-entry-context-id=100; x-entry-context=bb-b2c; _bb_locSrc=default; x-channel=web; _bb_bhid=; _bb_nhid=1723; _bb_vid=NTkyMDMzMDM5MzQ1NzUwNzY2; _bb_dsevid=; _bb_dsid=; _bb_cid=1; csrftoken=9Wikugay15mSJ43gfEFbXBp6ijgBx86UoRL64eyRZs7jauJ3njThy6wGjGBiCKQE; _bb_home_cache=cbc52c35.1.visitor; _bb_bb2.0=1; _is_tobacco_enabled=0; _is_bb1.0_supported=0; bb2_enabled=true; _gcl_au=1.1.2135621399.1739354959; ufi=1; _gid=GA1.2.936058660.1739354959; jarvis-id=e77ad7f9-185d-463e-89e3-c77980dd1b0b; adb=0; _fbp=fb.1.1739354959339.559349315840106680; _bb_lat_long=MTIuOTc2NTk0NHw3Ny41OTkyNzA4; _bb_aid="MzAwNDkxOTI2MA=="; is_global=0; _bb_addressinfo=MTIuOTc2NTk0NHw3Ny41OTkyNzA4fFNoYW50aGFsYSBOYWdhcnw1NjAwMDF8QmVuZ2FsdXJ1fDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=560001; _bb_sa_ids=14979; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xNDk3OQ==; is_integrated_sa=1; _bb_tc=0; _bb_rdt="MzEwNTE1NjUwMA==.0"; _bb_rd=6; ts=2025-02-12%2015:42:35.299; _ga=GA1.1.1176812744.1739354959; _ga_FRRYG5VKHX=GS1.1.1739354959.1.1.1739355347.60.0.0; csurftoken=eU18iw.NTkyMDMzMDM5MzQ1NzUwNzY2.1739359665451.zKoOeWppoXtv1eF5KngyZ855h0quMHum1JLX5Xah0GY=',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }
    # cookie, pincode, city = None, None, None
    try:
        currently_unavailable = ''
        response = requests.get(url=url, headers=headers)
        data = str()

        if response.status_code == 200:
            response_selector = Selector(response.text)
            currently_unavailable = response_selector.xpath(
                "//*[contains(text(),'Currently Unavailable')]/text()").get()
            data = json.loads(
                response_selector.xpath('''//script[contains(text(), '{"props":{"pageProps":{')]//text()''').get())
        else:
            pass

        if currently_unavailable:
            mycursor = conn.cursor()
            # item = dict()
            sql = f"UPDATE pdp_links SET status = 'unavailable' WHERE id = {id}"
            mycursor.execute(sql)
            conn.commit()
            # item['id'] = id
            return None
        else:
            pagesave = f"F:\\Nirav\\Project_page_save\\big_basket\\pdp\\12-02-2025\\"
            filepath = pagesave + f"{product_id}.html.gz"
            # Todo: pagesave
            os.makedirs(pagesave, exist_ok=True)
            with gzip.open(filepath, 'w') as f:
                f.write(response.text.encode("utf-8"))

            product_name = "N/A"
            attributes = "N/A"
            if data['props']['pageProps']['productDetails']['children'][0]['desc']:
                desc = data['props']['pageProps']['productDetails']['children'][0]['desc']
                if data['props']['pageProps']['productDetails']['children'][0]['brand']['name']:
                    brand = data['props']['pageProps']['productDetails']['children'][0]['brand']['name']
                    desc = brand + " " + desc
                product_name = desc
            if data['props']['pageProps']['productDetails']['children'][0]['w']:
                pack_desc = None
                if data['props']['pageProps']['productDetails']['children'][0]['pack_desc']:
                    pack_desc = data['props']['pageProps']['productDetails']['children'][0]['pack_desc']
                w = data['props']['pageProps']['productDetails']['children'][0]['w']
                if pack_desc:
                    w = w + " " + pack_desc
                attributes = w

            item = dict()
            item['Product Code'] = data['props']['pageProps']['productDetails']['children'][0]['id']
            # Extracting Product Name :-
            item['Product Name'] = product_name
            item['id'] = id

            # Extracting Attributes :-
            item['Attributes'] = attributes

            # Extracting MRP
            try:
                mrp = data['props']['pageProps']['productDetails']['children'][0]['pricing']['discount']['mrp']
                item['MRP'] = float(mrp)
            except:
                item['MRP'] = "N/A"

            # Extracting Discount
            try:
                discount = data['props']['pageProps']['productDetails']['children'][0]['pricing']['discount']['d_text']
                item['Discount'] = discount
            except:
                item['Discount'] = "N/A"

            if item['Discount']:
                pass
            else:
                item['Discount'] = "N/A"

            if 'add' in data['props']['pageProps']['productDetails']['children'][0]['availability']['button'].lower():
                item['Availability'] = True
            else:
                item['Availability'] = False

            # Extract breadcrumb Category, Sub Category, Other Category
            breadcrumb = data['props']['pageProps']['productDetails']['children'][0]['breadcrumb']
            category_hierarchy = {f"l{index + 1}": category['name'].capitalize() for index, category in
                                  enumerate(breadcrumb)}
            try:
                item['Category'] = category_hierarchy['l1']
            except:
                item['Category'] = "N/A"
            try:
                item['Sub Category'] = category_hierarchy['l2']
            except:
                item['Sub Category'] = "N/A"
            try:
                item['Other Category'] = category_hierarchy['l3']
            except:
                item['Other Category'] = "N/A"

            # Extract breadcrumb Selling Price :-
            try:
                product_price = \
                    data['props']['pageProps']['productDetails']['children'][0]['pricing']['discount']['prim_price'][
                        'sp']
                item['Selling Price'] = float(product_price)
            except:
                item['Selling Price'] = "N/A"

            # Extract breadcrumb Image URL :-
            try:
                all_images = [image['xxl'] for image in
                              data['props']['pageProps']['productDetails']['children'][0]['images']]
                item['Image URL'] = " | ".join(all_images)
            except:
                item['Image URL'] = "N/A"

            # Extract About Product, Other Info
            product_specification = "N/A"
            manufacturing_info = "N/A"
            for information in data['props']['pageProps']['productDetails']['children'][0]['tabs']:
                if 'Other Product Info' == information['title']:
                    content_selector = Selector(information['content'])
                    content_selector.xpath('//style').remove()
                    manufacturing_info = [re.sub('\\s+', ' ', product_info).strip() for product_info in
                                          content_selector.xpath('.//text()').getall() if
                                          re.sub('\\s+', ' ', product_info).strip()]
                    if manufacturing_info:
                        manufacturing_info = " ".join(manufacturing_info)
                elif 'About the Product' == information['title']:
                    text = re.sub('<head>.*<\/head>', '', re.sub('\\s+', ' ', information['content']))
                    content_selector = Selector(text)
                    values = " ".join(content_selector.xpath('//div//text()').getall())
                    # print(values)
                    values = re.sub('\\s+', ' ', values).strip()
                    product_specification = values
                else:
                    text = re.sub('<head>.*<\/head>', '', re.sub('\\s+', ' ', information['content']))
                    content_selector = Selector(text)
                    values = " ".join(content_selector.xpath('//div//text()').getall())
                    # print(values)
                    values = re.sub('\\s+', ' ', values).strip()
                    if 'About the Product'.lower() in values.lower():
                        if product_specification == "N/A":
                            product_specification = values.replace('About the Product', '').strip()

            item['About Product'] = product_specification
            item['Other Info'] = manufacturing_info
            description_json = dict()
            description_json['other_info'] = item['Other Info']
            description_json['about_product'] = item['About Product']
            item['Description JSON'] = json.dumps(description_json)
            item['Product URL'] = f"https://www.bigbasket.com/pd/{product_id}/"

            if item:
                sql = f"UPDATE pdp_links SET status = 'Done' WHERE id = {id}"
                cur.execute(sql)
                conn.commit()
            return item
    except Exception as e:
        print("=====>", e)


db = ConfigDatabase(database="big_basket", table='pdp_links')
ob1 = ConfigDatabase(table="pdp_links", database="big_basket")
ob2 = ConfigDatabase(table="pdp_data", database="big_basket")


def main(start, end, results):
    conn = connection_pool.get_connection()  # Get a connection from the pool
    cur = conn.cursor()
    for result in results[start:end]:
        product_id = result['product_url'].split('/pd/')[-1].split('/')[0]
        id = result['id']
        item = fetch_data(id, product_id, conn, cur)
        if item:
            print(item)
            try:
                field_list = []
                value_list = []
                new_item = item.copy()
                del new_item['id']
                for field in new_item:
                    field_list.append(str(f"`{field}`"))
                    value_list.append(str(new_item[field]).replace("'", "''"))
                fields = ','.join(field_list)
                values = "','".join(value_list)
                insert_db = f"insert into {ob2.table}" + "( " + fields + " ) values ( '" + values + "' )"
                cur.execute(insert_db)
                conn.commit()
                print(f"Item Successfully Inserted...")
            except Exception as e:
                print(str(e))


if __name__ == '__main__':
    data_c = 205511
    run_count = 0
    results = db.fetchResultsfromSql(conditions={'status': 'pending'})
    while data_c != 0 and run_count < 100:
        total_count = data_c
        variable_count = total_count // 32
        if variable_count == 0:
            variable_count = total_count ** 2
        count = 1
        threads = [Thread(target=main, args=(i, variable_count + i, results)) for i in
                   range(0, total_count, variable_count)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        run_count += 1

