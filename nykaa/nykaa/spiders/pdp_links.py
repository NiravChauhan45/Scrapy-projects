# import hashlib
# import json
# import os
# import re
# from datetime import datetime
# from typing import Iterable, Any
#
# import requests
# import scrapy
# from parsel import Selector
# from scrapy import cmdline, Request
# from scrapy.http import Response
# from nykaa.items import NykaaPdpLinksItem
#
#
# class ExtractPdpDataSpider(scrapy.Spider):
#     name = "pdp_links"
#     # allowed_domains = ["www.nykaa.com"]
#     start_urls = ["https://www.nykaa.com"]
#
#     def get_rating(self, selector):
#         rating = selector.xpath(
#             "//h2[@data-at='customer-reviews']/following-sibling::*//div[@data-at='product-rating']/text()").get(
#             '').strip()
#         if rating:
#             return rating
#         else:
#             rating = selector.xpath("//div[@class='css-xoezkq']/text()").get('').strip()
#             if rating:
#                 return rating
#             else:
#                 "NA"
#
#     def get_description(self, selector):
#         description = selector.xpath("//div[@class='css-1392ehc']//div[@class='css-1obcna']/text()").get('').strip()
#         return description
#
#     def get_all_images(self, product_data):
#         images_urls_lst = product_data.get('plp_pdp_bridge').get('images')
#         image_list = []
#         for image_url in images_urls_lst:
#             image_list.append(image_url.get('url'))
#         return image_list
#
#     def get_size_chart(self, size_chart_lst):
#         size_chart = []
#         for size in size_chart_lst:
#             size_chart.append(size.get('name'))
#         if size_chart:
#             return " | ".join(size_chart)
#         else:
#             return "NA"
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.headers = {
#             'accept': '*/*',
#             'accept-language': 'en-US,en;q=0.9',
#             'cache-control': 'no-cache',
#             'cookie': 'bcookie=3f88050b-d273-4ac9-a7e5-1aeddaa0f2a8; EXP_plp-quick-filters=variant1; EXP_new-relic-client=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739193541331; rum_abMwebSort=71; _gcl_au=1.1.376661896.1739193543; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; EXP_SSR_CACHE=182338fc37e6d3e8a85abbd1a1dd2b09; PHPSESSID=ab45e830af6443078d4edd70ead02a78; _clck=18jtqpz%7C2%7Cftb%7C0%7C1867; WZRK_G=e5912dd1ce9b403594cf51299d464f2c; _gid=GA1.2.456186803.1739196588; _pin_unauth=dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C20130%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1739801388%7C12%7CMCAAMB-1739801388%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739203788s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; _fbp=fb.1.1739196589554.897197178485079799; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiJhNjkxYjdkYi0xOGY3LTQxMzctYmI4ZS04N2JjYTllZjkyNTgifQ==; __stgeo=IjAi; __stbpnenable=MQ==; __stdf=MA==; form_key=QNpdHiz6JpbGgCu0; _ga=GA1.1.1264073131.1739193543; s_nr=1739198376065-New; mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A194f0225bc4422-089610b641ba02-26011b51-e1000-194f0225bc4422%22%2C%22%24device_id%22%3A%20%22194f0225bc4422-089610b641ba02-26011b51-e1000-194f0225bc4422%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fwomen%2Findianwear%2Fsalwar-suits-and-sets%2Fc%2F69%3Froot%3Dnav_3%26ptype%3Dlisting%252Cwomen%252Cindian-wear%252Csuit-sets%252C4%252Csuit-sets%26f%3Dbrand_filter%253D63680_%26p%3D3%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fwomen%2Findianwear%2Fsalwar-suits-and-sets%2Fc%2F69%3Froot%3Dnav_3%26ptype%3Dlisting%252Cwomen%252Cindian-wear%252Csuit-sets%252C4%252Csuit-sets%26f%3Dbrand_filter%253D63680_%26p%3D3%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22entry_page_type%22%3A%20%22plp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%7D; NYK_VISIT=3f88050b-d273-4ac9-a7e5-1aeddaa0f2a8~1739206649075; bm_sz=B9633C0B19C1A761C89F4529B25C3357~YAAQpYosMT0kPc6UAQAA78LQ8BrZPZrcQy2qxDCGD/1TPy2sYy9t1W2atcymHYlxMsSSpCC7F8861VP4/zRsdzmb2Uxut/GNuCcoA770xqNzCGDPbrVozrgAx6xX860CJp90+btxy2ZOZ1hAIwq1CGg+Eb4zAx2oxXmD0KQq4P7INOWEOcXfXUN9d+e1DnauKhgRSK41abfAkSQR6bcOPUg0leCDw8kR5n/m/yNpTsxMeo5jJuVFVDcpi7A0BWUB+vgJHYI3V2J+rWdicTjpTxbfxpNEqJle3hebKsmPP/hs3UP780SQLjFM9G2D4whxvDjR0j9Lyji6b3rCUoOK2fR3r2mQ17adftOIy/pwrnRnTHw1tAqAbyAB+gRvH1Efscsx3hG90uZHoj2dWWMXknLXPy3o+T3woJzRZyzitceGz6Wo2GOeOiuANU8x0A1fc5+wUYVCUHwjco7GJIs3JKVYSm8J3RI4yPVxyzbTXkoqZW28F5bnp2Wa8UEvKMqH6HuNQB+QpaxEjj6yA5JAIB47a4lbQDKd/rFIu5rodH8Fs3wSQXU5UOWny18Hl09qpOHRK1eMaM5fMTYpH0Dk0ana~3555653~3556920; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQpYosMfwlPc6UAQAAqc7Q8A39S/TtGOMc0y/rXFDKz3N6Ab8GHN8HTyf/EvzTzBqvqJfDeAwaqDwW2rr93vqBYgEPspA7xkbfqms58ddkbwnurzMsfYIoeGlH5+9Wplz72j4aD/czgitNVbE3IgihTdZMc7IAVmgOP1xxCPF+gK2sCYl5zMVDUK97bzVXgI+u0yl5SxEYbQ0ItzbvpqydwKNlZR62pqI2h0x9WO3Uz/cTtYR8fNMeZkZlgl/QemuKg3QlQ5zNoPim6bi+ZgscvX4PmBFwOZzUuxrDgjyEcLK0LsGhPGCg3SOJtvDckOF5PIhhH9jV87xKIBt2ry65q6jlp1zogGyiH27X1OGsH65sDN7YyyvE/efKLHWJ5c4B5c21hn3OVybnnkSDn4k1JizpYc0J7mK2KQY1AV2MmcA33taMyKmghy/ngKHrPxgzb5T9e8li4WPHG9sVDvDDXQHWUcFCJJnENutFdCz15zvYbBq8iEKcwKLIepIr6hAIehCMeiPU1aUaFYQs0X9DHj+gJk0jXr1avrI=~-1~-1~1739210402; NYK_PCOUNTER=5; _ga_DZ4MXZBLKH=GS1.1.1739206649.2.1.1739206856.21.0.0; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A5%2C%22s%22%3A1739206805%2C%22t%22%3A1739206858%7D; _clsk=vv899w%7C1739206860159%7C16%7C0%7Cr.clarity.ms%2Fcollect; _clsk=vv899w%7C1739206860159%7C16%7C0%7Cr.clarity.ms%2Fcollect; _clsk=vv899w%7C1739206860159%7C16%7C0%7Cr.clarity.ms%2Fcollect; NYK_ECOUNTER=478; EXP_SSR_CACHE=182338fc37e6d3e8a85abbd1a1dd2b09; EXP_new-relic-client=variant1; EXP_pdp-brandbook=pdp-brandbook-a; EXP_pdp-sizesection-v2=pdp-sizesection-v2; EXP_plp-quick-filters=variant1; EXP_quick-view=quick-view-visible; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQpYosMZbAPc6UAQAAKlnW8A0u3eojh2kBXpwXTKXfTm1A/IUoL/JomJW79KAOX6XIeXO6aRQ3VXsJ6UWIyhC4ZQiTljWQlBoI4p9NoY7Mp4sf8qbhX1Xy2JDNBA4lPml6iOIppOIijSBxH9WO5XXB2jszB1+MscssIl/r8vDK+uzd0TH2Lp0yzRhkqkUZoLuMHB83fSs/CaOaUYSe4/ZymsbYvUa1rb5ZsO6iEQXm6FVTrDoI891KfUtLC+ETB464h1BSDWByX4CC/eNzy+cutglxnUS6Ml08De/Wxw44okBj2gfQkNhrQoVVTDFFV7VS7Lgrsj6X5KX1XVf3nvcumaEt3gQGnMIvt4YoCfd/WgFffHhxHd4O3vJzqR+gHoXDjzarscfhpnAhbUomstpvWrA66hUZ7qlH0az70CQy/8OcN5VZ8EF7W413M5cGMid/1npiBsXYjn8bTqcIkxUM0ILWdaXaCC/q/GvSwZNchKo6ZEJW/g+GDiK0WXtMtITTI3lgcAFN8KrSbuNFFlRnEvHMdANWc0j8lzo=~0~-1~1739210402; bcookie=3f88050b-d273-4ac9-a7e5-1aeddaa0f2a8; bm_sz=09158C5D010A4BD96A9DA1EFA847BCD1~YAAQpYosMQS0Mc6UAQAAYQ9z8Br9eM+AWCrv+0Q1RXhNKWhF7T2ms+lFnxyuenU941VgppYeip9qWQDg4JtNx5PKOe8LIwNtsho8IdIqtK4L/VmEdmlxmNYLCodv8BJWwwa1wow6Zqi9zRT6methdX4IdfYkb9VN7PuFmEZ4gGISi1jW1AoJ7A0dkQw17rNr3TnIj4/aTv1RxZitgjOc6UNz0PSXmuS6xB7BxXvtkW+zmt448d7rZXLhem8ema7RpTmr3V9eMTqakHCICOjldNBkSvMEVQW4ui5z4Qfn8Lo2yhl1qnphmA9z5ENbaY4vHgAYBNV8Pdz+Kb6ktWYClg6/Ee9v7IpVWMgYuh3NIW7LieXFwV8yLPVPPQ1zMLYE+rnbtJjz4bObbWxZ/8Z4pLqLkdf27PPYwLZBNjv9KW40VuuvkGfuAGIBCi+RGGKIzWcVgeQ4b54BOC9158QRSwwRLvhgje4It6jspiMuv5D0hAqoCpFvnsZ/gnvGKT9ob5KVVC8x6hGR0NwhUwEchsA4gxH+7C868iHHtRecC7YLgFXaMgypVtGa4Q==~4276535~3224642',
#             'domain': 'NYKAA_FASHION',
#             'pragma': 'no-cache',
#             'priority': 'u=1, i',
#             'referer': 'https://www.nykaafashion.com/women/indianwear/salwar-suits-and-sets/c/69?f=brand_filter%3D7657_&p=4',
#             'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-origin',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
#             'x-csrf-token': 'QNpdHiz6JpbGgCu0'
#         }
#
#     def start_requests(self):
#         url = 'https://www.google.com'
#         yield scrapy.Request(
#             url=url,
#             callback=self.parse,
#             dont_filter=True
#         )
#
#     def parse(self, response, **kwargs):
#         category_url_lst = [
#             "https://www.nykaafashion.com/women/indianwear/salwar-suits-and-sets/c/69",
#             "https://www.nykaafashion.com/women/indianwear/sarees/c/10",
#             "https://www.nykaafashion.com/women/indianwear/ethnic-dresses/c/4543",
#             "https://www.nykaafashion.com/women/indianwear/lehengas/c/652",
#             "https://www.nykaafashion.com/women/indianwear/co-ord-sets/c/57387",
#             "https://www.nykaafashion.com/women/indianwear/dress-material/c/7555",
#             "https://www.nykaafashion.com/women/indianwear/blouse/c/164"
#         ]
#         for url in category_url_lst:
#             category_id = url.split('/c/')[-1]
#             brands_dict = {"libas": "63680", "soch": "7657", "kalki": "14065", "koski": "15416",
#                            "suta": "10088"}
#             page_count = 1
#             for brand_key, brand_value in brands_dict.items():
#                 url = (f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2"
#                        f"&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os"
#                        f"=desktop&categoryId={category_id}&currentPage={page_count}&brand_filter={brand_value}")
#                 yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_1, dont_filter=True,
#                                      meta={"category_id": category_id, "brand_key": brand_key,
#                                            "brand_value": brand_value, "page_count": page_count, "url": url})
#
#     def parse_1(self, response):
#         category_id = response.meta.get('category_id')
#         brand_value = response.meta.get('brand_value')
#         brand_key = response.meta.get('brand_key')
#
#         json_data = json.loads(response.text)
#         products_lst = json_data.get('response').get('products')
#         for product_data in products_lst:
#             item = NykaaPdpLinksItem()
#             product_url = "https://www.nykaafashion.com" + product_data.get('actionUrl')
#
#             # Todo: make_pdp_requests
#             product_name = product_data.get('title')
#             product_id = product_data.get('id')
#             image_urls = " | ".join(self.get_all_images(product_data))
#             in_stock = "Available" if not product_data.get('isOutOfStock') else "Not Available"
#             mrp = product_data.get('price')
#             price = product_data.get('discountedPrice')
#             discount = product_data.get('discount')
#
#             size_chart = ''
#             try:
#                 size_chart = self.get_size_chart(product_data.get('plp_pdp_bridge').get('variants').get('size'))
#             except:
#                 pass
#             colour = product_data.get('sibling_colour_codes') if product_data.get('sibling_colour_codes') else "NA"
#             tags = " | ".join([i.get('title') for i in product_data.get('tag')])
#             hash_id = str(
#                 int(hashlib.md5(bytes(str(product_id) + str(brand_key) + str(category_id), "utf8")).hexdigest(), 16) % (
#                         10 ** 10))
#             item['category_id'] = category_id
#             item['brand'] = brand_key
#             item['product_id'] = product_id
#             item['product_name'] = product_name
#             item['product_url'] = product_url
#             item['in_stock'] = in_stock
#             item['images_urls'] = image_urls
#             item['mrp'] = mrp
#             item['price'] = price
#             item['discount'] = discount
#             item['size_chart'] = size_chart
#             item['colour'] = colour
#             item['tags'] = tags
#             item['hash_id'] = hash_id
#             yield item
#
#         # Todo: Pagination
#         if products_lst:
#             page_count = response.meta.get('page_count') + 1
#             print("Page count: ", page_count)
#             url = (f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2"
#                    f"&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop"
#                    f"&categoryId={category_id}&currentPage={page_count}&brand_filter={brand_value}")
#             yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_1, dont_filter=True,
#                                  meta={"category_id": category_id, "brand_key": brand_key, "brand_value": brand_value,
#                                        "page_count": page_count, "url": url})
#
#
# if __name__ == '__main__':
#     cmdline.execute(f"scrapy crawl {ExtractPdpDataSpider.name}".split())
