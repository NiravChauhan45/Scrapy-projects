from typing import Iterable, Any
from scrapy import cmdline
import scrapy
from parsel import Selector
from reformation.items import ReformationSiteMapPlItem


class PlPageSitemapSpider(scrapy.Spider):
    name = "pl_page_sitemap"
    allowed_domains = ["www.thereformation.com"]

    def start_requests(self):
        cookies = {
            'dwac_0644a165d42080eb78142cac75': 'YuLtSwedyj_JcSXnQNAzrh2Yt2n8lKdpW1E%3D|dw-only|||USD|false|US%2FPacific|true',
            'cqcid': 'abMAqVKQ53kSiOAqYsFs6Fq6hl',
            'cquid': '||',
            'sid': 'YuLtSwedyj_JcSXnQNAzrh2Yt2n8lKdpW1E',
            'newCustomer': 'new',
            'dwanonymous_914668167e2805280fee994f0c25aa1b': 'abMAqVKQ53kSiOAqYsFs6Fq6hl',
            '__cq_dnt': '0',
            'dw_dnt': '0',
            'dwsid': 'cLjUZZjBAEPcYMtEHaBKcw_CjkdjyG0VTkAiuENcoXyHUKyC9WzyhjWyYTPgvjEzQfZMXZsJ3Z1hY_KmZu1nwQ==',
            '_cfuvid': 'Z40SnaZDMNDaCamouM5dOu1yDRKo7_497avRcC.ANMo-1764747655160-0.0.1.1-604800000',
            'lux_uid': '176474765619401556',
            '_gid': 'GA1.2.323227154.1764747656',
            '_gcl_au': '1.1.696092158.1764747656',
            'capi_lift_channel': 'Referral',
            'scarab.visitor': '%224ABC1C682DDA4B77%22',
            '_fbp': 'fb.1.1764747656756.867575000437608490',
            '_pin_unauth': 'dWlkPU0yRmlOelF6TVdNdE1EWmhaaTAwTWpNeUxUZzVZV0V0TUdZeVpqQTJNelkwT1RObA',
            '__attentive_id': '00f195b81e77448e902534080516b75c',
            '__attentive_session_id': '63417c83ff70435aa67e75c7e67d7f58',
            '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzY0NzQ3NjU2OTkzLFwidW9cIjoxNzY0NzQ3NjU2OTkzLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjAwZjE5NWI4MWU3NzQ0OGU5MDI1MzQwODA1MTZiNzVjXCJ9In0=',
            '__attentive_cco': '1764747656995',
            '__cq_uuid': 'bcb2VLigA8O6GGagVDLLm9ZwYo',
            '__attentive_ss_referrer': 'ORGANIC',
            '_tt_enable_cookie': '1',
            '_ttp': '01KBHJGG06710NG65BM99EVS8K_.tt.1',
            'GlobalE_CT_Data': '%7B%22CUID%22%3A%7B%22id%22%3A%22534543961.650912919.1008%22%2C%22expirationDate%22%3A%22Wed%2C%2003%20Dec%202025%2008%3A10%3A57%20GMT%22%7D%2C%22CHKCUID%22%3Anull%2C%22GA4SID%22%3A213402807%2C%22GA4TS%22%3A1764747657418%2C%22Domain%22%3A%22www.thereformation.com%22%7D',
            'GlobalE_Full_Redirect': 'false',
            'FPID': 'FPID2.2.%2F9%2BV0t05On6FLcOdn6cIbufSkuRZEJcUNs1Xk2j0RU4%3D.1764747656',
            'FPLC': 'iCD6ActYhdJhSPZuXy%2FZQj3slIOUJVdAIc6uEE9Jx44S67FwGu2r8JJEDbxcxZtrTmpMgsKVlaSEItFawqbqxImpxGkio8S4RVerfxaSGxKeYLMckT6BcQpUMII4dg%3D%3D',
            '__attentive_dv': '1',
            'refWelcomeModal': 'true',
            '__stripe_mid': '265c4973-90ac-4fbf-990e-a3b9586e0fc0f1692b',
            '__stripe_sid': 'a895fbc2-c34d-4c17-a0e3-877f29c5b6564f1253',
            'GlobalE_Data': '%7B%22countryISO%22%3A%22MP%22%2C%22cultureCode%22%3A%22en-GB%22%2C%22currencyCode%22%3A%22USD%22%2C%22apiVersion%22%3A%222.1.4%22%7D',
            'scarab.profile': '%22g%252F0103940%7C1764747764%22',
            '__cq_bc': '%7B%22bhcn-reformation-us%22%3A%5B%7B%22id%22%3A%220103940%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%220103940CVD%22%7D%5D%7D',
            '__cq_seg': '0~0.48!1~0.35!2~0.23!3~-0.10!4~0.57!5~0.03!6~0.20!7~0.02!8~0.47!9~-0.03',
            'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Dec+03+2025+13%3A29%3A23+GMT%2B0530+(India+Standard+Time)&version=202503.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=c248c6b8-836a-4d5b-adf1-bdb0638f4603&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false',
            '_ga': 'GA1.1.225395567.1764747656',
            '_uetsid': '67cbcd30d01b11f0abaa9faf175b8b87',
            '_uetvid': '67cbe390d01b11f0b9ac230f5be1b292',
            '__attentive_pv': '8',
            'fs_lua': '1.1764748764209',
            'fs_uid': '#o-19Y02A-na1#2c2a9058-359d-40e0-96ed-a5cfc93d1eed:31fb18f8-5276-47fc-9082-eca0f1c1ba77:1764747656388::8#/1796283672',
            'GlobalE_Analytics': '%7B%22merchantId%22%3A1008%2C%22shopperCountryCode%22%3A%22MP%22%2C%22cdn%22%3A%22https%3A%2F%2Fwebservices.global-e.com%2F%22%2C%22clientId%22%3A%2240db048c-a84a-47ec-9ec5-15e2db618374%22%2C%22sessionId%22%3A%220f3e7421-b1f0-4fb9-b3c6-21412ffb3cba%22%2C%22sessionIdExpiry%22%3A1764750565035%2C%22configurations%22%3A%7B%22eventSendingStrategy%22%3A0%7D%2C%22featureToggles%22%3A%7B%22FT_3DA%22%3Afalse%2C%22FT_3DA_UTM_SOURCE_LIST%22%3A%5B%5D%2C%22FT_3DA_STORAGE_LIFETIME%22%3A4320%2C%22FT_BF_GOOGLE_ADS%22%3Afalse%2C%22FT_BF_GOOGLE_ADS_LIFETIME%22%3A30%2C%22isOperatedByGlobalE%22%3Afalse%7D%2C%22lockBrowsingStartOnSessionId%22%3A%220f3e7421-b1f0-4fb9-b3c6-21412ffb3cba%22%2C%22dataUpdatedAt%22%3A1764748765035%7D',
            'ttcsid': '1764747657229::wk6-R1ai9-Pb7vJnU5ZK.1.1764748776766.0',
            'ttcsid_C9J3CFRC77U92U7NNRQG': '1764747657228::nafGvqZgkwi1PiotGmqs.1.1764748776766.0',
            '_ga_7BLG0E10ZJ': 'GS2.1.s1764747656$o1$g1$t1764748791$j33$l0$h335478962',
            '_ga_M3XP66ENNS': 'GS2.1.s1764747657$o1$g1$t1764748791$j7$l0$h0',
        }
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        url = 'https://www.thereformation.com/sitemap_0-product.xml'
        yield scrapy.Request(url=url, cookies=cookies, headers=headers, dont_filter=True)

    def parse(self, response, **kwargs):
        selector = Selector(text=response.text)
        results = selector.xpath("//loc/text()").getall()
        for product_url in results:
            item = ReformationSiteMapPlItem()
            item['product_url'] = product_url
            yield item


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PlPageSitemapSpider.name}".split())
