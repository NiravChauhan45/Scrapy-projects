import requests
import all_functions as fuc
import json
import db_config as db
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import pymysql
import hashlib
from json_repair import repair_json
import os
import gzip
from parsel import Selector


def product_details(product_url):
    # Todo: Database Connection
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="bloomingdales"
    )

    cursor = connection.cursor()

    pagesave_id = int(hashlib.md5(bytes(str(product_url), "utf8")).hexdigest(), 16) % (10 ** 18)
    # pagesave_path = fr"D:\Nirav Chauhan\Pagesave\{db.database_name}\{db.current_date}"
    pagesave_path = fr"D:\Nirav Chauhan\Pagesave\{db.database_name}\29_11_2025"
    full_path = f"{pagesave_path}\\{pagesave_id}.html.gz"

    if not os.path.exists(full_path):
        response = fuc.get_response(product_url)
        selector = fuc.parseResponse(response)
        # Todo: Make pagesave
        # fuc.make_pagesave(response, pagesave_id)

        # Todo: Update link status
        update_sql = f"UPDATE {db.pdp_links} SET pagesave_id = %s WHERE product_url = %s"
        update_values = (pagesave_id, product_url)
        cursor.execute(update_sql, update_values)
        connection.commit()
        logger.info("Pagesave_id successfully Updated..")
    else:
        with gzip.open(full_path, "rb") as file:
            response_text = file.read()
        logger.success("Reading Pagesave..")
        response = response_text.decode('utf-8')
        selector = Selector(text=response)

    if response:
        json_data = ''
        try:
            json_data = selector.xpath('//script[@id="productMktData"]/text()').get()
            json_data = json_data.replace("var utag_data =", "").replace("};", "}").strip()
            json_data = json.loads(json_data)
        except Exception as e:
            print(e)

        try:
            json_data1 = selector.xpath("//script[contains(text(),'product_original_price')]/text()").get()
            if json_data1:
                json_data1 = json_data1.replace('window.__INITIAL_STATE__=', '')
                fixed_json = repair_json(json_data1)
                json_data1 = json.loads(fixed_json)

                j_data = json_data1.get('pageData').get('product').get('product').get('messages').get('relationships').get('memberProductMap')
                # for key,value in json_data1.items():
                #     if "pageData" in key:
                #         for key, value in value.items():
                #             if "product" in key and "productId" not in key and "productUrl" not in key:
                #                 product_data = value.get('product').get('pageData.product.product.messages')


        except Exception as e:
            print(e)
        variation_list = fuc.getVariationLIst(json_data)
        if variation_list:
            item = dict()
            for index, variant in enumerate(variation_list):
                item['Website'] = fuc.getWebName()
                item['PID'] = fuc.getPid(json_data, product_url)
                item['Name'] = fuc.getPname(json_data, selector)
                item['Short Description'] = "N/A"
                item['Description'] = fuc.getDescription(selector)
                item['Category'] = fuc.getCategory(selector)
                item['Image URL'] = fuc.getImageurl(json_data, selector)
                item['Price'] = fuc.getVPrice(selector, variation_list[index])
                item['Price Currency'] = fuc.getVPriceCurrency(variation_list[index])
                item['Sale Price'] = fuc.saleVPrice(variation_list[index])
                item['Final Price'] = fuc.saleVPrice(variation_list[index])
                item['Discount'] = fuc.getVDiscount(item['Price'], item['Sale Price'])
                item['IsOnSale'] = "N/A"
                item['IsInStock'] = fuc.getVIsinStock(variation_list[index])
                item['Keywords'] = "N/A"
                item['Brand'] = fuc.getBrand(json_data, selector)
                item['Manufacturer'] = "N/A"
                item['MPN'] = "N/A"
                item['UPC or EAN'] = "N/A"
                item['SKU'] = fuc.getVSKU(variation_list[index], item['PID'])
                item['Colour'] = fuc.getVColour(variation_list[index])
                item['Gender'] = "N/A"
                item['Size'] = fuc.getVSize(variation_list[index])
                item['Varint_Price'] = item['Sale Price']
                item['Alternate Image URLs'] = fuc.getAlternateImage(json_data, selector, item['Image URL'])
                item['Link URL'] = product_url
                item['Num Ratings'] = fuc.getNumRatings(json_data)
                item['Average Ratings'] = fuc.getAvgRatings(json_data)
                item['hash_id'] = fuc.getVHashId(product_url, item['SKU'], item['Colour'], item['Size'])
                item['pagesave_id'] = pagesave_id
                # fuc.make_pagesave(response, item['hash_id'])
                fuc.insertItemToSql(item, product_url, connection, cursor)

            # Todo: Done-Pending
            try:
                sql = f"UPDATE {db.pdp_links} SET status = %s WHERE pagesave_id = %s"
                values = ('insert_done', pagesave_id)
                cursor.execute(sql, values)
                connection.commit()
                logger.success("Item Successfully Updated...")
            except Exception as e:
                print(e)
        else:
            logger.exception("Variant Not Available")
            item = dict()
            item['Website'] = fuc.getWebName()
            item['PID'] = fuc.getPid(json_data, product_url)
            item['Name'] = fuc.getPname(json_data, selector)
            item['Short Description'] = "N/A"
            item['Description'] = fuc.getDescription(selector)
            item['Category'] = fuc.getCategory(selector)
            item['Image URL'] = fuc.getImageurl(json_data, selector)
            item['Price'] = fuc.getPrice(json_data, selector)
            item['Price Currency'] = fuc.getPriceCurrency(json_data, selector)
            item['Sale Price'] = fuc.salePrice(json_data, selector)
            item['Final Price'] = fuc.salePrice(json_data, selector)
            item['Discount'] = fuc.getDiscount(item['Price'], item['Sale Price'])
            item['IsOnSale'] = "N/A"
            item['IsInStock'] = fuc.getIsinStock(selector)
            item['Keywords'] = "N/A"
            item['Brand'] = fuc.getBrand(json_data, selector)
            item['Manufacturer'] = "N/A"
            item['MPN'] = "N/A"
            item['UPC or EAN'] = "N/A"
            item['SKU'] = fuc.getSKU(json_data, item['PID'])
            item['Colour'] = fuc.getColour(json_data)
            item['Gender'] = "N/A"
            item['Size'] = "N/A"
            item['Varint_Price'] = item['Sale Price']
            item['Alternate Image URLs'] = fuc.getAlternateImage(json_data, item['Image URL'])
            item['Link URL'] = product_url
            item['Num Ratings'] = fuc.getNumRatings(selector)
            item['Average Ratings'] = fuc.getAvgRatings(selector)
            item['hash_id'] = fuc.getHashId(product_url, item['SKU'], item['Colour'])
            item['pagesave_id'] = pagesave_id

            # fuc.make_pagesave(response, item['hash_id'])
            fuc.insertItemToSql(item, product_url, connection, cursor)
            # Todo: Done-Pending
            try:
                sql = f"UPDATE {db.pdp_links} SET status = %s WHERE pagesave_id = %s"
                values = ('insert_done', pagesave_id)
                cursor.execute(sql, values)
                connection.commit()
                logger.success("Item Successfully Updated...")
            except Exception as e:
                print(e)
    else:
        print("Data Not Found")


if __name__ == "__main__":
    # Todo: Using for loop
    sql_query = f"SELECT * FROM {db.pdp_links} WHERE status='Pagesave_Done' and product_url like '%1901065%';"
    db.cursor.execute(sql_query)
    results = db.cursor.fetchall()
    for product_url in results:
        product_url = product_url[1]
        product_details(product_url)

    # Todo: Using Threading
    # sql_query = f"SELECT * FROM {db.pdp_links} WHERE status='Pagesave_Done';"
    # db.cursor.execute(sql_query)
    # results = db.cursor.fetchall()
    #
    # # Todo: Extract URLs
    # product_urls = [row[1] for row in results]
    #
    # # Todo: ThreadPoolExecutor
    # with ThreadPoolExecutor(max_workers=100) as executor:  # adjust worker count as needed
    #     futures = {executor.submit(product_details, url): url for url in product_urls}
    #
    #     for future in as_completed(futures):
    #         url = futures[future]
    #         try:
    #             future.result()  # get returned value or cause exception to surface
    #         except Exception as e:
    #             print(f"Error processing {url}: {e}")
