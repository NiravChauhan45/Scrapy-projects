import gzip
import json
import os.path
from datetime import datetime
from typing import Iterable

import scrapy
from scrapy import Request, cmdline, Selector
from kohinoor_electronics.items import product_data_item
from kohinoor_electronics.config.database_config import ConfigDatabase


class ProductDataSpider(scrapy.Spider):
    name = "product_data"
    allowed_domains = ["www.kohinoorelectronics.com"]

    # other name column
    def other_column_json_generator(self, response_data):
        response = Selector(text=response_data)
        moq = '1'

        # price
        try:
            price = response.xpath("//li[@class='joy-price-value']/text()").get().strip()
        except:
            price = 'N/A'

        # brand
        try:
            # brand = response.xpath("//nav[@aria-label='breadcrumb']//li[position()>1]/a/text()").getall()[-1].strip()
            brand = response.xpath(
                "//p[@class='text-gray-5 product-specification add-Read-More showlesscontent']/text()").get().strip()
        except:
            brand = 'N/A'

        # images
        try:
            images = response.xpath("//div[@class='slide-img-thumb']/img/@src").getall()
        except:
            images = 'N/A'

        # product_code
        try:
            product_code = response.xpath("//p[@class='m-0']/text()").get().strip()
        except:
            product_code = 'N/A'

        delivery = "Kohinoor_logout"

        # key_features
        try:
            key_features = response.xpath(
                "//ul[@class='font-size-14 pl-3 ml-1 text-gray-110 addReadMore']/li/span/text()").getall()
        except:
            key_features = 'N/A'

        data_vendor = "Actowiz"

        # emi_options
        try:
            emi_data_name_lt = response.xpath("//div[@class='card mb-0']//div[contains(@class,'card-header')]")
            emi_data_lst = response.xpath("//div[@class='card mb-0']//div[contains(@class,'card-body')]//table")
            final_emi_data_dict = {}
            for bank_name_dt, emi_dt in zip(emi_data_name_lt, emi_data_lst):
                bank_name = bank_name_dt.xpath(".//a[contains(@class,'card-title')]/text()").get().split("CREDIT CARD")[
                    0].replace('DEBIT CARD',
                               '').strip()
                emi_lst = []
                for per_emi_dt in emi_dt.xpath(".//tr[position()>1]"):
                    emi_dict = {}
                    montly_emi_plan = per_emi_dt.xpath('./td[1]/text()').get().strip().split()[0]
                    # total_cost = per_emi_dt.xpath('./td[3]/text()').get().replace('₹', '').replace(',', '').split('.')[
                    #     0].strip()
                    # interest_amount = int(total_cost) - int(price)
                    interest = per_emi_dt.xpath('./td[2]/text()').get().split('(')[
                        -1].replace(')', '').replace('%', '').strip()

                    total_cost = per_emi_dt.xpath('./td[3]/text()').get().replace('₹', '').replace(',', '').replace(
                        '/-', '').strip()
                    emi_dict['interest'] = float(interest)
                    emi_dict['total_cost'] = total_cost
                    emi_dict['montly_emi_plan'] = montly_emi_plan
                    emi_lst.append(emi_dict)
                final_emi_data_dict[bank_name] = emi_lst
        except:
            final_emi_data_dict = 'N/A'

        # additional_info
        try:
            additional_info = response.xpath("//div[@class='icon-content']/a/text()").getall()
        except:
            additional_info = 'N/A'

        # isEmiApplicable
        try:
            isEmiApplicable = "true" if response.xpath(
                "//span[@class='kohi-promotion-action-button']/text()") else "false"
        except:
            isEmiApplicable = 'N/A'

        # product_description
        try:
            product_description_lst = response.xpath(
                "//div[@id='Jpills-two-example1']/p/text() | //div[@id='Jpills-two-example1']/p/strong/text() | //div[contains(@id,'Jpills-two-example1')]//span[@class='a-list-item']/text()").getall()
            product_description = " ".join(
                [product_description.strip().replace('")', '`)') for product_description in product_description_lst])
        except:
            product_description = 'N/A'

        # Maximum_Retail_Price
        try:
            Maximum_Retail_Price = response.xpath(
                "//ul[@class='mrp-price']/li[@class='dash-line']/text()").get().strip()
        except:
            Maximum_Retail_Price = 'N/A'

        # SKU
        try:
            SKU = response.xpath("//span[@class='sku']/text()").get().strip()
        except:
            SKU = 'N/A'

        # product specification
        try:
            product_specification_lst = response.xpath("//div[@class='mx-md-3 pt-1 product-specification-tab']")
            final_specification_dict = {}
            for product_data in product_specification_lst:
                features = product_data.xpath("./h3/text()").get().strip()
                if "Manufacturer Details" in features:
                    continue
                inner_specification_dict = {}
                for product_detail in product_data.xpath(".//div[@class='col-6 col-md-4']"):
                    product_attribute_name = product_detail.xpath("./h4/text()").get().strip()
                    product_attribute_value = product_detail.xpath("./p/text()").get().strip()
                    inner_specification_dict[product_attribute_name] = product_attribute_value
                final_specification_dict[features] = inner_specification_dict
        except:
            final_specification_dict = 'N/A'

        # manufacturer_details
        try:
            product_specification_lst = response.xpath("//div[@class='mx-md-3 pt-1 product-specification-tab']")
            manufacturer_details_dict = {}
            for product_data in product_specification_lst:
                features = product_data.xpath("./h3/text()").get().strip()
                if "Manufacturer Details" in features:
                    for product_detail in product_data.xpath(".//div[@class='col-6 col-md-4']"):
                        product_attribute_name = product_detail.xpath("./h4/text()").get().strip()
                        product_attribute_value = product_detail.xpath("./p/text()").get().strip()
                        manufacturer_details_dict[product_attribute_name] = product_attribute_value
        except:
            manufacturer_details_dict = 'N/A'

        # Exchange_Offer
        try:
            Exchange_Offer = response.xpath(
                "//span[contains(text(),'Exchange Offer:')]/following-sibling::span[@class='description']/text()").get().lstrip().rstrip()
            if Exchange_Offer:
                Exchange_Offer = Exchange_Offer
            else:
                Exchange_Offer = 'N/A'
        except:
            Exchange_Offer = 'N/A'

        # GST_Invoice
        try:
            GST_Invoice = response.xpath(
                "//span[contains(text(),'GST Invoice:')]/following-sibling::span[@class='description']/text()").get().strip()
            if GST_Invoice:
                GST_Invoice = GST_Invoice
            else:
                GST_Invoice = 'N/A'
        except:
            GST_Invoice = 'N/A'

        # Todo: Making others column dict
        other_final_dict = {'MOQ': moq,
                            'Price': price,
                            'brand': brand,
                            'images': images,
                            'product_code': product_code,
                            'delivery': delivery,
                            'keyFeatures': key_features,
                            'data_vendor': data_vendor,
                            'emi_options': final_emi_data_dict,
                            'additional_info': additional_info,
                            'isEmiApplicable': isEmiApplicable,
                            'description': product_description,
                            'Maximum Retail Price': Maximum_Retail_Price,
                            'SKU': SKU,
                            'product_specification': final_specification_dict,
                            'manufacturer_details': manufacturer_details_dict,
                            'Exchange_Offer': Exchange_Offer,
                            'GST_Invoice': GST_Invoice
                            }
        return other_final_dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.today_date = datetime.now().strftime("%d_%m_%Y")
        self.product_data_pagesave_path = f'F:\\Nirav\\Project_page_save\\kohinoor_electronics\\page_save_product_page\\{self.today_date}\\'
        self.db = ConfigDatabase(database="kohinoor_electronics", table="extract_product_urls")

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'})
        for result in results:
            product_id = result['product_id']
            product_url = result['product_url']
            # access_path = f'{self.product_data_pagesave_path}{str(product_id)}.html.gz'
            access_path = f'{self.product_data_pagesave_path}{str(product_id)}.html'
            if os.path.exists(access_path):
                yield scrapy.Request(url=f'file:///{access_path}',
                                     dont_filter=True,
                                     callback=self.parse,
                                     meta={
                                         'product_url': product_url, 'product_id': product_id
                                     })
            else:
                cookies = {
                    '_ga': 'GA1.1.1660656804.1729616472',
                    '_gcl_au': '1.1.162818000.1729673784',
                    'token': '2V0OQX2D4M9CEC5VVPIZESTFI8YBU7CPMF4TEH50NFP1VTDPVD4LEYSS1GSY',
                    'csrftoken': 'hoyV02Gg6Su77FbvDORIGE7Q0N75yBqQ78EJ1ZO6LrCB4R7MCEXNbf0oQ7ZAf1R0',
                    '_fbp': 'fb.1.1729673788701.623873045734384720',
                    'website_user_form': 'true',
                    'sessionid': 'moc5k1z1bl91pwfwkzcii0v49g5d6aac',
                    'counter': '4',
                    '_clck': '1y1xw8q%7C2%7Cfqa%7C0%7C1757',
                    '_ga_B63L29Q67Z': 'GS1.1.1729746816.7.1.1729753116.0.0.0',
                    '_ga_YCWYEKBRMQ': 'GS1.1.1729746816.7.1.1729753116.3.0.0',
                    '_clsk': '1vi3c69%7C1729753117651%7C47%7C1%7Cx.clarity.ms%2Fcollect',
                }
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    # 'cookie': '_ga=GA1.1.1660656804.1729616472; _gcl_au=1.1.162818000.1729673784; token=2V0OQX2D4M9CEC5VVPIZESTFI8YBU7CPMF4TEH50NFP1VTDPVD4LEYSS1GSY; csrftoken=hoyV02Gg6Su77FbvDORIGE7Q0N75yBqQ78EJ1ZO6LrCB4R7MCEXNbf0oQ7ZAf1R0; _fbp=fb.1.1729673788701.623873045734384720; website_user_form=true; sessionid=moc5k1z1bl91pwfwkzcii0v49g5d6aac; counter=4; _clck=1y1xw8q%7C2%7Cfqa%7C0%7C1757; _ga_B63L29Q67Z=GS1.1.1729746816.7.1.1729753116.0.0.0; _ga_YCWYEKBRMQ=GS1.1.1729746816.7.1.1729753116.3.0.0; _clsk=1vi3c69%7C1729753117651%7C47%7C1%7Cx.clarity.ms%2Fcollect',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                }
                yield scrapy.Request(url=product_url, headers=headers, cookies=cookies, dont_filter=True,
                                     meta={'product_url': product_url, 'product_id': product_id}, callback=self.parse)

    def parse(self, response, **kwargs):
        product_id = response.meta.get('product_id')
        product_url = response.meta.get('product_url')

        # page save
        try:
            if not os.path.exists(self.product_data_pagesave_path):
                os.makedirs(self.product_data_pagesave_path)
            main_path = f'{self.product_data_pagesave_path}{str(product_id)}.html.gz'
            if not os.path.exists(main_path):
                with gzip.open(main_path, 'wb') as f:
                    f.write(response.text.encode('utf-8'))
                print(f"page save for this {product_id}")
        except Exception as e:
            print(e)

        try:
            catalog_name = response.xpath(
                '//h2[@class="font-size-18 font-size-20-lg text-black text-lh-1dot2"]/text()').get().strip()
        except:
            catalog_name = 'N/A'

        catalog_id = product_id
        source = "Kohinoor"
        scraped_date = datetime.now().strftime("%Y-%m-%d %X")
        product_name = catalog_name

        # image_url
        try:
            image_url = response.xpath(
                "//ul[contains(@class,'vertical-thumbnail-slider')]/li/div/img[@class='img-fluid']/@data-thumb").get()
        except:
            image_url = 'N/A'

        # category_hierarchy
        try:
            category_hierarchy_lst = [cat_hierarchy.strip() for cat_hierarchy in
                                      response.xpath(
                                          "//nav[@aria-label='breadcrumb']//li[position()>1]/a/text()").getall()[
                                      :-1]]

            category_hierarchy_l1 = category_hierarchy_lst[0]
            category_hierarchy_l2 = category_hierarchy_lst[1]
            category_hierarchy = {'l1': category_hierarchy_l1, 'l2': category_hierarchy_l2}
        except:
            category_hierarchy = 'N/A'

        try:
            product_price = response.xpath("//li[@class='joy-price-value']/text()").get().strip()
        except:
            product_price = 'N/A'

        # arrival_date
        try:
            arrival_date_str = response.xpath("//div[@class='DeliveryMessage']/b[1]/text()").get().strip()
            arrival_date_year = "2024"
            full_date_str = f"{arrival_date_str} {arrival_date_year}"
            date_obj = datetime.strptime(full_date_str, "%b %d %Y")
            arrival_date = date_obj.strftime("%Y-%m-%d") + " 00:00:00"
        except:
            arrival_date = 'N/A'

        shipping_charges = 'N/A'

        # is_sold_out
        try:
            is_sold_out = response.xpath(
                "//div[@class='text-gray-9 font-size-14  d-inline-block']/span/text()").get().strip()

            if "Out Of Stock" in is_sold_out:
                is_sold_out = "TRUE"
            else:
                is_sold_out = "FALSE"
        except:
            is_sold_out = 'N/A'

        try:
            mrp = response.xpath("//ul[@class='mrp-price']/li[@class='dash-line']/text()").get().strip()
        except:
            mrp = 'N/A'

        # discount
        try:
            discount_amount = int(mrp) - int(product_price)
            discount = int((discount_amount / int(mrp)) * 100)
            if discount == 0:
                discount = 'N/A'
            else:
                discount = discount
            # print(discount)
            # discount = response.xpath("//ul[@class='dis-price']/li[@class='dis-price-value ']/text()").get().split()[
            #     -1].replace('(', '').replace(')', '').replace('%', '')
        except:
            discount = 'N/A'

        page_url = 'N/A'
        number_of_rating = 'N/A'
        avg_rating = 'N/A'
        position = 'N/A'
        country_code = 'IN'
        others = self.other_column_json_generator(response_data=response.text)

        item = product_data_item()
        item['product_id'] = product_id
        item['catalog_name'] = catalog_name
        item['catalog_id'] = catalog_id
        item['source'] = source
        item['scraped_date'] = scraped_date
        item['product_name'] = product_name
        item['image_url'] = image_url
        item['category_hierarchy'] = json.dumps(category_hierarchy)
        item['product_price'] = product_price
        item['arrival_date'] = arrival_date
        item['shipping_charges'] = shipping_charges
        item['is_sold_out'] = is_sold_out
        item['discount'] = discount
        item['mrp'] = mrp
        item['page_url'] = page_url
        item['product_url'] = product_url
        item['number_of_ratings'] = number_of_rating
        item['avg_rating'] = avg_rating
        item['position'] = position
        item['country_code'] = country_code
        item['others'] = json.dumps(others)
        item['page_save_id'] = product_id
        yield item

        # # TODO - Done-Pending....
        try:
            self.db.crsrSql.execute(
                f"update {self.db.table} set status='Done' where product_id = '{product_id}'")
            self.db.connSql.commit()
            print(f"Status for :{product_id} Updated=Done")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl product_data".split())
