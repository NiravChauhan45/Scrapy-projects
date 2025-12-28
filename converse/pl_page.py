from loguru import logger
from parsel import Selector
import gzip
import hashlib
import pymysql
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


def get_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="converse_new"
    )

    cursor = connection.cursor()
    return connection, cursor


def get_variations(product_url):
    connection, cursor = get_connection()
    cookies = {
        'bm_sv': '74784A9F2937C7073D5C385C987E34DF~YAAQsiTDF+YKQKqaAQAAZTOQvx1NdY4Hew7u7hU99vgf3cp66qUvKmT8A5SiPvz616Uktx4yx6FgyhB1OxVaAHf2qjy2NQ6j/ItshcHmMgohB0yr/qoov59k1JpP4X+NSvMS0fnJJCbno4DgnZ+OeVO1akNfCJmpATsFxOL0VM2TI0oyQTh6sYCd5xm7XHoUwu4SNihMYNYVikjCCJNXOsS4Ytl9GcQEb+PLjDte60llCRHHAJNx7AJCItqv8nFVpP4J~1',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }
    response = requests.get(product_url, cookies=cookies, headers=headers)
    if response.status_code == 200:
        logger.success(f"Status code is {response.status_code}")

    selector = Selector(text=response.text)

    color_variation_list = selector.xpath(
        '//div[@class="pdp-variations__single-variation  selectable"] | //div[contains(@class,"pdp-variations__single-variation selectable")]')  # a/@href
    if color_variation_list:
        for colour in color_variation_list:
            colour_url = colour.xpath('.//a/@href').get()
            item = dict()

            if colour_url:
                # item['product_url'] = product_url

                item['colour_url'] = colour_url

            if colour_url:
                hash_id = int(hashlib.md5(bytes(str(colour_url) + str(product_url), "utf8")).hexdigest(), 16) % (
                        10 ** 18)
                item['hash_id'] = hash_id

            try:
                # Convert dicts, lists, tuples → JSON
                value_list = [
                    json.dumps(v) if isinstance(v, (dict, list, tuple)) else v
                    for v in item.values()
                ]

                # Build query dynamically
                field_list = [f"`{field}`" for field in item.keys()]
                placeholders = ["%s"] * len(item)

                fields = ",".join(field_list)
                placeholders_str = ",".join(placeholders)

                insert_db = (
                    f"INSERT IGNORE INTO pdp_links_new"
                    f"({fields}) VALUES ({placeholders_str})"
                )

                cursor.execute(insert_db, value_list)
                connection.commit()
                logger.info("Item Successfully Inserted...")
            except Exception as e:
                logger.error(f"SQL Insert Error: {e}")

        # Todo:Update link status
        update_sql = f"UPDATE pdp_links SET status = %s WHERE product_url = %s"
        update_values = ('Done', product_url)
        cursor.execute(update_sql, update_values)
        connection.commit()

        logger.success("Item Successfully Updated...")
    else:
        # Todo:Update link status
        update_sql = f"UPDATE pdp_links SET status = %s WHERE product_url = %s"
        update_values = ('Colour Not Found', product_url)
        cursor.execute(update_sql, update_values)
        connection.commit()
        logger.error("Colour Variation Not Found")


if __name__ == "__main__":
    # Todo: Using Threading
    connection, cursor = get_connection()

    sql_query = f"SELECT * FROM pdp_links WHERE status='Pending';"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    # for result in results:
    #     product_url = result[1]
    #     get_variations(product_url)

    product_urls = [row[1] for row in results]

    # ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=50) as executor:  # adjust worker count as needed
        futures = {executor.submit(get_variations, url): url for url in product_urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()  # get returned value or cause exception to surface
            except Exception as e:
                print(f"Error processing {url}: {e}")
