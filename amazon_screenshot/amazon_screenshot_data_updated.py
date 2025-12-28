import asyncio
import datetime
import hashlib
import json
import os
import re
import sys
from parsel import Selector
from playwright.async_api import async_playwright
# import mysql.connector
import pymysql
from create_table_ import create_table, pending_links
from loguru import logger
import db_config as db


def get_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database=db.database_name
    )
    return connection


new_connection = get_connection()
new_cursor = new_connection.cursor()


def scrape_amazon(start_index, end):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        # start = sys.argv[1]
        # end = sys.argv[2]
        pdp_query = f"SELECT * FROM {db.pdp_link_table} WHERE status='Done' and id between {start_index} and {end}"
        cursor.execute(pdp_query)
        results = cursor.fetchall()
        if len(results) == 0:
            create_table()
            # pending_links()

        for result in results:
            id = result[0]
            new_category = result[2]
            name_of_the_brand = result[1]
            name_of_the_product = result[3]
            single_pack = result[5]
            bundle_pack = result[6]
            quantity_of_the_product = result[4]
            product_url = result[9]
            quantity = result[7]
            packing_of_the_product = result[8]
            new_zipcode = result[12]
            amazon_approve_not_approve = result[10]
            city_name = result[11]
            pack_shot_name = ''

            with open(fr"{db.pagesave_filepath}\{id}.html", "r", encoding="utf-8") as f:
                html = f.read()
            response = Selector(text=html)

            if product_url:
                try:
                    pid = product_url.split('/dp/')[-1].split('/')[0].strip()
                    if pid:
                        if '?' in pid:
                            pid = pid.split('?')[0].strip()
                    else:
                        pid = 'N/A'
                except Exception as error:
                    logger.error(error)

                try:
                    service_availibility_1 = response.xpath(
                        "//strong[contains(text(),'Amazon Fresh is not available for this location.')]/text()").get()
                except Exception as error:
                    logger.error(error)

                try:
                    service_availibility_2 = response.xpath(
                        "//span[contains(text(),'Amazon Fresh is not available for your selected location.')]/text() | //span[contains(text(),' This store is not available for your selected location.')]/text()").get(
                        '').strip()
                except Exception as error:
                    logger.error(error)

                per_gm = ''
                mrp = ''
                stock_avaibility = ''
                selling_price = ''
                discount = ''
                save_rs = ''
                count = 0
                pack_shot_name = ''
                on_site_sku_name = ''

                if service_availibility_1 or service_availibility_2:
                    try:
                        if pid != 'N/A':
                            pack_shot_name = f"{pid}_{new_zipcode}_{db.current_date}.png"
                            os.makedirs(db.screenshot_filepath, exist_ok=True)
                        else:
                            pack_shot_name = 'N/A'
                    except Exception as error:
                        logger.error(error)

                    try:
                        if pack_shot_name != 'N/A':
                            path = fr"{db.screenshot_filepath}\{pack_shot_name}"
                            # await page.screenshot(path=path, full_page=True)
                    except Exception as error:
                        logger.error(error)

                    stock_avaibility = 'Not listed'
                else:
                    try:
                        if pid != 'N/A':
                            pack_shot_name = f"{pid}_{new_zipcode}_{db.current_date}.png"
                            os.makedirs(db.screenshot_filepath, exist_ok=True)
                        else:
                            pack_shot_name = 'N/A'
                    except Exception as error:
                        logger.error(error)

                    try:
                        if pack_shot_name != 'N/A':
                            path = fr"{db.screenshot_filepath}\{pack_shot_name}"
                            # await page.screenshot(path=path, full_page=True)
                    except Exception as error:
                        logger.error(error)

                    try:
                        mrp = "".join(
                            response.xpath(
                                '//span[contains(text(),"M.R.P")]//span[@class="a-offscreen"]/text()').get())
                        if not mrp:
                            mrp = response.xpath(
                                '//div[@data-csa-c-content-id="apex_with_rio_cx"]//span[contains(text(),"M.R.P")]//span[@class="a-offscreen"]/text()').get(
                                '').strip()
                        if mrp:
                            mrp = "".join(mrp).replace('₹', '').strip()
                            mrp = int(float(mrp))
                        else:
                            mrp = "N/A"
                    except:
                        mrp = "N/A"

                    try:
                        price = response.xpath(
                            '//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//span[@class="a-offscreen"]/text()').get(
                            '').strip()
                        if not price:
                            price = response.xpath(
                                '//div[@data-csa-c-content-id="apex_with_rio_cx"]//span[@class="a-price-whole"]/text()').get(
                                '').strip()
                        if price:
                            price = "".join(price).replace('₹', '').strip()
                            price = int(float(price))
                        else:
                            price = mrp
                    except:
                        price = "N/A"

                    try:
                        selling_price = re.findall("\\d+", str(price))[0]
                    except:
                        selling_price = mrp

                    if mrp == "N/A" and selling_price != "N/A":
                        mrp = selling_price

                    try:
                        discount = response.xpath(
                            "//span[contains(@class,'reinventPriceSavingsPercentageMargin')]/text()").get(
                            '').replace('-', '').replace('%', '')
                    except:
                        discount = "N/A"

                    try:
                        save_rs = int(float(mrp) - float(selling_price))
                        if int(save_rs) == 0:
                            save_rs = '0'
                    except:
                        save_rs = "N/A"

                    try:
                        if response.xpath(
                                '//span[contains(text(),"In Stock")]/text() | //span[contains(text(),"In stock")]/text()').get(
                            '').strip():
                            stock_avaibility = "In Stock"
                        else:
                            stock_avaibility = "Out of Stock"
                    except:
                        stock_avaibility = 'Not listed'

                    try:
                        if mrp or selling_price:
                            per_gm = response.xpath(
                                '//span[@data-a-size="mini"]/span[@class="a-offscreen"]/text()').get()
                            per_gm = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', per_gm)[0].strip()
                            per_gam_text = response.xpath(
                                '(//span[@class="a-size-mini a-color-base aok-align-center a-text-normal"])[1]/text()').getall()[
                                -1].replace('/', '').replace(')', '').strip()
                            per_gm = f"{per_gm}/{per_gam_text}"
                        else:
                            per_gm = 'N/A'
                    except:
                        per_gm = "N/A"

                    try:
                        count_json = response.xpath(
                            "//script[@type='a-state' and contains(text(), 'quantityText')]/text()").get()
                        if count_json:
                            json_data = json.loads(count_json)
                            count = json_data.get('qsItems')[-1].get('id')
                        else:
                            count = response.xpath(
                                "//ul[@class='a-nostyle a-list-link']/li[@class='a-dropdown-item'][last()]/a/text()")
                            if not count:
                                count = response.xpath("//select[@name='quantity']/option/text()").getall()[-1]
                    except Exception as error:
                        logger.error(error)

                    # Todo: Update count
                    if stock_avaibility == "Out of Stock" or stock_avaibility == "Not listed":
                        count = "N/A"
                try:
                    on_site_sku_name = response.xpath(
                        '//h1[@id="title"]/span[@id="productTitle"]/text()').get(
                        '').strip()
                except:
                    on_site_sku_name = 'N/A'

                hash_id = str(int(hashlib.md5(bytes(str(str(
                    id) + city_name + product_url + name_of_the_brand + new_category + new_zipcode + name_of_the_product + quantity_of_the_product),
                                                    "utf8")).hexdigest(), 16) % (10 ** 10))
                item = {'Sr.No': id,
                        "Portal Name": "Amazon Fresh",
                        "Product Url": product_url if product_url else "N/A",
                        "Date (Crawler Date)": datetime.datetime.now().strftime("%d-%m-%Y"),
                        "Time (Crawler Time)": datetime.datetime.now().strftime("%H:%M"),
                        "City Name": city_name,
                        "Pincode": new_zipcode,
                        "Brand": name_of_the_brand,
                        "Category": new_category,
                        "SKU Packshot": pack_shot_name if pack_shot_name else 'N/A',
                        "SKU Name": name_of_the_product,
                        "Pack Size": quantity_of_the_product,
                        "Single Pack": single_pack if single_pack else 'N/A',
                        "Bundle Pack": bundle_pack if bundle_pack else 'N/A',
                        "Per Gm Price (Unit Price)": per_gm if per_gm else "N/A",
                        "MRP": mrp if mrp else 'N/A',
                        "Selling price": selling_price if selling_price else 'N/A',
                        "Discount (%)": discount if discount else 'N/A',
                        "Save Rs.": save_rs if save_rs else 'N/A',
                        "On-site SKU Name": on_site_sku_name,
                        "Availability Status": stock_avaibility,
                        "Quantity Caping": str(count).strip() if count != 'N/A' else count,
                        "Remarks": "N/A",
                        "Quantity": quantity if quantity else 'N/A',
                        "Packaging of the product": packing_of_the_product,
                        "amazon_approve_not_approve": amazon_approve_not_approve,
                        'hash_id': hash_id
                        }
                print(json.dumps(item))

            else:

                try:
                    # pack_shot_name = str(int(hashlib.md5(bytes(
                    #     str(str(
                    #         id) + city_name + product_url + name_of_the_brand + new_category + new_zipcode + name_of_the_product + quantity_of_the_product),
                    #     "utf8")).hexdigest(),
                    #                          16) % (
                    #                              10 ** 10))
                    pack_shot_name = f"{id}_{new_zipcode}_{db.current_date}"
                    pack_shot_name = f"{pack_shot_name}.png"
                    # os.makedirs(db.filepath, exist_ok=True)
                except:
                    pack_shot_name = 'N/A'

                try:
                    if pack_shot_name != 'N/A':
                        path = fr"{db.screenshot_filepath}\{pack_shot_name}"
                except Exception as e:
                    print(e)

                hash_id = str(int(hashlib.md5(bytes(str(str(
                    id) + city_name + product_url + name_of_the_brand + new_category + new_zipcode + name_of_the_product + quantity_of_the_product),
                                                    "utf8")).hexdigest(), 16) % (10 ** 10))

                item = {
                    "Sr.No": id,
                    "Portal Name": "Amazon Fresh",
                    "Product Url": product_url if product_url else 'N/A',
                    "Date (Crawler Date)": datetime.datetime.now().strftime("%d-%m-%Y"),
                    "Time (Crawler Time)": datetime.datetime.now().strftime("%H:%M"),
                    "City Name": city_name,
                    "Pincode": new_zipcode,
                    "Brand": name_of_the_brand if name_of_the_brand else 'N/A',
                    "Category": new_category if new_category else 'N/A',
                    "SKU Packshot": pack_shot_name,
                    "SKU Name": name_of_the_product if name_of_the_product else 'N/A',
                    "Pack Size": quantity_of_the_product if quantity_of_the_product else 'N/A',
                    "Single Pack": single_pack if single_pack else 'N/A',
                    "Bundle Pack": bundle_pack if bundle_pack else 'N/A',
                    "Per Gm Price (Unit Price)": 'N/A',
                    "MRP": 'N/A',
                    "Selling price": 'N/A',
                    "Discount (%)": 'N/A',
                    "Save Rs.": 'N/A',
                    "On-site SKU Name": "N/A",
                    "Availability Status": 'Not listed',
                    "Quantity Caping": 'N/A',
                    "Remarks": "N/A",
                    "Quantity": quantity if quantity else 'N/A',
                    "Packaging of the product": packing_of_the_product if packing_of_the_product else 'N/A',
                    "amazon_approve_not_approve": amazon_approve_not_approve,
                    "hash_id": hash_id
                }
                print(json.dumps(item))

            # Todo: make connection
            new_connection = get_connection()
            new_cursor = new_connection.cursor()

            field_list = []
            value_list = []
            for field in item:
                field_list.append(str(f"`{field}`"))
                value_list.append(str(item[field]).replace("'", "’"))
            fields = ','.join(field_list)
            values = "','".join(value_list)
            insert_db = f"insert ignore into {db.pdp_data_table}" + "( " + fields + " ) values ( '" + values + "' )"
            try:
                new_cursor.execute(insert_db)
                new_connection.commit()
                logger.success(f"Data successfully inserted for id: {item.get('hash_id')}")
            except Exception as e:
                new_connection.rollback()
                logger.error(f"Failed to insert data: {e}")
            try:
                # Todo: update status in database
                update_query = f"UPDATE {db.pdp_link_table} SET status='Finally_Done' WHERE id = {id}"
                new_cursor.execute(update_query)
                new_connection.commit()
                logger.success(f"Your data successfull updated using for this table id: {id}")
            except Exception as error:
                logger.error(error)

    except Exception as error:
        logger.error(f"Error fetching PDP links: {error}")
    # try:
    #     # Todo: update status in database
    #     update_query = f"UPDATE {db.pincode_table} SET status='Done' WHERE zipcode = {pincode}"
    #     new_cursor.execute(update_query)
    #     new_connection.commit()
    #     logger.success(f"Your pincode successfull updated using for this pincode: {pincode}")
    #     new_cursor.close()
    #     new_connection.close()
    # except Exception as error:
    #     logger.error(error)


# await page.close()
# # break
# await browser.close()
# Run the scraper

try:
    start_index = sys.argv[1]
except Exception as e:
    print(e)

try:
    end = sys.argv[2]
except Exception as e:
    print(e)

if __name__ == '__main__':
    scrape_amazon(start_index, end)
