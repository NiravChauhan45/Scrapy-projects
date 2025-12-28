import gzip
import json
import os
from datetime import datetime
import random

import scrapy
from scrapy import cmdline
import mysql.connector
from amazon_new.config.database_config import ConfigDatabase
from amazon_new.items import AmazonPdpItem


class PdpProductDataSpider(scrapy.Spider):
    name = "pdp_product_data"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.today_date = datetime.now().strftime("%d_%m_%Y")
        self.product_data_pagesave_path = f'F:\\Nirav\\Project_page_save\\amazon_new\\pdp_page_save_path\\'
        self.db = ConfigDatabase(database="amazon_new", table="pl_page_data")
        # self.conn = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="actowiz",
        #     database="kohinoor_electronics"
        # )
        # self.cur = self.conn.cursor()

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'})
        for result in results:
            product_name = result['product_name']
            product_url = result['product_url']
            sponsored = result['sponsored']
            badge = result['badge']
            page_rank = result['page_rank']
            srp_no = result['srp_no']
            price = result['Price']
            price_per_unit = result['Price_per_unit']
            hash_key = result['hash_key']

            access_path = f'{self.product_data_pagesave_path}{str(hash_key)}.html'
            if os.path.exists(access_path):
                yield scrapy.Request(url=f'file:///{access_path}',
                                     dont_filter=True,
                                     callback=self.parse,
                                     meta={
                                         'product_name': product_name, 'product_url': product_url,
                                         'sponsored': sponsored, 'badge': badge,
                                         'page_rank': page_rank, 'srp_no': srp_no, 'price': price,
                                         'price_per_unit': price_per_unit, 'hash_key': hash_key,
                                         "impersonate": self.browser
                                     })
            else:
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'accept-language': 'en-US,en;q=0.6',
                    'cache-control': 'max-age=0',
                    'cookie': 'session-id=138-0636516-5591551; session-id-time=2082787201l; i18n-prefs=USD; skin=noskin; ubid-main=132-3724160-6986134; session-token=y3rGkjrZzQk7FS5CfXRUuewEsYr7CgclrLALQLpzBWo4iSLBggD+DhjVg//TQQoL5pn/4rLuYuE4hVbp0E0/UOg2U3FRWZ2kvMeRt8YWAFDtdVk+LTRXkA2HDvaVoiLH4yPugwLDWauHd7YjSmEyTkc7ZBx1FwL34jlxph5O8gFuObQcaMQIrua8wRu05iE+n2I50S7Wjyz8j69Z1vCvAABfUK7o9++zzJ/tiJZMPXECAt5KruXUdIMoDXjDJE7N6oxNmZ60oM7A9cus74QUtm8CG4oqYLO4Yx/aYcBISxwwE/uaKcGEn2rpgjDomekwK4Uu8gmdleagyXsxuajj9X7IR2LkqI60; csm-hit=adb:adblk_yes&t:1730259772365&tb:ZPTTHZW50XDKRTZWT66W+sa-ZZ4KDK70X5E2EP0BD012-MEFHWZ49NV1PMMSNJX91|1730259772365; i18n-prefs=USD; session-id=138-0636516-5591551; session-id-time=2082787201l; session-token=zvqcQ4no0va/CqiIjtZoMveXfx1j9GVO3P/VumeQsAKyLLTGpxTb9sCHQ3F+2gg4oL/I1i1oLQqw+EPqWqOXOZ8fpV+mJyz4tVKanJl2nSQKV16MpD/GXweiqE5Jri/jprAlSbdxYt9jC8td0204sG2+pW+ms5jo12nrovpiRI3eWVVAJzgJvYBkouMN3/8eRvRZdGaRviipPKCLDRVEU2B00V24XPCJdKM9e6wryhq/fJ5pEyf8/KtGGwKVAGKv2m78lfxmjtEwGXHgoyccjPgBGcs+pqSUkF6hUlX90SZtG0WJEHMkRheo05VdfdMRraV+AKNjTAHIAQHmo4slOCqU2Q2X3Ytz; ubid-main=131-2316807-8739625',
                    'priority': 'u=0, i',
                    'referer': 'https://www.amazon.com/',
                    'sec-ch-ua': '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-ch-ua-platform-version': '"10.0.0"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'sec-gpc': '1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
                }
                yield scrapy.Request(url=product_url, headers=headers, dont_filter=True,
                                     meta={
                                         'product_name': product_name, 'product_url': product_url,
                                         'sponsored': sponsored, 'badge': badge,
                                         'page_rank': page_rank, 'srp_no': srp_no, 'hash_key': hash_key, 'price': price,
                                         'price_per_unit': price_per_unit,
                                         "impersonate": self.browser
                                     }, callback=self.parse)

    def parse(self, response, **kwargs):
        product_name = response.meta.get('product_name')
        product_url = response.meta.get('product_url')
        price = response.meta.get('price')
        price_per_unit = response.meta.get('price_per_unit')
        sponsored = response.meta.get('sponsored')
        badge = response.meta.get('badge')
        srp_no = response.meta.get('srp_no')
        page_rank = response.meta.get('page_rank')
        hash_key = response.meta.get('hash_key')

        # primary_image
        try:
            primary_image = response.xpath("//div[@class='imgTagWrapper']/img/@src").get()
        except:
            primary_image = 'N/A'

        # product_title
        try:
            product_title = response.xpath("//span[@id='productTitle']/text()").get().strip()
        except:
            product_title = 'N/A'

        # star_rating
        try:
            star_ratings = response.xpath(
                "//span[@id='acrPopover']//span[@class='a-size-base a-color-base']/text()").get().strip()
        except:
            star_ratings = 'N/A'

        # no_of_reviews
        try:
            no_of_reviews = response.xpath("//span[@id='acrCustomerReviewText']/text()").get().split()[0].replace(',',
                                                                                                                  '')
        except:
            no_of_reviews = 'N/A'

        # brand_name
        try:
            brand_name = response.xpath(
                "//tr[@class='a-spacing-small po-brand']//span[@class='a-size-base po-break-word']/text()").get()
        except:
            brand_name = 'N/A'

        # secondary_image
        try:
            secondary_image = [img_data.strip() for img_data in
                               response.xpath("//div[@id='altImages']//span[@class='a-button-text']/img/@src").getall()
                               if ".gif" not in img_data]
        except:
            secondary_image = 'N/A'

        # videos
        try:
            videos = response.xpath("//a[@class='a-link-normal vse-carousel-item']/@href").getall()
            if videos:
                videos = videos
            else:
                videos = 'N/A'
        except:
            videos = 'N/A'

        # active_ingredients
        try:
            active_ingredients = response.xpath(
                "//tr[@class='a-spacing-small po-active_ingredients']/td[@class='a-span9']/span/text()").get().strip()
            if active_ingredients:
                active_ingredients = active_ingredients
            else:
                active_ingredients = 'N/A'
        except:
            active_ingredients = 'N/A'

        # product_benefits
        try:
            product_benefits = response.xpath(
                "//tr[@class='a-spacing-small po-product_benefit']/td[@class='a-span9']/span/text()").get().strip()
            if product_benefits:
                product_benefits = product_benefits
            else:
                product_benefits = 'N/A'
        except:
            product_benefits = 'N/A'

        # item_form
        try:
            item_form = response.xpath(
                "//tr[@class='a-spacing-small po-item_form']/td[@class='a-span9']/span/text()").get().strip()
        except:
            item_form = 'N/A'

        # flavor
        try:
            flavor = response.xpath(
                "//tr[@class='a-spacing-small po-flavor']/td[@class='a-span9']/span/text()").get().strip()
        except:
            flavor = 'N/A'

        # age_range
        try:
            age_range = response.xpath(
                "//tr[@class='a-spacing-small po-age_range_description']/td[@class='a-span9']/span/text()").get().strip()
        except:
            age_range = 'N/A'

        # material_type_free
        try:
            material_type_free = response.xpath(
                "//tr[@class='a-spacing-small po-material_type_free']/td[@class='a-span9']/span/text()").get().strip()
        except:
            material_type_free = 'N/A'

        # no_of_items
        try:
            no_of_items = response.xpath(
                "//tr[@class='a-spacing-small po-number_of_items']/td[@class='a-span9']/span/text()").get().strip()
        except:
            no_of_items = 'N/A'

        # included_components
        try:
            included_components = response.xpath(
                "//tr[@class='a-spacing-small po-included_components']/td[@class='a-span9']/span/text()").get().strip()
        except:
            included_components = 'N/A'

        # about_this_item
        try:
            about_this_item = [about_this_data.replace('  ', '').strip() for about_this_data in
                               response.xpath("//li[@class='a-spacing-mini']/span/text()").getall()]
            if about_this_item:
                about_this_item = about_this_item
            else:
                about_this_item = 'N/A'
        except:
            about_this_item = 'N/A'

        # manufacturer
        try:
            manufacturer = response.xpath(
                "//span[contains(text(),'Manufacturer')]/following-sibling::span/text()").get()
        except:
            manufacturer = 'N/A'

        # product_detail
        try:
            product_detail = {}
            product_detail_lst = response.xpath(
                "//div[@id='detailBullets_feature_div']//span[@class='a-list-item']")
            for product_detail_data in product_detail_lst:
                product_detail_key = \
                    product_detail_data.xpath("./span[@class='a-text-bold']/text()").get().split('  ')[0].strip()
                product_des_value = product_detail_data.xpath(
                    "./span[@class='a-text-bold']/following-sibling::span/text()").get().replace('  ', '')
                product_detail[product_detail_key] = product_des_value
        except:
            product_detail = 'N/A'

        # important_information
        try:
            important_information = {}
            important_information_lst = response.xpath(
                "//div[@id='important-information']/div[@class='a-section content']")
            for imp_info in important_information_lst:
                imp_info_key = imp_info.xpath("./h4/text()").get().strip()
                imp_info_value = imp_info.xpath("./p/text()").get().strip()
                important_information[imp_info_key] = imp_info_value
        except:
            important_information = 'N/A'

        # safety_information
        try:
            safety_information = response.xpath(
                "//div[@id='important-information']/div[@class='a-section content']/h4[contains(text(),'Safety Information')]/following-sibling::p/text()").get().strip()
        except:
            safety_information = 'N/A'

        # ingredients
        try:
            ingredients = response.xpath(
                "//div[@id='important-information']/div[@class='a-section content']/h4[contains(text(),'Ingredients')]/following-sibling::p/text()").get().strip()
        except:
            ingredients = 'N/A'

        # directions
        try:
            directions = response.xpath(
                "//div[@id='important-information']/div[@class='a-section content']/h4[contains(text(),'Directions')]/following-sibling::p/text()").get().strip().replace(
                '  ', ' ')
        except:
            directions = 'N/A'

        # legal_disclaimer
        try:
            legal_disclaimer = response.xpath(
                "//div[@id='important-information']/div[@class='a-section content']/h4[contains(text(),'Legal Disclaimer')]/following-sibling::p/text()").get().strip()
        except:
            legal_disclaimer = 'N/A'

        # product_asin
        try:
            product_asin = response.xpath(
                "//div[@id='detailBullets_feature_div']//span[contains(text(),'ASIN')]/following-sibling::span/text()").get()
        except:
            product_asin = 'N/A'

        try:
            product_description_lst = [product_des.strip() for product_des in
                                       response.xpath("//div[@id='productDescription']//text()").getall() if
                                       product_des]
            product_description = [product_des for product_des in product_description_lst if product_des]
            if product_description:
                product_description = product_description
            else:
                product_description = 'N/A'
        except:
            product_description = 'N/A'

        # breadcrumb_menu
        try:
            breadcrumb_menu = [breadcrub_menu_data.strip() for breadcrub_menu_data in response.xpath(
                "//div[@id='wayfinding-breadcrumbs_feature_div']//li//a[@class='a-link-normal a-color-tertiary']/text()").getall()]
        except:
            breadcrumb_menu = 'N/A'

        # price
        try:
            price = price
        except:
            price = 'N/A'

        # price_discount
        try:
            price_discount_lst = response.xpath(
                "//td[contains(text(),'  You Save: ')]/following-sibling::td/span[@class='a-color-price']/text() | //span[contains(@class,'savingsPercentage')]/text()").getall()
            price_discount = [price_dis.strip() for price_dis in price_discount_lst][-1].replace('(', '').replace(')',
                                                                                                                  '').replace(
                '%', '').replace('-', '')
        except:
            price_discount = 'N/A'

        # price_per_unit
        try:
            price_per_unit = price_per_unit
            # price_per_unit = response.xpath(
            #     "//div[@id='corePrice_desktop']//span[@class='a-price a-text-price a-size-small']//span[contains(@class,'a-offscreen')]/text()").get().strip().replace(
            #     '$', '')
        except:
            price_per_unit = 'N/A'

        item = AmazonPdpItem()
        item['Primary_image'] = primary_image
        item['Product_title'] = product_title
        # item['Product_url'] = product_url
        item['Price'] = price
        item['Price_per_unit'] = price_per_unit
        item['Price_discount'] = price_discount
        item['Star_ratings'] = star_ratings
        item['No_of_reviews'] = no_of_reviews
        item['Page_rank'] = page_rank
        item['SRP_no'] = srp_no
        item['Brand_name'] = brand_name
        item['Product_ASIN'] = product_asin
        item['Badges'] = badge
        item['Sponsored'] = sponsored
        item['Breadcrumb_menu'] = breadcrumb_menu
        item['Brand'] = brand_name
        item['Secondary_images'] = secondary_image
        item['videos'] = videos

        item['Product_benefits'] = product_benefits
        item['Active_ingredients'] = active_ingredients
        item['Item_form'] = item_form
        item['Flavor'] = flavor
        item['Age_Range'] = age_range
        item['Material_type_free'] = material_type_free
        item['Number_of_items'] = no_of_items
        item['Included_components'] = included_components
        item['About_this_item'] = about_this_item
        item['Manufacturer'] = manufacturer
        item['Product_description'] = product_description
        item['Product_details'] = json.dumps(product_detail)
        item['Important_information'] = json.dumps(important_information)
        item['Safety_information'] = safety_information
        item['Ingredients'] = ingredients
        item['Directions'] = directions
        item['Legal_disclaimer'] = legal_disclaimer
        item['page_save_id'] = hash_key
        yield item
        # page save
        try:
            if not os.path.exists(self.product_data_pagesave_path):
                os.makedirs(self.product_data_pagesave_path)
            main_path = f'{self.product_data_pagesave_path}page_count_{str(hash_key)}.html.gz'
            if not os.path.exists(main_path):
                with gzip.open(main_path, 'wb') as f:
                    f.write(response.text.encode('utf-8'))
                print(f"page save for this page_count_{hash_key}")
        except Exception as e:
            print(e)

        # # TODO - Done-Pending....
        try:
            self.db.crsrSql.execute(
                f"update {self.db.table} set status='Done' where hash_key = '{hash_key}'")
            self.db.connSql.commit()
            print(f"Status for :{hash_key} Updated=Done")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl pdp_product_data".split())
