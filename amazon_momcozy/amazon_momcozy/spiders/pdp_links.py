from typing import Iterable

import scrapy
from scrapy import cmdline, Request
from amazon_momcozy.config.database_config import ConfigDatabase


class PdpLinksSpider(scrapy.Spider):
    name = "pdp_links"

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.db = ConfigDatabase(database=f"amazon_momcozy", table='category_links')

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'}, start=self.start, end=self.end)
        for result in results:
            category_name = result['category_name']
            category_url = result['category_url']
            cookies = {
                'x-amz-captcha-1': '1740064659874893',
                'x-amz-captcha-2': 'odk+bw8e4WQAhUKpt2xPWA==',
                'session-id': '131-7967661-8597542',
                'session-id-time': '2082787201l',
                'i18n-prefs': 'USD',
                'sp-cdn': '"L5Z9:IN"',
                'ubid-main': '131-4199319-4736135',
                'regStatus': 'pre-register',
                'AMCV_7742037254C95E840A4C98A6%40AdobeOrg': '1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0',
                'session-token': 'h0Fj03eudFCKiSAcYCw4tZ+f7f5K/o3SRiu2g0TxON49Wp9zVhC+JTAH2nw7alWA+3EV25EMoBfU4OXAKMXTfJl5LL8JLz4D72OYF7M+UpauCqLCsmLUNevfY+b5wxQ3xtctJp/jKNUKDC8bNyK2aeBbblE4d1COxSw+V4htPrU83yzKjHt1SUtV+jszyFLfsRac/CDL6zroDyo3UCl+vaFysAT5WicP8fY0sf04qvh/q2dDReYV0pGqhapGJ15w+K8ZRvY1Kxb/3rvzmOdZZhIhZi4QzIeksHdb5RRSrzPYtKaIkFPqRZeyVX2dKYg/KVLFCgFhj7Rlbk+IId03PMmbFMJYRyqB',
                'csm-hit': 'tb:QCMD6DMT856DX06D796K+s-XEHBACSBMYC3KYRTR39G|1742458045034&t:1742458045034&adb:adblk_no',
            }
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'device-memory': '8',
                'downlink': '1.4',
                'dpr': '1.2000000000000002',
                'ect': '3g',
                'pragma': 'no-cache',
                'priority': 'u=0, i',
                'referer': 'https://www.amazon.com/stores/page/289B876A-CE6F-4247-9629-8AD6549CB51D',
                'rtt': '400',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'viewport-width': '1600',
                # 'cookie': 'x-amz-captcha-1=1740064659874893; x-amz-captcha-2=odk+bw8e4WQAhUKpt2xPWA==; session-id=131-7967661-8597542; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:IN"; ubid-main=131-4199319-4736135; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; session-token=h0Fj03eudFCKiSAcYCw4tZ+f7f5K/o3SRiu2g0TxON49Wp9zVhC+JTAH2nw7alWA+3EV25EMoBfU4OXAKMXTfJl5LL8JLz4D72OYF7M+UpauCqLCsmLUNevfY+b5wxQ3xtctJp/jKNUKDC8bNyK2aeBbblE4d1COxSw+V4htPrU83yzKjHt1SUtV+jszyFLfsRac/CDL6zroDyo3UCl+vaFysAT5WicP8fY0sf04qvh/q2dDReYV0pGqhapGJ15w+K8ZRvY1Kxb/3rvzmOdZZhIhZi4QzIeksHdb5RRSrzPYtKaIkFPqRZeyVX2dKYg/KVLFCgFhj7Rlbk+IId03PMmbFMJYRyqB; csm-hit=tb:QCMD6DMT856DX06D796K+s-XEHBACSBMYC3KYRTR39G|1742458045034&t:1742458045034&adb:adblk_no',
            }
            yield scrapy.Request(url=category_url, cookies=cookies, headers=headers, dont_filter=True)

    def parse(self, response, **kwargs):
        for data in response.xpath("//li[@data-testid='product-grid-item']"):
            product_url = 'https://www.amazon.com' + data.xpath("./div/a/@href").get()
            print(product_url)



if __name__ == '__main__':
    cmdline.execute(f'scrapy crawl {PdpLinksSpider.name} -a start=1 -a end=30'.split())
