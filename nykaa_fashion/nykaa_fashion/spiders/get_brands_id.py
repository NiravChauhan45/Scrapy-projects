import hashlib
import json
from datetime import datetime
import mysql.connector
import scrapy
from scrapy import cmdline
from nykaa_fashion.items import NykaaCatItemBrandId

from nykaa_fashion.config.database_config import ConfigDatabase


class GetBrandsIdSpider(scrapy.Spider):
    name = "get_brands_id"
    allowed_domains = ["www.nykaa.com"]
    start_urls = ["https://www.nykaa.com"]

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="nykaa_fashion"
    )

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.today_date = datetime.now().strftime('%d_%m_%Y')
        self.db = ConfigDatabase(database="nykaa_fashion", table='new_category_links')  # cat_links

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'}, start=self.start,
                                              end=self.end)
        for result in results:
            main_category_name = result['main_category_name']
            category_id = result['category_id']
            category_name = result['category_name']
            sub_category_name = result['sub_category_name']
            sub_category_id = result['sub_category_id']
            sub_category_url = result['sub_category_url']
            hash_id = result['hash_id']
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'cookie': 'bcookie=64632cb1-b42a-4183-a718-b45b7e06a5fa; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739857170367; rum_abMwebSort=47; _gcl_au=1.1.1529669365.1739857171; PHPSESSID=5e3bec16f8d04e5cb5c34bff7266e306; NYK_VISIT=64632cb1-b42a-4183-a718-b45b7e06a5fa~1739857170979; WZRK_G=454ed4bf23e14d36862ed8003e651e0e; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; _clck=o7yi1n%7C2%7Cftj%7C0%7C1875; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; _gid=GA1.2.1076706932.1739857266; _pin_unauth=dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ; __stdf=MA==; form_key=LbTc1NQwomowFttR; __stgeo=IjAi; __stbpnenable=MQ==; _fbp=fb.1.1739857266632.49241544539590200; AMCVS_FE9A65E655E6E38A7F000101%40AdobeOrg=1; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C20138%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1740463903%7C12%7CMCAAMB-1740463903%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739866303s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_cc=true; __stp=eyJ2aXNpdCI6InJldHVybmluZyIsInV1aWQiOiIwYjJlZWU3MS0zZjIwLTRhMDMtOGM2ZC0xOTAzNGRjZjlhZjQifQ==; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; CurrencyCode=INR; _ga=GA1.1.556808966.1739857225; s_nr=1739859134331-Repeat; mage-messages=; section_data_ids=%7B%7D; bm_sz=ECAD1B3A5A2AFB7DA68EED69B3C878C5~YAAQTHLBF3d34ASVAQAAIozzFxoqqvr9hj9KWHymx9cOPmW5kAweLqvzfe85LGILiNxmmxIQo3d3j1OX/BTbtHW+TSGgVF/gjc6RxqUQV3wfmOIUZE7xpS2yJPhcNlYJMavhL/ViGyX0dkZbz8lR4Au6F+tWSZ3sZDcUNQT1WfrDIDTb8OJnexmBeuLdM9zKEfU6uPEhUH2R7p3hVuhkui01QTDvs9UCUNHQhFalfH6ybbRRIiawX+ll2jv1jlXsePV3I2qG7QjrhfR8FasVcy9UiHrMdABRJNVd4YIFpNOH4kdYRnBc9NbySs+0gYmP/rCUidMHVoYebG7onlhMd0C8Aapa4UyfIMM2KcqpemCaoQET1WYBGtPgCAs79YaVP5o3evTA9JZahL7pQO6scVmt4desjMSdc0k556KWId2rYrOYWSCzzcBR6JkR+rT4wEc9pgPlGrxZNZipp5aXM9zDefS612bfonDEHXGR5qBT8RkqU+Svl3Ix/KZnfTpM8NSFfkVr6xQqQ7LSPqRKipVe+oUt6mjeh/3gL9SU8bxZYlk=~3687746~3355972; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQTHLBF+154ASVAQAAUI7zFw0rzTB7GfQyaRnzb92uVsZs2PSfD44ax45mpA+XAhf9ka5rT8Zzc6UvplWhmh5rVGayZV1JuauBS06aN1041keH58co415+Qk+K1R4ff16o6PFGJioJwc8qP6W9MJYII7Zt0+QVVy3PQwPO+4R8aAlqXiUdcnWgjAZucyRHxGZNWSeXC/psmpp0+4zWf8USXE6d4vLJoVR1eTYaDiJwlQH2165JUfEliFU6Y+VRZD3pb3oRaeQGDrEb4WhQgIHmA6dBd1xhOpAtzpLFApXIHx8jZzS4sozDfXn+IkfmwEujc8ffCwOt6egP8Yc4Z0F+kVXHCPlFNXDoynT4lcHqPSltkXx/4Dig9aF5Yf8XHbJhQUrX3L0cRbtd76IQM8tOpqtSiOkGvnQEqHABaJ82an0sYi+uh387y0UnnmAiTdK57jn8RhwI5rWMSXtDp849MNyLP6fWDEa95oKTXHZXpo0U+m7teg+6PrtFbGWMHsYxyqX5gyToG932/TT8u0oNKni1p1BxXjNC1ia+4g==~-1~-1~1739866356; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A5%2C%22s%22%3A1739863552%2C%22t%22%3A1739863464%7D; NYK_PCOUNTER=45; _clsk=1ff9w0h%7C1739863476540%7C18%7C0%7Ck.clarity.ms%2Fcollect; _ga_DZ4MXZBLKH=GS1.1.1739857224.1.1.1739863476.8.0.0; EXP_new-relic-client=variant1; NYK_ECOUNTER=1399; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; EXP_new-relic-client=variant1; EXP_pdp-brandbook=pdp-brandbook-a; EXP_pdp-sizesection-v2=pdp-sizesection-v2; EXP_plp-quick-filters=variant1; EXP_quick-view=quick-view-visible; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~-1~YAAQTHLBF5CT4gSVAQAAbnv1Fw2CgJ2OA5k3l2H0vK+EQ5r9rO7lJVh6dqQhF3cmygoT57LVFuW9Z9Y5gVVxCVeuM7/x6/oALAUepSBIqe8Qt9PYHezJZ+c0CqdDunH8P2p9E6IA33KR4X4CPMhdZ/jfBpQ1TfsVYJqakMFRZuNUzMXEN86o+IX02P6vvzAYelzbkBkkbmB6baGrkDriLc7FXCyC3PiqDz4qbGtG8KmcFLaW1uuMShq+fjn6kp1LJwcVe3iXvGSLX77hZW4xgZHn1WgsvkbfHJhI3oS7GcyhR+Dz9/XuE6wWY8Umqcm45U4OOdaSMw6ab55SsyBODQhyWivLcUw0hu/zYCtcB0SYSV8YGFgT59Cuq6hCdJl3nuql6FyhKwPo2Vx6HVEc2lmvFJ75I50Da83AdCGTqF9ArLd/yW1eLXa9SC4yfpXOG2cNXme+DL/L8+JbVZMlgGkESisLKozYpligd9i2hZ9ZkWf3Yi5eoppgOlwa2n/Cp+1ptH+YkxGb/HCbMXNb2yFI62jbG59ibxKqt74tyg==~0~-1~1739866356; bcookie=64632cb1-b42a-4183-a718-b45b7e06a5fa; bm_sz=ECAD1B3A5A2AFB7DA68EED69B3C878C5~YAAQTHLBF5GT4gSVAQAAbnv1FxojPNy1T8cYY68LYWV00URxRx3clxu+F3uftr7Cp9UUf/2qRTPeIBUm8JyH6lrkUGsKxm46O9vDNUyYmzAzZlpDZeJLxmbz8fhJoT3Dg6Dw4oUGOvmt12akZrXvwWizJSPGeuB9zUopm43NLzjwxOmfUC/UVrvUIlkPruLuD5K0nUYXbfiqfEdZD1FRxyjvBsCJxQYoJNfFVSy3PXx0TNMA9Vu9ikzqV5wltMBgzlRzzknLX/3aWnHiUeTZYAN0ORq1s7l1GNbiKslJSWyD/U+QwpT6K9Dmu8Y0PiCybxjFNiR4MkWwrd952T5/WD5ayv1H2oGtVVAvfi4r52xtSxeFOMoD6gZZM6ImliTFEUvdXVbZU1lm3ucF6nYu7ICK6V8br/IcwoUIHIl+MdzQrVsJpGIHv6ATLjGslYCWe73cdLl9N0n3e+VuEYsGkDVfpP5QeXda3n/mRHU9xxFq1+/ubB1Q8BSRDXJWPMgPXjE0xN67BEr4dgbLQMnY9YEGAguhAhOs0dhd7bB9byu3SIM=~3687746~3355972',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
            }
            yield scrapy.Request(url=sub_category_url, headers=headers, callback=self.parse, dont_filter=True,
                                 meta={"main_category_name": main_category_name,
                                       'category_id': category_id,
                                       "category_name": category_name,
                                       "sub_category_name": sub_category_name,
                                       "sub_category_id": sub_category_id,
                                       "sub_category_url": sub_category_url,
                                       "hash_id": hash_id,
                                       "url": sub_category_url})

    def parse(self, response, **kwargs):
        main_category_name = response.meta['main_category_name']
        category_id = response.meta['category_id']
        category_name = response.meta['category_name']
        sub_category_name = response.meta['sub_category_name']
        sub_category_id = response.meta['sub_category_id']
        sub_category_url = response.meta['sub_category_url']
        old_hash_id = response.meta.get('hash_id')

        json_data = json.loads(response.xpath("//script[@id='__PRELOADED_STATE__']/text()").get())
        brand_list = json_data.get('listingV2').get('filters')
        for filter_data in brand_list:
            item = NykaaCatItemBrandId()
            if filter_data.get('key') == "brand_filter":
                for brand in filter_data.get('values'):
                    brand_id = brand.get('id')
                    brand_name = brand.get('name')
                    product_count = brand.get('productCount')
                    item['main_category_name'] = main_category_name
                    item['category_id'] = category_id
                    item['category_name'] = category_name
                    item['sub_category_name'] = sub_category_name
                    item['sub_category_id'] = sub_category_id
                    item['sub_category_url'] = sub_category_url
                    item['brand_id'] = brand_id
                    item['brand_name'] = brand_name
                    item['product_count'] = product_count
                    item['hash_id'] = str(
                        int(hashlib.md5(
                            bytes(str(item['main_category_name']) + str(item['category_name']) + str(
                                item['sub_category_name']) + str(brand_id),
                                  "utf8")).hexdigest(),
                            16) % (
                                10 ** 10))
                    yield item
        mycursor = self.conn.cursor()
        sql = f"UPDATE new_category_links SET status = 'Done' WHERE hash_id = {old_hash_id}"
        mycursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {GetBrandsIdSpider.name} -a start=1 -a end=40".split())
