import asyncio
import datetime
import json
import re
import time

import mysql.connector
import pandas as pd
from parsel import Selector
from playwright.async_api import async_playwright

product_details = [
    {
        "Name Of the Brand": "Dabur Amla",
        "Name of the Product": "Dabur Amla Hair Oil 550 ml",
        "Quantity of the Product": "550ml",
        "Packaging of the product": "Pet Bottle",
        "Amazon_Fresh": "https://www.amazon.in/Dabur-Amla-Hair-Oil-Strong/dp/B0832ZWDHR"
    },
    {
        "Name Of the Brand": "Dabur Red",
        "Name of the Product": "Dabur Red Tooth Paste 100 gm",
        "Quantity of the Product": "100gm",
        "Packaging of the product": "Tube",
        "Amazon_Fresh": "https://www.amazon.in/Dabur-Red-Ayurvedic-Paste-100/dp/B0067GFOOS"
    },
    {
        "Name Of the Brand": "Odonil",
        "Name of the Product": "Odonil air freshner block pack of 5",
        "Quantity of the Product": "Pack of 5",
        "Packaging of the product": "Box pack",
        "Amazon_Fresh": "https://www.amazon.in/Odonil-Bathroom-Air-Freshener-Zipper/dp/B07VCC76MN"
    },
    {
        "Name Of the Brand": "Dabur Honey",
        "Name of the Product": "Dabur Honey 1 Kg",
        "Quantity of the Product": "1000gm",
        "Packaging of the product": "Glass Bottle",
        "Amazon_Fresh": "https://www.amazon.in/Dabur-100-Pure-Honey-Extra/dp/B07H6NMLY9"
    },
    {
        "Name Of the Brand": "Real",
        "Name of the Product": "Real Mixed Fruit Juice 1Ltr",
        "Quantity of the Product": "1000ml",
        "Packaging of the product": "Tetra Pack",
        "Amazon_Fresh": "https://www.amazon.in/Real-Fruit-Power-Mixed-1L/dp/B013P5X7XI"
    },
    {
        "Name Of the Brand": "Dant Kanti",
        "Name of the Product": "Patanjali Dant Kanti Natural Tooth Paste 300 gm",
        "Quantity of the Product": "300gm",
        "Packaging of the product": "Tube",
        "Amazon_Fresh": "https://www.amazon.in/Patanjali-Active-Toothpaste-Crystal-Tightens/dp/B0DSC2TMKL"
    },
    {
        "Name Of the Brand": "Tropicana",
        "Name of the Product": "Tropicana Mixed fruit 1Ltr",
        "Quantity of the Product": "1000ml",
        "Packaging of the product": "Tetra Pack",
        "Amazon_Fresh": "https://www.amazon.in/Tropicana-Fruit-Juice-Delight-Carton/dp/B00TTX2KCA"
    },
    {
        "Name Of the Brand": "Maaza",
        "Name of the Product": "Maaza Rs. 10 Tetra",
        "Quantity of the Product": "125ml/135ml",
        "Packaging of the product": "Tetra Pack",
        "Amazon_Fresh": "https://www.amazon.in/Maaza-Refresh-Mango-Fruit-Drink/dp/B08GYR6X8Z"
    },
    {
        "Name Of the Brand": "Colgate",
        "Name of the Product": "Colgate Tooth Paste Strong Teeth 300 gm",
        "Quantity of the Product": "300gm",
        "Packaging of the product": "Tube",
        "Amazon_Fresh": "https://www.amazon.in/Colgate-Toothpaste-Strong-Teeth-Anti-cavity/dp/B007BBUZ60/"
    }
]

zipcode = '110016'
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="amazon_fresh_q_9"
)
cursor = connection.cursor()
query = "SELECT * FROM input_08_04_2025_new where status='Pending'"
cursor.execute(query)
results = cursor.fetchall()


async def scrape_dmart():
    async with async_playwright() as p:
        zipcodes = ['110016', '110001']  # '110001'
        data_list = list()
        for zipcode in zipcodes:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.amazon.in")
            await page.click('//a[@id="nav-global-location-popover-link"]')
            await page.fill('//input[@class="GLUX_Full_Width a-declarative"]', zipcode)
            await page.click('//span[@id="GLUXZipUpdate-announce"]')
            await page.wait_for_timeout(3000)

            # data_list = list()

            for result in results:
                id = result[0]
                new_category = result[1]
                name_of_the_brand = result[2]
                name_of_the_product = result[3]
                single_pack = result[4]
                bundle_pack = result[5]
                quentity_of_the_product = result[6]
                product_url = result[9]
                await page.goto(product_url)
                await page.wait_for_timeout(500)

                pid = product_url.split('/dp/')[-1].split('/')[0].strip()
                if '?' in pid:
                    pid = pid.split('?')[0].strip()

                current_date = datetime.datetime.now().strftime("%d_%m_%Y")
                pack_shot_name = f"{pid}_{zipcode}_{current_date}.png"
                try:
                    await page.screenshot(
                        path=fr"F:\Nirav\Project_page_save\amazon_fresh_screenshot\new\{pack_shot_name}",
                        full_page=True)
                except Exception as e:
                    print(e)

                crawl_date = datetime.datetime.now().strftime("%d-%m-%Y")
                crawl_time = datetime.datetime.now().strftime("%H:%M")

                full_html = await page.content()

                response = Selector(text=full_html)

                sku_name_list = response.xpath('//h1[@id="title"]//text()').getall()

                sku_name = " ".join(sku_name_list).strip()
                bundle = False
                try:
                    pattern = r"(?<=\(Pack of )\d+"
                    match = re.search(pattern, sku_name)
                    if match:
                        bundle = int(match.group())
                except:
                    continue

                try:
                    mrp = "".join(
                        response.xpath('//span[contains(text(),"M.R.P")]//span[@class="a-offscreen"]/text()').get())
                    if mrp:
                        mrp = "".join(mrp).replace('₹', '').strip()
                        mrp = int(float(mrp))
                    else:
                        mrp = "N/A"
                except:
                    mrp = "N/A"

                try:
                    category = response.xpath(
                        "//ul[@class='a-unordered-list a-horizontal a-size-small']//span[@class='a-list-item']//a/text()").getall()[
                        -1].strip()
                except:
                    category = 'N/A'

                try:
                    price = response.xpath(
                        '//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//span[@class="a-offscreen"]/text()').get(
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

                if response.xpath('//span[contains(text(),"In Stock")]'):
                    stock_avaibility = "In Stock"
                else:
                    stock_avaibility = "Out of Stock"

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

                item = {
                    "Sr.No": id,
                    "Portal Name": "Amazon Fresh",
                    "Product Url": product_url,
                    "Date (Crawler Date)": crawl_date,
                    "Time (Crawler Time)": crawl_time,
                    "City Name": "Delhi",
                    "Pincode": f"{zipcode}",
                    "Brand": name_of_the_brand,
                    "Category": new_category,
                    "SKU Packshot": f"{pack_shot_name}",
                    "SKU Name": name_of_the_product,
                    "Pack Size": quentity_of_the_product,
                    "Single Pack": single_pack,
                    "Bundle Pack": bundle_pack,
                    "Per Gm Price (Unit Price)": per_gm if per_gm else "N/A",
                    "MRP": mrp,
                    "Selling price": selling_price,
                    "Discount (%)": discount,
                    "Save Rs.": save_rs,
                    "Availability Status": stock_avaibility,
                    "Quantity Caping": count if count != 'N/A' else 0,
                    "Remarks": "N/A",
                }
                data_list.append(item)
                print(data_list)
        df = pd.DataFrame(data_list)
        df.fillna("N/A", inplace=True)
        filepath = fr'F:\Nirav\Project_code\bb_playwrite\output_files\Amazon_fresh_data_{crawl_date}.xlsx'
        df.to_excel(filepath, index=False)
        await browser.close()


# Run the scraper
asyncio.run(scrape_dmart())
