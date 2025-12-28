import asyncio
import datetime
import re
import time

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

zipcode = '110016'


# zipcode = '400013'


async def scrape_dmart():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        # await page.goto("https://www.dmart.in")
        await page.goto("https://www.bigbasket.com")
        await page.click('(//button[contains(@class,"AddressDropdown")]//span[contains(text(),"Select Location")])[2]')
        page.locator('xpath=//input[1][@placeholder="Search for area or street name"]')
        await page.fill('//input[1][@placeholder="Search for area or street name"]', f'{zipcode}')
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)  # Wait for results to load

        # await page.fill('button[type="button"]', product)
        await page.click('div[class="pincode-widget_pincode-right__TwcOu"]')
        await page.wait_for_timeout(3000)

        await page.click('//button[contains(text(), "CONFIRM LOCATION")]')
        await page.wait_for_timeout(3000)

        data_list = list()

        for index, product in enumerate(product_details, start=1):

            await page.goto(product['Dmart'])
            await page.wait_for_timeout(5000)

            pid = product['Dmart'].split('selectedProd=')[-1]

            await page.screenshot(
                path=fr"F:\Nirav\9 Quick Commerce SS\Big_basket\{pid}_110016.png",
                full_page=True)

            crawl_date = datetime.datetime.now().strftime("%d-%m-%Y")
            crawl_time = datetime.datetime.now().strftime("%H:%M:%S")

            full_html = await page.content()

            response = Selector(text=full_html)

            sku_name_list = response.xpath(
                '//h1[@class="text-label-component_title-container__Bcu9q"]//span//text()').getall()

            sku_name = " ".join(sku_name_list)
            bundle = False
            try:
                if 'x' in sku_name_list[-1]:
                    bundle = True
            except:
                await page.screenshot(
                    path=fr"D:\Data\Gaurav\PROJECT\DMART SELENIUM\9 Quick Commerce SS\Dmart\{pid}_400013.png",
                    full_page=True)
                continue

            try:
                mrp = "".join(response.xpath('//span[contains(text(), "MRP ")]//text()').getall())
                mrp = re.findall("\\d+", mrp)[0]
            except:
                mrp = "N/A"

            try:
                price = "".join(response.xpath('//span[contains(text(), "DMart ")]//text()').getall())
            except:
                price = "N/A"

            try:
                selling_price = re.findall("\\d+", price)[0]
            except:
                selling_price = "N/A"

            try:
                discount = int(((float(mrp) - float(selling_price)) * 100) / float(mrp))
            except:
                discount = "N/A"

            try:
                save = "".join(response.xpath('//div[contains(text(), "Save")]//text()').getall())
                save_rs = re.findall("\\d+", save)[0]
            except:
                save_rs = "N/A"

            if response.xpath('//label[contains(text(), "ADD TO CART")]'):
                add_to_cart = "In Stock"
            else:
                add_to_cart = "Out of Stock"

            try:
                per_gm = "".join(
                    response.xpath('//span[@class="price-details-component_price-info__upgwm"]//text()').getall())
            except:
                per_gm = "N/A"

            await page.click('//label[contains(text(), "ADD TO CART")]')

            count = 1
            for i in range(9):
                try:
                    element = await page.wait_for_selector(
                        '(//div[@class="cart-action_action__qzot9 "]//button[@type="button"])[2]', timeout=2000)

                    if element:
                        await element.click()  # Click if the element exists
                        count += 1
                        time.sleep(1)
                    else:
                        print("Element not found, exiting loop.")
                        break  # Exit loop if element is not available
                except:
                    break  # Exit loop if element is not available

            item = {
                "Sr.No": index,
                "Portal Name": "DMart",
                "Product Url": product["Dmart"],
                "Date (Crawler Date)": crawl_date,
                "Time (Crawler Time)": crawl_time,
                "City Name": "Mumbai",
                "Pincode": f"{zipcode}",
                "Brand": product['Name Of the Brand'],
                "Category": "N/A",
                "SKU Packshot": f"{pid}_400013.png",
                "SKU Name": sku_name,
                "Pack Size": product['Quantity of the Product'],
                "Single Pack": "N/A" if bundle else "1",
                "Bundle Pack": sku_name_list[-1].split("x")[0].replace(":", "").strip() if bundle else "N/A",
                "Per Gm Price (Unit Price)": per_gm,
                "MRP": mrp,
                "Selling price": selling_price,
                "Discount (%)": discount,
                "Save Rs.": save_rs,
                "Availability Status": add_to_cart,
                "Quantity Caping": count,
                "Remarks": "N/A",
                # "Pack shot/Screenshot": f"{pid}_400013.png",
                # "Quantity of the Product": product["Quantity of the Product"],
                # "Packaging of the product": product["Packaging of the product"],
            }

            data_list.append(item)

            print(data_list)

        df = pd.DataFrame(data_list)
        df.fillna("N/A", inplace=True)
        df.to_excel(f"Dmart_data_{crawl_date}.xlsx", index=False)
        await browser.close()


# Run the scraper
asyncio.run(scrape_dmart())
