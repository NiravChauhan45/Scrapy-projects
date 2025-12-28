from typing import Iterable

import scrapy
from scrapy import cmdline, Request
from amazon_momcozy.config.database_config import ConfigDatabase
from amazon_momcozy.items import AmazonMomcozyItem


class CategoryLinksSpider(scrapy.Spider):
    name = "category_links"

    def __init__(self, start, end, **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.end = end

    def start_requests(self):
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
            'session-token': 'DZnMC90yHJwlZnhm8aIY46NOZyvwW9oO7XSA/XzjIwjuXoipmqptraKBwzN1/SjFr/RVGSo2yPcgPs9Q3z0f7hsH4G81bhpHcenK1VT52WMWMZgiqc+PKvAlcYEB+zHmyAvlb73L/QDqu58cSuXgsL2tmCa6dKHAKcPNthskzHWB6gW9Ea8sgolPtezcAAR+nxNkweHbV6u3Jx3WvzV1zINnHjsMRp+/QdQWuWX2BJlaVZDZdWRTCJrf8RytA30DvHQXr2Ng28vGGKvI+H8Dyp1r4xDU9fmSGtA4r4K49amUrxrWqNqtJFr81voXDodM7EvXUd9nvUFtKgUDNRnZgxWZyIFHZ8X3',
            'csm-hit': 'tb:GT3XHP689CHB46DT25ZK+s-MNRZZXK9PSR67E8RYYR5|1742453940321&t:1742453940321&adb:adblk_no',
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
            'rtt': '300',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'viewport-width': '1600',
            # 'cookie': 'x-amz-captcha-1=1740064659874893; x-amz-captcha-2=odk+bw8e4WQAhUKpt2xPWA==; session-id=131-7967661-8597542; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:IN"; ubid-main=131-4199319-4736135; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; session-token=DZnMC90yHJwlZnhm8aIY46NOZyvwW9oO7XSA/XzjIwjuXoipmqptraKBwzN1/SjFr/RVGSo2yPcgPs9Q3z0f7hsH4G81bhpHcenK1VT52WMWMZgiqc+PKvAlcYEB+zHmyAvlb73L/QDqu58cSuXgsL2tmCa6dKHAKcPNthskzHWB6gW9Ea8sgolPtezcAAR+nxNkweHbV6u3Jx3WvzV1zINnHjsMRp+/QdQWuWX2BJlaVZDZdWRTCJrf8RytA30DvHQXr2Ng28vGGKvI+H8Dyp1r4xDU9fmSGtA4r4K49amUrxrWqNqtJFr81voXDodM7EvXUd9nvUFtKgUDNRnZgxWZyIFHZ8X3; csm-hit=tb:GT3XHP689CHB46DT25ZK+s-MNRZZXK9PSR67E8RYYR5|1742453940321&t:1742453940321&adb:adblk_no',
        }
        url = 'https://www.amazon.com/stores/Momcozy/page/289B876A-CE6F-4247-9629-8AD6549CB51D'
        yield scrapy.Request(url=url, headers=headers, cookies=cookies, dont_filter=True)

    def parse(self, response, **kwargs):
        for data in response.xpath("//ul[@class='Navigation__navList__HrEra']/li")[2:]:
            if data.xpath('./a'):
                item = AmazonMomcozyItem()
                item['category_url'] = "https://www.amazon.com" + data.xpath('./a/@href').get()
                item['category_name'] = data.xpath('./a//span/text()').get()


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {CategoryLinksSpider.name} -a start=1 -a end=1".split())
