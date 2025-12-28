import sys
import db_config as db
import all_functions as fuc
import hashlib
import os
import gzip
from loguru import logger
from parsel import Selector
import pymysql
from concurrent.futures import ThreadPoolExecutor, as_completed
import json


def get_connections():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=db.database_name
    )
    cursor = connection.cursor()
    return connection, cursor


def product_details(result):
    product_id = result[1]
    # variation_id = result[2]
    variation_url = result[3]
    hash_id = result[4]
    connection, cursor = get_connections()

    pagesave_id = int(hashlib.md5(bytes(str(hash_id), "utf8")).hexdigest(), 16) % (10 ** 18)
    pagesave_path = fr"D:\Nirav Chauhan\Pagesave\{db.database_name}\{db.current_date}"
    full_path = f"{pagesave_path}\\{pagesave_id}.html.gz"

    if not os.path.exists(full_path):
        response = fuc.get_response(variation_url)
        logger.info("Making Pagesave..")

        # Todo: Make pagesave
        fuc.make_pagesave(response, pagesave_id)
        response = Selector(text=response.text)
    else:
        with gzip.open(full_path, "rb") as file:
            response_text = file.read()
        logger.success("Reading Pagesave..")
        response = response_text.decode('utf-8')
        response = Selector(text=response)

    # Todo: json_data
    json_data = ''
    try:
        json_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        json_data = json.loads(json_data)
    except Exception as e:
        logger.error(e)

    variation_list = fuc.getVariationLIst(json_data)
    if isinstance(variation_list, dict):
        for key in variation_list.keys():
            if 'size' in key:
                variation_list = [variation_list]
                break
            else:
                variation_list = response.xpath(
                    '//div[@class="pdp_sizepicker"]//span[@data-sizepicker-value]/text()').getall()
                if not variation_list:
                    variation_list = fuc.getVariationLIst(json_data)
                    variation_list = [variation_list]

    if variation_list:
        item = dict()
        for index, variant in enumerate(variation_list):
            item['Website'] = fuc.getWebName()
            item[
                'PID'] = product_id  # fuc.getPid(product_url, response) if fuc.getPid(product_url, response) else product_id
            item['Name'] = fuc.getPname(json_data, response)
            item['Short Description'] = fuc.getShortDescription(json_data, response)
            item['Description'] = fuc.getDescription(response)
            item['Category'] = fuc.getCategory(response, item['Name'])
            item['Image URL'] = fuc.getImageUrl(response)
            item['Price'] = fuc.getPrice(response, variant) if fuc.getPrice(response, variant) else fuc.getSalePrice(response, variant)
            item['Price Currency'] = fuc.getCurrency(response, variant)
            item['Sale Price'] = fuc.getSalePrice(response, variant)
            item['Final Price'] = fuc.getSalePrice(response, variant)
            item['Discount'] = fuc.getDiscount(item['Price'], item['Sale Price'])
            item['IsOnSale'] = fuc.getIsonSale(response)
            item['IsInStock'] = fuc.getInStock(response, variant)
            item['Keywords'] = "N/A"
            item['Brand'] = fuc.getBrand(response, variant)
            item['Manufacturer'] = "N/A"
            item['MPN'] = fuc.getMpn(response, variant)
            item['UPC or EAN'] = "N/A"
            item['SKU'] = fuc.getSku(response, variant)
            item['Colour'] = fuc.getColour(response, variant)
            if not item['MPN']:
                mpn = str(item['PID']) + str(item['Colour'])
                item['MPN'] = hashlib.sha256(mpn.encode()).hexdigest()[:12]
            item['Gender'] = "N/A"
            item['Size'] = fuc.getSize(response, variant, index)
            item['Varint_Price'] = fuc.getSalePrice(response, variant)
            item['Alternate Image URLs'] = fuc.getAlternateImageUrls(response)
            item['Link URL'] = variation_url
            item['Num Ratings'] = "N/A"
            item['Average Ratings'] = "N/A"
            item['hash_id'] = fuc.getHashID(item['PID'], item['SKU'], item['Colour'], item['Size'])
            item['pagesave_id'] = pagesave_id

            if not item['SKU']:
                pid = item['PID']
                colour = ''
                size = ''
                sku = ''
                if item['Colour']:
                    colour = item['Colour'].replace(' ', '-')
                    sku = f"{pid}-{colour}"
                if item['Size']:
                    size = item['Size'].replace(' ', '-')
                    sku = f"{sku}-{size}"
                item['SKU'] = sku

            fuc.insertItemToSql(item, connection, cursor)
        # Todo: Update link status
        update_sql = f"UPDATE {db.variations_links} SET status = %s WHERE hash_id = %s"
        update_values = ('Pagesave_Done', hash_id)
        cursor.execute(update_sql, update_values)
        connection.commit()

        logger.success("Item Successfully Updated...")
    else:
        logger.exception("Variant Not Available")


if __name__ == '__main__':
    connection, cursor = get_connections()

    start_id = sys.argv[1]
    end_id = sys.argv[2]

    # sql_query = f"SELECT * FROM {db.variations_links} WHERE status='Pending' AND id=321;"
    # sql_query = f"SELECT * FROM {db.variations_links} WHERE status='Pending' AND id BETWEEN {start_id} AND {end_id};"
    sql_query = f"SELECT * FROM {db.variations_links} WHERE status='Pending';"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    # for result in results:
    #     product_details(result)

    # # ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=100) as executor:  # adjust worker count as needed
        futures = {executor.submit(product_details, result): result for result in results}

        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()  # get returned value or cause exception to surface
            except Exception as e:
                print(f"Error processing {url}: {e}")
