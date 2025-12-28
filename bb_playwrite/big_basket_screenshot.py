import asyncio
import datetime
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
        "BB": "https://www.bigbasket.com/pd/40193954/dabur-amla-hair-oil-for-strong-long-thick-hair-550-ml"
    },
    {
        "Name Of the Brand": "Dabur Red",
        "Name of the Product": "Dabur Red Tooth Paste 100 gm",
        "Quantity of the Product": "100gm",
        "Packaging of the product": "Tube",
        "BB": "https://www.bigbasket.com/pd/100012572/dabur-red-indias-no1-ayurvedic-fluroide-free-paste-100-g/"
    },
    {
        "Name Of the Brand": "Odonil",
        "Name of the Product": "Odonil air freshner block pack of 5",
        "Quantity of the Product": "Pack of 5",
        "Packaging of the product": "Box pack",
        "BB": "https://www.bigbasket.com/pd/40176346/odonil-nature-air-freshener-zipper-mix-10-g/"
    },
    {
        "Name Of the Brand": "Dabur Honey",
        "Name of the Product": "Dabur Honey 1 Kg",
        "Quantity of the Product": "1000gm",
        "Packaging of the product": "Glass Bottle",
        "BB": "https://www.bigbasket.com/pd/202277/dabur-100-pure-honey-worlds-no1-honey-brand-with-no-sugar-adulteration-1-kg/"
    },
    {
        "Name Of the Brand": "Real",
        "Name of the Product": "Real Mixed Fruit Juice 1Ltr",
        "Quantity of the Product": "1000ml",
        "Packaging of the product": "Tetra Pack",
        "BB": "https://www.bigbasket.com/pd/40253188/real-mixed-fruit-juice-vitamin-boost-refreshing-drink-no-preservatives-1-l/"
    },
    {
        "Name Of the Brand": "Dabur",
        "Name of the Product": "Dabur Glucose D 1 Kg",
        "Quantity of the Product": "1000gm",
        "Packaging of the product": "Pet Bottle/Box pack",
        "BB": "https://www.bigbasket.com/pd/264322/dabur-glucose-d-energy-boost-with-vitamin-d-with-dabur-red-paste-200-g-free-1-kg-pet-jar/"
    },
    {
        "Name Of the Brand": "Good Home",
        "Name of the Product": "Good Home Air Freshner Block 2+1",
        "Quantity of the Product": "2+1 pack",
        "Packaging of the product": "Box pack",
        "BB": "https://www.bigbasket.com/pd/40298399/good-home-air-freshener-rose-lavender-floral-lasts-upto-45-days-225-gm/"
    },
    {
        "Name Of the Brand": "Apis",
        "Name of the Product": "Apis Honey 500gm = 500 gm BOGO",
        "Quantity of the Product": "500gm+500gm",
        "Packaging of the product": "Glass Bottle/Pet Jar",
        "BB": "https://www.bigbasket.com/pd/40045719/apis-himalaya-honey-500-g/"
    },
    {
        "Name Of the Brand": "Tropicana",
        "Name of the Product": "Tropicana Mixed fruit 1Ltr",
        "Quantity of the Product": "1000ml",
        "Packaging of the product": "Tetra Pack",
        "BB": "https://www.bigbasket.com/pd/40326796/tropicana-frutz-mixed-fruit-magic-1-l/"
    },
    {
        "Name Of the Brand": "Tropicana",
        "Name of the Product": "Tropicana Mixed fruit 200 ml",
        "Quantity of the Product": "200ml",
        "Packaging of the product": "Tetra Pack",
        "BB": "https://www.bigbasket.com/pd/292475/tropicana-100-mixed-fruit-juice-200-ml/"
    },
    {
        "Name Of the Brand": "Dant Kanti",
        "Name of the Product": "Patanjali Dant Kanti Natural Tooth Paste 100 gm",
        "Quantity of the Product": "100gm",
        "Packaging of the product": "Tube",
        "BB": "https://www.bigbasket.com/pd/40075288/patanjali-dant-kanti-medicated-oral-gel-100-g/"
    }
]

# zipcode = '400013'

# Connect to the database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="big_basket_q_9"
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
            await page.goto("https://www.bigbasket.com")
            await page.click(
                '(//button[contains(@class,"AddressDropdown")]//span[contains(text(),"Select Location")])[2]')
            await page.fill(
                '(//input[@class="Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn"])[2]',
                zipcode)
            await page.click(
                '(//li[@class="AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX"]//span[contains(text(),"New Delhi, Delhi, India")])[1]')
            await page.wait_for_timeout(3000)  # 3000

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

                pid = product_url.split('/pd/')[-1].split('/')[0].strip()
                current_date = datetime.datetime.now().strftime("%d_%m_%Y")
                pack_shot_name = f"{pid}_{zipcode}_{current_date}.png"
                await page.screenshot(
                    path=fr"F:\Nirav\Project_page_save\big_basket_screenshot\{pack_shot_name}",
                    full_page=True)

                crawl_date = datetime.datetime.now().strftime("%d-%m-%Y")
                crawl_time = datetime.datetime.now().strftime("%H:%M")

                full_html = await page.content()

                response = Selector(text=full_html)

                sku_name_list = response.xpath(
                    '//h1[@class="Description___StyledH-sc-82a36a-2 bofYPK"]/text()').getall()
                sku_name = " ".join(sku_name_list).strip()

                bundle = False
                try:
                    if 'x' in sku_name_list[-1]:
                        bundle = True
                except:
                    await page.screenshot(
                        path=fr"F:\Nirav\Project_page_save\big_basket_screenshot\new\{pid}_400013.png",
                        full_page=True)
                    continue

                try:
                    mrp = "".join(response.xpath('//td[contains(text(),"MRP:")]/following-sibling::td/text()').getall())
                    if mrp:
                        mrp = "".join(mrp).replace('₹', '').strip()
                    else:
                        mrp = "N/A"
                except:
                    mrp = "N/A"

                try:
                    category = response.xpath(
                        "//div[@class='Breadcrumb___StyledDiv-sc-1jdzjpl-0 hlQOJm']//a/span/text()").getall()[
                        -1].strip()
                except:
                    category = 'N/A'

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

                if response.xpath('(//button[contains(text(),"Add to basket")])[1]'):
                    add_to_cart = "In Stock"
                else:
                    add_to_cart = "Out of Stock"

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
                    "Date (Crawler Date)": crawl_date,
                    "Time (Crawler Time)": crawl_time,
                    "City Name": "Delhi",
                    "Pincode": f"{zipcode}",
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
                }
                data_list.append(item)
                print(data_list)
        df = pd.DataFrame(data_list)
        df.fillna("N/A", inplace=True)
        filepath = fr'F:\Nirav\Project_code\bb_playwrite\output_files\Big_Basket_data_{crawl_date}.xlsx'
        df.to_excel(filepath, index=False)
        await browser.close()


# Run the scraper
asyncio.run(scrape_dmart())
