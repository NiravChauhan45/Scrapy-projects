import scrapy
import reformation.db_config as db
from scrapy import cmdline
from reformation.config.database_config import ConfigDatabase
from reformation.db_config import variations_links
from reformation.items import ReformationVariationItem
import hashlib


class VariationsLinksSpider(scrapy.Spider):
    name = "variations_links"
    allowed_domains = ["www.thereformation.com"]

    def __init__(self, start_id, end, **kwargs):
        super().__init__(**kwargs)
        self.cookies = {
            '_gcl_au': '1.1.2034444316.1765174144',
            'FPID': 'FPID2.2.JqBFpWlx8Ekcz3iivvFRlqcmkZXaNhTR1odHNrfELAQ%3D.1765172366',
            'FPLC': 'Tgv8faj59G%2Fs2vAEWMgW8vlAJf1tqz5uqERFFNc0qipK56IK0ebK82aaixE8dDrUAoE4j%2F3cMFs6ZBfHH8ue01jSH3D0RTjAcsx2H4%2ByIuPZ8VYnq0KTRgRW5zOzWQ%3D%3D',
            '__cq_uuid': 'bcb2VLigA8O6GGagVDLLm9ZwYo',
            '__stripe_mid': '364fab9e-cd15-4a1a-8689-6915eeb3abb4362c1b',
            '__stripe_sid': 'ad39290e-9bbc-493e-94ff-722b1a165360c3b05c',
            'dwac_0644a165d42080eb78142cac75': 'PcLMlrgDgQOmvI1Uq89CACFtNCyEhEpeVnM%3D|dw-only|||USD|false|US%2FPacific|true',
            'cqcid': 'absH9el6oYZpmGsfkYuC88SOGV',
            'cquid': '||',
            'sid': 'PcLMlrgDgQOmvI1Uq89CACFtNCyEhEpeVnM',
            'newCustomer': 'new',
            'dwpersonalization_914668167e2805280fee994f0c25aa1b': '9770b5c81785d7c175a3a6665420260206030000000',
            'dwanonymous_914668167e2805280fee994f0c25aa1b': 'absH9el6oYZpmGsfkYuC88SOGV',
            '__cq_dnt': '0',
            'dw_dnt': '0',
            'dwsid': '_an4FA-iNIk1-i40Qb_pFuEGAK4zJf_UxTXGtPRpEUHPzrgBG7H-a9I81-wbjFPkay9klIVQEartJ9BtiDBrLA==',
            '_cfuvid': '7udDs59UoYGvJo8RsuUThOCjqgKxt8JrWnAwTWJUwl8-1765174147227-0.0.1.1-604800000',
            'capi_lift_channel': 'Referral',
            'lux_uid': '176517415395246616',
            '_pin_unauth': 'dWlkPU0yRmlOelF6TVdNdE1EWmhaaTAwTWpNeUxUZzVZV0V0TUdZeVpqQTJNelkwT1RObA',
            '__attentive_id': 'f6703669f0bd4067ae6ec5f189ad0c0b',
            '__attentive_session_id': '6d8282add846483fb475c095f02eda53',
            '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzY1MTc0MTYwODI0LFwidW9cIjoxNzY1MTc0MTYwODI0LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImY2NzAzNjY5ZjBiZDQwNjdhZTZlYzVmMTg5YWQwYzBiXCJ9In0=',
            '__attentive_cco': '1765174160829',
            '_fbp': 'fb.1.1765174161078.535208241593282659',
            '_gid': 'GA1.2.2105813566.1765174162',
            '_gat_UA-26305999-1': '1',
            '__cq_bc': '%7B%22bhcn-reformation-us%22%3A%5B%7B%22id%22%3A%220103940%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%220103940CVD%22%7D%5D%7D',
            '_tt_enable_cookie': '1',
            '_ttp': '01KBY98C91CNX92R0Q9SV00FR9_.tt.1',
            'scarab.visitor': '%224C1967A116946649%22',
            'scarab.profile': '%22g%252F0103940%7C1765174161%22',
            '__attentive_ss_referrer': 'ORGANIC',
            '__attentive_dv': '1',
            'GlobalE_CT_Data': '%7B%22CUID%22%3A%7B%22id%22%3A%22956473441.525640755.1008%22%2C%22expirationDate%22%3A%22Mon%2C%2008%20Dec%202025%2006%3A39%3A28%20GMT%22%7D%2C%22CHKCUID%22%3Anull%2C%22GA4SID%22%3A789853891%2C%22GA4TS%22%3A1765174168494%2C%22Domain%22%3A%22www.thereformation.com%22%7D',
            'GlobalE_Full_Redirect': 'false',
            'refWelcomeModal': 'true',
            'GlobalE_Data': '%7B%22countryISO%22%3A%22MP%22%2C%22cultureCode%22%3A%22en-GB%22%2C%22currencyCode%22%3A%22USD%22%2C%22apiVersion%22%3A%222.1.4%22%7D',
            'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Dec+08+2025+11%3A39%3A37+GMT%2B0530+(India+Standard+Time)&version=202503.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=c248c6b8-836a-4d5b-adf1-bdb0638f4603&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false',
            '__cq_seg': '0~0.44!1~-0.06!2~-0.20!3~0.37!4~-0.43!5~0.41!6~0.09!7~0.25!8~0.42!9~-0.15!f0~15~5!n0~1',
            '_ga': 'GA1.1.1770795153.1765172366',
            '_ga_7BLG0E10ZJ': 'GS2.1.s1765172365$o1$g1$t1765174177$j60$l0$h2108608928',
            '_ga_M3XP66ENNS': 'GS2.1.s1765170575$o4$g1$t1765174177$j60$l0$h0',
            '_uetsid': '704e4890d3fc11f0895d4fb241cc7599',
            '_uetvid': '704ec140d3fc11f0bdeaa3384ac3eec6',
            'fs_lua': '1.1765174177439',
            'fs_uid': '#o-19Y02A-na1#2c2a9058-359d-40e0-96ed-a5cfc93d1eed:668d2fb8-9414-4890-8db0-53728125add3:1765170568835::17#/1796283716',
            '__attentive_pv': '2',
            'GlobalE_Analytics': '%7B%22merchantId%22%3A1008%2C%22shopperCountryCode%22%3A%22MP%22%2C%22cdn%22%3A%22https%3A%2F%2Fwebservices.global-e.com%2F%22%2C%22clientId%22%3A%2205405c73-750d-4dbe-8208-c72281860390%22%2C%22sessionId%22%3A%223e236b97-f78b-4e94-ae37-959ff74ac328%22%2C%22sessionIdExpiry%22%3A1765175980680%2C%22configurations%22%3A%7B%22eventSendingStrategy%22%3A0%7D%2C%22featureToggles%22%3A%7B%22FT_3DA%22%3Afalse%2C%22FT_3DA_UTM_SOURCE_LIST%22%3A%5B%5D%2C%22FT_3DA_STORAGE_LIFETIME%22%3A4320%2C%22FT_BF_GOOGLE_ADS%22%3Afalse%2C%22FT_BF_GOOGLE_ADS_LIFETIME%22%3A30%2C%22isOperatedByGlobalE%22%3Afalse%7D%2C%22lockBrowsingStartOnSessionId%22%3A%223e236b97-f78b-4e94-ae37-959ff74ac328%22%2C%22dataUpdatedAt%22%3A1765174180680%7D',
            'ttcsid': '1765174161724::T1OdTvpuds_IIf8MOw-l.1.1765174186364.0',
            'ttcsid_C9J3CFRC77U92U7NNRQG': '1765174178236::ZhwaXRnGPhFGvpdcF2JQ.1.1765174186364.1',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.start_id = start_id
        self.end = end
        self.db = ConfigDatabase(database=db.database_name, table=db.pdp_links_sitemap)

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'}, start=self.start_id, end=self.end)
        for result in results:
            product_url = result.get('product_url')
            yield scrapy.Request(url=product_url, headers=self.headers, cookies=self.cookies,
                                 cb_kwargs={'product_url': product_url},
                                 dont_filter=True)

    def parse(self, response, **kwargs):
        product_url = kwargs.get('product_url')
        product_id = product_url.split('/')[-1].replace(".html", "")

        color_variation_list = response.xpath(
            "//button[contains(@class,'product-attribute__swatch swatch--color swatch--color-pdp')]/@data-attr-value").getall()

        if color_variation_list:
            for color_code in color_variation_list:
                item = ReformationVariationItem()
                item['product_id'] = product_id
                variation_id = f"{product_id}{color_code}"
                item['variation_id'] = variation_id
                item['variation_url'] = f"https://www.thereformation.com/products/%20/{variation_id}.html"
                item['hash_id'] = int(hashlib.md5(bytes(str(product_url) + str(variation_id), "utf8")).hexdigest(),
                                      16) % (10 ** 18)
                yield item
            sql = f"UPDATE {db.pdp_links_sitemap} SET status = %s WHERE product_url=%s"
            values = ('Done', product_url)
            db.cursor.execute(sql, values)
            db.connection.commit()
        else:
            item = ReformationVariationItem()
            item['product_id'] = product_id
            item['variation_id'] = product_id
            item['variation_url'] = f"https://www.thereformation.com/products/%20/{product_id}.html"
            item['hash_id'] = int(hashlib.md5(bytes(str(product_url), "utf8")).hexdigest(),
                                  16) % (10 ** 18)
            yield item
            sql = f"UPDATE {db.pdp_links_sitemap} SET status = %s WHERE product_url=%s"
            values = ('Done', product_url)
            db.cursor.execute(sql, values)
            db.connection.commit()
            print('colour variation not found')


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {VariationsLinksSpider.name} -a start_id=1 -a end=500000".split())
