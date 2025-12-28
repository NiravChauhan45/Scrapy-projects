# import hashlib
# import json
# import os
# import re
# from datetime import datetime
# from typing import Iterable
# import requests
#
# import requests
# import scrapy
# from parsel import Selector
# from scrapy import Request, cmdline
# from nykaa_fashion.items import NykaaFashionItem
#
#
# class GetLinksSpider(scrapy.Spider):
#     name = "get_pdp_data"
#
#     def get_response(self, requests_product_url):
#         cookies = {
#             'bcookie': '3c904978-9c87-492e-9705-bfca55f114ff',
#             'EXP_plp-quick-filters': 'variant1',
#             'EXP_pdp-sizesection-v2': 'pdp-sizesection-v2',
#             'tm_stmp': '1738908703092',
#             'rum_abMwebSort': '36',
#             'EXP_pdp-brandbook': 'pdp-brandbook-a',
#             'EXP_quick-view': 'quick-view-visible',
#             'PHPSESSID': 'fb3e9a0b1cb044bb93b2598c3b70838d',
#             'EXP_SSR_CACHE': 'e73a4ec92663a42c1f6f9a846b433544',
#             '_gcl_au': '1.1.1428334476.1738908704',
#             'NYK_VISIT': '3c904978-9c87-492e-9705-bfca55f114ff~1738908703766',
#             'WZRK_G': 'e1640d66fbbc4efba95390583789b9e8',
#             '_clck': '102ifvm%7C2%7Cft8%7C0%7C1864',
#             'mage-messages': '%5B%5D',
#             '_gid': 'GA1.2.514694034.1738909263',
#             '_fbp': 'fb.1.1738909265491.324093250967041491',
#             '__stgeo': 'IjAi',
#             '__stbpnenable': 'MQ==',
#             '__stdf': 'MA==',
#             '_gcl_gs': '2.1.k1$i1738913459$u8179629',
#             '_gcl_aw': 'GCL.1738913469.CjwKCAiA2JG9BhAuEiwAH_zf3pkTmxw14Y4ys0OvrkyvDIslFRhvaRX73j8l-I5v-amWQ0iezHaaMRoCTJoQAvD_BwE',
#             'mp_0cd3b66d1a18575ebe299806e286685f_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22%24device_id%22%3A%20%22194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22entry_page_product_id%22%3A%20%2213344864%22%2C%22entry_page_type%22%3A%20%22pdp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D',
#             '_ga': 'GA1.1.834599270.1738908704',
#             'AMCVS_FE9A65E655E6E38A7F000101%40AdobeOrg': '1',
#             'AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg': '-1303530583%7CMCIDTS%7C20127%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1739525548%7C7%7CMCAAMB-1739525548%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1738927948s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0',
#             's_nr': '1738920748795-Repeat',
#             's_cc': 'true',
#             '_pin_unauth': 'dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ',
#             '__stp': 'eyJ2aXNpdCI6InJldHVybmluZyIsInV1aWQiOiI1OGExMzhjMS1lMmU0LTQ1ZjMtYjcxMi1lZTM4ZWJiMzMxNGIifQ==',
#             '__sts': 'eyJzaWQiOjE3Mzg5MjA3NDk2NzksInR4IjoxNzM4OTIwNzQ5Njc5LCJ1cmwiOiJodHRwcyUzQSUyRiUyRnd3dy5ueWthYWZhc2hpb24uY29tJTJGcCUyRjE0MjkyNTE5IiwicGV0IjoxNzM4OTIwNzQ5Njc5LCJzZXQiOjE3Mzg5MjA3NDk2Nzl9',
#             'bm_sz': 'D5FD0B6DD3C97C6B81B123E8D4B2F773~YAAQbUdYaO1vuNuUAQAAMSPV3xq2iYR59ywfN7/emXiDgSTfNwiy2ONhxfcpsR2914sBg2HdvItCegYJyvcRdzibtx9H+SWIUUKwRsDoYjuecu1ADI8DYGvNcGySzXEmSq3SIAtxavCDhI++/LDK3FCpMv+s3G0ZXDAK4tC0hVmsxSLaCTEgmlDRAxWWMKA7dhUJzVJftdQS8aPqJ+c8upzx4rPgITNcQ0lWDRxqhWr+vv9GOR3VvIh85Yexv4aTc2sX+ph1vT1ggrVbd+nKnkMNm+dA4FXZhn0AbFRS5Q13Ebcb8VGQ1kAuG5KWwJapJKuPEj+Mem7KHHUDfMwIfaJPKLXJHCW+nDQGY+IDSLShxmfqq5xdoS7ibF/0ShvNsdGWfo0NcChnbeWC/TNygIuLlZhIz506cRgS/IhiyvlQjUoCNk86V9qEgWMIYNV0VUTN/J1wDdeYQ/Vh5sAJHYnQjQlwINvlx3w1T+dKl9Ae5XRDbjR6O/zna2B4CwExyRK0h5YYv5FmMVFSdQkjXoJBRGpapBeKLT56/P91yi6wMCs/tViqDg70/Cg+/bdYZeRl5xdIozCYc2eGW7lx~4404790~3556656',
#             '_ga_DZ4MXZBLKH': 'GS1.1.1738908703.1.1.1738921934.59.0.0',
#             'NYK_PCOUNTER': '88',
#             'NYK_ECOUNTER': '2562',
#             'WZRK_S_WRK-4W9-R55Z': '%7B%22p%22%3A38%2C%22s%22%3A1738918272%2C%22t%22%3A1738921935%7D',
#             '_abck': '3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQbUdYaPZvuNuUAQAA+yvV3w0Bb+lN/2EhlOKE6dMJQS1uVAx3B8twNWGrzgcCtbdhMvk1fO4F+I8iQ/OR7vjHfQAzfPndU3uAmU6NgFvRHNB/ssZAR41qPZDQtMMFIs/Lv0umHh8fUQjS7zTcbHrOPKF2cE558Cx1loMtZ197u9HUFlmRhoYyTPimLkXO+rLbUkfNhn7mvWM3nrnwBx0tWC5Akc7ONl/DUwHSKsNwfjvZMQKTUlVkj8Z21/o1x6aYpCWvxOwkofl3OtqDTvcZnEMu3AveICfH+OKTTi5ZOQ3JMuVDNNKi/bBBwx1mbyZGRpgINTjT7UfQbHj3IbbrUYNt9pW8t+orrOeA6S2LGc4NBPiuCOh7mNg8j8C0r9hf3FPef/JaIE631qJ7H/4TyEVfL1vpPxvPJLKDOm7XQoQJwsUy6o+15fQRfNDuDQP1/zxCybdt+MaTR7kgBqqu7yl0o0aRh1VbjQtKzoEzG6nfU3ppfcWGL8is5FGctfo3W8j428cgNBKVIhNm~-1~||0||~1738923670',
#             '_clsk': '1boqk9q%7C1738921935888%7C67%7C0%7Ck.clarity.ms%2Fcollect',
#         }
#         headers = {
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             'accept-language': 'en-US,en;q=0.9',
#             'cache-control': 'no-cache',
#             # 'cookie': 'bcookie=3c904978-9c87-492e-9705-bfca55f114ff; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1738908703092; rum_abMwebSort=36; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; PHPSESSID=fb3e9a0b1cb044bb93b2598c3b70838d; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; _gcl_au=1.1.1428334476.1738908704; NYK_VISIT=3c904978-9c87-492e-9705-bfca55f114ff~1738908703766; WZRK_G=e1640d66fbbc4efba95390583789b9e8; _clck=102ifvm%7C2%7Cft8%7C0%7C1864; mage-messages=%5B%5D; _gid=GA1.2.514694034.1738909263; _fbp=fb.1.1738909265491.324093250967041491; __stgeo=IjAi; __stbpnenable=MQ==; __stdf=MA==; _gcl_gs=2.1.k1$i1738913459$u8179629; _gcl_aw=GCL.1738913469.CjwKCAiA2JG9BhAuEiwAH_zf3pkTmxw14Y4ys0OvrkyvDIslFRhvaRX73j8l-I5v-amWQ0iezHaaMRoCTJoQAvD_BwE; mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22%24device_id%22%3A%20%22194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22entry_page_product_id%22%3A%20%2213344864%22%2C%22entry_page_type%22%3A%20%22pdp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; _ga=GA1.1.834599270.1738908704; AMCVS_FE9A65E655E6E38A7F000101%40AdobeOrg=1; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C20127%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1739525548%7C7%7CMCAAMB-1739525548%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1738927948s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_nr=1738920748795-Repeat; s_cc=true; _pin_unauth=dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ; __stp=eyJ2aXNpdCI6InJldHVybmluZyIsInV1aWQiOiI1OGExMzhjMS1lMmU0LTQ1ZjMtYjcxMi1lZTM4ZWJiMzMxNGIifQ==; __sts=eyJzaWQiOjE3Mzg5MjA3NDk2NzksInR4IjoxNzM4OTIwNzQ5Njc5LCJ1cmwiOiJodHRwcyUzQSUyRiUyRnd3dy5ueWthYWZhc2hpb24uY29tJTJGcCUyRjE0MjkyNTE5IiwicGV0IjoxNzM4OTIwNzQ5Njc5LCJzZXQiOjE3Mzg5MjA3NDk2Nzl9; bm_sz=D5FD0B6DD3C97C6B81B123E8D4B2F773~YAAQbUdYaO1vuNuUAQAAMSPV3xq2iYR59ywfN7/emXiDgSTfNwiy2ONhxfcpsR2914sBg2HdvItCegYJyvcRdzibtx9H+SWIUUKwRsDoYjuecu1ADI8DYGvNcGySzXEmSq3SIAtxavCDhI++/LDK3FCpMv+s3G0ZXDAK4tC0hVmsxSLaCTEgmlDRAxWWMKA7dhUJzVJftdQS8aPqJ+c8upzx4rPgITNcQ0lWDRxqhWr+vv9GOR3VvIh85Yexv4aTc2sX+ph1vT1ggrVbd+nKnkMNm+dA4FXZhn0AbFRS5Q13Ebcb8VGQ1kAuG5KWwJapJKuPEj+Mem7KHHUDfMwIfaJPKLXJHCW+nDQGY+IDSLShxmfqq5xdoS7ibF/0ShvNsdGWfo0NcChnbeWC/TNygIuLlZhIz506cRgS/IhiyvlQjUoCNk86V9qEgWMIYNV0VUTN/J1wDdeYQ/Vh5sAJHYnQjQlwINvlx3w1T+dKl9Ae5XRDbjR6O/zna2B4CwExyRK0h5YYv5FmMVFSdQkjXoJBRGpapBeKLT56/P91yi6wMCs/tViqDg70/Cg+/bdYZeRl5xdIozCYc2eGW7lx~4404790~3556656; _ga_DZ4MXZBLKH=GS1.1.1738908703.1.1.1738921934.59.0.0; NYK_PCOUNTER=88; NYK_ECOUNTER=2562; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A38%2C%22s%22%3A1738918272%2C%22t%22%3A1738921935%7D; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQbUdYaPZvuNuUAQAA+yvV3w0Bb+lN/2EhlOKE6dMJQS1uVAx3B8twNWGrzgcCtbdhMvk1fO4F+I8iQ/OR7vjHfQAzfPndU3uAmU6NgFvRHNB/ssZAR41qPZDQtMMFIs/Lv0umHh8fUQjS7zTcbHrOPKF2cE558Cx1loMtZ197u9HUFlmRhoYyTPimLkXO+rLbUkfNhn7mvWM3nrnwBx0tWC5Akc7ONl/DUwHSKsNwfjvZMQKTUlVkj8Z21/o1x6aYpCWvxOwkofl3OtqDTvcZnEMu3AveICfH+OKTTi5ZOQ3JMuVDNNKi/bBBwx1mbyZGRpgINTjT7UfQbHj3IbbrUYNt9pW8t+orrOeA6S2LGc4NBPiuCOh7mNg8j8C0r9hf3FPef/JaIE631qJ7H/4TyEVfL1vpPxvPJLKDOm7XQoQJwsUy6o+15fQRfNDuDQP1/zxCybdt+MaTR7kgBqqu7yl0o0aRh1VbjQtKzoEzG6nfU3ppfcWGL8is5FGctfo3W8j428cgNBKVIhNm~-1~||0||~1738923670; _clsk=1boqk9q%7C1738921935888%7C67%7C0%7Ck.clarity.ms%2Fcollect',
#             'pragma': 'no-cache',
#             'priority': 'u=0, i',
#             'referer': 'https://www.nykaafashion.com/woodland-mens-solid-full-sleeves-yellow-jacket/p/14292520',
#             'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'document',
#             'sec-fetch-mode': 'navigate',
#             'sec-fetch-site': 'same-origin',
#             'upgrade-insecure-requests': '1',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
#         }
#         response = requests.get(
#             requests_product_url,
#             cookies=cookies,
#             headers=headers,
#         )
#         today_date = datetime.now().strftime('%d_%m_%Y')
#         pagesave = f"F:\\Nirav\\Project_page_save\\nykaa_fashion\\{today_date}\\"
#
#         product_id = requests_product_url.split("/")[-1]
#         # page save
#         try:
#             os.makedirs(pagesave, exist_ok=True)
#             main_path = f'{pagesave}{product_id}.html'
#             if not os.path.exists(main_path):
#                 with open(main_path, "w", encoding="utf-8") as f:
#                     f.write(response.text)
#                 print(f"page save for this {product_id}")
#         except Exception as e:
#             print(e)
#         return Selector(text=response.text)
#
#     def get_variation_id(self, variation_id_lst):
#         variation = []
#         for id in variation_id_lst:
#             variation.append(id.get('id'))
#         return " | ".join(variation)
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
#     def remove_non_ascii(self, text):
#         return re.sub(r'[^\x00-\x7F]+', '', text).replace("\\r\\n", '').replace('\r\n', '').strip()
#
#     def remove_escape_characters(self, text):
#         cleaned_text = re.sub(r'\\[ntrbu]"', '', text)  # This will remove escaped newline, tab, etc.
#         return cleaned_text.replace('\n', ' ').replace("\\ud83d\\udc4d\\ud83d\\ude0e", '').replace("\ud83d\ude0a",
#                                                                                                    '').strip()
#
#     def get_content_of_reviews(self, product_id):
#         cookies = {
#             'bcookie': '3c904978-9c87-492e-9705-bfca55f114ff',
#             'EXP_plp-quick-filters': 'variant1',
#             'EXP_pdp-sizesection-v2': 'pdp-sizesection-v2',
#             'tm_stmp': '1738908703092',
#             'rum_abMwebSort': '36',
#             'EXP_pdp-brandbook': 'pdp-brandbook-a',
#             'EXP_quick-view': 'quick-view-visible',
#             'PHPSESSID': 'fb3e9a0b1cb044bb93b2598c3b70838d',
#             'EXP_SSR_CACHE': 'e73a4ec92663a42c1f6f9a846b433544',
#             '_gcl_au': '1.1.1428334476.1738908704',
#             'WZRK_G': 'e1640d66fbbc4efba95390583789b9e8',
#             '_clck': '102ifvm%7C2%7Cft8%7C0%7C1864',
#             'mage-messages': '%5B%5D',
#             '_gid': 'GA1.2.514694034.1738909263',
#             '_fbp': 'fb.1.1738909265491.324093250967041491',
#             '__stgeo': 'IjAi',
#             '__stbpnenable': 'MQ==',
#             '__stdf': 'MA==',
#             '_gcl_gs': '2.1.k1$i1738913459$u8179629',
#             '_gcl_aw': 'GCL.1738913469.CjwKCAiA2JG9BhAuEiwAH_zf3pkTmxw14Y4ys0OvrkyvDIslFRhvaRX73j8l-I5v-amWQ0iezHaaMRoCTJoQAvD_BwE',
#             'mp_0cd3b66d1a18575ebe299806e286685f_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22%24device_id%22%3A%20%22194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22entry_page_product_id%22%3A%20%2213344864%22%2C%22entry_page_type%22%3A%20%22pdp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D',
#             '_ga': 'GA1.1.834599270.1738908704',
#             'AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg': '-1303530583%7CMCIDTS%7C20127%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1739525548%7C7%7CMCAAMB-1739525548%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1738927948s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0',
#             's_nr': '1738920748795-Repeat',
#             '_pin_unauth': 'dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ',
#             '__stp': 'eyJ2aXNpdCI6InJldHVybmluZyIsInV1aWQiOiI1OGExMzhjMS1lMmU0LTQ1ZjMtYjcxMi1lZTM4ZWJiMzMxNGIifQ==',
#             'NYK_VISIT': '3c904978-9c87-492e-9705-bfca55f114ff~1738928950890',
#             'bm_sz': 'D5FD0B6DD3C97C6B81B123E8D4B2F773~YAAQinAsMcNqbt2UAQAAnjhY4BqA9lYDBr0kGJK/9SSWfCtRNw7oQOnvA9iJAoAKZK8YNkFpbSGVMbJ7JIDSQeuuC4UX8bhS6mwjnHaMqbq5qYUcKtGgQpnymqA2IP2b4bODKSwGsdw1yfltWzSQgHn12vK0L1PdVB4na/P57/0gKqGk9FVchuyJvJAkZSfsskzGjB5twNn9ARVOl4R4yFx0fAzP4MqKkLUkgChkUJa0SNLrGSEI2hQJMV0RetOWdsfkFRv8QRbmxeFT2i0UEPWpfUcyW9siDheRmbmBg8UHlpqrhD+9TIccseQBDNypU8GR2sNQ+0mPM+dPQToc9ai/95qdgTtpVse36xqNehAmH9YKI5PmWMzq6rt6f6kXukAwbKj4iTSiuKdG7unkNu5aRHBSlJQz1mRXd4LDAdfLPETPy035wxbyv1d79r33gOHp5FnXazbcjKK6ld6UFBcOlg9uRN+SYh4QwEjuWXzm842QqgiF3zw0vmn3mjA8u8sd/Egob8FOoiDXJdgjuqCIpGw/cVg42+B01QMhBLcvFTlMJ4Vi3dDjeZC7rzJl011qUuhVpY2EnSVdx04YuY2/hEkiNASlrbr2loRBVwwFCA==~4404790~3556656',
#             'NYK_PCOUNTER': '5',
#             'NYK_ECOUNTER': '14',
#             '_ga_DZ4MXZBLKH': 'GS1.1.1738928951.3.1.1738930525.7.0.0',
#             '_clsk': 'tg8nkk%7C1738930527319%7C22%7C0%7Ck.clarity.ms%2Fcollect',
#             'WZRK_S_WRK-4W9-R55Z': '%7B%22p%22%3A3%2C%22s%22%3A1738930506%2C%22t%22%3A1738930646%7D',
#             '_abck': '3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQpYosMYyA8syUAQAA+h9a4A3fjXiMmpRNw0vRt7ECFb0stl297rN3MzuKpEL+37s9K4BNeJJCX2uE+CulWHhLAX+f1kVNLEQH6/3SgoFim8sNEaHDrs3YlNxLVANUnI+i8/t+2KnlYy3JjhsPamf8Z/uZFVhQDtZpRy9G0XKxe2p141jaDHi2t0Mjgl6B4VZUiJbJYSlmkWn1GWEdlTw0kkd1AfIZ4WKDE73ptIYXWNjBF67IycYFGOVs2mPgZtZxdglNvmSze3mjBN4rhGOiDe9DPFmgqkKqZbYUbEMztfBGBcBc+PX9gZHeSuH2o9acrkF74wqNgqVWFSqyuOJ59c/cQTd698KvUM+DcYuNWoroUfgWrZ2yxIBXXUBwyChcyJ+BPEiGswGjRq1AM2zfsiqpx+0abyaBLtL9+NONgoE6QSot2U1z8Z08NkWaVGGAxMSym5hGMFPR53AmbgIH/EIkUUk9GSPHzYuiCiHZTudrnSQCX+RrFnE8LZWe3Uer~-1~-1~1738931155',
#         }
#         headers = {
#             'accept': '*/*',
#             'accept-language': 'en-US,en;q=0.9',
#             'cache-control': 'no-cache',
#             # 'cookie': 'bcookie=3c904978-9c87-492e-9705-bfca55f114ff; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1738908703092; rum_abMwebSort=36; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; PHPSESSID=fb3e9a0b1cb044bb93b2598c3b70838d; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; _gcl_au=1.1.1428334476.1738908704; WZRK_G=e1640d66fbbc4efba95390583789b9e8; _clck=102ifvm%7C2%7Cft8%7C0%7C1864; mage-messages=%5B%5D; _gid=GA1.2.514694034.1738909263; _fbp=fb.1.1738909265491.324093250967041491; __stgeo=IjAi; __stbpnenable=MQ==; __stdf=MA==; _gcl_gs=2.1.k1$i1738913459$u8179629; _gcl_aw=GCL.1738913469.CjwKCAiA2JG9BhAuEiwAH_zf3pkTmxw14Y4ys0OvrkyvDIslFRhvaRX73j8l-I5v-amWQ0iezHaaMRoCTJoQAvD_BwE; mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22%24device_id%22%3A%20%22194df0abbc1556-0411b89edc729b-26011b51-e1000-194df0abbc1556%22%2C%22entry_page_product_id%22%3A%20%2213344864%22%2C%22entry_page_type%22%3A%20%22pdp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.nykaafashion.com%2Fmen%2Ftopwear%2Fc%2F6824%3Froot%3Dnav_3%26ptype%3Dlisting%252Cmen%252Ctopwear%252Cshop-all%252C3%252Cshop-all%26p%3D6%22%2C%22%24initial_referring_domain%22%3A%20%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; _ga=GA1.1.834599270.1738908704; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C20127%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1739525548%7C7%7CMCAAMB-1739525548%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1738927948s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_nr=1738920748795-Repeat; _pin_unauth=dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ; __stp=eyJ2aXNpdCI6InJldHVybmluZyIsInV1aWQiOiI1OGExMzhjMS1lMmU0LTQ1ZjMtYjcxMi1lZTM4ZWJiMzMxNGIifQ==; NYK_VISIT=3c904978-9c87-492e-9705-bfca55f114ff~1738928950890; bm_sz=D5FD0B6DD3C97C6B81B123E8D4B2F773~YAAQinAsMcNqbt2UAQAAnjhY4BqA9lYDBr0kGJK/9SSWfCtRNw7oQOnvA9iJAoAKZK8YNkFpbSGVMbJ7JIDSQeuuC4UX8bhS6mwjnHaMqbq5qYUcKtGgQpnymqA2IP2b4bODKSwGsdw1yfltWzSQgHn12vK0L1PdVB4na/P57/0gKqGk9FVchuyJvJAkZSfsskzGjB5twNn9ARVOl4R4yFx0fAzP4MqKkLUkgChkUJa0SNLrGSEI2hQJMV0RetOWdsfkFRv8QRbmxeFT2i0UEPWpfUcyW9siDheRmbmBg8UHlpqrhD+9TIccseQBDNypU8GR2sNQ+0mPM+dPQToc9ai/95qdgTtpVse36xqNehAmH9YKI5PmWMzq6rt6f6kXukAwbKj4iTSiuKdG7unkNu5aRHBSlJQz1mRXd4LDAdfLPETPy035wxbyv1d79r33gOHp5FnXazbcjKK6ld6UFBcOlg9uRN+SYh4QwEjuWXzm842QqgiF3zw0vmn3mjA8u8sd/Egob8FOoiDXJdgjuqCIpGw/cVg42+B01QMhBLcvFTlMJ4Vi3dDjeZC7rzJl011qUuhVpY2EnSVdx04YuY2/hEkiNASlrbr2loRBVwwFCA==~4404790~3556656; NYK_PCOUNTER=5; NYK_ECOUNTER=14; _ga_DZ4MXZBLKH=GS1.1.1738928951.3.1.1738930525.7.0.0; _clsk=tg8nkk%7C1738930527319%7C22%7C0%7Ck.clarity.ms%2Fcollect; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A3%2C%22s%22%3A1738930506%2C%22t%22%3A1738930646%7D; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQpYosMYyA8syUAQAA+h9a4A3fjXiMmpRNw0vRt7ECFb0stl297rN3MzuKpEL+37s9K4BNeJJCX2uE+CulWHhLAX+f1kVNLEQH6/3SgoFim8sNEaHDrs3YlNxLVANUnI+i8/t+2KnlYy3JjhsPamf8Z/uZFVhQDtZpRy9G0XKxe2p141jaDHi2t0Mjgl6B4VZUiJbJYSlmkWn1GWEdlTw0kkd1AfIZ4WKDE73ptIYXWNjBF67IycYFGOVs2mPgZtZxdglNvmSze3mjBN4rhGOiDe9DPFmgqkKqZbYUbEMztfBGBcBc+PX9gZHeSuH2o9acrkF74wqNgqVWFSqyuOJ59c/cQTd698KvUM+DcYuNWoroUfgWrZ2yxIBXXUBwyChcyJ+BPEiGswGjRq1AM2zfsiqpx+0abyaBLtL9+NONgoE6QSot2U1z8Z08NkWaVGGAxMSym5hGMFPR53AmbgIH/EIkUUk9GSPHzYuiCiHZTudrnSQCX+RrFnE8LZWe3Uer~-1~-1~1738931155',
#             'domain': 'NYKAA_FASHION',
#             'pragma': 'no-cache',
#             'priority': 'u=1, i',
#             'referer': 'https://www.nykaafashion.com/campus-sutra-mens-grey-zip-front-jacket-with-fleece-detail/p/13344864?all-reviews=1',
#             'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#             'sec-ch-ua-mobile': '?0',
#             'sec-ch-ua-platform': '"Windows"',
#             'sec-fetch-dest': 'empty',
#             'sec-fetch-mode': 'cors',
#             'sec-fetch-site': 'same-origin',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
#             'x-csrf-token': '6y85SbRl8Kahs5BU',
#         }
#         params = {
#             'product_id': product_id,
#             'fields': 'design_code,review_rating_json',
#             'platform': 'WEBSITE',
#         }
#         response = requests.get(
#             'https://www.nykaafashion.com/rest/appapi/V2/products/specific',
#             params=params,
#             cookies=cookies,
#             headers=headers,
#         )
#         selector = Selector(text=response.text)
#         json_data = json.loads(selector._text)
#         review_lst = json_data.get('response').get('product').get('review_rating_json').get('top_reviews')
#
#         review_list = []
#         for review in review_lst:
#             review_dict = {}
#             review_dict['name'] = review.get('nickname')
#             review_dict['title'] = review.get('title')
#             review_dict['detail'] = review.get('detail')
#             review_list.append(review_dict)
#         return json.dumps(review_list)
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
#     def start_requests(self):
#         url = f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop&categoryId=6824&currentPage=0"
#         headers = {
#             'domain': 'NYKAA_FASHION',
#             'sec-ch-ua-platform': '"Windows"',
#             'x-csrf-token': '6y85SbRl8Kahs5BU',
#             'Referer': 'https://www.nykaafashion.com/men/topwear/c/6824?root=nav_3&ptype=listing%2Cmen%2Ctopwear%2Cshop-all%2C3%2Cshop-all&p=3',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
#             'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#             'sec-ch-ua-mobile': '?0',
#             'Cookie': 'EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; EXP_new-relic-client=variant1; EXP_pdp-brandbook=pdp-brandbook-a; EXP_pdp-sizesection-v2=pdp-sizesection-v2; EXP_plp-quick-filters=variant1; EXP_quick-view=quick-view-visible; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQinAsMVElOd2UAQAACcFQ3w2/XvJFv9vzMcCXp7E7VIOZU4elTOHrAKNIk47iCl6Tn73GX5iOzc432aFfH7jNLhFkYrQswaBgMhTrYue/0ksigryDiNsprFmNB4m51BrBfSr3kXoJuvPuxNOQBd/41I53mcv3BdNMGJxTSaTs2vlwSG/AJY7Pvjec61+IV2PkNyf5sdWXW1poISIxVocGdq4UPmLSe7Yz62WBYl8RUPon7yKwxgAl674FweKHjaCzqs8Pp6LBj6Y8zZN4E9ssudKtnRkTgwSFMVMKy8u4FJ/E2TDuh4DAB/pSLIVg2y8P4YosFYldqx50S3tRwpqJqTa0ca3iXZRLwHFXQWF/ydkYF5SqWpD2S+PaxraonCSDetmC1a9X7D9QzHLglhrhWtolr2AXAzWF2vKWUPzu88G5/tz9RHDs/yNFWqCQcw/LgmoQY2gI5Bd42mcV5K4My9Q7K9I4GwzY7Dbi6bgj9bROeRxEfIXmkIP6Mzl1Mk2XCnf6OTDryDmcyZIfd5RYkxmsqGMzgjOTLA==~0~-1~1738916186; bcookie=3c904978-9c87-492e-9705-bfca55f114ff; bm_sz=F9F5BE4EB0D25E71352E386475F39B0C~YAAQpYosMemzwcyUAQAAw5g13xrwUGCklXd8J6HaOdVpd8ntT7nJONhOTrwy63l7UmsJ1BHD97SbGpC7P+HJrKiUpUT2Wk4mGf/otibVRkVa7vv8/KEyHHeIXdEAZYsFPXWoIXrUs6RAubjJlYUYzAa0c5fQmafV6Jj1NReGmcm47Jn5Pj2PqlJVFR/WT1sBsjK4dz95l8+6gWu5CBo8fOYHtg3eQAS43eKAYiJgD6i4fhAB+n8mcpLGHnntGbZHokpTw645/WXFgH8pUwhFwR3bYKrgpMVq6PJYNtDXB5I7+BxCertHCI6ysiDS39rj6KdFrAfT2Lk0f3/4DCeujD0JtXPuY4MakdpARFCKDHjt6oYAm6CeNFfFlkgkCi4JtR5I3ebTvi8ovnYReTu9sT2/xdZ16wUO7mSJk9SurtnATcq5JW0g705OudTfZj0POXig5YIoHe/I6Y9PeGL9aqfbv5Qd6I3RQB1XAMbSaRWjjDu61PHpzqBQVkHtccJos9JTWFC2gOe4KMrMyRUttSF6m/ll7w7qCLAs9lYEayH47eGrwPrnNJGdM090~3490886~3159094'
#         }
#         yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)
#
#     def parse(self, response, **kwargs):
#         global no_of_rating, content_of_reviews, no_of_reviews
#         json_data = json.loads(response.text)
#         products_lst = json_data.get('response').get('products')
#         for product_data in products_lst:
#             item = NykaaFashionItem()
#             product_url = "https://www.nykaafashion.com" + product_data.get('actionUrl')
#             # Todo: make_pdp_requests
#             selector = self.get_response(product_url)
#             product_name = product_data.get('title')
#             product_sub_name = product_data.get('subTitle')
#             product_id = product_data.get('id')
#             product_sku = product_data.get('sku')
#             image_url = product_data.get('imageUrl')
#             in_stock = "Available" if not product_data.get('isOutOfStock') else "Not Available"
#             description = self.get_description(selector)
#             image_urls = " | ".join(self.get_all_images(product_data))
#             mrp = product_data.get('price')
#             price = product_data.get('discountedPrice')
#             discount = product_data.get('discount')
#             variation = self.get_variation_id(product_data.get('plp_pdp_bridge').get('variants').get('size'))
#             rating = self.get_rating(selector)
#             try:
#                 no_of_rating_text = selector.xpath(
#                     "//h2[@data-at='customer-reviews']/following-sibling::*//p/text()").get(
#                     '').strip()
#                 no_of_rating = re.search(r'\d+', no_of_rating_text).group()
#             except:
#                 no_of_rating = 'NA'
#
#             reviews = 'NA'
#
#             try:
#                 content_of_reviews = self.get_content_of_reviews(product_id) if self.get_content_of_reviews(
#                     product_id) else "NA"
#                 no_of_reviews = len(json.loads(content_of_reviews)) if content_of_reviews else "NA"
#             except:
#                 ''
#             size_chart = self.get_size_chart(product_data.get('plp_pdp_bridge').get('variants').get('size'))
#             colour = product_data.get('sibling_colour_codes') if product_data.get('sibling_colour_codes') else "NA"
#
#             item['product_name'] = product_name
#             item['product_url'] = product_url
#             item['product_id'] = product_id
#             item['product_sku'] = product_sku
#             item['product_sub_name'] = product_sub_name
#             item['image_url'] = image_url
#             item['in_stock'] = in_stock
#             item['description'] = description
#             item['images_urls'] = image_urls
#             item['mrp'] = mrp
#             item['price'] = price
#             item['discount'] = discount
#             item['variation'] = variation
#             item['rating'] = rating if rating is not None else "NA"
#             item['no_of_rating'] = no_of_rating
#             item['reviews'] = reviews
#             item['no_of_reviews'] = no_of_reviews
#             item['content_of_reviews'] = content_of_reviews if content_of_reviews else "NA"
#             item['size_chart'] = size_chart
#             item['colour'] = colour
#             yield item
#
#         for i in range(1, 40):
#             url = f"https://www.nykaafashion.com/rest/appapi/V2/categories/products?PageSize=50&filter_format=v2&apiVersion=5&currency=INR&country_code=IN&deviceType=WEBSITE&sort=popularity&device_os=desktop&categoryId=6824&currentPage={i}"
#             headers = {
#                 'domain': 'NYKAA_FASHION',
#                 'sec-ch-ua-platform': '"Windows"',
#                 'x-csrf-token': '6y85SbRl8Kahs5BU',
#                 'Referer': 'https://www.nykaafashion.com/men/topwear/c/6824?root=nav_3&ptype=listing%2Cmen%2Ctopwear%2Cshop-all%2C3%2Cshop-all&p=3',
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
#                 'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
#                 'sec-ch-ua-mobile': '?0',
#                 'Cookie': 'EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; EXP_new-relic-client=variant1; EXP_pdp-brandbook=pdp-brandbook-a; EXP_pdp-sizesection-v2=pdp-sizesection-v2; EXP_plp-quick-filters=variant1; EXP_quick-view=quick-view-visible; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQinAsMVElOd2UAQAACcFQ3w2/XvJFv9vzMcCXp7E7VIOZU4elTOHrAKNIk47iCl6Tn73GX5iOzc432aFfH7jNLhFkYrQswaBgMhTrYue/0ksigryDiNsprFmNB4m51BrBfSr3kXoJuvPuxNOQBd/41I53mcv3BdNMGJxTSaTs2vlwSG/AJY7Pvjec61+IV2PkNyf5sdWXW1poISIxVocGdq4UPmLSe7Yz62WBYl8RUPon7yKwxgAl674FweKHjaCzqs8Pp6LBj6Y8zZN4E9ssudKtnRkTgwSFMVMKy8u4FJ/E2TDuh4DAB/pSLIVg2y8P4YosFYldqx50S3tRwpqJqTa0ca3iXZRLwHFXQWF/ydkYF5SqWpD2S+PaxraonCSDetmC1a9X7D9QzHLglhrhWtolr2AXAzWF2vKWUPzu88G5/tz9RHDs/yNFWqCQcw/LgmoQY2gI5Bd42mcV5K4My9Q7K9I4GwzY7Dbi6bgj9bROeRxEfIXmkIP6Mzl1Mk2XCnf6OTDryDmcyZIfd5RYkxmsqGMzgjOTLA==~0~-1~1738916186; bcookie=3c904978-9c87-492e-9705-bfca55f114ff; bm_sz=F9F5BE4EB0D25E71352E386475F39B0C~YAAQpYosMemzwcyUAQAAw5g13xrwUGCklXd8J6HaOdVpd8ntT7nJONhOTrwy63l7UmsJ1BHD97SbGpC7P+HJrKiUpUT2Wk4mGf/otibVRkVa7vv8/KEyHHeIXdEAZYsFPXWoIXrUs6RAubjJlYUYzAa0c5fQmafV6Jj1NReGmcm47Jn5Pj2PqlJVFR/WT1sBsjK4dz95l8+6gWu5CBo8fOYHtg3eQAS43eKAYiJgD6i4fhAB+n8mcpLGHnntGbZHokpTw645/WXFgH8pUwhFwR3bYKrgpMVq6PJYNtDXB5I7+BxCertHCI6ysiDS39rj6KdFrAfT2Lk0f3/4DCeujD0JtXPuY4MakdpARFCKDHjt6oYAm6CeNFfFlkgkCi4JtR5I3ebTvi8ovnYReTu9sT2/xdZ16wUO7mSJk9SurtnATcq5JW0g705OudTfZj0POXig5YIoHe/I6Y9PeGL9aqfbv5Qd6I3RQB1XAMbSaRWjjDu61PHpzqBQVkHtccJos9JTWFC2gOe4KMrMyRUttSF6m/ll7w7qCLAs9lYEayH47eGrwPrnNJGdM090~3490886~3159094'
#             }
#             yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)
#
#
# if __name__ == '__main__':
#     cmdline.execute(f"scrapy crawl {GetLinksSpider.name}".split())
