import json
import os.path
import re
from datetime import datetime

import requests
import scrapy
from scrapy import cmdline
from ajio_nua_e_com.items import AjioNuaEComItem
import ajio_nua_e_com.db_config as db


class PlDataSpider(scrapy.Spider):
    name = "pl_data"
    allowed_domains = ["www.ajio.com"]
    start_urls = ["https://www.ajio.com"]

    def start_requests(self):
        keyword_list = ["campus", "redtape"]
        pincode = "110001"
        for keyword in keyword_list:
            yield scrapy.Request("https://example.com",
                                 meta={"keyword": keyword, "pincode": pincode},
                                 callback=self.parse,
                                 dont_filter=True)

    def parse(self, response, **kwargs):

        pincode = response.meta.get("pincode")
        keyword = response.meta.get("keyword")
        product_rank = 0

        for page_number in range(1, 5 + 1):
            url = f"https://www.ajio.com/api/search?currentPage={page_number}&pageSize=45&format=json&query={keyword}%3Arelevance&text={keyword}"
            headers = {
                'sec-ch-ua-platform': '"Windows"',
                'Referer': 'https://www.ajio.com/search/?text=sparks',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-ch-ua-mobile': '?0',
                'ai': 'www.ajio.com',
                'vr': 'WEB-1.15.0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'Accept': 'application/json',
                'os': '4',
                'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'Cookie': 'TS01a68201=015d0fa2269d031a2b4f0a359b8609dcd393524355b8f92c360708e89b89bfaf8cb8b141d61d45034e7e625e85c764b25a77b51f8e; TS01d405db=015d0fa226b5b4ee5b24e36f1d58299d73d79aee5b4e9273e292abb72718def30f6e795852a80a34ef66f3fdf862396c0eb51a1d2d28899587563d85ecd7e188933df4e63bbbd1b383ac3ddbbee1f3a2ef98a31b0c7d91b8a8a6b2c6b57c52815bc6926224; V=201; _abck=BF88F86384BDD2242EDFC75766226D6D~-1~YAAQVvXSF1jYrDaZAQAAQReLUQ5qkREhwkgP8fCgE0Q4EHsPAqlXiF+1/ApVjl283T9Y3ty4N6j5WaR9nDCoqb8MYHBJqcFbp//Vx0Lubgd7LZcXDYG4MlZDMevaxyh3M81NEHJbnZo2rZtXPRO6anKNVqQMoOWdIMu02icxuA1lIpWfvORmMrEX2OFKZJm4I1827LSlHG0tvqDO5t5UOm+TwmP53+My8h+yQewezxhqdx5IO9lleokgaY+r+vZ37NomEGeGXAN/pX5iEiVvVl+120t5ZyVgCfjUmlZ8mJ26JoKaKrjLlob0fXHkV/XjyYb+goXeEvG5sGrTrHwuxxpa7+SkHyqYt0DFS847QZsokR6Ho1IelBXa79AkXci7+D/x1ELLgqy5Ax2Vp4xdYBaln9iN+uWIYnOmd9fmK6kxjydejmaBY9qfGehpkO/xJs0xkmWW~-1~-1~-1~-1~-1; ak_bmsc=492C416183234E4939770B712AC7AA82~000000000000000000000000000000~YAAQVvXSF1nYrDaZAQAAQReLUR2q9Txa+Q5d7vh2HoIin+7q3rB63gzF1/tl4wTe30DavmMX/93+KQzgirrUcchSX3lPcEds3pTPurN1G8khJJgJQLcAogKeXkZO5xMHqCgCrzHE86aiuoxdXM0761NwwAajMAvTRl+ZKU8yt7uao7coYJDltgKkIor0ac17sJE9L6gAGNkIg/SKzlfhDNWIQxpPt35WU4uT6VwqfKXtKNKQF5xXs+Co8XTYBHEbEWak66JuqlFGnTmEnX87NCAnaICPDvalgoNTJ7XAPS/IKSKFjZt8QmmTQlJEsQ+hAJumA0XJyRRL4LFC+IAq/XrmG2Yhzso6tn0=; bm_sv=AFD5214FA0423D328232F8B745F28561~YAAQVvXSF2jerDaZAQAA3VuMUR1LHIKKuPQVg+lEwHcoKERyRAbo1z6nWnyL0iFKC3F2vJps7oXBqPAEdsyRDihfeCuENTW9M0Jip7UM/lBEqOkKwQZc5RDcxnxPZ/NRuiQBNg9MXpwAAS3Afs6lWYaS2EsaPnXcf6kGGX6qlGDLYQYzSOu5FikcfPvaT4rpkLsowlI98gSs8wBnzZZCDLdd081TKK3QAxWMxsMn56whufJ3SDqDfgd/tLTlYA==~1; bm_sz=1DE3AE139ACE94876598CEBB51410809~YAAQVvXSF1rYrDaZAQAAQReLUR14YR3p5NPoMv+HhxbzT8c76/DVwaj3IoqhalsYgdadasOOpN4+5QQo+bgbHBrg8LeMwrhsD/OGhHbNSrxZoxzq8zBMn7VhSHDv1OCGsVyEcBdGGe+v9hopcKSfI5DpweK/dE1OHcESSK4ZOexDjGiWeG+WbaN3I0mKfvar5HPrw0UeV772MlWAzFd5DOpVr0rgKWh27sl+7bh+59YN1X4NOmabALMkhAGYfB56bsgHOLGRrPtJIqFDAVvtzrkuDk9lkY+B4NCpFc2yX56J2cOYFWb9MFENzPMPhrVCQCnxw3+RISHCbsKGPUVxdm2AMUt57IeKLgKr7g==~3618870~3224368; ADRUM_BT=R:40|i:6210|g:24497d50-71c1-47e4-b652-e7d3357ccca64052880|e:111|n:customer1_be12de70-87be-45ee-86d9-ba878ff9a400'
            }
            response = requests.get(url, headers=headers)

            pagesave_path = f"{db.pagesave_path}\\{keyword}"
            os.makedirs(pagesave_path, exist_ok=True)
            pagesave_path = f"{pagesave_path}\\{pincode}_{keyword}_{page_number}.json"

            json_data = response.text
            json_data = json.loads(json_data)

            # Todo:pagesave
            with open(pagesave_path, "w") as file:
                file.write(json.dumps(json_data))

            for product_data in json_data.get("products"):

                product_rank = product_rank + 1

                item = AjioNuaEComItem()
                # Todo: platform
                try:
                    item['platform'] = "Ajio"
                except Exception as e:
                    print(e)

                # Todo: datetime
                try:
                    item['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(e)

                # Todo: keyword
                try:
                    keyword = keyword
                    item['keyword'] = keyword
                except Exception as e:
                    print(e)

                # Todo: pincode
                try:
                    pincode = pincode
                    item['pincode'] = pincode
                except Exception as e:
                    print(e)

                # Todo: product_url
                product_url = ''
                try:
                    product_url = "https://www.ajio.com" + product_data.get('url')
                    item['product_url'] = product_url if product_url else "N/A"
                except Exception as e:
                    print(e)

                # Todo: product_id
                product_id = ''
                try:
                    product_id = product_url.split("/p/")[-1]
                    item['product_id'] = product_id if product_id else "N/A"
                except Exception as e:
                    print(e)
                unique_key = f"{pincode}_{keyword}_{product_id}_{page_number}"

                # Todo:product_name
                try:
                    product_name = product_data.get('name') if product_data.get('name') else "N/A"
                    item['product_name'] = re.sub("\\s+", " ", product_name).strip()
                except Exception as e:
                    print(e)

                # Todo:product_rank
                try:
                    item['Product_rank'] = product_rank
                except Exception as e:
                    print(e)

                # Todo: mrp
                mrp = ''
                try:
                    mrp = product_data.get('wasPriceData').get('value') if product_data.get('wasPriceData').get(
                        'value') else "N/A"
                    item['mrp'] = mrp
                except Exception as e:
                    print(e)

                # Todo: selling_price
                try:
                    selling_price = product_data.get('price').get('value') if product_data.get('price').get(
                        'value') else mrp
                    item['selling_price'] = selling_price
                except Exception as e:
                    print(e)

                # Todo: discount_percent
                try:
                    discount_percent = product_data.get('discountPercent') if product_data.get(
                        'discountPercent') else "N/A"
                    if discount_percent:
                        try:
                            item['discount_percent'] = re.search(r'\d+', discount_percent).group()
                        except:
                            item['discount_percent'] = "N/A"
                    else:
                        item['discount_percent'] = "N/A"
                except Exception as e:
                    print(e)

                # Todo:product_image
                try:
                    product_image = [image_url.get('url') for image_url in product_data.get('images') if image_url]
                    item['Product Image link'] = product_image[0] if product_image else "N/A"
                except Exception as e:
                    print(e)

                # Todo:unique_key
                try:
                    item['unique_key'] = unique_key
                except Exception as e:
                    print(e)

                yield item


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PlDataSpider.name}".split())
