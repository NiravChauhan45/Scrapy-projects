import datetime
import gzip
import hashlib
import json
import os
import re
import requests
import scrapy
from parsel import Selector
from scrapy import cmdline
from big_basket_com.items import BigBasketComItem
import big_basket_com.db_config as db
from big_basket_com.config.database_config import ConfigDatabase


def pagesave_data(pagesave_id, response):
    # Todo: page save
    try:
        pagesave = f"E:\\Nirav\\Project_page_save\\big_basket_com\\{db.delivery_date}\\"
        os.makedirs(pagesave, exist_ok=True)
        main_path = f'{pagesave}{pagesave_id}.html.gz'
        if not os.path.exists(main_path):
            with gzip.open(main_path, "wb") as f:
                f.write(response.text.encode('utf-8'))
            print(f"page save for this {pagesave_id}")
    except Exception as e:
        print(e)


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"

    # allowed_domains = ["www.bigbasket.com"]

    def start_requests(self):
        db1 = ConfigDatabase(database=f"{db.database_name}", table=f'pincodes')
        results = db1.fetchResultsfromSql(conditions={'status': 'Pending'})

        for result in results:
            city_name = result.get('city')
            pincode = result.get('pincode')


            cookies = result.get('cookies')
            headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'common-client-static-version': '101',
                'content-type': 'application/json',
                'origin': 'https://www.bigbasket.com',
                'priority': 'u=1, i',
                'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-channel': 'BB-WEB',
                'x-csurftoken': 'ZFkgNg.Nzc3NjM3OTIyMDYzMzQzMzQy.1750418032109./xZe9Uv8LCpGHyc2g2ySzDXut74y8hwQWe1mzl52t6A=',
                'x-entry-context': 'bbnow',
                'x-entry-context-id': '10',
                'x-tracker': '7076a676-5048-476c-92b2-2f918222a8bc',
                # 'cookie': '_bb_locSrc=default; x-channel=web; _bb_vid=Nzc3NjM3OTIyMDYzMzQzMzQy; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=0O2rJeYy3VMjqFN9DKWTXC3wFw1Z1bJcBIKGYFnQ4dWF5nrZgsdf62S1pdvPjnrr; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; _is_bb1.0_supported=0; is_integrated_sa=1; bb2_enabled=true; _is_tobacco_enabled=1; csurftoken=ZFkgNg.Nzc3NjM3OTIyMDYzMzQzMzQy.1750418032109./xZe9Uv8LCpGHyc2g2ySzDXut74y8hwQWe1mzl52t6A=; ufi=1; bigbasket.com=3db64f09-fc27-4612-8d37-7d83c4639c77; _gcl_au=1.1.1010237511.1750417995; jarvis-id=26af49f3-7f99-496a-ae2c-7795c8419b86; adb=0; _gid=GA1.2.1819353206.1750417995; _fbp=fb.1.1750417995145.91391976770167600; is_global=0; _bb_lat_long="MjMuMDcyMDE4NHw3Mi41NDIxMzM5OTk5OTk5OQ=="; _bb_cid=15; _bb_aid="Mjk3NDE3MjYzNw=="; _bb_addressinfo=MjMuMDcyMDE4NHw3Mi41NDIxMzM5OTk5OTk5OXxHaGF0bG9kaXlhfDM4MDA2MXxBaG1lZGFiYWR8MXxmYWxzZXx0cnVlfHRydWV8QmlnYmFza2V0ZWVy; _bb_pin_code=380061; _bb_sa_ids=10123; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjEwMTIz; ts=2025-06-20%2016:55:07.437; _ga_FRRYG5VKHX=GS2.1.s1750417995$o1$g1$t1750418668$j7$l0$h0; _ga=GA1.2.944164019.1750417995',
            }
            # url = 'https://www.bigbasket.com/pd/40329221'
            url = 'https://www.bigbasket.com/pd/40197770'
            yield scrapy.Request(url=url, cookies=json.loads(cookies),
                                 headers=headers,
                                 meta={"city_name": city_name, "pincode": pincode,
                                       "product_url": url,
                                       "headers": headers, "cookies": cookies}, dont_filter=True,
                                 callback=self.parse)

    def parse(self, response, **kwargs):
        new_cookies = response.meta.get("cookies")
        headers = response.meta.get("headers")

        item = BigBasketComItem()

        json_data = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()

        json_data = json.loads(json_data)

        platform = "Big Basket"
        scrape_time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        pincode = response.meta.get('pincode')
        product_url = response.meta.get('product_url')

        # Todo: product_id
        product_id = ''
        try:
            product_id = product_url.split("/pd/")[-1].split("/")[0] if product_url else "N/A"
        except Exception as e:
            print("product id error: ", e)

        # Todo: product_name
        product_name = ''
        try:
            product_name = response.xpath("//h1[@class='Description___StyledH-sc-82a36a-2 bofYPK']/text()").get()
        except Exception as e:
            print("Product Name error: ", e)

        # Todo : Brand
        brand = ''
        try:
            brand = response.xpath("//a[@class='Description___StyledLink-sc-82a36a-1 gePjxR']/text()").get()
        except Exception as e:
            print("Brand error: ", e)

        # Todo : Product Description
        product_description = ''
        try:
            product_des_list = json_data.get('props').get('pageProps').get('productDetails').get('children')[0].get(
                'tabs')
            for des in product_des_list:
                if 'About the Product' in des.get('title'):
                    if des.get("content"):
                        selector = Selector(text=des.get("content"))
                        product_description = selector.xpath("//p/text() | //div/text() | //div//p/text()").getall()
                        product_description = " ".join(product_description)
                        product_description = re.sub("\\s+", " ", product_description).strip()
                        break
        except Exception as e:
            print("Product Description Cat't Get Successfully : ", e)

        # Todo : MRP
        mrp = ''
        try:
            mrp = response.xpath("//td[contains(text(),'MRP: ')]/following-sibling::td/text()").get()
            if mrp:
                mrp = mrp.replace("₹", "")
                mrp = int(mrp)
        except Exception as e:
            print("MRP Error: ", e)

        # Todo : Price
        price = ''
        try:
            price = response.xpath("//td[contains(text(),'Price: ')]/text()").getall()
            if price:
                price_text = "".join(price)  #
                match = re.search(r'\d+(?:\.\d+)?', price_text)
                if match:
                    price = float(match.group())
        except Exception as e:
            print("MRP Error: ", e)

        if not mrp:
            mrp = price

        if not price:
            price = mrp

        # Todo: Discount
        try:
            discount_text = response.xpath(
                "//td[contains(text(),'You Save:')]/following-sibling::td[contains(text(),'OFF')]/text()").get()
            try:
                digits = re.findall(r'\d+', discount_text)
                discount = "".join(digits)
            except:
                discount = int(((mrp - price) / mrp) * 100)
                if discount == 0 or discount == '0':
                    discount = "N/A"
        except:
            discount = "N/A"

        # Todo: Availability
        availability = ''
        try:
            availability_text = response.xpath("//span[contains(text(),'Out of Stock')]/text()").get()
            currently_unavailable = response.xpath("//span[contains(text(),'Currently Unavailable')]/text()").get()
            if availability_text == "Out of Stock":
                availability = "Out of Stock"
            elif currently_unavailable == "Currently Unavailable":
                availability = "Currently Unavailable"
            else:
                availability = "In Stock"
        except Exception as e:
            print("availability: ", e)

        # Todo: No. of Quantity Available
        if availability == "In Stock":
            no_of_quantity_available = ''
            try:
                json_data = {
                    'prod_id': product_id,
                    # 'qty': 1000,
                    '_bb_client_type': 'web',
                    # 'first_atb': 1
                }
                # for i in range(30):
                # with requests.Session() as session:
                #     session.cookies.update(json.loads(new_cookies))
                response1 = requests.post('https://www.bigbasket.com/mapi/v3.5.2/c-incr-i/',
                                          headers=headers, cookies=json.loads(new_cookies),
                                          json=json_data)
                if response1.json()['status'] != 'OK':
                    no_of_quantity_available = response1.json()['allowed']
                    # break
            except Exception as e:
                print("No. of Quantity Available: ", e)
        else:
            no_of_quantity_available = "N/A"
            mrp = "N/A"
            price = "N/A"
            discount = "N/A"

        item['Platform'] = platform
        item['Scrape Time'] = scrape_time
        item['Date'] = date
        item['Pincode'] = pincode
        item['Product Url'] = product_url
        item['Product ID'] = product_id
        item['Product Name'] = product_name
        item['Brand'] = brand
        item['Product Description'] = product_description
        item['MRP'] = mrp if mrp else "N/A"
        item['Price'] = price if price else "N/A"
        item['Discount'] = discount if discount else "N/A"
        item['Availability'] = availability
        item['No.of Quantity Available'] = no_of_quantity_available
        item['hash_key'] = str(
            int(hashlib.md5(bytes(
                str(item['Pincode'] + item['Product ID'] + item['Brand']), "utf8")).hexdigest(),
                16) % (
                    10 ** 10))

        # Todo: Pagesave
        pagesave_data(item['hash_key'], response)
        yield item


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpDataSpider.name}".split())
