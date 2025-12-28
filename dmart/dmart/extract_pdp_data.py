import gzip
import os
import random
import mysql.connector
from curl_cffi import requests
import json
from loguru import logger
from parsel import Selector
import datetime
from concurrent.futures import ThreadPoolExecutor


# Load JSON from a file
def load_json(pincode):
    json_filepath = r"F:\Nirav\Project_code\dmart\dmart\cookies_json.json"
    with open(json_filepath, "r") as file:
        json_data = json.load(file)
        return json_data.get(pincode)


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="dmart"
    )


def pagesave(response, pagesave_id):
    """Save response HTML page as gzipped file"""
    pagesave_path = r'F:\Nirav\Project_page_save\dmart\02_04_2025'
    try:
        os.makedirs(pagesave_path, exist_ok=True)
        main_path = fr'{pagesave_path}\{pagesave_id}.html.gz'
        if not os.path.exists(main_path):
            with gzip.open(main_path, "wb") as f:
                f.write(response.text.encode('utf-8'))
            print(f"Page saved for {pagesave_id}")
    except Exception as e:
        print(f"Error saving page: {e}")


def process_pincode(pincode):
    """Process each pincode in a separate thread"""
    table_name = 'pdp_02_04_2025'
    field_names_escaped = ['`Date (Crawler Date)`', '`Time (Crawler Time)`', '`City Name`', '`Pincode`', '`Brand`',
                           '`Category`', '`SKU Packshot`', '`SKU Name`', '`Pack Size`', '`Single Pack`',
                           '`Bundle Pack`',
                           '`Per Gm Price (Unit Price)`', '`MRP`', '`Selling Price`', '`Discount%`', '`Save Rs.`',
                           '`Availability Status`', '`Quantity Caping`', '`Remarks`', '`Pack shot/Screenshot`',
                           '`pagesave_id`']
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cookies = load_json(pincode)
        urls = [
            "https://www.dmart.in/product/lays-american-style-cream---onion-pwafer0lays1xx71220?selectedProd=810501"]
        for url in urls:
            if cookies:
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                }
                browser = random.choice(["chrome110", "edge99", "safari15_5"])
                response = requests.get(url, cookies=cookies, headers=headers, impersonate=browser)

                selector = Selector(text=response.text)
                json_data = json.loads(selector.xpath('//script[@id="__NEXT_DATA__"]/text()').get())
                product_data = json_data['props']['pageProps']['pdpData']['dynamicPDP']['data']['productData']

                city_name = 'Mumbai'
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                brand = product_data['manufacturer']
                category = product_data['categoryName']
                product_id = url.split('=')[-1]

                pagesave(response, product_id)

                for sku_data in product_data['sKUs']:
                    sku_id = sku_data['skuUniqueID']
                    if sku_id in product_id:
                        sku_packshot = ''
                        sku_name = sku_data['name']
                        pack_size = sku_data['variantTextValue']
                        single_pack = ''
                        bundle_pack = ''
                        per_gm_price = sku_data['variantInfoTxtValue'].replace('(₹', '').replace(')',
                                                                                                 '').strip().replace(
                            ' / ', '/') if sku_data['variantInfoTxtValue'] else ''
                        mrp = sku_data['priceMRP']
                        selling_price = sku_data['priceSALE']

                        if mrp and selling_price:
                            mrp = int(float(mrp))
                            selling_price = int(float(selling_price))
                            discount_percentage = int(((mrp - selling_price) / mrp) * 100)
                        else:
                            discount_percentage = 0

                        save_rs = sku_data['savePrice'].split('.')[0] if sku_data['savePrice'] else ''
                        availability_status = 'In Stock' if sku_data['invType'] == 'A' else 'Out of Stock'
                        quantity_caping = ''
                        remarks = ''
                        pack_shot_screenshot = ''
                        pagesave_id = product_id
                        insert_query = f"INSERT INTO {table_name} ({', '.join(field_names_escaped)}) VALUES ({', '.join(['%s'] * len(field_names_escaped))});"
                        field_values = (
                            current_date, current_time, city_name, pincode, brand, category, sku_packshot, sku_name,
                            pack_size, single_pack, bundle_pack, per_gm_price, mrp, selling_price, discount_percentage,
                            save_rs, availability_status, quantity_caping, remarks, pack_shot_screenshot, pagesave_id
                        )
                        cursor.execute(insert_query, field_values)
                        conn.commit()
                        print(f"Data inserted successfully for product_id: {product_id}, pincode: {pincode}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error processing pincode {pincode}: {e}")


def get_pdp_data():
    """Run multiple pincodes in parallel using ThreadPoolExecutor"""
    pincode_list = ['110001', '110016', '700017', '700019', '226001', '226004', '400001', '400013', '800001', '800013']
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_pincode, pincode_list)


# Run the function
get_pdp_data()
