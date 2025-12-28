import json
from typing import Iterable, Any
from urllib.parse import urlencode
import scrapy
from numpy.distutils.conv_template import header
from scrapy import cmdline


class PlDataSpider(scrapy.Spider):
    name = "pl_data"
    allowed_domains = ["www.bigbasket.com"]

    # start_urls = ["https://www.bigbasket.com"]

    def start_requests(self):
        cookies = {
            '_bb_locSrc': 'default',
            'x-channel': 'web',
            '_bb_vid': 'NzczMzMwNjU0NzMyMjkyMzM0',
            '_bb_nhid': '7427',
            '_bb_dsid': '7427',
            '_bb_dsevid': '7427',
            '_bb_bhid': '',
            '_bb_loid': '',
            'csrftoken': 'QkQerY2z1ZCkDqJHIVAagLeQfMzDi4ne6iC9kXjNhcIgVX0FaN2zIOVQsUPPoXyJ',
            'isintegratedsa': 'true',
            'jentrycontextid': '10',
            'xentrycontextid': '10',
            'xentrycontext': 'bbnow',
            '_bb_bb2.0': '1',
            '_is_bb1.0_supported': '0',
            'is_integrated_sa': '1',
            'bb2_enabled': 'true',
            'ufi': '1',
            'adb': '0',
            'jarvis-id': '022d9e4d-fc6e-4f50-a1b0-8b59460a6c6b',
            '_gcl_au': '1.1.848610519.1750161314',
            '_gid': 'GA1.2.698776612.1750161354',
            '_client_version': '2843',
            'sessionid': 'b87757q7ppk9dbktvbisoj9ok2k1ihw2',
            '_bb_tc': '0',
            '_bb_rdt': '"MzEwNTg0NDE2Nw==.0"',
            '_bb_rd': '6',
            '_fbp': 'fb.1.1750161375374.941128944389918348',
            'bigbasket.com': '4887b5f7-0a2a-4b08-9a2c-64bd67e00abb',
            '_bb_lat_long': '"MTguOTM4NTM1Mnw3Mi44MzYzMzQ="',
            '_bb_cid': '4',
            '_bb_aid': '"MzAwNTUzOTIyMA=="',
            'is_global': '0',
            '_bb_addressinfo': 'MTguOTM4NTM1Mnw3Mi44MzYzMzR8Q2hoYXRyYXBhdGkgU2hpdmFqaSBUZXJtaW51cyBBcmVhfDQwMDAwMXxNdW1iYWl8MXxmYWxzZXx0cnVlfHRydWV8QmlnYmFza2V0ZWVy',
            '_bb_pin_code': '400001',
            '_bb_sa_ids': '10674',
            '_is_tobacco_enabled': '1',
            '_bb_cda_sa_info': 'djIuY2RhX3NhLjEwLjEwNjc0',
            'csurftoken': 'DnfW5w.NzczMzMwNjU0NzMyMjkyMzM0.1750162528284.QYUo0DAJfQcOKBPAN+t5prU45EP3u2PudkyrTgzwrvE=',
            '_bb_hid': '1833',
            '_sp_van_encom_hid': '1832',
            '_gat_UA-27455376-1': '1',
            '_gat_gtag_UA_27455376_1': '1',
            '_ga': 'GA1.2.2057859633.1750161341',
            '_ga_FRRYG5VKHX': 'GS2.1.s1750161340$o1$g1$t1750163664$j10$l0$h0',
            'ts': '2025-06-17%2018:04:24.576',
        }
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'common-client-static-version': '101',
            'content-type': 'application/json',
            'osmos-enabled': 'true',
            'priority': 'u=1, i',
            'referer': 'https://www.bigbasket.com/ps/?q=patanjali&nc=as&page=1&filter=%5B%7B%22name%22%3A%22Brands%22%2C%22type%22%3A%22brand%22%2C%22values%22%3A%5B%7B%22id%22%3A2586%2C%22name%22%3A%22Patanjali%22%2C%22image%22%3A%22%22%2C%22slug%22%3A%22patanjali%22%2C%22level%22%3A0%2C%22url%22%3A%22patanjali%22%2C%22is_selected%22%3Afalse%7D%5D%7D%5D',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'x-channel': 'BB-WEB',
            'x-entry-context': 'bbnow',
            'x-entry-context-id': '10',
            'x-tracker': '27c8bca4-b1b6-455b-b13f-07ae439faf4f',
            'cookie': '_bb_locSrc=default; x-channel=web; _bb_vid=NzczMzMwNjU0NzMyMjkyMzM0; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=QkQerY2z1ZCkDqJHIVAagLeQfMzDi4ne6iC9kXjNhcIgVX0FaN2zIOVQsUPPoXyJ; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; _is_bb1.0_supported=0; is_integrated_sa=1; bb2_enabled=true; ufi=1; adb=0; jarvis-id=022d9e4d-fc6e-4f50-a1b0-8b59460a6c6b; _gcl_au=1.1.848610519.1750161314; _gid=GA1.2.698776612.1750161354; _client_version=2843; sessionid=b87757q7ppk9dbktvbisoj9ok2k1ihw2; _bb_tc=0; _bb_rdt="MzEwNTg0NDE2Nw==.0"; _bb_rd=6; _fbp=fb.1.1750161375374.941128944389918348; bigbasket.com=4887b5f7-0a2a-4b08-9a2c-64bd67e00abb; _bb_lat_long="MTguOTM4NTM1Mnw3Mi44MzYzMzQ="; _bb_cid=4; _bb_aid="MzAwNTUzOTIyMA=="; is_global=0; _bb_addressinfo=MTguOTM4NTM1Mnw3Mi44MzYzMzR8Q2hoYXRyYXBhdGkgU2hpdmFqaSBUZXJtaW51cyBBcmVhfDQwMDAwMXxNdW1iYWl8MXxmYWxzZXx0cnVlfHRydWV8QmlnYmFza2V0ZWVy; _bb_pin_code=400001; _bb_sa_ids=10674; _is_tobacco_enabled=1; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjEwNjc0; csurftoken=DnfW5w.NzczMzMwNjU0NzMyMjkyMzM0.1750162528284.QYUo0DAJfQcOKBPAN+t5prU45EP3u2PudkyrTgzwrvE=; _bb_hid=1833; _sp_van_encom_hid=1832; _gat_UA-27455376-1=1; _gat_gtag_UA_27455376_1=1; _ga=GA1.2.2057859633.1750161341; _ga_FRRYG5VKHX=GS2.1.s1750161340$o1$g1$t1750163664$j10$l0$h0; ts=2025-06-17%2018:04:24.576',
        }
        brands = ['apis', 'colgate', 'dabur', 'frooti', 'glucon-d', 'good home', 'maaza', 'nihar', 'odonil', 'patanjali', 'real', 'tropicana']
        page_count = 1
        params = {
            'type': 'ps',
            'slug': 'patanjali',
            'page': f'{page_count}',
            'filters': '[{"name":"Brands","type":"brand","values":["patanjali"]}]',
        }
        url = 'https://www.bigbasket.com/listing-svc/v2/products'
        updated_url = f"{url}?{urlencode(params)}"
        yield scrapy.Request(
            url=updated_url,
            headers=headers,
            cookies=cookies,
            body=json.dumps(params),
            callback=self.parse,
            meta={"page_count":page_count},
            dont_filter=True
        )

    def parse(self, response, **kwargs):
        page_count = response.meta.get("page_count")
        json_data = json.loads(response.text)
        try:
            number_of_page = json_data['tabs'][0].get("product_info").get("number_of_pages")
            print(number_of_page)
        except:
            number_of_page = "N/A"

if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PlDataSpider.name}".split())
