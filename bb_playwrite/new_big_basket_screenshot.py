import asyncio
import datetime
import os
import re
import time
import mysql.connector

import pandas as pd
from parsel import Selector
from playwright.async_api import async_playwright


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="big_basket_q_9"
    )
    return connection


select_table = 'input_11_04_2025'
connection = get_connection()
cursor = connection.cursor()
query = f"SELECT * FROM {select_table} where status='Pending'"
cursor.execute(query)
results = cursor.fetchall()
insert_table = "pdp_data_11_04_2025"


async def scrape_dmart():
    async with async_playwright() as p:
        for result in results:
            browser = await p.chromium.launch(headless=False)
            id = result[0]
            new_category = result[1]
            name_of_the_brand = result[2]
            name_of_the_product = result[3]
            single_pack = result[4]
            bundle_pack = result[5]
            quentity_of_the_product = result[6]
            product_url = result[9]
            new_zipcode = result[10]
            city_name = result[10]
            quantity = result[7]
            packing_of_the_product = result[8]
            page = await browser.new_page()

            await page.goto("https://www.bigbasket.com")
            await page.click(
                '(//button[contains(@class,"AddressDropdown")]//span[contains(text(),"Select Location")])[2]')
            await page.fill(
                '(//input[@class="Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn"])[2]',
                new_zipcode)
            await page.click('(//li[@class="AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX"])[1] | (//li[@class="AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN"])[1]')
            await page.wait_for_timeout(3000)
            await page.goto(product_url)
            await page.wait_for_timeout(500)
            full_html = await page.content()
            response = Selector(text=full_html)

            if not response.xpath("//span[contains(text(),'The selected city is not serviceable at the moment')]"):
                pid = product_url.split('/pd/')[-1].split('/')[0].strip()
                current_date = datetime.datetime.now().strftime("%d_%m_%Y")
                pack_shot_name = f"{pid}_{new_zipcode}_{current_date}.png"
                filepath = fr"F:\Nirav\Project_page_save\big_basket_screenshot\{current_date}"
                os.makedirs(filepath, exist_ok=True)

                try:
                    await page.screenshot(
                        path=fr"{filepath}\{pack_shot_name}",
                        full_page=True)
                except Exception as e:
                    print(e)

                full_html = await page.content()
                response = Selector(text=full_html)

                try:
                    mrp = "".join(response.xpath('//td[contains(text(),"MRP:")]/following-sibling::td/text()').getall())
                    if mrp:
                        mrp = "".join(mrp).replace('₹', '').strip()
                    else:
                        mrp = "N/A"
                except:
                    mrp = "N/A"

                try:
                    price = "".join(
                        response.xpath(
                            "//td[@class='Description___StyledTd-sc-82a36a-4 fLZywG']//text()").getall()).strip()
                    price = price.replace('₹', '').strip()
                except:
                    price = "N/A"

                try:
                    if price:
                        selling_price = price.split(':')[-1].strip()
                    else:
                        selling_price = mrp
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

                try:
                    if response.xpath('(//button[contains(text(),"Add to basket")])[1]'):
                        add_to_cart = "In Stock"
                    else:
                        add_to_cart = "Out of Stock"
                except:
                    add_to_cart='N/A'
                try:
                    per_gm = "".join(
                        response.xpath('//td[contains(text(),"Price")]/following-sibling::td/text()').getall())
                    # per_gm = re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', per_gm)[0].strip()
                    per_gm = per_gm.replace('(', '').replace(')', '').replace('₹', '').replace(' / ', '/')
                except:
                    per_gm = "N/A"

                try:
                    await page.click('(//button[contains(text(),"Add to basket")])[1]')
                    await page.wait_for_timeout(50)
                    count = 0
                    while True:
                        element = await page.wait_for_selector(
                            '(//button[contains(@class,"PdCartCTA___StyledButton2-sc-mq73zq-3")])[1]', timeout=2000)
                        if element:
                            full_html = await page.content()
                            response = Selector(full_html)
                            original_count = response.xpath("//div[contains(@class,'cdHBKF')]/text()").get('').strip()
                            count += 1
                            if original_count:
                                if count == int(original_count):
                                    await element.click()
                                    await page.wait_for_timeout(50)
                                else:
                                    count = count - 1
                                    break
                            else:
                                break
                            time.sleep(1)
                        else:
                            print("Element not found, exiting loop.")
                            break  # Exit loop if element is not available
                except:
                    count = 0

            item = {
                "Sr.No": id,
                "Portal Name": "Big Basket",
                "Product Url": product_url,  # product["BB"]
                "Date (Crawler Date)": datetime.datetime.now().strftime("%d-%m-%Y"),
                "Time (Crawler Time)": datetime.datetime.now().strftime("%H:%M"),
                "City Name": city_name,
                "Pincode": new_zipcode,
                "Brand": name_of_the_brand,
                "Category": new_category,
                "SKU Packshot": pack_shot_name,
                "SKU Name": name_of_the_product,
                "Pack Size": quentity_of_the_product,
                "Single Pack": single_pack,
                "Bundle Pack": bundle_pack,
                "Per Gm Price (Unit Price)": per_gm if per_gm else "N/A",
                "MRP": mrp,
                "Selling price": selling_price if selling_price else mrp,
                "Discount (%)": discount,
                "Save Rs.": save_rs,
                "Availability Status": add_to_cart,
                "Quantity Caping": count,
                "Remarks": "N/A",
                "Quantity": quantity,
                "Packaging of the product": packing_of_the_product
            }
            print(item)
            new_connection = get_connection()
            new_cursor = new_connection.cursor()

            # Todo: Insert data in database
            placeholders = ', '.join(['%s'] * len(item))
            columns = ', '.join([f"`{key}`" for key in item.keys()])
            sql = f"INSERT IGNORE INTO {insert_table} ({columns}) VALUES ({placeholders})"
            new_cursor.execute(sql, list(item.values()))
            new_connection.commit()

            # Todo: update status in database
            update_query = f"UPDATE {select_table} SET status='Done' WHERE id = {id}"
            new_cursor.execute(update_query)
            new_connection.commit()
            new_cursor.close()
            new_connection.close()
        await browser.close()


# Run the scraper
asyncio.run(scrape_dmart())
