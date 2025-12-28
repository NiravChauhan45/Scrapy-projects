import json

from parsel import Selector
from nykaa_fs.config.database_config import ConfigDatabase
from curl_cffi import requests
database_name = 'nykaa_latest'
table_name = 'cat_links_latest_trial'
db = ConfigDatabase(database=database_name, table=table_name)
table_creation_query = f"""
                        CREATE TABLE IF NOT EXISTS `{table_name}` (
                          `id` int NOT NULL AUTO_INCREMENT,
                          `main_cat_name` varchar(100) DEFAULT NULL,
                          `cat_name` varchar(100) DEFAULT NULL,
                          `sub_cat_name` varchar(100) DEFAULT NULL,
                          `cat_id` varchar(10) DEFAULT NULL,
                          `cat_url` text,
                          `status` varchar(50) DEFAULT 'pending',
                          `price_range` varchar(20) DEFAULT NULL,
                          PRIMARY KEY (`id`),
                          UNIQUE KEY (`price_range`,`cat_id`,`cat_name`,`sub_cat_name`, `main_cat_name`)
                        );
                       """
db.crsrSql.execute(table_creation_query)


cookies = {
    'bcookie': 'acada8b9-f715-48e7-9dd8-0dc9a7cbceaf',
    'EXP_NEW_SIGN_UP': 'DEFAULT',
    'EXP_CART_LOGIN_SEGMENT': 'A',
    'EXP_ADP_RV_REORDER': 'B',
    'EXP_ADP_RV_SEGMENT': 'A',
    'EXP_AB_AUTOFILL': 'B',
    'EXP_ADP_RV_VIEW_SIMILAR_HLP': 'A',
    'EXP_ADP_RV_PLP_CONFIGURABLE_NO_RESULTS': 'A',
    'EXP_ADP_RV_PRODUCT_V3': 'CONTROL',
    'EXP_AB_HLP_CARD_REVAMP': 'CONTROL',
    'EXP_AB_WISHLIST': 'A',
    'EXP_AB_PRICE_REVEAL_NEW': 'A',
    'EXP_EDD_DELIVERY_WIDGET': 'A',
    'EXP_ADP_RV_MULTI_COUPONS': 'A',
    'EXP_AB_DWEB_MULTICOUPON': 'A',
    'EXP_ADP_RV_SEARCH_BAR_NEW': 'A',
    'EXP_AB_AUTH_PAGE': 'A',
    'EXP_AB_AUTH_DWEB': 'CONTROL',
    'EXP_INCORRECT_SLUG_REDIRECT': 'A',
    'EXP_SLP_RELATED_SEARCHES': 'A',
    'EXP_AB_HLP_CTA': 'A',
    'EXP_AB_PDP_IMAGE': 'DEFAULT',
    'EXP_AB_CALLOUT_NUDGE': 'A',
    'EXP_AB_PRICE_REVAMP': 'A',
    'EXP_AB_TRUECALLER': 'DEFAULT',
    'EXP_AB_GOOGLE_ONE_TAP': 'DEFAULT',
    'EXP_AB_HLP_PAGE': 'A',
    'EXP_ORGANIC_GUIDES': 'A',
    'EXP_AB_NEW_PLP': 'A',
    'EXP_PDP_RATING_REVAMP': 'A',
    'EXP_AB_BREADCRUMB_POSITION': 'A',
    'EXP_PRODUCT_CARD_CTA': 'A',
    'EXP_AB_MULTI_MRP': 'A',
    'EXP_AB_BRAND_SEP_PDP': 'A',
    'EXP_AB_TOP_NAV_CONFIG': 'CONTROL',
    'EXP_QUERY_PARAM_EXP_DWEB': 'CONTROL',
    'EXP_AB_BEAUTY_PORTFOLIO': 'A',
    'EXP_AB_HAMBURGUR_BANNER': 'A',
    'EXP_AB_HP_SEARCH_ANIMATION': 'CONTROL',
    'EXP_AB_PDP_HAMBURGER': 'CONTROL',
    'EXP_AB_RECO_PRODUCT_V4': 'A',
    'EXP_AB_WEB_AUTOREAD_OTP': 'A',
    'EXP_AD_BRV': 'random',
    'EXP_PDP_RELEVANT_CATEGORY': 'A',
    'EXP_AB_PRODUCT_HIGHLIGHTS_CAROUSEL': 'A',
    'EXP_AB_PR_FLASH_SALE_V5': 'A',
    'EXP_AB_PRICE_FLUCTUATION': 'A',
    'EXP_AB_IOC_CART_NUDGE': 'A',
    'EXP_SNP_PRICE_FLUCTUATION_NUDGE': 'A',
    'run': '46',
    'EXP_REVIEW_COLLECTION': '1',
    'D_LST': '1',
    'D_PDP': '1',
    'PHPSESSID': 'NY4lOPgb9G5gIfD1721109091120',
    'WZRK_G': '8be39919e4284de1b38e70092d24204c',
    'EXP_PLP_INLINE_FILTER': 'REVAMPED',
    'EXP_PLP_PINKBOX_CTA': 'CONTROL',
    'EXP_AB_HLP_OFFERS': 'DEFAULT',
    'EXP_AB_AUTO_FILL_OTP': 'A',
    'EXP_AB_REMOVE_LOGIN_BOTTOMSHEET': 'DEFAULT',
    'EXP_AB_HORIZONTAL_WIDGET_TYPE': 'CONTROL',
    'EXP_AB_SOCIAL_PROOF_HLP': 'O_7',
    'deduplication_cookie': 'Desktop_web_footer',
    'deduplication_cookie': 'Desktop_web_footer',
    'tt_deduplication_cookie': 'Desktop_web_footer',
    'tt_deduplication_cookie': 'Desktop_web_footer',
    'tt_deduplication_cookie': 'Desktop_web_footer',
    'btIdentify': '3e62843b-7afb-4714-b33a-680697756594',
    '_bti': '%7B%22bsin%22%3A%22%22%7D',
    'unbxd.userId': 'uid-1723446894716-374',
    'AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg': '2121618341%7CMCIDTS%7C19948%7CMCMID%7C92083031616342837933557661350989532064%7CMCAAMLH-1724051694%7C12%7CMCAAMB-1724051694%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1723454094s%7CNONE%7CMCAID%7CNONE',
    'EXP_AB_ZENDESK_CHAT': 'A',
    'EXP_ADP_RV_VIEW_SIMILAR': 'C',
    'EXP_QUERY_PARAM_EXP': 'C',
    'EXP_AB_DWEB_SHOPPING_BAG_URL': 'A',
    'EXP_CART_GRATIFICATION_POPUP': 'B',
    'EXP_EXP_MULTI_COUPONS_REVAMP': 'DEFAULT',
    'EXP_FULL_SCREEN_RECO_WIDGET': 'DEFAULT',
    'EXP_AB_BEST_SELLER_PDP': 'DEFAULT',
    'EXP_AB_PDP_HOME': 'B',
    'EXP_ITEM_DISCOUNT': 'CONTROL',
    'EXP_AB_PRODUCT_VARIENTS_ORDER': 'A',
    'EXP_APPSFLYER_DOWNLOAD_CTA': 'DEFAULT',
    'EXP_AB_ENABLE_HLP_NEW_API': 'A',
    'N_S_B': '1',
    'S_S_B_S': '0',
    'countryCode': 'US',
    'N_PV': 'true',
    'C_DFA': 'false',
    'B_NAV': 'false',
    'N_P_M_S_P': 'true',
    'ADDRESS_BACK_FRICTION': 'false',
    'E_C': 'false',
    'undefined': 'false',
    'EXP_SPECULATIVE_PRERENDERING': 'DEFAULT',
    'EXP_ORDERS_REVAMP': 'DEFAULT',
    '_cfuvid': 'x2Hxq3dkBw35IpiuZCac77mDPMcVmA6BK6vBJypCZ1c-1729253248323-0.0.1.1-604800000',
    '_gcl_au': '1.1.461054102.1729253227',
    'EXP_AB_PLP_PR_V5': 'DEFAULT',
    'EXP_UPDATED_AT': '1729510035439',
    'EXP_SSR_CACHE': 'ba0d4fe8cf765806c9cba73c80294971',
    '__cf_bm': '.aGOrQj_Y5ibkNXxflJxydW8zq5.CAg0H7pjxUDeL9Q-1729579036-1.0.1.1-BjCgoQ4N20ScuCXQwAo6k14sglxCCBwu0ERqCI5S8JKI1ZwViyX0g8zFTbMpLw0HFAhDaK5wDt7X3_gVEKhHLQ',
    'cf_clearance': 'ADxTgM6fX4EqGZeosYeTirKMJ.EpT7LVmcEIVrNk5Ys-1729579037-1.2.1.1-LSckyM8Ngevg1t1HboFpgTUn13A0IooskotyAtc.b6.vjkK61JnJzZ2oqtbjffldD98gJ8RDcikX9yjg.WtcHP3Qxlz7anijV_m1mzFSsHVt5kbQYuy1zQz7.6glmjpRhvGkf00cw3yK3bZvxMrCXt4_5Xe1j1k0jpOdjhS4QknzinUImyV71oidJPkToHmFYbUxmfd7qHB1lOJVKSELnPRpFtnaWxNQCEl080IEJ89zaIhKmtcxe4ZCmIWfSOfA8EcMUwH5q8xhc1dDIKj7cx7.axG.uKXWLF7QhLZqSvjaFFEbguue9A5iN.stP3W5SkjSynIsP.Vthfkz_1VkZR5vPJwFpiXHh5V3p3CT6SKP98vGHo3h.smsB5NjRSFX',
    'head_data_react': '{"id":"","nykaa_pro":false,"group_id":""}',
    'pro': 'false',
    '_gid': 'GA1.2.1497177367.1729578999',
    '_clck': 'gpws9u%7C2%7Cfq8%7C0%7C1752',
    'ck_ptype': 'lst',
    'ck_id': '233',
    'ck_root': 'nav_3',
    'ck_dir': 'desc',
    'ck_order': 'popularity',
    '_ga': 'GA1.1.1291350165.1720180102',
    '_uetsid': 'fe056dc0903f11efa30081afaf257caf',
    '_uetvid': '7f491e108d4911efbc785dcb0906df6b',
    '_ga_JQ1CQHSXRX': 'GS1.2.1729578999.40.1.1729579077.60.0.0',
    'cto_bundle': 'Sosy1192dXRidU8zZURHbkRUT20yYUZVc2V2SXZzMTZKbmZFVDRFRkFzdnElMkZxdmRXUjc0ZWVSV1M2em9HbWt2a2tWZUpYREklMkZGa21XaXJvOGVLRElsUHBsVFltQUYlMkJuYldKSm85clg0SXBZOHBGVXJHaWFzOUdsRUF5Z1dVRkduS0FoTFFaenZEWWFDdCUyQkhHdmFOWHlkbWRyQSUzRCUzRA',
    '_clsk': '242tdq%7C1729579078732%7C2%7C0%7Cx.clarity.ms%2Fcollect',
    'WZRK_S_656-WZ5-7K5Z': '%7B%22p%22%3A2%2C%22s%22%3A1729579039%2C%22t%22%3A1729579197%7D',
    '_ga_LKNEBVRZRG': 'GS1.1.1729578998.46.1.1729579302.60.0.0',
    'SITE_VISIT_COUNT': '309',
}
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'bcookie=acada8b9-f715-48e7-9dd8-0dc9a7cbceaf; EXP_NEW_SIGN_UP=DEFAULT; EXP_CART_LOGIN_SEGMENT=A; EXP_ADP_RV_REORDER=B; EXP_ADP_RV_SEGMENT=A; EXP_AB_AUTOFILL=B; EXP_ADP_RV_VIEW_SIMILAR_HLP=A; EXP_ADP_RV_PLP_CONFIGURABLE_NO_RESULTS=A; EXP_ADP_RV_PRODUCT_V3=CONTROL; EXP_AB_HLP_CARD_REVAMP=CONTROL; EXP_AB_WISHLIST=A; EXP_AB_PRICE_REVEAL_NEW=A; EXP_EDD_DELIVERY_WIDGET=A; EXP_ADP_RV_MULTI_COUPONS=A; EXP_AB_DWEB_MULTICOUPON=A; EXP_ADP_RV_SEARCH_BAR_NEW=A; EXP_AB_AUTH_PAGE=A; EXP_AB_AUTH_DWEB=CONTROL; EXP_INCORRECT_SLUG_REDIRECT=A; EXP_SLP_RELATED_SEARCHES=A; EXP_AB_HLP_CTA=A; EXP_AB_PDP_IMAGE=DEFAULT; EXP_AB_CALLOUT_NUDGE=A; EXP_AB_PRICE_REVAMP=A; EXP_AB_TRUECALLER=DEFAULT; EXP_AB_GOOGLE_ONE_TAP=DEFAULT; EXP_AB_HLP_PAGE=A; EXP_ORGANIC_GUIDES=A; EXP_AB_NEW_PLP=A; EXP_PDP_RATING_REVAMP=A; EXP_AB_BREADCRUMB_POSITION=A; EXP_PRODUCT_CARD_CTA=A; EXP_AB_MULTI_MRP=A; EXP_AB_BRAND_SEP_PDP=A; EXP_AB_TOP_NAV_CONFIG=CONTROL; EXP_QUERY_PARAM_EXP_DWEB=CONTROL; EXP_AB_BEAUTY_PORTFOLIO=A; EXP_AB_HAMBURGUR_BANNER=A; EXP_AB_HP_SEARCH_ANIMATION=CONTROL; EXP_AB_PDP_HAMBURGER=CONTROL; EXP_AB_RECO_PRODUCT_V4=A; EXP_AB_WEB_AUTOREAD_OTP=A; EXP_AD_BRV=random; EXP_PDP_RELEVANT_CATEGORY=A; EXP_AB_PRODUCT_HIGHLIGHTS_CAROUSEL=A; EXP_AB_PR_FLASH_SALE_V5=A; EXP_AB_PRICE_FLUCTUATION=A; EXP_AB_IOC_CART_NUDGE=A; EXP_SNP_PRICE_FLUCTUATION_NUDGE=A; run=46; EXP_REVIEW_COLLECTION=1; D_LST=1; D_PDP=1; PHPSESSID=NY4lOPgb9G5gIfD1721109091120; WZRK_G=8be39919e4284de1b38e70092d24204c; EXP_PLP_INLINE_FILTER=REVAMPED; EXP_PLP_PINKBOX_CTA=CONTROL; EXP_AB_HLP_OFFERS=DEFAULT; EXP_AB_AUTO_FILL_OTP=A; EXP_AB_REMOVE_LOGIN_BOTTOMSHEET=DEFAULT; EXP_AB_HORIZONTAL_WIDGET_TYPE=CONTROL; EXP_AB_SOCIAL_PROOF_HLP=O_7; deduplication_cookie=Desktop_web_footer; deduplication_cookie=Desktop_web_footer; tt_deduplication_cookie=Desktop_web_footer; tt_deduplication_cookie=Desktop_web_footer; tt_deduplication_cookie=Desktop_web_footer; btIdentify=3e62843b-7afb-4714-b33a-680697756594; _bti=%7B%22bsin%22%3A%22%22%7D; unbxd.userId=uid-1723446894716-374; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=2121618341%7CMCIDTS%7C19948%7CMCMID%7C92083031616342837933557661350989532064%7CMCAAMLH-1724051694%7C12%7CMCAAMB-1724051694%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1723454094s%7CNONE%7CMCAID%7CNONE; EXP_AB_ZENDESK_CHAT=A; EXP_ADP_RV_VIEW_SIMILAR=C; EXP_QUERY_PARAM_EXP=C; EXP_AB_DWEB_SHOPPING_BAG_URL=A; EXP_CART_GRATIFICATION_POPUP=B; EXP_EXP_MULTI_COUPONS_REVAMP=DEFAULT; EXP_FULL_SCREEN_RECO_WIDGET=DEFAULT; EXP_AB_BEST_SELLER_PDP=DEFAULT; EXP_AB_PDP_HOME=B; EXP_ITEM_DISCOUNT=CONTROL; EXP_AB_PRODUCT_VARIENTS_ORDER=A; EXP_APPSFLYER_DOWNLOAD_CTA=DEFAULT; EXP_AB_ENABLE_HLP_NEW_API=A; N_S_B=1; S_S_B_S=0; countryCode=US; N_PV=true; C_DFA=false; B_NAV=false; N_P_M_S_P=true; ADDRESS_BACK_FRICTION=false; E_C=false; undefined=false; EXP_SPECULATIVE_PRERENDERING=DEFAULT; EXP_ORDERS_REVAMP=DEFAULT; _cfuvid=x2Hxq3dkBw35IpiuZCac77mDPMcVmA6BK6vBJypCZ1c-1729253248323-0.0.1.1-604800000; _gcl_au=1.1.461054102.1729253227; EXP_AB_PLP_PR_V5=DEFAULT; EXP_UPDATED_AT=1729510035439; EXP_SSR_CACHE=ba0d4fe8cf765806c9cba73c80294971; __cf_bm=.aGOrQj_Y5ibkNXxflJxydW8zq5.CAg0H7pjxUDeL9Q-1729579036-1.0.1.1-BjCgoQ4N20ScuCXQwAo6k14sglxCCBwu0ERqCI5S8JKI1ZwViyX0g8zFTbMpLw0HFAhDaK5wDt7X3_gVEKhHLQ; cf_clearance=ADxTgM6fX4EqGZeosYeTirKMJ.EpT7LVmcEIVrNk5Ys-1729579037-1.2.1.1-LSckyM8Ngevg1t1HboFpgTUn13A0IooskotyAtc.b6.vjkK61JnJzZ2oqtbjffldD98gJ8RDcikX9yjg.WtcHP3Qxlz7anijV_m1mzFSsHVt5kbQYuy1zQz7.6glmjpRhvGkf00cw3yK3bZvxMrCXt4_5Xe1j1k0jpOdjhS4QknzinUImyV71oidJPkToHmFYbUxmfd7qHB1lOJVKSELnPRpFtnaWxNQCEl080IEJ89zaIhKmtcxe4ZCmIWfSOfA8EcMUwH5q8xhc1dDIKj7cx7.axG.uKXWLF7QhLZqSvjaFFEbguue9A5iN.stP3W5SkjSynIsP.Vthfkz_1VkZR5vPJwFpiXHh5V3p3CT6SKP98vGHo3h.smsB5NjRSFX; head_data_react={"id":"","nykaa_pro":false,"group_id":""}; pro=false; _gid=GA1.2.1497177367.1729578999; _clck=gpws9u%7C2%7Cfq8%7C0%7C1752; ck_ptype=lst; ck_id=233; ck_root=nav_3; ck_dir=desc; ck_order=popularity; _ga=GA1.1.1291350165.1720180102; _uetsid=fe056dc0903f11efa30081afaf257caf; _uetvid=7f491e108d4911efbc785dcb0906df6b; _ga_JQ1CQHSXRX=GS1.2.1729578999.40.1.1729579077.60.0.0; cto_bundle=Sosy1192dXRidU8zZURHbkRUT20yYUZVc2V2SXZzMTZKbmZFVDRFRkFzdnElMkZxdmRXUjc0ZWVSV1M2em9HbWt2a2tWZUpYREklMkZGa21XaXJvOGVLRElsUHBsVFltQUYlMkJuYldKSm85clg0SXBZOHBGVXJHaWFzOUdsRUF5Z1dVRkduS0FoTFFaenZEWWFDdCUyQkhHdmFOWHlkbWRyQSUzRCUzRA; _clsk=242tdq%7C1729579078732%7C2%7C0%7Cx.clarity.ms%2Fcollect; WZRK_S_656-WZ5-7K5Z=%7B%22p%22%3A2%2C%22s%22%3A1729579039%2C%22t%22%3A1729579197%7D; _ga_LKNEBVRZRG=GS1.1.1729578998.46.1.1729579302.60.0.0; SITE_VISIT_COUNT=309',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEyMjUxNTkiLCJhcCI6IjEwMDE0NzQ3MTciLCJpZCI6IjE1ZmNlOTE2YTUzODcxOGEiLCJ0ciI6Ijg1MWY5N2Q5ZDZlZmIyNTQ3ZTIxY2M4MTA3Mzk2NzAwIiwidGkiOjE3Mjk1NzkzMDM1Njd9fQ==',
    'priority': 'u=1, i',
    'referer': 'https://www.nykaa.com/makeup/face/face-primer/c/233?ptype=lst&id=233&root=nav_3&dir=desc&order=popularity',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-851f97d9d6efb2547e21cc8107396700-15fce916a538718a-01',
    'tracestate': '1225159@nr=0-1-1225159-1001474717-15fce916a538718a----1729579303567',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'x-newrelic-id': 'undefined',
}
params = {
    'forDevice': 'desktop',
}

response = requests.get(
    'https://www.nykaa.com/app-api/index.php/react/navigation',
    params=params,
    cookies=cookies,
    headers=headers,
)

data = json.loads(response.text)
html_data = data.get('categories').get('categories')

selector = Selector(html_data)
main_cat = selector.xpath("//li[contains(@class,'MegaDropdownHeadingbox')]")
for main_category in main_cat:
    main_cat_name = main_category.xpath(".//a//text()").get().strip()
    categories = main_category.xpath(".//div[contains(@class,'MegaDropdown-ContentHeading')]")
    for category in categories:
        cat_name = category.xpath('.//a//text()').get()
        if not cat_name:
            cat_name = (category.xpath('.//text()').get())
        cat_name = cat_name.strip()
        sub_categories = category.xpath("./following-sibling::*[1]/li")
        if sub_categories == []:
            sub_categories = category.xpath("./following-sibling::div[contains(@class, 'megaDropdown') and not(child::*[1] = div)]/ul[1]/li")

        for sub_cat in sub_categories:
            if sub_cat.xpath('.//a//text()').get() != None:
                sub_cat_name = sub_cat.xpath('.//a//text()').get().strip()
                if not 'https://www.nykaa.com/' in sub_cat.xpath('.//a//@href').get():
                    cat_url = 'https://www.nykaa.com/' + sub_cat.xpath('.//a//@href').get().strip()
                else:
                    cat_url = sub_cat.xpath('.//a//@href').get().strip()
                cat_id = cat_url.strip().split('/c/')[-1] if not '?' in cat_url.strip().split('/c/')[-1] else cat_url.strip().split('/c/')[-1].split('?')[0]
                cat_id = int(cat_id) if cat_id.isdigit() else None

                price_lt = ['4000-*', '2000-3999', '1000-1999', '500-999', '0-499']
                for price_range in price_lt:
                    item ={
                        'main_cat_name': main_cat_name,
                        'cat_name': cat_name,
                        'sub_cat_name': sub_cat_name,
                        'cat_id': cat_id,
                        'price_range': price_range,
                        'cat_url': cat_url
                    }
                    db.insertItemToSql(item=item)