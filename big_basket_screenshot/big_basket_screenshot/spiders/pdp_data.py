import datetime
import hashlib
import os
import re
import scrapy
from loguru import logger
from scrapy import cmdline
from big_basket_screenshot.config.database_config import ConfigDatabase
import big_basket_screenshot.db_config as db
from big_basket_screenshot.items import BigBasketScreenshotItem


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"
    allowed_domains = ["www.bigbasket.com"]
    start_urls = ["https://www.bigbasket.com"]

    def __init__(self, start_index, end, **kwargs):
        super().__init__(**kwargs)
        self.start_index = start_index
        self.end = end
        self.db = ConfigDatabase(database=f"{db.database_name}", table=f'{db.pdp_link_table}')

    def start_requests(self):
        # results = self.db.fetchResultsfromSql(conditions={'status': 'Done'}, start=self.start_index, end=self.end)
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'}, start=self.start_index, end=self.end)
        for result in results:
            id = result['id']
            new_category = result['Category']
            name_of_the_brand = result['Name_Of_the_Brand']
            name_of_the_product = result['Name_of_the_Product']
            single_pack = result['Single_Pack']
            bundle_pack = result['Bundle_Pack']
            quantity_of_the_product = result['Quantity_of_the_Product']
            product_url = result['big_basket']
            quantity = result['Quantity']
            packing_of_the_product = result['Packaging_of_the_product']
            new_zipcode = result['zipcode']
            city_name = result['City_Name']
            quantity_caping = result['quantity_caping']
            big_basket_approve_not_approve = result['big_basket_approve_not_approve']

            meta = {'id': id, 'new_category': new_category, 'name_of_the_brand': name_of_the_brand,
                    'name_of_the_product': name_of_the_product, 'single_pack': single_pack, 'bundle_pack': bundle_pack,
                    'quantity_of_the_product': quantity_of_the_product, 'product_url': product_url,
                    'quantity': quantity, 'packing_of_the_product': packing_of_the_product, 'new_zipcode': new_zipcode,
                    'city_name': city_name, 'quantity_caping': quantity_caping,
                    'big_basket_approve_not_approve': big_basket_approve_not_approve}

            # pagesave_path = fr"{db.pagesave_filepath}\{id}.html"
            yield scrapy.Request(
                url=f"file:///D:/Nirav Chauhan/pagesave/Big_Basket_Screenshot/{db.current_date}/{id}.html", meta=meta,
                callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        new_id = response.meta.get('id')
        new_category = response.meta.get('new_category')
        name_of_the_brand = response.meta.get('name_of_the_brand')
        name_of_the_product = response.meta.get('name_of_the_product')
        single_pack = response.meta.get('single_pack')
        bundle_pack = response.meta.get('bundle_pack')
        quantity_of_the_product = response.meta.get('quantity_of_the_product')
        product_url = response.meta.get('product_url')
        quantity = response.meta.get('quantity')
        packing_of_the_product = response.meta.get('packing_of_the_product')
        new_zipcode = response.meta.get('new_zipcode')
        city_name = response.meta.get('city_name')
        quantity_caping = response.meta.get('quantity_caping')
        big_basket_approve_not_approve = response.meta.get('big_basket_approve_not_approve')

        pack_shot_name = ''
        per_gm = ''
        mrp = ''
        stock_avaibility = ''
        selling_price = ''
        discount = ''
        save_rs = ''
        count = 0
        pack_shot_name = ''
        on_site_sku_name = ''
        if not product_url:
            try:
                pack_shot_name = f"{new_id}_{new_zipcode}_{db.current_date}"
                pack_shot_name = f"{pack_shot_name}.png"
            except:
                pack_shot_name = 'N/A'

            try:
                if pack_shot_name != 'N/A':
                    path = fr"{db.screenshot_filepath}\{pack_shot_name}"
            except Exception as e:
                print(e)
        else:
            try:
                pid = product_url.split('/pd/')[-1].split('/')[0].strip()
                if pid:
                    if '?' in pid:
                        pid = pid.split('?')[0].strip()
                else:
                    pid = 'N/A'
            except Exception as error:
                logger.error(error)

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
                    response.xpath('//td[contains(text(),"MRP:")]/following-sibling::td/text()').getall())
                if mrp:
                    mrp = "".join(mrp).replace('₹', '').strip()
                else:
                    mrp = "N/A"
            except:
                mrp = "N/A"

                # Todo: price
            try:
                price = "".join(
                    response.xpath(
                        "//td[@class='Description___StyledTd-sc-82a36a-4 fLZywG']//text()").getall()).strip()
                price = price.replace('₹', '').strip()
            except:
                price = "N/A"

                # Todo: selling_price
            try:
                if price:
                    selling_price = price.split(':')[-1].strip()
                else:
                    selling_price = mrp
            except:
                selling_price = mrp

            # Todo: assign selling_price if mrp is not an available
            if selling_price != "N/A" and mrp == "N/A":
                mrp = selling_price

                # Todo: discount and save_rs

            try:
                discount_text = response.xpath(
                    "//td[contains(text(),'You Save:')]/following-sibling::td[contains(text(),'OFF')]/text()").get()
                if discount_text:
                    if "%" in discount_text:
                        digits = re.findall(r'\d+', discount_text)
                        discount = "".join(digits)
                else:
                    discount = 'N/A'
            except:
                discount = "N/A"

                # Todo: save_rs
            try:
                if not save_rs:
                    # save_rs = int(float(mrp) - float(selling_price))
                    save_rs = round(float(mrp) - float(selling_price))
                    if int(save_rs) == 0:
                        save_rs = '0'
            except:
                save_rs = "N/A"

                # Todo: add_to_cart
            try:
                if response.xpath('(//button[contains(text(),"Add to basket")])[1]') or "InStock" in response.text:
                    add_to_cart = "In Stock"
                else:
                    add_to_cart = "Out of Stock"
            except:
                add_to_cart = 'Not listed'

            # Todo: Update quantity_caping value if add_to_cart "Out of stock" or "Not listed"
            if add_to_cart == "Out of Stock" or add_to_cart == "Not listed":
                quantity_caping = "N/A"

                # Todo: per_gm
            try:
                per_gm = "".join(
                    response.xpath('//td[contains(text(),"Price")]/following-sibling::td/text()').getall())
                per_gm = per_gm.replace('(', '').replace(')', '').replace('₹', '').replace(' / ', '/')
            except:
                per_gm = "N/A"

            try:
                on_site_sku_name = response.xpath(
                    '//h1[@class="Description___StyledH-sc-82a36a-2 bofYPK"]/text()').get('').strip()
            except:
                on_site_sku_name = 'N/A'

            try:
                quantity_caping = response.xpath(
                    "//div[@class='PdCartCTA___StyledDiv2-sc-mq73zq-2 cdHBKF']/text()").get()
            except Exception as e:
                print(e)
        hash_id = str(int(hashlib.md5(bytes(str(str(
            new_id) + city_name + product_url + name_of_the_brand + new_category + new_zipcode + name_of_the_product + quantity_of_the_product),
                                            "utf8")).hexdigest(), 16) % (10 ** 10))

        item = BigBasketScreenshotItem()
        item["Sr.No"] = new_id
        item["Portal Name"] = "BigBasket"
        item["Product Url"] = product_url if product_url else 'N/A'
        item["Date (Crawler Date)"] = datetime.datetime.now().strftime("%d-%m-%Y")
        item["Time (Crawler Time)"] = datetime.datetime.now().strftime("%H:%M")
        item["City Name"] = city_name
        item["Pincode"] = new_zipcode
        item["Brand"] = name_of_the_brand if name_of_the_brand else 'N/A'
        item["Category"] = new_category if new_category else 'N/A'
        item["SKU Packshot"] = pack_shot_name
        item["SKU Name"] = name_of_the_product if name_of_the_product else 'N/A'
        item["Pack Size"] = quantity_of_the_product if quantity_of_the_product else 'N/A'
        item["Single Pack"] = single_pack if single_pack else 'N/A'
        item["Bundle Pack"] = bundle_pack if bundle_pack else 'N/A'
        item["Per Gm Price (Unit Price)"] = per_gm if per_gm else 'N/A'
        item["MRP"] = mrp if mrp else 'N/A'
        item["Selling price"] = selling_price if selling_price else 'N/A'
        item["Discount (%)"] = discount if discount else 'N/A'
        item["Save Rs."] = save_rs if save_rs else "N/A"
        item["On-site SKU Name"] = on_site_sku_name
        item["Availability Status"] = add_to_cart if product_url else 'Not listed'
        item["Quantity Caping"] = quantity_caping if quantity_caping else 'N/A'
        item["Remarks"] = "N/A"
        item["Quantity"] = quantity if quantity else 'N/A'
        item["Packaging of the product"] = packing_of_the_product if packing_of_the_product else 'N/A'
        item["big_basket_approve_not_approve"] = big_basket_approve_not_approve
        item["hash_id"] = hash_id
        yield item


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpDataSpider.name} -a start_index=1 -a end=16000".split())
