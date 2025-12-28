import asyncio
import datetime
import hashlib
import json
import os
import re
import time
import db_config as db
import mysql.connector
import pandas as pd
from parsel import Selector
from playwright.async_api import async_playwright


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="amazon_fresh_screenshot"
    )
    return connection


connection = get_connection()
cursor = connection.cursor()
query = f"SELECT * FROM {db.amazon_pdp_link} where status='Pending'"
cursor.execute(query)
results = cursor.fetchall()


async def scrape_dmart():
    async with async_playwright() as p:
        for result in results:
            id = result[0]
            new_category = result[1]
            name_of_the_brand = result[2]
            name_of_the_product = result[3]
            single_pack = result[4]
            bundle_pack = result[5]
            quentity_of_the_product = result[6]
            product_url = result[9]
            quantity = result[7]
            packing_of_the_product = result[8]
            new_zipcode = result[10]
            city_name = result[11]

            browser = await p.webkit.launch(headless=False)
            # page = await browser.new_page()
            if product_url:
                try:
                    page = await browser.new_page()
                    await page.goto(product_url)
                    response = Selector(text=await page.content())
                except Exception as e:
                    await browser.close()
                    print(e)

            if product_url:
                try:
                    # Todo: Retry Captcha
                    if product_url:
                        for i in range(5):
                            if response.xpath("//h4[contains(text(),'Enter the characters you see below')]"):
                                await page.wait_for_timeout(50)
                                await page.reload()
                                response = Selector(text=await page.content())
                                if response.xpath("//h4[contains(text(),'Enter the characters you see below')]"):
                                    await page.wait_for_timeout(50)
                                    await page.reload()
                                else:
                                    break
                            else:
                                break
                except Exception as e:
                    print(e)

            try:
                if product_url:
                    await page.click('//input[@class="GLUX_Full_Width a-declarative"]')
                    await page.wait_for_timeout(500)
                    await page.fill('//input[@class="GLUX_Full_Width a-declarative"]', new_zipcode)
                    await page.click('//span[@id="GLUXZipUpdate-announce"]')
                    await page.wait_for_timeout(5000)
            except Exception as e:
                print(e)

            try:
                pid = product_url.split('/dp/')[-1].split('/')[0].strip()
                if pid:
                    if '?' in pid:
                        pid = pid.split('?')[0].strip()
                else:
                    pid = 'N/A'
            except:
                pid = 'N/A'

            current_date = datetime.datetime.now().strftime("%d_%m_%Y")

            # try:
            #     if pid != 'N/A':
            #         pack_shot_name = f"{pid}_{new_zipcode}_{current_date}.png"
            #         filepath = fr"D:\Nirav Chauhan\screenshot\Amazon_Fresh_Screenshot\{db.current_date}"
            #         os.makedirs(filepath, exist_ok=True)
            #     else:
            #         pack_shot_name = 'N/A'
            # except:
            #     pack_shot_name = 'N/A'
            #
            # try:
            #     if pack_shot_name != 'N/A':
            #         path = fr"{filepath}\{pack_shot_name}"
            #         await page.screenshot(path=path, full_page=True)
            # except Exception as e:
            #     print(e)

            try:
                full_html = await page.content()
                response = Selector(text=full_html)
            except Exception as e:
                print(e)

            service_availibility = response.xpath("//strong[contains(text(),'Amazon Fresh is not available for this location.')]/text()").get()

            per_gm=''
            mrp=''
            selling_price=''
            discount=''
            save_rs=''
            count=0
            pack_shot_name=''
            if not service_availibility:
                try:
                    if pid != 'N/A':
                        pack_shot_name = f"{pid}_{new_zipcode}_{current_date}.png"
                        filepath = fr"D:\Nirav Chauhan\screenshot\Amazon_Fresh_Screenshot\{db.current_date}"
                        os.makedirs(filepath, exist_ok=True)
                    else:
                        pack_shot_name = 'N/A'
                except:
                    pack_shot_name = 'N/A'

                try:
                    if pack_shot_name != 'N/A':
                        path = fr"{filepath}\{pack_shot_name}"
                        await page.screenshot(path=path, full_page=True)
                except Exception as e:
                    print(e)

                try:
                    mrp = "".join(
                        response.xpath('//span[contains(text(),"M.R.P")]//span[@class="a-offscreen"]/text()').get())
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

                try:
                    discount = int(((float(mrp) - float(selling_price)) * 100) / float(mrp))
                    if int(discount) == 0:
                        discount = 'N/A'
                except:
                    discount = "N/A"

                try:
                    save_rs = int(float(mrp) - float(selling_price))
                    if int(save_rs) == 0:
                        save_rs = 'N/A'
                except:
                    save_rs = "N/A"

                if product_url:
                    if response.xpath('//span[contains(text(),"In Stock")]'):
                        stock_avaibility = "In Stock"
                    else:
                        stock_avaibility = "Out of Stock"
                else:
                    stock_avaibility = 'Not listed'


                try:
                    if mrp != 'N/A' and mrp:
                        per_gm = response.xpath('//span[@data-a-size="mini"]/span[@class="a-offscreen"]/text()').get()
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
                    json_data = json.loads(count_json)
                    count = json_data.get('qsItems')[-1].get('id')
                except:
                    count = 'N/A'
            else:
                stock_avaibility = 'Not listed'
            hash_id = str(
                int(hashlib.md5(bytes(
                    str(new_category + new_zipcode + name_of_the_product), "utf8")).hexdigest(),
                    16) % (
                        10 ** 10))
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
                    "Pack Size": quentity_of_the_product,
                    "Single Pack": single_pack if single_pack else 'N/A',
                    "Bundle Pack": bundle_pack if bundle_pack else 'N/A',
                    "Per Gm Price (Unit Price)": per_gm if per_gm else "N/A",
                    "MRP": mrp if mrp else 'N/A',
                    "Selling price": selling_price if selling_price else 'N/A',
                    "Discount (%)": discount if discount else 'N/A',
                    "Save Rs.": save_rs if save_rs else 'N/A',
                    "Availability Status": stock_avaibility,
                    "Quantity Caping": count if count != 'N/A' else 0,
                    "Remarks": "N/A",
                    "Quantity": quantity if quantity else 'N/A',
                    "Packaging of the product": packing_of_the_product,
                    'hash_id':hash_id
                    }
            print(item)
            new_connection = get_connection()
            new_cursor = new_connection.cursor()

            # Todo: Insert data in database
            placeholders = ', '.join(['%s'] * len(item))
            columns = ', '.join([f"`{key}`" for key in item.keys()])
            sql = f"INSERT IGNORE INTO {db.amazon_pdp_data} ({columns}) VALUES ({placeholders})"
            new_cursor.execute(sql, list(item.values()))
            new_connection.commit()

            # Todo: update status in database
            update_query = f"UPDATE {db.amazon_pdp_link} SET status='Done' WHERE id = {id}"
            new_cursor.execute(update_query)
            new_connection.commit()
            new_cursor.close()
            new_connection.close()

            await browser.close()


# Run the scraper
asyncio.run(scrape_dmart())
