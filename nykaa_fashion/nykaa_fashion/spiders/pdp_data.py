import hashlib
import json
import os
import re
from datetime import datetime
from typing import Iterable
from itertools import zip_longest
import scrapy
from scrapy import Request, cmdline
from nykaa_fashion.items import NykaaFashionItem
from nykaa_fashion.config.database_config import ConfigDatabase


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"

    def remove_extra_space(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def get_vendor_detail(self, product_data):
        manufacturer_details_dict = {}
        manufacturer_details_list = []
        for product_detail in product_data.get('pdp_sections'):
            if "Vendor details" in product_detail.get('title'):
                if 'Manufacturer details' in product_detail.get(
                        'subtitle') or 'Country of origin' in product_detail.get('subtitle'):
                    if product_detail.get('attributes'):
                        for i in product_detail.get('attributes'):
                            manufacturer_details_dict[i.get('label')] = i.get('value')
        manufacturer_details_list.append(manufacturer_details_dict)
        manufacturer_details = "".join(json.dumps(manufacturer_details_list))
        cleaned = re.sub(r'[\[\]{}]', '', manufacturer_details)
        cleaned = cleaned.replace(",", " |")
        cleaned = " ".join(cleaned.split())
        return cleaned

    def get_image_urls(self, image_url, product_data):
        images_urls = []
        try:
            for img_url in product_data.get('sizeOptions').get('options')[2].get('productMedia'):
                images_urls.append(img_url.get('url'))
            images_urls.remove(image_url)
            return " | ".join(images_urls)
        except:
            return

    def get_short_description(self, product_data):
        description_text = "".join(
            [i.get('value') for i in product_data.get('pdp_sections') if "Know your product" in i.get('title')])
        clean_text = re.sub(r"<.*?>", "", description_text)
        clean_text = re.sub(r'[":]', '', clean_text)
        return clean_text

    def get_variant_price(self, product_data):
        variant_price_list = []
        for i in product_data.get('sizeOptions').get('options'):
            size = i.get('sizeName')
            price = i.get('discountedPrice')
            variant_price = f"{size} - {price}"
            variant_price_list.append(variant_price)
        return " | ".join(variant_price_list)

    def get_description(self, product_data):
        description_lst = []
        description_dict = {}
        for product_detail in product_data.get('pdp_sections'):
            if "Product details" in product_detail.get('title'):
                for prod in product_detail.get('child_widgets'):
                    if prod.get('attributes'):
                        for i in prod.get('attributes'):
                            description_dict[i.get('label')] = i.get('value')
                    else:
                        title = prod.get('title')
                        value = prod.get('value')
                        description_dict[title] = value
        description_lst.append(description_dict)
        description = "".join(json.dumps(description_lst))
        cleaned = re.sub(r'[\[\]{}]', '', description)
        cleaned = cleaned.replace(",", " |")
        cleaned = " ".join(cleaned.split())
        return cleaned

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.today_date = datetime.now().strftime('%d_%m_%Y')
        self.pagesave = f"F:\\Nirav\\Project_page_save\\nykaa_fashion\\pdp\\{self.today_date}\\"
        self.db = ConfigDatabase(database="nykaa_fashion", table='pdp_links')

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'}, start=self.start, end=self.end)
        for result in results:
            main_category_name = result['main_category_name']
            category_name = result['category_name']
            sub_category_name = result['sub_category_name']
            product_id = result['product_id']
            product_name = self.remove_extra_space(result['product_name'])
            product_url = result['product_url']
            in_stock = result['in_stock']
            images_urls = result['images_urls']
            mrp = result['mrp']
            price = result['price']
            discount = result['discount']
            size_chart = result['size_chart']
            colour = result['colour']
            tags = result['tags']
            sku = result['sku']
            image_url = result['image_url']
            brand = result['brand']
            hash_id = result['hash_id']
            filepath = self.pagesave + f"{product_id}.html"
            if os.path.exists(filepath):
                yield scrapy.Request(url=f"file:///{filepath}",
                                     meta={"main_category_name": main_category_name, "category_name": category_name,
                                           "sub_category_name": sub_category_name, "in_stock": in_stock,
                                           "product_url": product_url,
                                           "product_name": product_name, "brand": brand,
                                           "product_id": product_id, "sku": sku, "image_url": image_url,
                                           "images_urls": images_urls, "mrp": mrp,
                                           "price": price, "discount": discount, "size_chart": size_chart,
                                           "hash_id": hash_id,
                                           "colour": colour,
                                           "tags": tags}, dont_filter=True, callback=self.parse)
            else:
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'no-cache',
                    'cookie': 'bcookie=ba330375-373b-47c8-86ec-f6a4746f154c; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739248725013; rum_abMwebSort=90; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; _gcl_au=1.1.1959989807.1739248726; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; PHPSESSID=be883e49fb424c15bb5c74e7f05c5d18; NYK_VISIT=ba330375-373b-47c8-86ec-f6a4746f154c~1739248726208; _ga=GA1.1.1217532890.1739248726; WZRK_G=bad937a95f8b42beaf8ccc829a0bbaf3; _clck=57u7n5%7C2%7Cftc%7C0%7C1868; bm_sz=1C644CBDFCD0C345AE7DE52AF187F1CE~YAAQinAsMYGuSt+UAQAAFu1U8xoSvnnhMhq4H9sPOuJVDUVUVxwD51QcvYCCG7WLzAFYkZafxM3da9XGyNqqxqJcRfkIz7/k2SvVSgS5249KB9SY/75n6t4Xiw2Ivi+ZzeP7WqkNfal+7+4xcbUZg0oVhNldfJR4815z06FczqcLcY19pdREA7iigiwHVZgV+TzLAdzbHH4EAZbL8HNmkKW9HMQryYaJNw/u0Av1oif+O+gSw1GYXTYd8vPWffQlGKjdMhcN8QXDYZ8utk2I93qrJ2tV3oVWFtH9SXieTaxJQ9l8z0gf33e/nYnySZQLcxYioVVJ0KWu9ArPMNJeff9B9OWbI2zO5qZZQYgvF6eMn3FVJpyjPnt+hqhTTClc/hXXTUprX0VEZX+DGTW+Cm7SFxMhVe51VoDntoAtD855getvPEtJ0BorWj05T1Qv+GagQTFj27at0U8NeICH3uu7~4403769~4602165; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQinAsMa+uSt+UAQAAN+9U8w1gY29Hcwz283EEThAS4jvRzKQyBVBIO09arQb0fydElIttovyqM0Z5el/ZyWA3+YMJKQu4MPzhrwpDg1MfNCiV3QOnmEwsGpxFXPL7pSImzNHm+pQiZYoI0SBabG7SFSqO0V3aQDdhdzgONK9/oOn3coOG1OsFwEazIaCYfhcFzceqquZ7RhlQpLuyHcK+zDHQtb+vmjLj04eH7prKi1XOFpAYj5YwcGxJOBn/srXDdgWbtMTHcuA3oxqbtKKSaGfDvFuj09E1T0qihS0b4C8ivCoglO6E7hCYA5XRC2oV6uuDj9rY0LI468c8Jr8oQulcacUYuUMl1uRIIfg1YBV4VdYJLoUc/s//09FH6ucZWI6X4UHk9yDMxT8GU5s8aiZ7PEHlOCV8HybUMC6a48dYdFBdt6xLFDh0Kl38PB1+GBSlx2e6JyQffjyJXE1h2iylh3jCJfnlq+OAki0YHp7X12bqYEnmC5pVOwhsKWrlEUZA8cspttNKDjUFcGvEuQKWcFbkxHBRTRo=~-1~-1~1739251217; NYK_PCOUNTER=3; NYK_ECOUNTER=42; _ga_DZ4MXZBLKH=GS1.1.1739248726.1.1.1739249061.58.0.0; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A6%2C%22s%22%3A1739247617%2C%22t%22%3A1739249061%7D; _clsk=5b2d0e%7C1739249061976%7C5%7C0%7Ck.clarity.ms%2Fcollect; _clsk=5b2d0e%7C1739249061976%7C5%7C0%7Ck.clarity.ms%2Fcollect; _clsk=5b2d0e%7C1739249061976%7C5%7C0%7Ck.clarity.ms%2Fcollect; EXP_SSR_CACHE=182338fc37e6d3e8a85abbd1a1dd2b09; EXP_new-relic-client=variant1; EXP_pdp-brandbook=pdp-brandbook-a; EXP_pdp-sizesection-v2=pdp-sizesection-v2; EXP_plp-quick-filters=variant1; EXP_quick-view=quick-view-visible; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQpYosMQotVM6UAQAAVO9W8w1oxkB+BHu0I4lVSkF0UEF2JpdCwGUujZpRbrddL0uKyl8UVFJXrRWpgOdUcMvM4RmuO4sRKTQnaIEBvZsOfrOkwQSa2tWgR5se+yb2PlKUGbgU9tgpy3BzyNmXamTMU3wMTTfOIDoVoysMUBzj0DhtGYXP1UceSJeVjZ/nvXv2/fWkjibZDSO4rZEtNuLdhGXJykMvbhsHA03hOt9Ig0bftGNDnDg7MWRdzFQGVF1Yj8MkdYSR9NVIyVKzXC8imEoxPSEp7k+wcOcOZmxB4RVKAUqMq3InSSaJPN4M/OojuS4Ronfq1kjQKHzXJLSMggxNQiY3850s+L2J4zqvURanH+t7w7kGeazDEo4ZwGE5CkXN4N1bU9u586hJ67v0YOWbHpsEI1ACRziBUxLR3iU+YKM1uOiNY5GOxta0OhccNqGeFqcT9JNg8FRnay1rCa25kxYNYs7vpbGgxIClt00DTs6KsvdkejUstiCJ+qEPpNKanyGpjj6IMsOXetQK57E+nWwCf5/04uA=~0~-1~1739251217; bcookie=3f88050b-d273-4ac9-a7e5-1aeddaa0f2a8; bm_sz=1C644CBDFCD0C345AE7DE52AF187F1CE~YAAQpYosMQstVM6UAQAAVO9W8xrd7kRJm6JPxpr5tVp7YQHV6z/MKJ5pnQs/j8fg8b/lDtr4HEne3AupBiHiwuoWJGd0fo8Uda6CMnpTsMsowoXu2tuIzW76b6Q30QKNMIf6hm8pYaaiBLS4h44bvaeSOnvUCWl5AYqVjuOKpR3iDY1RpE7GMy07ci4nIjOGnPx20Ui7NhMFytPFNmbW6YpX+5QUJz+VLjXfsPKch8Ff5yP6sR8rtgRmifsD3xFW5F0T58izKQY2htMaeyd3FxhnUfqpMAm4uA2Av8iHSNmf35NspO1HYjGJKXwwL2KuQkh3RkM7F5pIip0shv6ECPNVKz90elNVUrcte4Gd7zbqf3I4noX1dWGVLCN+KPOiEbx/N2o942i5+ZKtmbbg2ghOAVw0t574JNIgsq3Jq6UiEAnocn9/mJAqOLjH/KpAVYEow/pC02uocU+ylK156Ndl17dfSO5yHw==~4403769~4602165',
                    'pragma': 'no-cache',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
                }
                yield scrapy.Request(url=product_url, headers=headers,
                                     meta={"main_category_name": main_category_name, "category_name": category_name,
                                           "sub_category_name": sub_category_name, "in_stock": in_stock,
                                           "product_url": product_url,
                                           "product_name": product_name, "brand": brand,
                                           "product_id": product_id, "sku": sku, "image_url": image_url,
                                           "images_urls": images_urls, "mrp": mrp,
                                           "price": price, "discount": discount, "size_chart": size_chart,
                                           "hash_id": hash_id,
                                           "colour": colour,
                                           "tags": tags}, dont_filter=True, callback=self.parse)

    def parse(self, response, **kwargs):
        images_urls = response.meta.get('images_urls')

        item = NykaaFashionItem()
        json_data = response.xpath("//script[@id='__PRELOADED_STATE__']/text()").get()
        j_data = json.loads(json_data)
        # hash_id = response.meta.get("hash_id")
        product_data = ''
        try:
            product_data = j_data.get('details').get('skuData').get('product')
        except:
            ''
        if product_data:
            product_id = product_data.get('id')
            product_name = product_data.get("subTitle")
            short_description = self.get_short_description(product_data)
            description = self.get_description(product_data)
            category = "/".join([i.get('key') for i in product_data.get('breadcrumbs')][1:])
            image_url = product_data.get('imageUrl')
            price = product_data.get('price')
            price_currency = "INR"
            sale_price = product_data.get('discountedPrice')
            final_price = sale_price
            discount = price - sale_price
            is_on_sale = ''
            is_in_stock = "True" if not product_data.get('isOutOfStock') else "False"
            product_brand = product_data.get('title')
            manufacturer = self.get_vendor_detail(product_data)
            product_sku = product_data.get('sku')
            colour = product_data.get('product_detail_color')
            gender = product_data.get('breadcrumbs')[1].get('key')
            size = " | ".join([i.get('sizeName') for i in product_data.get('sizeOptions').get('options')])
            variant_price = self.get_variant_price(product_data)
            image_alternate_urls = self.get_image_urls(image_url, product_data)
            product_url = "https://www.nykaafashion.com" + product_data.get('action_url')
            avg_ratings = product_data.get('review_rating_json').get('star_rating')
            num_ratings = product_data.get('review_rating_json').get('star_rating_count')

            item['PID'] = product_id if product_id else "N/A"
            item['Name'] = product_name if product_name else "N/A"
            item['Short Description'] = short_description if short_description else "N/A"
            item['Description'] = description if description else "N/A"
            item['Category'] = category if category else "N/A"
            item['Image URL'] = image_url if image_url else "N/A"
            item['Price'] = price if price else "N/A"
            item['Price Currency'] = price_currency
            item['Sale Price'] = sale_price if sale_price else 'N/A'
            item['Final Price'] = final_price if final_price else 'N/A'
            item['Discount'] = discount if discount else 'N/A'
            item['IsOnSale'] = is_on_sale if is_on_sale else 'N/A'
            item['IsInStock'] = is_in_stock if is_in_stock else 'N/A'
            item['Keywords'] = 'N/A'
            item['Brand'] = product_brand if product_brand else 'N/A'
            item['Manufacturer'] = manufacturer if manufacturer else 'N/A'
            item['MPN'] = 'N/A'
            item['UPC or EAN'] = 'N/A'
            item['SKU'] = product_sku if product_sku else 'N/A'
            item['Colour'] = colour if colour else 'N/A'
            item['Gender'] = gender if gender else 'N/A'
            item['Size'] = size if size else 'N/A'
            item['Variant Price'] = variant_price if variant_price else 'N/A'
            item['Alternate Image URLs'] = image_alternate_urls if image_alternate_urls else images_urls
            item['Link URL'] = product_url
            item['Num Ratings'] = num_ratings if num_ratings else 'N/A'
            item['Average Ratings'] = avg_ratings if avg_ratings else 'N/A'
            item['hash_id'] = str(
                int(hashlib.md5(bytes(
                    str(item['Name']), "utf8")).hexdigest(),
                    16) % (
                        10 ** 10))
            yield item
            # print(item)

            # Todo: page save
            try:
                os.makedirs(self.pagesave, exist_ok=True)
                main_path = f'{self.pagesave}{product_id}.html'
                if not os.path.exists(main_path):
                    with open(main_path, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"page save for this {product_id}")
            except Exception as e:
                print(e)


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpDataSpider.name} -a start=1 -a end=101".split())
