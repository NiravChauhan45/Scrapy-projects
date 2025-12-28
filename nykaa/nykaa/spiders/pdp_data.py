# Todo : Get data using Xpath

# import gzip
# import hashlib
# import json
# import os
# import re
# from datetime import datetime
# from typing import Iterable
#
# import requests
# import scrapy
# from parsel import Selector
# from scrapy import cmdline, Request
# from nykaa.items import NykaaPdpDataItem
#
# from nykaa.config.database_config import ConfigDatabase
#
#
# class ExtractPdpDataSpider(scrapy.Spider):
#     name = "pdp_data"
#     allowed_domains = ["www.nykaa.com"]
#     start_urls = ["https://www.nykaa.com"]
#
#     def __init__(self, start, end, **kwargs):
#         super().__init__(**kwargs)
#         self.start = start
#         self.end = end
#         # self.today_date = datetime.now().strftime('%d_%m_%Y')
#         self.today_date = "20_02_2025"
#         self.pagesave = f"F:\\Nirav\\Project_page_save\\nykaa\\{self.today_date}\\"
#         self.offer_pagesave = f"F:\\Nirav\\Project_page_save\\nykaa\\offers\\{self.today_date}\\"
#         self.db = ConfigDatabase(database="nykaa", table='pdp_links_t')
#
#     def get_star(self, response):
#         star = response.xpath(
#             "//h2[@data-at='customer-reviews']/following-sibling::*//div[@data-at='product-rating']/text()").get(
#             '').strip()
#         if star:
#             return star
#         else:
#             star = response.xpath("//div[@class='css-xoezkq']/text()").get('').strip()
#             if star:
#                 return star
#             else:
#                 return "NA"
#
#     def get_offer(self, product_id, mrp, price):
#         cookies = {
#             'bcookie': 'ba330375-373b-47c8-86ec-f6a4746f154c',
#             'EXP_plp-quick-filters': 'variant1',
#             'EXP_pdp-sizesection-v2': 'pdp-sizesection-v2',
#             'tm_stmp': '1739248725013',
#             'rum_abMwebSort': '90',
#             'EXP_pdp-brandbook': 'pdp-brandbook-a',
#             'EXP_quick-view': 'quick-view-visible',
#             '_gcl_au': '1.1.1959989807.1739248726',
#             'EXP_SSR_CACHE': 'e73a4ec92663a42c1f6f9a846b433544',
#             'PHPSESSID': 'be883e49fb424c15bb5c74e7f05c5d18',
#             'NYK_VISIT': 'ba330375-373b-47c8-86ec-f6a4746f154c~1739248726208',
#             'WZRK_G': 'bad937a95f8b42beaf8ccc829a0bbaf3',
#             '_clck': '57u7n5%7C2%7Cftc%7C0%7C1868',
#             '_gid': 'GA1.2.1176014782.1739257973',
#             '_pin_unauth': 'dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ',
#             '_ga': 'GA1.1.1217532890.1739248726',
#             '__stp': 'eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiI2YmVkNjY0Zi1hNzIwLTRjNDgtYmU3NC1kOTExNDE5YzY3ODkifQ==',
#             '__stdf': 'MA==',
#             'form_key': 'YbThqqINmvOoMsfY',
#             'AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg': '-1303530583%7CMCIDTS%7C20131%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1739862773%7C12%7CMCAAMB-1739862773%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739265173s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0',
#             's_nr': '1739257973726-New',
#             'mp_0cd3b66d1a18575ebe299806e286685f_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A194f3da8f7a538-0edf36df0fad27-26011b51-e1000-194f3da8f7b538%22%2C%22%24device_id%22%3A%20%22194f3da8f7a538-0edf36df0fad27-26011b51-e1000-194f3da8f7b538%22%2C%22entry_page_product_id%22%3A%20%2214325460%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22entry_page_type%22%3A%20%22pdp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%7D',
#             '_ga_DZ4MXZBLKH': 'deleted',
#             'WZRK_S_WRK-4W9-R55Z': '%7B%22p%22%3A51%2C%22s%22%3A1739256515%2C%22t%22%3A1739261419%7D',
#             '_clsk': '5b2d0e%7C1739261421503%7C91%7C0%7Ck.clarity.ms%2Fcollect',
#             '_clsk': '5b2d0e%7C1739261421503%7C91%7C0%7Ck.clarity.ms%2Fcollect',
#             'bm_sz': 'EA6F9643E2366B96B4A7CE1958FFC4B9~YAAQpYosMTgMa86UAQAAMgoS9BqfTs9hIsq0ft1+wkodKzSngo1JPJLj9Jw89t4CdplaxlxydogtUp0JrJYJqJlX7lRbPP4a6UF96RiU9eqowG6sqgCxkc2Ig7oGcCc/dtSE53i2hkdQA7yoZbbBBwaO4Wg17SEv2CVvagVwh85iVC+J/6qDQ0yPCdWSkyqejwX9GCm4ExtbCjPdWk8UW0XM8zM5p0W2n+YKzC2aC1VVaACMzct+7lVMC/YlspI6nd2GzHnPmZP/kNMm+L2ZySCEkd+lt3vqPWbDoiOCyevgRWKcTOSnIAuoekTEkfG83oeIiecEKvVJE0HVqXjB0cO4rNAZmzX9MAbY9WkrT4UMt6dxCacWY35e2oByl2H5cwJsfiZ8VdlOIlW7E8Ec5VFMVaCJ5NwuICJ/86A3NP3TI8e9hKlRSLCZES+yq5YNUYGiMjoJJtDank2dUIrXK9p92rUk+HPzC+05Pt9MVtPgMM7UNvbKeoGLTYYZvRaxmvY+Ap2o9vXC1+2/hh+wEMnuVcC6BkvvE8S6krA3urBq3CPLydD/uOYGp5fFVuYfJcr1lwID0ysxGWrF8BlsK81OCIEjitCJ~3682369~4538929',
#             '_ga_DZ4MXZBLKH': 'GS1.1.1739248726.1.1.1739261452.26.0.0',
#             '_abck': '3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQpYosMXIMa86UAQAATAwS9A2HmAkOeYaPmMRZbAy9ZZ2IZPZpu0QC4vCaPyWJ2gvtLu57Jp1/ZYm9LpwlxP58ctGaYuZgHtAMsmfamkZ+z4qeM1OqXclu/aZyHShhDH/YsHatydRI6St6MWG9/qoR/ZpdAQ5hsa9RZEgQRHZ5rE2uOOTps7TRBA//O/s95wJpfDoDXA4SdhZRLFx4SfeBn3nPh7KC8UMqxGxJjMK5e2n+5gSQDwlWIRf7sPJ61ptYT2XagSxlfsamgOZGI73a9nhHFtYgQB1JfiobPP/b/c4cCHwamXdsl9pJet+V5PzJgFMo116Sp9nHRQFXQarhE72QBb1IWARtUu7KVx0ojez3ZJtONjxt9ewsPELGvyyn5GUGqII/cuUZa41ad8VTvGSBUq3gQ8BkYvqZhX4HtbgfUqZNl0B0z1AaXoesr94xXpdb627QfX6yPeoplMoF+1Z9zdnr1Bj8uZN7XTlSnCRpxh2BeOcNvCwj9QiOEY8/GEYGmhL+DSzIPepMOC5cfmIJyvejEZTPNQA=~-1~-1~1739262454',
#             'NYK_PCOUNTER': '96',
#             'NYK_ECOUNTER': '503',
#         }
#         headers = {
#             'accept': '*/*',
#             'accept-language': 'en-US,en;q=0.9',
#             'cache-control': 'no-cache',
#             # 'cookie': 'bcookie=ba330375-373b-47c8-86ec-f6a4746f154c; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739248725013; rum_abMwebSort=90; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; _gcl_au=1.1.1959989807.1739248726; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; PHPSESSID=be883e49fb424c15bb5c74e7f05c5d18; NYK_VISIT=ba330375-373b-47c8-86ec-f6a4746f154c~1739248726208; WZRK_G=bad937a95f8b42beaf8ccc829a0bbaf3; _clck=57u7n5%7C2%7Cftc%7C0%7C1868; _gid=GA1.2.1176014782.1739257973; _pin_unauth=dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ; _ga=GA1.1.1217532890.1739248726; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiI2YmVkNjY0Zi1hNzIwLTRjNDgtYmU3NC1kOTExNDE5YzY3ODkifQ==; __stdf=MA==; form_key=YbThqqINmvOoMsfY; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C20131%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1739862773%7C12%7CMCAAMB-1739862773%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739265173s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_nr=1739257973726-New; mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A194f3da8f7a538-0edf36df0fad27-26011b51-e1000-194f3da8f7b538%22%2C%22%24device_id%22%3A%20%22194f3da8f7a538-0edf36df0fad27-26011b51-e1000-194f3da8f7b538%22%2C%22entry_page_product_id%22%3A%20%2214325460%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22entry_page_type%22%3A%20%22pdp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%7D; _ga_DZ4MXZBLKH=deleted; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A51%2C%22s%22%3A1739256515%2C%22t%22%3A1739261419%7D; _clsk=5b2d0e%7C1739261421503%7C91%7C0%7Ck.clarity.ms%2Fcollect; _clsk=5b2d0e%7C1739261421503%7C91%7C0%7Ck.clarity.ms%2Fcollect; bm_sz=EA6F9643E2366B96B4A7CE1958FFC4B9~YAAQpYosMTgMa86UAQAAMgoS9BqfTs9hIsq0ft1+wkodKzSngo1JPJLj9Jw89t4CdplaxlxydogtUp0JrJYJqJlX7lRbPP4a6UF96RiU9eqowG6sqgCxkc2Ig7oGcCc/dtSE53i2hkdQA7yoZbbBBwaO4Wg17SEv2CVvagVwh85iVC+J/6qDQ0yPCdWSkyqejwX9GCm4ExtbCjPdWk8UW0XM8zM5p0W2n+YKzC2aC1VVaACMzct+7lVMC/YlspI6nd2GzHnPmZP/kNMm+L2ZySCEkd+lt3vqPWbDoiOCyevgRWKcTOSnIAuoekTEkfG83oeIiecEKvVJE0HVqXjB0cO4rNAZmzX9MAbY9WkrT4UMt6dxCacWY35e2oByl2H5cwJsfiZ8VdlOIlW7E8Ec5VFMVaCJ5NwuICJ/86A3NP3TI8e9hKlRSLCZES+yq5YNUYGiMjoJJtDank2dUIrXK9p92rUk+HPzC+05Pt9MVtPgMM7UNvbKeoGLTYYZvRaxmvY+Ap2o9vXC1+2/hh+wEMnuVcC6BkvvE8S6krA3urBq3CPLydD/uOYGp5fFVuYfJcr1lwID0ysxGWrF8BlsK81OCIEjitCJ~3682369~4538929; _ga_DZ4MXZBLKH=GS1.1.1739248726.1.1.1739261452.26.0.0; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQpYosMXIMa86UAQAATAwS9A2HmAkOeYaPmMRZbAy9ZZ2IZPZpu0QC4vCaPyWJ2gvtLu57Jp1/ZYm9LpwlxP58ctGaYuZgHtAMsmfamkZ+z4qeM1OqXclu/aZyHShhDH/YsHatydRI6St6MWG9/qoR/ZpdAQ5hsa9RZEgQRHZ5rE2uOOTps7TRBA//O/s95wJpfDoDXA4SdhZRLFx4SfeBn3nPh7KC8UMqxGxJjMK5e2n+5gSQDwlWIRf7sPJ61ptYT2XagSxlfsamgOZGI73a9nhHFtYgQB1JfiobPP/b/c4cCHwamXdsl9pJet+V5PzJgFMo116Sp9nHRQFXQarhE72QBb1IWARtUu7KVx0ojez3ZJtONjxt9ewsPELGvyyn5GUGqII/cuUZa41ad8VTvGSBUq3gQ8BkYvqZhX4HtbgfUqZNl0B0z1AaXoesr94xXpdb627QfX6yPeoplMoF+1Z9zdnr1Bj8uZN7XTlSnCRpxh2BeOcNvCwj9QiOEY8/GEYGmhL+DSzIPepMOC5cfmIJyvejEZTPNQA=~-1~-1~1739262454; NYK_PCOUNTER=96; NYK_ECOUNTER=503',
#             'pragma': 'no-cache',
#             'priority': 'u=1, i',
#             'referer': 'https://www.nykaafashion.com/soch-women-s-yellow-floral-silk-blend-gathered-gown-with-cutdana-dupatta-set-of-2/p/17080929',
#             'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-origin',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
#         }
#         params = {
#             'customerGroupId': '0',
#             'domain': 'fashion',
#             'deviceType': 'WEBSITE',
#             'isLoyal': '1',
#             'productId': f'{product_id}',
#             'mrp': f'{mrp}',
#             'sp': f'{price}',
#             'fetchUniversalOffers': 'true',
#             'fetchCouponOffers': 'true',
#             'fetchPaymentMethodOffers': 'true',
#             'fetchTradeOffers': 'true',
#             'fetchBestOffers': 'true',
#         }
#         response = requests.get(
#             'https://www.nykaafashion.com/gateway-api/offer/api/v1/product/customer/offer',
#             params=params,
#             cookies=cookies,
#             headers=headers,
#         )
#         selector = Selector(text=response.text)
#         json_data = json.loads(selector._text)
#         offers_lst = json_data.get('data').get('coupons')
#         offers_list = []
#         for offer in offers_lst:
#             offer_dict = {'offerId': offer.get('offerId'), 'title': offer.get('title'),
#                           'description': offer.get('description'), 'offerType': offer.get('offerType')}
#             offers_list.append(offer_dict)
#         return json.dumps(offers_list,
#                           ensure_ascii=False)  # .replace(' \\u20b9', ' ₹').replace('\\u20b9', ' ₹').replace(' .', '.')
#
#     def get_rating(self, response):
#         rating = ''
#         if response.xpath("//div[@class='css-lpjc58']/div[@class='css-kmkjrs']/text()"):
#             rating_text = response.xpath("//div[@class='css-lpjc58']/div[@class='css-kmkjrs']/text()").get()
#             rating = re.search(r'\d+', rating_text).group()
#         else:
#             if response.xpath("//div[@class='css-kmkjrs']//text()").get():
#                 rating_text = response.xpath("//div[@class='css-kmkjrs']//text()").get()
#                 rating = re.search(r'\d+', rating_text).group()
#         return rating
#
#     def start_requests(self):
#         results = self.db.fetchResultsfromSql(conditions={'status': 'Done'}, start=self.start, end=self.end)
#         for result in results:
#             hash_id = result['hash_id']
#             product_url = result['product_url']
#             product_id = product_url.split("/")[-1].strip()
#             product_name = result['product_name']
#             images_urls = result['images_urls']
#             mrp = result['mrp']
#             price = result['price']
#             discount = result['discount']
#             size_chart = result['size_chart']
#             colour = result['colour']
#             tags = result['tags']
#             filepath = self.pagesave + f"{hash_id}.html"
#             if os.path.exists(filepath):
#                 yield scrapy.Request(url=f"file:///{filepath}",
#                                      meta={"product_url": product_url, "product_name": product_name,
#                                            "product_id": product_id,
#                                            "images_urls": images_urls, "mrp": mrp,
#                                            "price": price, "discount": discount, "size_chart": size_chart,
#                                            # "category_id": category_id,
#                                            "hash_id": hash_id,
#                                            "colour": colour,
#                                            "tags": tags}, dont_filter=True, callback=self.parse)
#             else:
#                 headers = {
#                     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#                     'accept-language': 'en-US,en;q=0.9',
#                     'cache-control': 'no-cache',
#                     'cookie': 'bcookie=ba330375-373b-47c8-86ec-f6a4746f154c; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739248725013; rum_abMwebSort=90; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; _gcl_au=1.1.1959989807.1739248726; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; PHPSESSID=be883e49fb424c15bb5c74e7f05c5d18; NYK_VISIT=ba330375-373b-47c8-86ec-f6a4746f154c~1739248726208; _ga=GA1.1.1217532890.1739248726; WZRK_G=bad937a95f8b42beaf8ccc829a0bbaf3; _clck=57u7n5%7C2%7Cftc%7C0%7C1868; bm_sz=1C644CBDFCD0C345AE7DE52AF187F1CE~YAAQinAsMYGuSt+UAQAAFu1U8xoSvnnhMhq4H9sPOuJVDUVUVxwD51QcvYCCG7WLzAFYkZafxM3da9XGyNqqxqJcRfkIz7/k2SvVSgS5249KB9SY/75n6t4Xiw2Ivi+ZzeP7WqkNfal+7+4xcbUZg0oVhNldfJR4815z06FczqcLcY19pdREA7iigiwHVZgV+TzLAdzbHH4EAZbL8HNmkKW9HMQryYaJNw/u0Av1oif+O+gSw1GYXTYd8vPWffQlGKjdMhcN8QXDYZ8utk2I93qrJ2tV3oVWFtH9SXieTaxJQ9l8z0gf33e/nYnySZQLcxYioVVJ0KWu9ArPMNJeff9B9OWbI2zO5qZZQYgvF6eMn3FVJpyjPnt+hqhTTClc/hXXTUprX0VEZX+DGTW+Cm7SFxMhVe51VoDntoAtD855getvPEtJ0BorWj05T1Qv+GagQTFj27at0U8NeICH3uu7~4403769~4602165; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQinAsMa+uSt+UAQAAN+9U8w1gY29Hcwz283EEThAS4jvRzKQyBVBIO09arQb0fydElIttovyqM0Z5el/ZyWA3+YMJKQu4MPzhrwpDg1MfNCiV3QOnmEwsGpxFXPL7pSImzNHm+pQiZYoI0SBabG7SFSqO0V3aQDdhdzgONK9/oOn3coOG1OsFwEazIaCYfhcFzceqquZ7RhlQpLuyHcK+zDHQtb+vmjLj04eH7prKi1XOFpAYj5YwcGxJOBn/srXDdgWbtMTHcuA3oxqbtKKSaGfDvFuj09E1T0qihS0b4C8ivCoglO6E7hCYA5XRC2oV6uuDj9rY0LI468c8Jr8oQulcacUYuUMl1uRIIfg1YBV4VdYJLoUc/s//09FH6ucZWI6X4UHk9yDMxT8GU5s8aiZ7PEHlOCV8HybUMC6a48dYdFBdt6xLFDh0Kl38PB1+GBSlx2e6JyQffjyJXE1h2iylh3jCJfnlq+OAki0YHp7X12bqYEnmC5pVOwhsKWrlEUZA8cspttNKDjUFcGvEuQKWcFbkxHBRTRo=~-1~-1~1739251217; NYK_PCOUNTER=3; NYK_ECOUNTER=42; _ga_DZ4MXZBLKH=GS1.1.1739248726.1.1.1739249061.58.0.0; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A6%2C%22s%22%3A1739247617%2C%22t%22%3A1739249061%7D; _clsk=5b2d0e%7C1739249061976%7C5%7C0%7Ck.clarity.ms%2Fcollect; _clsk=5b2d0e%7C1739249061976%7C5%7C0%7Ck.clarity.ms%2Fcollect; _clsk=5b2d0e%7C1739249061976%7C5%7C0%7Ck.clarity.ms%2Fcollect; EXP_SSR_CACHE=182338fc37e6d3e8a85abbd1a1dd2b09; EXP_new-relic-client=variant1; EXP_pdp-brandbook=pdp-brandbook-a; EXP_pdp-sizesection-v2=pdp-sizesection-v2; EXP_plp-quick-filters=variant1; EXP_quick-view=quick-view-visible; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQpYosMQotVM6UAQAAVO9W8w1oxkB+BHu0I4lVSkF0UEF2JpdCwGUujZpRbrddL0uKyl8UVFJXrRWpgOdUcMvM4RmuO4sRKTQnaIEBvZsOfrOkwQSa2tWgR5se+yb2PlKUGbgU9tgpy3BzyNmXamTMU3wMTTfOIDoVoysMUBzj0DhtGYXP1UceSJeVjZ/nvXv2/fWkjibZDSO4rZEtNuLdhGXJykMvbhsHA03hOt9Ig0bftGNDnDg7MWRdzFQGVF1Yj8MkdYSR9NVIyVKzXC8imEoxPSEp7k+wcOcOZmxB4RVKAUqMq3InSSaJPN4M/OojuS4Ronfq1kjQKHzXJLSMggxNQiY3850s+L2J4zqvURanH+t7w7kGeazDEo4ZwGE5CkXN4N1bU9u586hJ67v0YOWbHpsEI1ACRziBUxLR3iU+YKM1uOiNY5GOxta0OhccNqGeFqcT9JNg8FRnay1rCa25kxYNYs7vpbGgxIClt00DTs6KsvdkejUstiCJ+qEPpNKanyGpjj6IMsOXetQK57E+nWwCf5/04uA=~0~-1~1739251217; bcookie=3f88050b-d273-4ac9-a7e5-1aeddaa0f2a8; bm_sz=1C644CBDFCD0C345AE7DE52AF187F1CE~YAAQpYosMQstVM6UAQAAVO9W8xrd7kRJm6JPxpr5tVp7YQHV6z/MKJ5pnQs/j8fg8b/lDtr4HEne3AupBiHiwuoWJGd0fo8Uda6CMnpTsMsowoXu2tuIzW76b6Q30QKNMIf6hm8pYaaiBLS4h44bvaeSOnvUCWl5AYqVjuOKpR3iDY1RpE7GMy07ci4nIjOGnPx20Ui7NhMFytPFNmbW6YpX+5QUJz+VLjXfsPKch8Ff5yP6sR8rtgRmifsD3xFW5F0T58izKQY2htMaeyd3FxhnUfqpMAm4uA2Av8iHSNmf35NspO1HYjGJKXwwL2KuQkh3RkM7F5pIip0shv6ECPNVKz90elNVUrcte4Gd7zbqf3I4noX1dWGVLCN+KPOiEbx/N2o942i5+ZKtmbbg2ghOAVw0t574JNIgsq3Jq6UiEAnocn9/mJAqOLjH/KpAVYEow/pC02uocU+ylK156Ndl17dfSO5yHw==~4403769~4602165',
#                     'pragma': 'no-cache',
#                     'priority': 'u=0, i',
#                     'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#                     'sec-ch-ua-mobile': '?0',
#                     'sec-ch-ua-platform': '"Windows"',
#                     'sec-fetch-dest': 'document',
#                     'sec-fetch-mode': 'navigate',
#                     'sec-fetch-site': 'none',
#                     'sec-fetch-user': '?1',
#                     'upgrade-insecure-requests': '1',
#                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
#                 }
#                 yield scrapy.Request(url=product_url, headers=headers,
#                                      meta={"product_url": product_url, "product_name": product_name,
#                                            "product_id": product_id,
#                                            "images_urls": images_urls, "mrp": mrp,
#                                            "price": price, "discount": discount, "size_chart": size_chart,
#                                            # "category_id": category_id,
#                                            "hash_id": hash_id,
#                                            "colour": colour,
#                                            "tags": tags}, dont_filter=True, callback=self.parse)
#
#     def parse(self, response, **kwargs):
#         product_url = response.meta.get('product_url')
#         category_id = response.meta.get('category_id')
#         hash_id = response.meta.get('hash_id')
#         product_id = response.meta.get('product_id')
#         image_url = response.meta.get('images_urls')
#         price = response.meta.get('price')
#
#         # Todo: page save
#         try:
#             os.makedirs(self.pagesave, exist_ok=True)
#             main_path = f'{self.pagesave}{hash_id}.html.gz'
#             if not os.path.exists(main_path):
#                 with gzip.open(main_path, "wb") as f:
#                     f.write(response.text.encode('utf-8'))
#                 print(f"page save for this {product_id}")
#         except Exception as e:
#             print(e)
#
#         item = NykaaPdpDataItem()
#         breadcrumb = [i.strip() for i in response.xpath("//a[@class='css-1vilo37']/text()").getall()]
#         # item['category_id'] = category_id
#         item['pagesave_id'] = hash_id
#         item['Category'] = breadcrumb[1]
#         # item['product_id'] = product_id
#         item['Sub Category'] = breadcrumb[-1]
#         item['Brand'] = response.xpath("//h1[@data-at='product-name']/a/text()").get('').strip()
#         item['Url'] = product_url
#         item['Product Name'] = response.xpath("//h1[@data-at='product-name']/span/text()").get('').strip()
#         item['Image Url'] = " | ".join(
#             response.xpath("//img[contains(@class,'pdp-selector-img')]/@src").getall()) if response.xpath(
#             "//img[contains(@class,'pdp-selector-img')]/@src").getall() else image_url
#         item['Star'] = self.get_star(response)
#
#         item['Rating'] = self.get_rating(response)
#
#         item['Price'] = response.xpath("//div[contains(@class,'mrp-label')]//span[@class='css-5pw8k6']/text()").get(
#             '').replace(',', '')
#
#         if not item['Price']:
#             item['Price'] = response.xpath("//span[@class='css-1byl9fj']/text()").get().replace(',', '')
#
#         item['Discounted price'] = response.xpath("//span[@class=' css-1byl9fj']/text()").get('').replace(',', '')
#
#         if not item['Discounted price']:
#             item['Discounted price'] = item['Price']
#
#         item['color'] = response.xpath("//div[@data-at='color-shade']/text()").get('').strip()
#
#         item['Size'] = response.meta.get('size_chart')
#
#         item['Fabric'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Material')]/following-sibling::p/text()").get('').strip()
#
#         item['Occasion'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Occasion')]/following-sibling::p/text()").get('').strip()
#
#         item['Neckline'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Neckline')]/following-sibling::p/text()").get('').strip()
#
#         item['Type of Work'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Type of Work')]/following-sibling::p/text()").get(
#             '').strip()
#
#         item['Leg Style'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Leg Style')]/following-sibling::p/text()").get('').strip()
#
#         item['Sets Subcategory'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Sets Subcategory')]/following-sibling::p/text()").get(
#             '').strip()
#
#         item['Salwar Suits & Sets Subcategory'] = item['Sets Subcategory']
#
#         item['Sleeve Style'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Sleeve Style')]/following-sibling::p/text()").get(
#             '').strip()
#
#         item['Pattern'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Pattern')]/following-sibling::p/text()").get('').strip()
#
#         item['Fit'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Fit')]/following-sibling::p/text()").get('').strip()
#
#         item['Pack contains'] = response.xpath(
#             "//div[contains(text(),'Pack contains')]/following-sibling::*/text()").get('').strip()
#
#         item['Pack Size'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Pack Size')]/following-sibling::p/text()").get('').strip()
#
#         if not item['Pack Size']:
#             item['Pack Size'] = item['Pack contains']
#
#         item['Closure'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Closure')]/following-sibling::p/text()").get('').strip()
#
#         item['Rise Style'] = response.xpath(
#             "//div[@class='css-134y3ft']/p[contains(text(),'Rise Style')]/following-sibling::p/text()").get('').strip()
#
#         item['Care instructions'] = response.xpath(
#             "//div[contains(text(),'Care instructions')]/following-sibling::div[@class='css-1obcna']/text()").get(
#             '').strip()
#
#         item['Description'] = response.xpath("//div[@class='css-1392ehc']//div[@class='css-1obcna']/text()").get(
#             '').strip()
#
#         item['Promotion tag'] = " | ".join(
#             response.xpath("//span[@class='css-fcdoej']/text()").getall()) if response.xpath(
#             "//span[@class='css-fcdoej']/text()") else response.meta.get('tags')
#
#         item['hash_id'] = str(
#             int(hashlib.md5(bytes(
#                 str(item['Category'] + item['Sub Category'] + item['Brand'] + item['Url']), "utf8")).hexdigest(),
#                 16) % (
#                     10 ** 10))
#
#         item['Offer'] = self.get_offer(product_id, item['Price'], item['Discounted price'])
#
#         item['pagesave_id'] = hash_id
#
#         yield item
#
#
# if __name__ == '__main__':
#     cmdline.execute(f"scrapy crawl {ExtractPdpDataSpider.name} -a start=173 -a end=173".split())
