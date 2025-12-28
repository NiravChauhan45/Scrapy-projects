import json
from typing import Iterable, Any
from scrapy import cmdline
import scrapy
import random
import json
from nykaa_saller.items import NykaaSallerPlItem


class PlPageSpider(scrapy.Spider):
    name = "pl_page"
    allowed_domains = ["www.nykaa.com"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.cookies = {
            'storeId': 'nykaa',
            'bcookie': 'a5925d2c-d41c-40a9-b943-7a6df4554663',
            'EXP_AB_GLAM_PASS': 'A',
            'EXP_AB_SAVINGS_SHELF': 'DEFAULT',
            'EXP_AB_NYKAA_NOW_RAAP': 'A',
            'EXP_AB_NYKAA_NOW_CART': 'CONTROL',
            'EXP_AB_NYKAA_NOW_FILTER': 'DEFAULT',
            'EXP_AB_INLINE_FILTER_REVAMP': 'DEFAULT',
            'EXP_AB_CART_OFFERS': 'CONTROL',
            'EXP_AB_PARTIAL_CHECKOUT': 'A',
            'EXP_AB_EMAIL_VERIFICATION_REVAMP': 'A',
            'EXP_AB_NEW_SHOPPING_BAG': 'A',
            'EXP_AB_DWEB_SHOPPING_BAG_URL': 'A',
            'EXP_NEW_SIGN_UP': 'DEFAULT',
            'EXP_CART_GRATIFICATION_POPUP': 'B',
            'EXP_ITEM_DISCOUNT': 'A',
            'EXP_ORDERS_REVAMP': 'A',
            'EXP_CART_LOGIN_SEGMENT': 'A',
            'EXP_ADP_RV_REORDER': 'B',
            'EXP_AB_CP_GAMES': 'A',
            'EXP_ADP_RV_SEGMENT': 'A',
            'EXP_AB_AUTOFILL': 'B',
            'EXP_ADP_RV_VIEW_SIMILAR_HLP': 'A',
            'EXP_ADP_RV_VIEW_SIMILAR': 'A',
            'EXP_ADP_RV_PLP_CONFIGURABLE_NO_RESULTS': 'A',
            'EXP_ADP_RV_PRODUCT_V3': 'CONTROL',
            'EXP_AB_HLP_CARD_REVAMP': 'CONTROL',
            'EXP_AB_WISHLIST': 'A',
            'EXP_AB_PRICE_REVEAL_NEW': 'A',
            'EXP_PLP_INLINE_FILTER': 'REVAMPED',
            'EXP_EDD_DELIVERY_WIDGET': 'A',
            'EXP_ADP_RV_MULTI_COUPONS': 'A',
            'EXP_ADP_RV_SEARCH_BAR_NEW': 'A',
            'EXP_AB_AUTH_DWEB': 'A',
            'EXP_PLP_INLINE_WIDGETS': 'A',
            'EXP_PLP_PINKBOX_CTA': 'CONTROL',
            'EXP_SLP_RELATED_SEARCHES': 'A',
            'EXP_SEARCH_DN_WIDGETS': 'A',
            'EXP_QUERY_PARAM_EXP': 'B',
            'EXP_AB_PDP_IMAGE': 'DEFAULT',
            'EXP_AB_CALLOUT_NUDGE': 'A',
            'EXP_AB_TRUECALLER': 'DEFAULT',
            'EXP_AB_GOOGLE_ONE_TAP': 'DEFAULT',
            'EXP_AB_HLP_PAGE': 'A',
            'EXP_AB_NEW_PLP': 'A',
            'EXP_PRODUCT_CARD_CTA': 'A',
            'EXP_AB_SIZE_MINI_PRODUCT': 'A',
            'EXP_AB_TOP_NAV_CONFIG': 'CONTROL',
            'EXP_AB_PRODUCT_HIGHLIGHTS': 'A',
            'EXP_QUERY_PARAM_EXP_DWEB': 'CONTROL',
            'EXP_AB_BEAUTY_PORTFOLIO': 'A',
            'EXP_AB_HP_SEARCH_ANIMATION': 'CONTROL',
            'EXP_AB_PDP_HAMBURGER': 'CONTROL',
            'EXP_AB_HLP_OFFERS': 'DEFAULT',
            'EXP_AB_WEB_AUTOREAD_OTP': 'DEFAULT',
            'EXP_AD_BRV': 'variant1',
            'EXP_PDP_RELEVANT_CATEGORY': 'A',
            'EXP_AB_REMOVE_LOGIN_BOTTOMSHEET': 'DEFAULT',
            'EXP_AB_ZENDESK_CHAT': 'A',
            'EXP_AB_ACCOUNT_REVAMP': 'A',
            'EXP_AB_HORIZONTAL_WIDGET_TYPE': 'CONTROL',
            'EXP_AB_IOC_CART_NUDGE': 'DEFAULT',
            'EXP_APPSFLYER_DOWNLOAD_CTA': 'DEFAULT',
            'EXP_AB_PDP_SIMILAR_PRODUCT_SHEET': 'DEFAULT',
            'EXP_FULL_SCREEN_RECO_WIDGET': 'DEFAULT',
            'EXP_AB_BEST_SELLER_PDP': 'DEFAULT',
            'EXP_AB_ENABLE_HLP_NEW_API': 'DEFAULT',
            'EXP_SPECULATIVE_PRERENDERING': 'CONTROL',
            'EXP_AB_TAGS_RATING_ON_LISTING': 'ONLY_TAGS',
            'EXP_SEARCH_INP_ON_CART': 'CONTROL',
            'EXP_AB_NEW_TAGS_ON_PDP': 'A',
            'EXP_REVIEW_SUBMIT': 'A',
            'EXP_AB_GUIDES_V2': 'A',
            'EXP_AB_OFFER_DELTA_COMMUNICATION': 'A',
            'EXP_AB_HLP_COUPON_OFFERS': 'A',
            'EXP_AB_NEW_GC_PAGE': 'A',
            'EXP_PLP_DNW_DWEB': 'A',
            'EXP_ERROR_BOUNDARY': 'DEFAULT',
            'EXP_AB_STATUS_WIDGET': 'A',
            'EXP_PRIVE_CTA_DISABLE': 'DEFAULT',
            'EXP_AB_GETAPP_DWEB': 'DEFAULT',
            'EXP_AB_HLP_EDD': 'DEFAULT',
            'EXP_CTA_DISABLE_DWEB': 'DEFAULT',
            'EXP_AB_DIFFERENTIAL_PRICE': 'A',
            'EXP_AB_GETAPPNUDGE_MWEB': 'DEFAULT',
            'EXP_AB_MWEB_FILTERS_PLP': 'DEFAULT',
            'EXP_AB_VISUAL_FILTERS_PLP': 'DEFAULT',
            'EXP_AB_NYKAA_NOW_PDP': 'A',
            'EXP_AB_CONVENIENCE_FEE': 'A',
            'EXP_DWEB_CONVENIENCE_FEE': 'A',
            'EXP_SPECIAL_DEALS': 'CONTROL2',
            'EXP_CONVERSATION_ROUTE': 'A',
            'EXP_AB_FREE_GIFT': 'A',
            'EXP_AB_SALE_PRICE_TAG': 'DEFAULT',
            'EXP_UPDATED_AT': '1764827066518',
            'EXP_SSR_CACHE': '81dcca2e80f92a3dc5a7b13135524f51',
            'run': '96',
            'EXP_REVIEW_COLLECTION': '1',
            'D_LST': '1',
            'D_PDP': '1',
            'EXP_OL': 'DEFAULT',
            'PHPSESSID': 'yuEndBLp2FJNy8A1765804133805',
            'PRIVE_TIER': 'null',
            'head_data_react': '{"id":"","nykaa_pro":false,"group_id":""}',
            'pro': 'false',
            'EXP_H_F_M_M_S_P': '1',
            '_gcl_au': '1.1.73880013.1765804137',
            '_gid': 'GA1.2.833281605.1765804138',
            'WZRK_G': 'b42a64e83a46446791266cdf6470d601',
            '_clck': '2b0y99%5E2%5Eg1v%5E0%5E2175',
            'bm_sz': '33C7664279D7F1E81D4575581A1E4F5B~YAAQJhzFF50GfPaaAQAAMhQhIh6EeaZ9Y8XxpGkG8U7srPIaOK/uHCFpuawMpY2Nrc4dqGUymZ+iadvqmn/FHMKrRcfaL9d5xZbs7xvc1/fZrenj+cE/0yle4LZToDLTwMBZmFZPQrECUp4G+9pP1S9c0kxcZEPavOYsbdu22PCksGjhhSj6F2XwVj4A2Mv9zAsglY7BDI8th5JSNYc//e45tFY8oRnPuO0zSEOUp8Mk0WHNxUkzFmNgi0njSIoOIq+4FglK6h9ZsXSSmhX1CceRyn1C/DZkIavb6cpwmr8b6Jrx2Zgk2I81k9qFAn2rn1UyjEU0jOfXYLGvYjyZDuguM0Jj6DgNyMAG74TxeuByH2aK74XPmxAMDbO/72+lynwniJ6YXrWIwH7uT64gGnApX/1wvZ+XBmcAdT0v~3225657~4340022',
            'SITE_VISIT_COUNT': '2',
            '_ga': 'GA1.2.1225505589.1765804138',
            '_uetsid': '37b54a50d9b711f09120b1a45c85b868',
            '_uetvid': '37b5bea0d9b711f0972c07444b42cbf3',
            'cto_bundle': 'shjtjl8lMkY3d0xHOEFaYXNKalEzbldRRGJtOFo4ZUVOeTBsZDEzVjZiQXpiNXc0TklaWmtxbnFPVWJOc0d6OE9aV0gwWmJKJTJCaUZvOXlEJTJCaG5RRkRBUWpvMmR6V1Zhd3M0NkJUMkJLdFdEZlFxNkV6eUVFaW1KampwcEFaNUI3anV6enJyQg',
            '_abck': '573A39EC593488306FB34AAE9FA8FD86~0~YAAQJhzFFx8ffPaaAQAA1PwhIg+6AgENNIDqo+eE6CiffESxRZ6cLbfXcMQs09heVl1MMnr46sTjYf9gntIa6UDJn59o/96OYS/r5Cv8/a9LVEPDJ8/YEReoxtIC0Xr8FR9vPMLvNJ4tlSlf+JyXTXG2eo/hAaYCvnRLEWqXMevFW0L+FqqJJIhzuC31XWAUXsFcZLK5xe7gEh0zHesP/ta7I5Vtyrkaf41W0ALUUCV0q+X5/7woPBImr3E/nvhsROcuyx53A3JyvJdXnMStsy+Q2pi7YdH4bL2j5PskNuRcpIA5i6nKUnhv8Itboyuk5sIIOtzE75rU1FwlVaIgd0XGa3d/Il8x9Zz1KPNDos2jJbTatB9PaH5i+kgwcCcQ9qSDa07dxi+a7fgAlk0wpvjJ/JUUMJOHf6erxv/Zpjknwvww2DD0kqN8ksaXN66I/ogdU83gnNT9mh+ZH+OYtlo101sgbE8bKeGZICvjZiMSTCXRMXoGagRsCBYjZFK8DPCVdBJa1H0J9urJLJN70OFG+kQAX+ysGdStGj/5enpXLe168Bt2TG9IjFDR4w8WX9hilcobG2cBqx16hhXJaUEsLNCL1mAQEjGW1B+GvX52Ly0IRjC0ysddpZHFjAc3hUXfgu4JD8+m7+RNpBLmdpHevVzTLEQIvVVTQGdeiw==~-1~-1~1765807733~AAQAAAAE%2f%2f%2f%2f%2f6RY0JCLPutrRWJEGYipK2%2fFwCQq14w2uzrHsFPhThe8n8meeh2GqXqNn8vzBJ6stZ0IAKGKOkrcn93lQOsXedO%2fNNP5H9tkorE1~-1',
            'WZRK_S_656-WZ5-7K5Z': '%7B%22p%22%3A3%2C%22s%22%3A1765804137%2C%22t%22%3A1765804276%7D',
            '_gat_UA-31866293-9': '1',
            '_ga_JQ1CQHSXRX': 'GS2.2.s1765804138$o1$g1$t1765804294$j60$l0$h0',
            '_clsk': 'gbndrw%5E1765804295035%5E4%5E0%5El.clarity.ms%2Fcollect',
            '_ga_LKNEBVRZRG': 'GS2.1.s1765804137$o1$g1$t1765804295$j60$l0$h0',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=0, i',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        }

    def start_requests(self):
        url = f'https://www.nykaa.com/brands/rhe-cosmetics/c/30855?page_no=1&sort=popularity&root=search,brand_menu,brand_list,Rhe%20Cosmetics&searchType=Misc&suggestionType=brand&ssp=2&tst=rhe&searchItem=Rhe%20Cosmetics&sourcepage=home&searchRedirect=1'
        yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies,
                             meta={"impersonate": self.browser},
                             dont_filter=True)

    # page_no = 4
    def parse(self, response, **kwargs):
        page_no_list = response.xpath("//a[contains(@class,'css-10bo00h')]/text()").getall()
        if page_no_list:
            for page_no in page_no_list:
                url = f'https://www.nykaa.com/brands/rhe-cosmetics/c/30855?page_no={page_no}&sort=popularity&root=search,brand_menu,brand_list,Rhe%20Cosmetics&searchType=Misc&suggestionType=brand&ssp=2&tst=rhe&searchItem=Rhe%20Cosmetics&sourcepage=home&searchRedirect=1'
                print(url)
                yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies,
                                     meta={"impersonate": self.browser},
                                     dont_filter=True, callback=self.pagination_parse)

        else:
            print("Pagination List Not Found")

    def pagination_parse(self, response, **kwargs):
        json_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if json_data:
            json_data = json.loads(json_data)[1]
            for data in json_data.get('itemListElement'):
                product_name = data.get('name')
                product_url = data.get('url')
                item = NykaaSallerPlItem()
                item['product_name'] = product_name
                item['product_url'] = product_url
                yield item


if __name__ == '__main__':
    cmdline.execute(f'scrapy crawl {PlPageSpider.name}'.split())
