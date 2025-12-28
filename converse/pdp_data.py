import gzip
import hashlib
import os.path
from parsel import Selector
from loguru import logger
import all_functions as fuc
import json
import db_config as db
from concurrent.futures import ThreadPoolExecutor, as_completed
import pymysql
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=db.database_name
    )

    cursor = connection.cursor()
    return connection, cursor


def product_details(product_url):
    connection, cursor = get_connection()

    item = dict()

    pagesave_id = int(hashlib.md5(bytes(str(product_url), "utf8")).hexdigest(), 16) % (10 ** 18)
    pagesave_path = fr"E:\Nirav\Project_page_save\converse\{db.current_date}"

    full_path = f"{pagesave_path}\\{pagesave_id}.html.gz"

    if not os.path.exists(full_path):
        response = fuc.get_response(product_url)
        selector = fuc.parseResponse(response)
        # Todo: Make pagesave
        fuc.make_pagesave(response, pagesave_id, db.current_date)

        # Todo: Update link status
        update_sql = f"UPDATE {db.pdp_links} SET pagesave_id = %s WHERE product_url = %s"
        update_values = (pagesave_id, product_url)
        cursor.execute(update_sql, update_values)
        connection.commit()
    else:
        with gzip.open(full_path, "rb") as file:
            response_text = file.read()
        logger.success("Reading Pagesave..")
        response = response_text.decode('utf-8')
        selector = Selector(text=response)

    if response:
        json_data = ''
        try:
            json_data = selector.xpath("//script[contains(text(),'utag_data')]/text()").get('').replace("\n  ",
                                                                                                        "").replace(
                "\n", "").strip()
            json_data = json_data.replace("var utag_data =", "").replace("};", "}").strip()
            json_data = json.loads(json_data)
        except Exception as e:
            print(e)

        size_list = fuc.getSize(selector)

        product_id = ''
        try:
            product_id = product_url.split('pid=')[-1].split('&')[0]
            if 'https' in product_id:
                product_id = product_id.split('.html?')[0]
                product_id = product_id.split('/')[-1].strip()
        except Exception as e:
            print(e)

        if size_list:
            for size in size_list:
                item['Website'] = fuc.getWebName()
                item['PID'] = product_id if product_id else fuc.getPid(json_data, product_url)
                item['Name'] = fuc.getPname(json_data, selector)
                item['Short Description'] = fuc.getShorDescription(selector)
                item['Description'] = fuc.getDescription(selector)
                item['Category'] = fuc.getCategory(json_data)
                item['Image URL'] = fuc.getImageurl(json_data, selector)
                item['Price'] = fuc.getPrice(json_data, selector)
                if item['Price'] == 0.0 or item['Price'] is None or item['Price'] == "N/A":
                    item['Price'] = item['Sale Price']
                item['Price Currency'] = fuc.getPriceCurrency(json_data, selector)
                item['Sale Price'] = fuc.salePrice(json_data, selector)
                item['Final Price'] = fuc.salePrice(json_data, selector)
                item['Discount'] = fuc.getDiscount(item['Price'], item['Sale Price'])
                item['IsOnSale'] = "N/A"
                item['IsInStock'] = fuc.getIsinStock(json_data, selector, size)
                item['Keywords'] = "N/A"
                item['Brand'] = fuc.getBrand(json_data, selector)
                item['Manufacturer'] = "N/A"
                item['MPN'] = "N/A"
                item['UPC or EAN'] = "N/A"
                item['SKU'] = fuc.getSKU(json_data, item['PID'])
                item['Colour'] = fuc.getColour(json_data, selector)
                item['Gender'] = fuc.getGender(json_data, selector)
                item['Size'] = size.split("–")[0].strip() if '–' in size else size
                item['Varint_Price'] = item['Sale Price']
                item['Alternate Image URLs'] = fuc.getAlternateImage(selector)
                item['Link URL'] = product_url
                item['Num Ratings'] = fuc.getNumRatings(selector)
                item['Average Ratings'] = fuc.getAvgRatings(selector)
                item['hash_id'] = fuc.getHashId(product_url, item['SKU'], item['Colour'], item['Size'])
                item['pagesave_id'] = pagesave_id
                fuc.insertItemToSql(item, product_url, connection, cursor)

            # Todo: Update link status
            update_sql = f"UPDATE {db.pdp_links} SET status = %s WHERE product_url = %s"
            update_values = ('Pagesave_Done', product_url)
            cursor.execute(update_sql, update_values)
            connection.commit()

            logger.success("Item Successfully Updated...")
        else:
            item['Website'] = fuc.getWebName()
            item['PID'] = product_id if product_id else fuc.getPid(json_data, product_url)
            item['Name'] = fuc.getPname(json_data, selector)
            item['Short Description'] = fuc.getShorDescription(selector)
            item['Description'] = fuc.getDescription(selector)
            item['Category'] = fuc.getCategory(json_data)
            item['Image URL'] = fuc.getImageurl(json_data, selector)
            item['Price'] = fuc.getPrice(json_data, selector)
            if item['Price'] == 0.0 or item['Price'] is None or item['Price'] == "N/A":
                item['Price'] = item['Sale Price']
            item['Price Currency'] = fuc.getPriceCurrency(json_data, selector)
            item['Sale Price'] = fuc.salePrice(json_data, selector)
            item['Final Price'] = fuc.salePrice(json_data, selector)
            item['Discount'] = fuc.getDiscount(item['Price'], item['Sale Price'])
            item['IsOnSale'] = "N/A"
            size = 'N/A'
            item['IsInStock'] = fuc.getIsinStock(json_data, selector, size)
            item['Keywords'] = "N/A"
            item['Brand'] = fuc.getBrand(json_data, selector)
            item['Manufacturer'] = "N/A"
            item['MPN'] = "N/A"
            item['UPC or EAN'] = "N/A"
            item['SKU'] = fuc.getSKU(json_data, item['PID'])
            item['Colour'] = fuc.getColour(json_data, selector)
            item['Gender'] = fuc.getGender(json_data, selector)
            item['Size'] = "N/A"
            item['Varint_Price'] = item['Sale Price']
            item['Alternate Image URLs'] = fuc.getAlternateImage(selector)
            item['Link URL'] = product_url
            item['Num Ratings'] = fuc.getNumRatings(selector)
            item['Average Ratings'] = fuc.getAvgRatings(selector)
            item['hash_id'] = fuc.getHashId(product_url, item['SKU'], item['Colour'], item['Size'])
            item['pagesave_id'] = pagesave_id
            fuc.insertItemToSql(item, product_url, connection, cursor)

            # Todo: Update link status
            update_sql = f"UPDATE {db.pdp_links} SET status = %s WHERE product_url = %s"
            update_values = ('Pagesave_Done', product_url)
            cursor.execute(update_sql, update_values)
            connection.commit()
    else:
        print("Data Not Found")


if __name__ == "__main__":

    connection, cursor = get_connection()

    # # # Todo: Using for loop
    # #
    # sql_query = f"SELECT * FROM {db.pdp_links} WHERE status='Pending' limit 100;"
    # db.cursor.execute(sql_query)
    # results = db.cursor.fetchall()
    # for product_url in results:
    #     product_url = product_url[1]
    #     product_details(product_url)

    # Todo: Using Threading
    # sql_query = f"SELECT product_url FROM {db.pdp_links} WHERE status='Pending' AND id=20356;"
    sql_query = f"SELECT product_url FROM {db.pdp_links} WHERE status='Pending' AND id=23520;"
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Extract URLs
    product_urls = [row[0] for row in results]

    # ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=1) as executor:  # adjust worker count as needed
        futures = {executor.submit(product_details, url): url for url in product_urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()  # get returned value or cause exception to surface
            except Exception as e:
                print(f"Error processing {url}: {e}")
