import hashlib
import json
from typing import Iterable

import scrapy
from scrapy import cmdline, Request
from nykaa_fashion.config.database_config import ConfigDatabase
from nykaa_fashion.items import NykaaCategoryItem, NykaaCatItem


class CategoriesLinksSpider(scrapy.Spider):
    name = "cat_links"

    def start_requests(self):
        urls = ["https://www.nykaafashion.com/women/c/6557?root=topnav_1&f=category_filter%3D4497_",
                "https://www.nykaafashion.com/men/c/6823?root=topnav_1&f=category_filter%3D6826_"]
        for url in urls:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'cookie': 'bcookie=ea033885-0b2d-4e43-870d-ef31bc34ced6; EXP_plp-quick-filters=variant1; EXP_pdp-sizesection-v2=pdp-sizesection-v2; tm_stmp=1739448869414; rum_abMwebSort=8; EXP_pdp-brandbook=pdp-brandbook-a; EXP_quick-view=quick-view-visible; EXP_SSR_CACHE=e73a4ec92663a42c1f6f9a846b433544; PHPSESSID=aa20bc1c24b94827880a9e8d3118a3a8; _gcl_au=1.1.1461220228.1739448872; WZRK_G=a7b7fc6885d44ca2aa55b6c94b18633e; _clck=1jzunvf%7C2%7Cftf%7C0%7C1870; _gid=GA1.2.1145542768.1739537488; _pin_unauth=dWlkPVpHRXpNbU5pWVRJdE1HTTRNUzAwT0RVeUxXRmhPV0l0TVRFeVpqSTRNalZrWldNeQ; __stp=eyJ2aXNpdCI6Im5ldyIsInV1aWQiOiJjZGZjNTY5My03ZjgyLTQ2ZWUtYjQwZS1lMzhjNGY3MTBkMjgifQ==; __stdf=MA==; form_key=tRYe5TTTfUQkL2kH; __stgeo=IjAi; __stbpnenable=MQ==; _fbp=fb.1.1739537488650.699185177823263170; AMCVS_FE9A65E655E6E38A7F000101%40AdobeOrg=1; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C20134%7CMCMID%7C18915836392668149223411254796099779152%7CMCAAMLH-1740143694%7C12%7CMCAAMB-1740143694%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739546094s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_nr=1739538894468-New; s_cc=true; _ga=GA1.1.1635646680.1739448872; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; CurrencyCode=INR; mage-messages=; section_data_ids=%7B%7D; NYK_VISIT=ea033885-0b2d-4e43-870d-ef31bc34ced6~1739545762878; mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A194ff8495f0487-08864edcc5feed-26011b51-e1000-194ff8495f0487%22%2C%22%24device_id%22%3A%20%22194ff8495f0487-08864edcc5feed-26011b51-e1000-194ff8495f0487%22%2C%22entry_page_product_id%22%3A%20%2217486157%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22entry_page_type%22%3A%20%22plp%22%2C%22network_bandwidth%22%3A%20%224g%22%2C%22user_agent%22%3A%20%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F132.0.0.0%20Safari%2F537.36%22%7D; bm_sz=272012316C10893F56555A5D28644EA7~YAAQkawwF1IX9f6UAQAASCU4BRr77rN0Nod+cOel1nwPdGIZ0lgnOhDAxOFL/ZBxSyjekU1t6Ay8oWYSJEEF8ESby6hBIU4WkEPgpDBWHVQhmvF2ynFcEak/wAtDLyKDMYMMTDdYhDbb5vvwQ/4679IJMRP0pKtqEef9HV71f4x/8iR7UTlmco/dWY+c+WZpJ1DBUKV+A8CurMoLLcPhw1uYxgRyGkn+9aYF+bJ7JYmHg/AYU2/ZnhRt0i3lla785p4RkIpiNHJt2clmvTO0gWprPvLQJy9F8ZJTnTKCofqmuU5DmCLk5H0IqcKXsfCCWloqKexmw1sog5uH13DW5sQvPBIsuL29m6gJLVnz4tCXtFy5wKsB8IDy/chrq9SanNmXcbOdPrMtVjX3dF7K6XFs5W421cLw9dOiaNGSbCRbRI5kT5J4tIdlfvzX58ycgWBiDvhsaKLFwHXChEzwYb5pexI+oFCGF19KAINGn4dpmhHhxoGFkX41NPS07jqDlSlHHOYZ8ktfZPiv0D8ppi4gjtTHLKN8LF5qn/JgW2W0GLrIQh1BdVx9zic+uJBvJuEz8i+OpGh+NYKu3Qv0aQ==~4536112~4474438; NYK_PCOUNTER=36; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A36%2C%22s%22%3A1739545934%2C%22t%22%3A1739549150%7D; _abck=3DEB0D9E3B82CF02A4AB2A8D6AD6C2AE~0~YAAQkawwF8kY9f6UAQAAnjQ4BQ3g7CBcnQXreBQ4pC6Gacah2n1DT6fZ9SZ9F2j+WsgAwd68YYp09ZK5QFHa3GnhLpAIMv0a9EuI2Os5+xOvkfM85mhvR91UbMM1g1D9LvdUlW/yRM6hdtxRCFc299j4AeSQb2t4Xc77TB7rNMDqN0QSAS6VBaXTJa4THhxTWobuZ+0hJ+AZTG/CoCYkb5E0CrZ85dyqJU4LsYxVBtBaDLq4UHlA2HCh7Te2LxNYTcrljTUZZsLsEMtMobEYRbbK1NevMpPVs0d6UJyWvvgfWxAaRQhZE7SADnSM1zP9Fb1adX8K3ik5IuAhO/jmKvt1SGNnBc14pTp/AuUcha83TW7mhX049/tmM5+u7ZaYNjq2L2Z0td3zYqYvow0qM/4oPDwG0xlICbfMcFd6Yv6C7uOW3DaTLzoDH3QdgXlN3r53NXm3/0HghOrtbyO1/wybqsqFEMURh4o3vfq7ZJ7YfF7Mshr5DCznNTTG2VXQFJ2XWw==~-1~-1~1739549618; _clsk=niy44c%7C1739549186341%7C9%7C0%7Ck.clarity.ms%2Fcollect; _ga_DZ4MXZBLKH=GS1.1.1739545763.9.1.1739549186.23.0.0; NYK_ECOUNTER=651',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'referer': 'https://www.nykaafashion.com/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        item = NykaaCatItem()
        item['main_category_name'] = response.url.split('/c/')[0].split('/')[-1].strip()
        json_data = response.xpath("//script[@id='__PRELOADED_STATE__']/text()").get('').strip()
        if json_data:
            j_data = json.loads(json_data)
            category_list = j_data.get('listingV2').get('filters')
            for cat in category_list:
                if cat.get('title') == "Category":
                    if cat.get('values'):
                        for cat_data in cat.get('values'):
                            item['category_id'] = cat_data.get('id')
                            item['category_name'] = cat_data.get('name')
                            if cat_data.get('children'):
                                for sub_cat_data in cat_data.get('children'):
                                    item['sub_category_id'] = sub_cat_data.get('id')
                                    item['sub_category_name'] = sub_cat_data.get('name')
                                    item['sub_category_product_count'] = sub_cat_data.get('productCount')
                                    item['sub_category_url'] = f"https://www.nykaafashion.com/{item['main_category_name']}/{item['category_name']}/{item['sub_category_name']}/c/{item['sub_category_id']}"
                                    item['hash_id'] = str(
                                        int(hashlib.md5(
                                            bytes(str(item['main_category_name']) + str(
                                                item['category_name'] + item['sub_category_name']),
                                                  "utf8")).hexdigest(),
                                            16) % (
                                                10 ** 10))
                                    yield item


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {CategoriesLinksSpider.name}".split())
