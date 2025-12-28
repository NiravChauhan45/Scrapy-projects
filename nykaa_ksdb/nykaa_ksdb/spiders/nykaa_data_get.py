import gzip
import json
import os
import re

import scrapy

from scrapy.cmdline import execute
from nykaa_ksdb.items import NykaaKsdbItem
from nykaa_ksdb.config.database_config import ConfigDatabase
from parsel import Selector

from nykaa_ksdb.items import NykaaKsdbItem


class NykaaDataGetSpider(scrapy.Spider):
    name = "nykaa_data_get"
    allowed_domains = ["'www.nykaa.com'"]
    start_urls = ["https://'www.nykaa.com'"]

    def __init__(self, start_id=0, end=1000000, zipcode='', **kwargs):
        super().__init__(**kwargs)
        self.start_id = start_id
        self.end = end
        # self.zipcode = zipcode
        self.db = ConfigDatabase(database='nykaa_ksdb', table=f'nykaa_ksdb_input')

    def start_requests(self):
        results = self.db.fetchResultsfromSql(start=int(self.start_id), end=self.end, conditions={'status': 'Pending'})
        for result in results:
            product_url = result['product_url']
            if "/p/" in product_url:
                product_id = product_url.split("/p/")[-1]
                cookies = {
                    'run': '55',
                    'EXP_REVIEW_COLLECTION': '1',
                    'D_LST': '1',
                    'D_PDP': '1',
                    'bcookie': '0778155c-480a-40cf-903e-f698ea275c36',
                    'PHPSESSID': 'cAoCkdGjJNgvPbY1753093512078',
                    '_gcl_gs': '2.1.k1$i1753093509$u3073711',
                    '_gcl_au': '1.1.1673977329.1753093515',
                    'WZRK_G': '917b7cce687542b0b073b8c4073905cf',
                    '_gac_UA-31866293-9': '1.1753093516.Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB',
                    '_gcl_aw': 'GCL.1753093516.Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB',
                    'deduplication_cookie': 'GooglePaid',
                    'deduplication_cookie': 'GooglePaid',
                    '_ttgclid': 'Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB',
                    '_ttgclid': 'Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB',
                    '_ttgclid': 'Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB',
                    'tt_deduplication_cookie': 'GooglePaid',
                    'tt_deduplication_cookie': 'GooglePaid',
                    'tt_deduplication_cookie': 'GooglePaid',
                    'EXP_AB_DWEB_SHOPPING_BAG_URL': 'A',
                    'EXP_NEW_SIGN_UP': 'DEFAULT',
                    'EXP_CART_GRATIFICATION_POPUP': 'B',
                    'EXP_ITEM_DISCOUNT': 'A',
                    'EXP_ORDERS_REVAMP': 'A',
                    'EXP_CART_LOGIN_SEGMENT': 'A',
                    'EXP_ADP_RV_REORDER': 'A',
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
                    'EXP_PLP_PINKBOX_CTA': 'DEFAULT',
                    'EXP_SLP_RELATED_SEARCHES': 'A',
                    'EXP_QUERY_PARAM_EXP': 'DEFAULT',
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
                    'EXP_PDP_RELEVANT_CATEGORY': 'DEFAULT',
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
                    'EXP_SPECULATIVE_PRERENDERING': 'DEFAULT',
                    'EXP_AB_TAGS_RATING_ON_LISTING': 'ONLY_TAGS',
                    'EXP_SEARCH_INP_ON_CART': 'B',
                    'EXP_AB_NEW_TAGS_ON_PDP': 'DEFAULT',
                    'EXP_REVIEW_SUBMIT': 'A',
                    'EXP_AB_GUIDES_V2': 'A',
                    'EXP_AB_OFFER_DELTA_COMMUNICATION': 'DEFAULT',
                    'EXP_AB_HLP_COUPON_OFFERS': 'A',
                    'EXP_AB_NEW_GC_PAGE': 'A',
                    'EXP_PLP_DNW_DWEB': 'A',
                    'EXP_ERROR_BOUNDARY': 'DEFAULT',
                    'EXP_AB_STATUS_WIDGET': 'A',
                    'EXP_PRIVE_CTA_DISABLE': 'DEFAULT',
                    'EXP_AB_GETAPP_DWEB': 'A',
                    'EXP_AB_HLP_EDD': 'DEFAULT',
                    'EXP_CTA_DISABLE_DWEB': 'DEFAULT',
                    'EXP_AB_DIFFERENTIAL_PRICE': 'A',
                    'SHOW_PREVIEW_INFO_PAGE': 'false',
                    'OLD_LISTING_FLOW': 'false',
                    'GC_PREVIEW_EXPERIMENT': 'false',
                    'C_AUTH': 'true',
                    'VIEW_COUPON_EXPERIMENT': 'true',
                    'NEW_ORDERLISTING_PAGE': 'true',
                    'NEW_ORDERDETAIL_PAGE': 'true',
                    'EXP_AB_GETAPPNUDGE_MWEB': 'A',
                    'EXP_AB_EMAIL_VERIFICATION_REVAMP': 'A',
                    'EXP_AB_MWEB_FILTERS_PLP': 'CONTROL',
                    'EXP_AB_VISUAL_FILTERS_PLP': 'DEFAULT',
                    'EXP_AB_NYKAA_NOW_PDP': 'DEFAULT',
                    'EXP_AB_NYKAA_NOW_FILTER': 'DEFAULT',
                    'EXP_AB_NEW_SHOPPING_BAG': 'A',
                    'EXP_UPDATED_AT': '1757931113254',
                    'EXP_SSR_CACHE': '9c0eab0af8491d1ec25eeb8c542c593a',
                    'PRIVE_TIER': 'null',
                    'head_data_react': '{"id":"","nykaa_pro":false,"group_id":""}',
                    'pro': 'false',
                    '_gid': 'GA1.2.191188041.1758036041',
                    'pinCodeDel': '560001',
                    '_clck': '1n843fo%5E2%5Efze%5E0%5E2028',
                    'bm_sz': 'C4B0DE6793C2500227B59EAABF6DE2CF~YAAQnvQ3FyV9OU6ZAQAAPUcqVh3EqCt0mDkMQQw8CPPEZkoNZlipEPQXDhNr41K5VYw67Xcf48aTjcoOfjGyWtypkY5oOlbsNBPPluxsIgl35rpxgLIdiUjmx/epSmlL8rHpnd0gmdaGS6xYPrRJ9CnnXkRlm5w4TkyUCisCrXl5604JV1BcYQQYw5NOYsGmODfha1EVSQu+TGDuEovKxkmGsioDdFZajITQduDOgvibvSbI4qzLI1f7dzsan9T5CqaFgOqPZRPXOq0FPpcvpIMvBG5fWZeHUkBgqPqZJyS5BnhhzAFWM0k6u/WfeEz65RLev9sfBW85L3NUUbfo3K1VxUcHvGs09wmJ1RR4EOn1/R2DmmkhVPGxodV6rUUR9bQKAVoQPhVYJKeufwB0dOXstV7r5IdtU2fbC7M=~3356464~4539716',
                    'SITE_VISIT_COUNT': '79',
                    '_ga_LKNEBVRZRG': 'GS2.1.s1758087239$o26$g0$t1758087239$j60$l0$h0',
                    'cto_bundle': '_akRKl94JTJCNHVBU0s1MjVQWEl1QUxKbmhYZzh2TG10NWtVJTJCdTNzY21pMzBLNEtNZktoa1JGeWJnUFJNUDJFS243MnVkc2pYOHZMSTclMkJ6RGglMkJobW4lMkJIcllzQzE4Mm1sSnZVY21uaFRWRDJmVjBIRSUyRnZ3blRzR1FIczNyYiUyQmdUM1BybndjcU1sa3N2ZHRLemZSdnZRZWMzJTJCWW9DZXRmNmRTSnRtJTJCeHZGN29tZDl4ejJvTkZrYjVMeDdyaE5vRGduVEQlMkZjb2glMkJKc1A1eUV2eHR2MEZPMVA2SkxSZyUzRCUzRA',
                    '_ga': 'GA1.2.1683217558.1753093516',
                    '_uetsid': 'b517c030931011f0aad7513a3ff9cfcf',
                    '_uetvid': 'fe5d1770661c11f0809f59d32875aac4',
                    '_ga_JQ1CQHSXRX': 'GS2.2.s1758087240$o20$g0$t1758087240$j60$l0$h0',
                    '_abck': 'D86A1358FBB8EAD57F4F3C3A8D0CA530~0~YAAQnfQ3F+pn80uZAQAAs8kxVg4GDgrZ8Iak64yhctO+qVrbc6gGLyFllGz/RxqaeqOHG7ItKLtMYu6QgqkQO8l9mK6A14N2DxR5Ir9b4+ySqPl32ByJ2Orv79T9eZ2ExmaOVZPxSBrvDahxTKBuniU4VZsVp6BqCtjOUYPciz8L7EaZkUp+p9Tc59jxYMvaHG1PJ5b40fgCTKI5KRQm5MEhef/HqqoXxk8/JyBgstlJb3wP6n8q7OlDIoyqamGNgA7kBhwf5LAQpAxveK7sjWLzeonB3JZTf2iSYcG0TauQrbL4spvdUVFscd48dr7lpU7H9/lqMk8UOZjMsgy27Zf6/YG9KZoh5y2eXuAc/gx8+EX40yj8E9xMcwaqNtYrV7OGTiN8WyiMsTkzU7tHxEhceKHB0BnFwF+PhTNmHeT2uObv0m/VQeMRTKNPNd7ADtg/Mnz23hwjBeotwX5+qewlAvITv+jzq0WN+UoytMr/GPDjV9a5sfmiTMxzIXQEvVsf4w7GY+hO6RQseZIcZ2459DG5utmvc2p/AzQjE7xwYPrll5OX9kcQ1N1p6OBcfyBIehYtWMA/Ce0TXxptyhMeMzSRUf2KwprSgeys/0twMaXgsU97e71kE8+0rFjvv5RKiTANf/dRxDk1/N3zxO+DjEjx0d4qheaeCSrp~-1~-1~1758091327~AAQAAAAE%2f%2f%2f%2f%2f7mYztRsxRtAylvh6b7aUSkAMvIHYbDUDeNOgKPEXetYgF4pux%2f4jEVLvgZkOs5wkPKsyj+R%2fWHN7O0XYdLAzIxTpT%2f1Fv3Lg8sePrIynHeHnJBBUr1fM3sfgzASGFyFEsKSPr4%3d~-1',
                    '_clsk': '6hj12f%5E1758088519155%5E4%5E1%5El.clarity.ms%2Fcollect',
                    'countryCode': 'IN',
                    'storeId': 'nykaa',
                }
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    'priority': 'u=0, i',
                    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                    # 'cookie': 'run=55; EXP_REVIEW_COLLECTION=1; D_LST=1; D_PDP=1; bcookie=0778155c-480a-40cf-903e-f698ea275c36; PHPSESSID=cAoCkdGjJNgvPbY1753093512078; _gcl_gs=2.1.k1$i1753093509$u3073711; _gcl_au=1.1.1673977329.1753093515; WZRK_G=917b7cce687542b0b073b8c4073905cf; _gac_UA-31866293-9=1.1753093516.Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB; _gcl_aw=GCL.1753093516.Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB; deduplication_cookie=GooglePaid; deduplication_cookie=GooglePaid; _ttgclid=Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB; _ttgclid=Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB; _ttgclid=Cj0KCQjwyvfDBhDYARIsAItzbZF31N06pHs9hc3ri7zJoyqzt3kirIxUVS1LdahUDuIOMxkBr6kwDP4aAleDEALw_wcB; tt_deduplication_cookie=GooglePaid; tt_deduplication_cookie=GooglePaid; tt_deduplication_cookie=GooglePaid; EXP_AB_DWEB_SHOPPING_BAG_URL=A; EXP_NEW_SIGN_UP=DEFAULT; EXP_CART_GRATIFICATION_POPUP=B; EXP_ITEM_DISCOUNT=A; EXP_ORDERS_REVAMP=A; EXP_CART_LOGIN_SEGMENT=A; EXP_ADP_RV_REORDER=A; EXP_AB_CP_GAMES=A; EXP_ADP_RV_SEGMENT=A; EXP_AB_AUTOFILL=B; EXP_ADP_RV_VIEW_SIMILAR_HLP=A; EXP_ADP_RV_VIEW_SIMILAR=A; EXP_ADP_RV_PLP_CONFIGURABLE_NO_RESULTS=A; EXP_ADP_RV_PRODUCT_V3=CONTROL; EXP_AB_HLP_CARD_REVAMP=CONTROL; EXP_AB_WISHLIST=A; EXP_AB_PRICE_REVEAL_NEW=A; EXP_PLP_INLINE_FILTER=REVAMPED; EXP_EDD_DELIVERY_WIDGET=A; EXP_ADP_RV_MULTI_COUPONS=A; EXP_ADP_RV_SEARCH_BAR_NEW=A; EXP_AB_AUTH_DWEB=A; EXP_PLP_INLINE_WIDGETS=A; EXP_PLP_PINKBOX_CTA=DEFAULT; EXP_SLP_RELATED_SEARCHES=A; EXP_QUERY_PARAM_EXP=DEFAULT; EXP_AB_PDP_IMAGE=DEFAULT; EXP_AB_CALLOUT_NUDGE=A; EXP_AB_TRUECALLER=DEFAULT; EXP_AB_GOOGLE_ONE_TAP=DEFAULT; EXP_AB_HLP_PAGE=A; EXP_AB_NEW_PLP=A; EXP_PRODUCT_CARD_CTA=A; EXP_AB_SIZE_MINI_PRODUCT=A; EXP_AB_TOP_NAV_CONFIG=CONTROL; EXP_AB_PRODUCT_HIGHLIGHTS=A; EXP_QUERY_PARAM_EXP_DWEB=CONTROL; EXP_AB_BEAUTY_PORTFOLIO=A; EXP_AB_HP_SEARCH_ANIMATION=CONTROL; EXP_AB_PDP_HAMBURGER=CONTROL; EXP_AB_HLP_OFFERS=DEFAULT; EXP_AB_WEB_AUTOREAD_OTP=DEFAULT; EXP_AD_BRV=variant1; EXP_PDP_RELEVANT_CATEGORY=DEFAULT; EXP_AB_REMOVE_LOGIN_BOTTOMSHEET=DEFAULT; EXP_AB_ZENDESK_CHAT=A; EXP_AB_ACCOUNT_REVAMP=A; EXP_AB_HORIZONTAL_WIDGET_TYPE=CONTROL; EXP_AB_IOC_CART_NUDGE=DEFAULT; EXP_APPSFLYER_DOWNLOAD_CTA=DEFAULT; EXP_AB_PDP_SIMILAR_PRODUCT_SHEET=DEFAULT; EXP_FULL_SCREEN_RECO_WIDGET=DEFAULT; EXP_AB_BEST_SELLER_PDP=DEFAULT; EXP_AB_ENABLE_HLP_NEW_API=DEFAULT; EXP_SPECULATIVE_PRERENDERING=DEFAULT; EXP_AB_TAGS_RATING_ON_LISTING=ONLY_TAGS; EXP_SEARCH_INP_ON_CART=B; EXP_AB_NEW_TAGS_ON_PDP=DEFAULT; EXP_REVIEW_SUBMIT=A; EXP_AB_GUIDES_V2=A; EXP_AB_OFFER_DELTA_COMMUNICATION=DEFAULT; EXP_AB_HLP_COUPON_OFFERS=A; EXP_AB_NEW_GC_PAGE=A; EXP_PLP_DNW_DWEB=A; EXP_ERROR_BOUNDARY=DEFAULT; EXP_AB_STATUS_WIDGET=A; EXP_PRIVE_CTA_DISABLE=DEFAULT; EXP_AB_GETAPP_DWEB=A; EXP_AB_HLP_EDD=DEFAULT; EXP_CTA_DISABLE_DWEB=DEFAULT; EXP_AB_DIFFERENTIAL_PRICE=A; SHOW_PREVIEW_INFO_PAGE=false; OLD_LISTING_FLOW=false; GC_PREVIEW_EXPERIMENT=false; C_AUTH=true; VIEW_COUPON_EXPERIMENT=true; NEW_ORDERLISTING_PAGE=true; NEW_ORDERDETAIL_PAGE=true; EXP_AB_GETAPPNUDGE_MWEB=A; EXP_AB_EMAIL_VERIFICATION_REVAMP=A; EXP_AB_MWEB_FILTERS_PLP=CONTROL; EXP_AB_VISUAL_FILTERS_PLP=DEFAULT; EXP_AB_NYKAA_NOW_PDP=DEFAULT; EXP_AB_NYKAA_NOW_FILTER=DEFAULT; EXP_AB_NEW_SHOPPING_BAG=A; EXP_UPDATED_AT=1757931113254; EXP_SSR_CACHE=9c0eab0af8491d1ec25eeb8c542c593a; PRIVE_TIER=null; head_data_react={"id":"","nykaa_pro":false,"group_id":""}; pro=false; _gid=GA1.2.191188041.1758036041; pinCodeDel=560001; _clck=1n843fo%5E2%5Efze%5E0%5E2028; bm_sz=C4B0DE6793C2500227B59EAABF6DE2CF~YAAQnvQ3FyV9OU6ZAQAAPUcqVh3EqCt0mDkMQQw8CPPEZkoNZlipEPQXDhNr41K5VYw67Xcf48aTjcoOfjGyWtypkY5oOlbsNBPPluxsIgl35rpxgLIdiUjmx/epSmlL8rHpnd0gmdaGS6xYPrRJ9CnnXkRlm5w4TkyUCisCrXl5604JV1BcYQQYw5NOYsGmODfha1EVSQu+TGDuEovKxkmGsioDdFZajITQduDOgvibvSbI4qzLI1f7dzsan9T5CqaFgOqPZRPXOq0FPpcvpIMvBG5fWZeHUkBgqPqZJyS5BnhhzAFWM0k6u/WfeEz65RLev9sfBW85L3NUUbfo3K1VxUcHvGs09wmJ1RR4EOn1/R2DmmkhVPGxodV6rUUR9bQKAVoQPhVYJKeufwB0dOXstV7r5IdtU2fbC7M=~3356464~4539716; SITE_VISIT_COUNT=79; _ga_LKNEBVRZRG=GS2.1.s1758087239$o26$g0$t1758087239$j60$l0$h0; cto_bundle=_akRKl94JTJCNHVBU0s1MjVQWEl1QUxKbmhYZzh2TG10NWtVJTJCdTNzY21pMzBLNEtNZktoa1JGeWJnUFJNUDJFS243MnVkc2pYOHZMSTclMkJ6RGglMkJobW4lMkJIcllzQzE4Mm1sSnZVY21uaFRWRDJmVjBIRSUyRnZ3blRzR1FIczNyYiUyQmdUM1BybndjcU1sa3N2ZHRLemZSdnZRZWMzJTJCWW9DZXRmNmRTSnRtJTJCeHZGN29tZDl4ejJvTkZrYjVMeDdyaE5vRGduVEQlMkZjb2glMkJKc1A1eUV2eHR2MEZPMVA2SkxSZyUzRCUzRA; _ga=GA1.2.1683217558.1753093516; _uetsid=b517c030931011f0aad7513a3ff9cfcf; _uetvid=fe5d1770661c11f0809f59d32875aac4; _ga_JQ1CQHSXRX=GS2.2.s1758087240$o20$g0$t1758087240$j60$l0$h0; _abck=D86A1358FBB8EAD57F4F3C3A8D0CA530~0~YAAQnfQ3F+pn80uZAQAAs8kxVg4GDgrZ8Iak64yhctO+qVrbc6gGLyFllGz/RxqaeqOHG7ItKLtMYu6QgqkQO8l9mK6A14N2DxR5Ir9b4+ySqPl32ByJ2Orv79T9eZ2ExmaOVZPxSBrvDahxTKBuniU4VZsVp6BqCtjOUYPciz8L7EaZkUp+p9Tc59jxYMvaHG1PJ5b40fgCTKI5KRQm5MEhef/HqqoXxk8/JyBgstlJb3wP6n8q7OlDIoyqamGNgA7kBhwf5LAQpAxveK7sjWLzeonB3JZTf2iSYcG0TauQrbL4spvdUVFscd48dr7lpU7H9/lqMk8UOZjMsgy27Zf6/YG9KZoh5y2eXuAc/gx8+EX40yj8E9xMcwaqNtYrV7OGTiN8WyiMsTkzU7tHxEhceKHB0BnFwF+PhTNmHeT2uObv0m/VQeMRTKNPNd7ADtg/Mnz23hwjBeotwX5+qewlAvITv+jzq0WN+UoytMr/GPDjV9a5sfmiTMxzIXQEvVsf4w7GY+hO6RQseZIcZ2459DG5utmvc2p/AzQjE7xwYPrll5OX9kcQ1N1p6OBcfyBIehYtWMA/Ce0TXxptyhMeMzSRUf2KwprSgeys/0twMaXgsU97e71kE8+0rFjvv5RKiTANf/dRxDk1/N3zxO+DjEjx0d4qheaeCSrp~-1~-1~1758091327~AAQAAAAE%2f%2f%2f%2f%2f7mYztRsxRtAylvh6b7aUSkAMvIHYbDUDeNOgKPEXetYgF4pux%2f4jEVLvgZkOs5wkPKsyj+R%2fWHN7O0XYdLAzIxTpT%2f1Fv3Lg8sePrIynHeHnJBBUr1fM3sfgzASGFyFEsKSPr4%3d~-1; _clsk=6hj12f%5E1758088519155%5E4%5E1%5El.clarity.ms%2Fcollect; countryCode=IN; storeId=nykaa',
                }
                url = f'https://www.nykaa.com/%20/p/{product_id}'
                yield scrapy.Request(url, headers=headers, cookies=cookies,
                                     meta={"product_id": product_id, "product_url": url}, dont_filter=True)
                break
    def parse(self, response, **kwargs):
        product_id = response.meta.get("product_id")
        selector = Selector(text=response.text)
        json_data = selector.xpath("//script[contains(text(),'__PRELOADED_STATE__')]/text()").get()
        json_data = json_data.split("window.__PRELOADED_STATE__ = ")[-1]
        json_data = json.loads(json_data)
        # response.product_title
        source = 'Nykaa'
        country_code = 'IN'
        is_login = 0
        zip_code = '560001'
        try:
            catalog_name = selector.xpath("//h1[@class='css-1gc4x7i']/text()").get()
            catalog_name = re.sub("\\s+", " ", catalog_name).strip()
            if not catalog_name:
                catalog_name = json_data.get('options')[2]['product_title']
            product_name = json_data.get('response').get('name') if json_data.get('response').get('name') else catalog_name
            catalog_name = json_data.get('response').get('name') if json_data.get('response').get('name') else catalog_name
        except:
            product_name = ''
            catalog_name = ''
        try:
            product_id = product_id
            catalog_id = product_id
        except:
            product_id = ''
            catalog_id = ''

        # Todo: image_url
        try:
            image_url = json_data.get('productPage').get('product').get('imageUrl')
        except:
            image_url = "N/A"

        try:
            # response.gludo_stock
            gludo_stock = json_data.get('response').get('gludo_stock')
            if gludo_stock == True:
                is_sold_out = False
            else:
                is_sold_out = True
        except:
            is_sold_out = True
        other_dict = {}
        other_dict['delivery'] = 'one_time_Nykaa_logout'
        other_dict['data_vendor'] = 'Actowiz'
        try:
            MOQ = json_data.get('response').get('min_order_qty')
            other_dict['MOQ'] = str(MOQ)
        except:
            other_dict['MOQ'] = "1"

        try:
            slug = json_data.get('response').get('slug')
            if slug:
                product_url = 'https://www.nykaa.com/' + slug
            else:
                product_url = product_url_k
        except:
            product_url = product_url_k
        try:
            final_category_dic_list = []
            final_category_dic = {}
            for cat_level in json_data.get('response').get('primary_categories'):
                category_name_data = json_data.get('response').get('primary_categories').get(
                    f'{cat_level}').get('name')
                final_category_dic[f'{cat_level}'] = json_data.get('response').get(
                    'primary_categories').get(
                    f'{cat_level}').get('name')
                if category_name_data:
                    final_category_dic_list.append(
                        json_data.get('response').get('primary_categories').get(f'{cat_level}').get(
                            'name'))
            if not final_category_dic_list:
                final_category_dic = None
        except:
            final_category_dic = None
        try:
            number_of_ratings = json_data.get('response').get('rating_count')
            if number_of_ratings == 0:
                number_of_ratings = 'N/A'
        except:
            number_of_ratings = 'N/A'
        try:
            avg_rating = json_data.get('response').get('rating')
            if not avg_rating:
                avg_rating = 'N/A'
        except:
            avg_rating = 'N/A'
        try:
            review_count = json_data.get('response').get('review_count')
            other_dict['review_count'] = review_count
        except:
            review_count = 'N/A'
        try:
            mrp = json_data.get('response').get('price')
            if mrp:
                other_dict["Maximum Retail Price"] = mrp
        except:
            mrp = 'N/A'

        # product_price :-
        try:
            product_price = json_data.get('response').get('final_price')
            if product_price:
                other_dict['product_price'] = product_price

        except:
            product_price = 'N/A'

        # expiry_date :-
        try:
            expiry_date = json_data.get('response').get('expdt')
            if expiry_date:
                other_dict['expiry_date'] = expiry_date
        except:
            pass

        # discount :-
        try:
            if product_price != mrp:
                discount = json_data.get('response').get('discount')
                if discount == 0:
                    discount = 'N/A'
            else:
                discount = 'N/A'
        except:
            discount = 'N/A'

        # cash_on_delivery :-
        try:
            cash_on_delivery = json_data.get('response').get('policy_widget')[0]['text']
            if cash_on_delivery:
                other_dict['cash_on_delivery'] = cash_on_delivery
        except:
            pass

        try:
            brand = json_data.get('response').get('brand_name')
            other_dict['brand'] = brand
        except:
            brand = 'N/A'
        image_list = []

        try:
            for image_loop in json_data.get('response').get('carousel'):
                if image_loop['mediaType'] == 'image':
                    image_list.append(image_loop['url'])
        except:
            pass
        if image_list:
            other_dict['images'] = image_list
        offers_list = []
        try:
            # response.offers
            for offers_loop in json_data.get('response').get('offers'):
                offer_dict = {}
                offer_dict['title'] = offers_loop.get('title')
                offer_dict['details'] = offers_loop.get('description')
                offers_list.append(offer_dict)
        except:
            pass
        if offers_list:
            other_dict['offers'] = offers_list
        try:
            sku = json_data.get('response').get('sku')
            if sku:
                other_dict['sku'] = sku
        except:
            pass
        try:
            # response.description
            des_html = json_data['response']['description']
            des_response = SE(des_html)
            if des_response:
                des_response.xpath('.//style').remove()
            des_text = des_response.xpath('.//text()').getall()
            description = ' '.join(des_text)
            if description:
                other_dict['description'] = description.strip()
        except:
            description = ''

        product_detail = {}
        try:
            ASIN = product_id
            if ASIN:
                product_detail['ASIN'] = ASIN
            try:
                # response.manufacture[0].manufacturer_name
                Manufacturer = json_data.get('response').get('manufacture')[0].get('manufacturer_name')
                product_detail['Manufacturer'] = Manufacturer
            except:
                pass
            try:
                ImporterName = json_data.get('response').get('manufacture')[0].get(
                    'manufacturer_address')
                if ImporterName:
                    product_detail['ManufacturerAddress'] = ImporterName
            except:
                pass
            try:
                Packer = json_data.get('response').get('manufacture')[0].get('packer_name')
                if Packer:
                    product_detail['Packer'] = Packer
            except:
                pass
            try:
                country_of_origin = json_data.get('response').get('manufacture')[0].get(
                    'country_of_origin')
                if country_of_origin:
                    product_detail['country_of_origin'] = country_of_origin
            except:
                pass
            try:
                ImporterName = json_data.get('response').get('manufacture')[0].get('importer_name')
                if ImporterName:
                    product_detail['ImporterName'] = ImporterName
            except:
                pass
            try:
                ImporterName = json_data.get('response').get('manufacture')[0].get('importer_address')
                if ImporterName:
                    product_detail['ImporterAddress'] = ImporterName
            except:
                pass
        except:
            pass
        if product_detail:
            other_dict['product_detail'] = product_detail
        try:
            returnAvailable = json_data.get('response').get('return_data').get('return_available')
            other_dict['returnAvailable'] = returnAvailable
            if returnAvailable == True:
                returnMessage = json_data.get('response').get('return_data').get('return_msg')
                other_dict['returnMessage'] = returnMessage
        except:
            pass
        individualRatingsCount = {}
        try:
            # response.review_splitup[0].count
            for reviewSplitUp_data in json_data['response']['review_splitup']:
                rating_number = int(reviewSplitUp_data['id'])
                rating_value = reviewSplitUp_data['count']
                individualRatingsCount[f'{rating_number}'] = rating_value
        except:
            pass
        if individualRatingsCount:
            other_dict['individualRatingsCount'] = individualRatingsCount
        try:
            # response.show_bestseller
            show_bestseller = json_data.get('response').get('show_bestseller')
            if show_bestseller:
                other_dict['best_seller_badge'] = show_bestseller
        except:
            pass
        try:
            seller_detail = {}
            # response.seller_name
            seller_name = json_data.get('response').get('seller_name')
            if seller_name:
                seller_detail['seller_name'] = seller_name
            if seller_detail:
                other_dict['seller_detail'] = seller_detail
        except:
            pass
        try:
            # response.type
            arrival_type = json_data.get('response').get('type')
        except:
            pass
        sku_list = []
        try:

            # response.options[2].sku
            for sku_loop in json_data.get('response').get('options'):
                sku_no = sku_loop.get('sku')
                sku_list.append(sku_no)
        except:
            # response.sku
            sku_no = json_data.get('response').get('sku')
            sku_list.append(sku_no)
        if sku_list:
            other_dict['variation_id'] = sku_list
        try:
            # response.pdp_sections[0].child_widgets[0].attributes[0].value
            # response.pdp_sections[0].title
            Highlights_dict = {}
            for Highlights_loop in json_data.get('response').get('pdp_sections'):
                Highlights_title = Highlights_loop.get('title')
                if Highlights_title == 'Highlights':
                    for widget_loop in Highlights_loop.get('child_widgets'):
                        widget_type = widget_loop.get('widget_type')
                        if widget_type == 'attribute_columnize_widget':
                            for attributes_loop in widget_loop.get('attributes'):
                                label = attributes_loop.get('label')
                                value = attributes_loop.get('value')
                                Highlights_dict[f'{label}'] = value
            if Highlights_dict:
                other_dict['highlights'] = Highlights_dict
        except:
            pass

        item = NykaaKsdbItem()
        item['product_id'] = product_id
        item['catalog_name'] = catalog_name
        item['catalog_id'] = catalog_id
        item['source'] = source
        item['arrival_type'] = arrival_type
        item['source'] = 'Nykaa'
        item['product_name'] = product_name
        item['image_url'] = image_url
        item['category_hierarchy'] = json.dumps(final_category_dic, ensure_ascii=False)
        item['mrp'] = mrp
        item['product_price'] = product_price
        item['is_sold_out'] = is_sold_out
        item['discount'] = discount
        item['shipping_charges'] = shipping_charges
        item['shipping_charges_json'] = json.dumps(shipping_charges_json)
        item['mrp_json'] = json.dumps(mrp_json)
        item['product_price_json'] = json.dumps(product_price_json)
        item['discount_json'] = json.dumps(discount_json)
        item['page_url'] = 'N/A'
        item['product_url'] = product_url
        item['number_of_ratings'] = number_of_ratings
        item['avg_rating'] = avg_rating
        item['position'] = 'N/A'
        item['country_code'] = country_code
        item['others'] = json.dumps(other_dict, ensure_ascii=False)
        yield item
        try:
            self.db.crsrSql.execute(
                f"update {self.db.table} set status='Done' where Product_id = '{product_id_1}'")
            self.db.connSql.commit()
        except Exception as e:
            print(e)
        print(f'{product_id}_Done')


if __name__ == '__main__':
    execute(f"scrapy crawl nykaa_data_get -a start_id=1 -a end=10".split())
