import hashlib
import os
from datetime import datetime
from curl_cffi import requests
import json
import mysql.connector
import scrapy
from scrapy.cmdline import execute
from nykaa_fs.config.database_config import ConfigDatabase


class PdpLinkSpider(scrapy.Spider):
    name = "pdp_link"
    allowed_domains = ["www.example.com"]
    start_urls = ["https://www.example.com"]
    db = ConfigDatabase(database='nykaa_latest', table='new_cat_links')
    db2 = ConfigDatabase(database='nykaa_latest', table='prod_link_latest_trial')

    def __init__(self, start, end):
        self.start = start
        self.end = end
        table_creation_query = f"""
                               CREATE TABLE IF NOT EXISTS {self.db2.table} (
                                  `id` int NOT NULL AUTO_INCREMENT,
                                  `main_cat_name` varchar(100) DEFAULT NULL,
                                  `cat_name` varchar(100) DEFAULT NULL,
                                  `sub_cat_name` varchar(100) DEFAULT NULL,
                                  `prod_id` int DEFAULT NULL,
                                  `prod_url` text,
                                  `cat_id` varchar(20) DEFAULT NULL,
                                  `hash_id` text,
                                  `tags` text,
                                  `status` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'pending',
                                  PRIMARY KEY (`id`),
                                  UNIQUE KEY `UNIQUE` (`prod_id`)
                                ) ENGINE=InnoDB AUTO_INCREMENT=115642 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
 
                               """
        self.db2.crsrSql.execute(table_creation_query)

    def parse(self, response):
        # todo: pagesave path
        path = f'D:/Data/Chirag/pagesave/nykaa_latest_december/pdp_links/'

        cat_data = self.db.fetchResultsfromSql(conditions={'status': 'pending'},
                                               start=self.start, end=self.end)
        if not os.path.exists(path):
            os.makedirs(path)

        for data_ in cat_data:
            cat_id = data_['cat_id']
            main_cat_name = data_['main_cat_name']
            cat_name = data_['cat_name']
            price_range = data_['price_range']
            # segment = data_['segment_code']
            sub_cat_name = data_['sub_cat_name']
            url = data_['cat_url'].split('?')[0] if '?' in data_['cat_url'] else data_['cat_url']

            page_no = 1

            while page_no<501:
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
                    'EXP_AD_BRV': 'random',
                    'EXP_PDP_RELEVANT_CATEGORY': 'A',
                    'EXP_AB_PRODUCT_HIGHLIGHTS_CAROUSEL': 'A',
                    'EXP_AB_PR_FLASH_SALE_V5': 'A',
                    'EXP_AB_PRICE_FLUCTUATION': 'A',
                    'EXP_SNP_PRICE_FLUCTUATION_NUDGE': 'A',
                    'WZRK_G': '8be39919e4284de1b38e70092d24204c',
                    'EXP_PLP_INLINE_FILTER': 'REVAMPED',
                    'EXP_AB_HLP_OFFERS': 'DEFAULT',
                    'EXP_AB_AUTO_FILL_OTP': 'A',
                    'EXP_AB_REMOVE_LOGIN_BOTTOMSHEET': 'DEFAULT',
                    'EXP_AB_HORIZONTAL_WIDGET_TYPE': 'CONTROL',
                    'EXP_AB_SOCIAL_PROOF_HLP': 'O_7',
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
                    'EXP_AB_BEST_SELLER_PDP': 'DEFAULT',
                    'EXP_AB_PDP_HOME': 'B',
                    'EXP_AB_PRODUCT_VARIENTS_ORDER': 'A',
                    'EXP_APPSFLYER_DOWNLOAD_CTA': 'DEFAULT',
                    'N_S_B': '1',
                    'S_S_B_S': '0',
                    'EXP_SPECULATIVE_PRERENDERING': 'DEFAULT',
                    'EXP_ORDERS_REVAMP': 'DEFAULT',
                    '_gcl_au': '1.1.461054102.1729253227',
                    'EXP_AB_WEB_AUTOREAD_OTP': 'DEFAULT',
                    'EXP_AB_IOC_CART_NUDGE': 'DEFAULT',
                    'EXP_ITEM_DISCOUNT': 'A',
                    'EXP_AB_ENABLE_HLP_NEW_API': 'DEFAULT',
                    'EXP_AB_PLP_PR_V5': 'A',
                    'EXP_AB_PDP_ACTION_CTA_V2': 'A',
                    'EXP_AB_CP_GAMES': 'A',
                    'EXP_AB_TAGS_RATING_ON_LISTING': 'ONLY_TAGS',
                    'run': '86',
                    'EXP_REVIEW_COLLECTION': '1',
                    'D_LST': '1',
                    'D_PDP': '1',
                    'PHPSESSID': 'r6p4Sym8gMYRGoe1732180080963',
                    'EXP_PLP_PINKBOX_CTA': 'CONTROL',
                    'EXP_SNP_BEST_PRICE': 'A',
                    'EXP_FULL_SCREEN_RECO_WIDGET': 'DEFAULT',
                    'EXP_SSR_CACHE': '4a873da976d834a88328d8404e6ee3a3',
                    'head_data_react': '{"id":"","nykaa_pro":false,"group_id":""}',
                    'pro': 'false',
                    '_gid': 'GA1.2.965404068.1733714003',
                    '_ga_LKNEBVRZRG': 'deleted',
                    '_clck': 'gpws9u%7C2%7Cfrk%7C0%7C1752',
                    '_cfuvid': 'eD0jpKpH3rNndntBI5pATh782J5wgcgcLoK6BFG4580-1733744267857-0.0.1.1-604800000',
                    'ck_ptype': 'lst',
                    'ck_dir': 'desc',
                    'ck_order': 'popularity',
                    'ck_root': 'nav_2',
                    'EXP_UPDATED_AT': '1731565381735',
                    'ck_id': '1292',
                    'ck_redirectpath': 'slug',
                    'ck_page_no': '1',
                    'ck_sort': 'popularity',
                    'ck_eq': 'desktop',
                    '__cf_bm': 'T9_dNvUZjhhwSA8Mwp3oalo4TbFAis3A3myrbp9xrh8-1733751228-1.0.1.1-xq2mLOWdWzE25EZ.ySf92_JNVv_hhLplEBJJNuMo7L50tjtz9IiXKX6JETGWUJKXseTFjvBSpmLcbwFdYI3CBA',
                    'cf_clearance': 'eU1fRV365FzlhUQxELF39eLDyJzn_g5DkA.ZZpq.KNI-1733751229-1.2.1.1-LeVrgyJjaMrxsZzzs0yE9bB.qe_uury_9DChenEAnHSadDnYXTL9pWqFNNiE6EEkgOrf6z1u.N0x6zrkxXkT0OxD3hM_a.aWBWiqsLWlkKAxtzTdMpz5VpncD2jLjHPzdC_PRruI3UENBzYRZNwLX4kvtKN_LsHZdelNs9EFh4H7kWwAwbulSZNKjg55FsJg_yo7bASAMtYhmCo5t46BtUjE71ilX3H_4Y92od2OFo7pcZkeoQIOUgOtd7..rRj1vtaDy9C4HmqMJmmCgJFWtx5H6JKvA.hFCUE99LtExufHxQ158SxppE3jV6dh3mN.kXY3V3ST0xFD_B9zPdRlEDUHKC9AhmLzTZKVR5XL_wO4T60kO5HdQAWNr525pUjk',
                    'SITE_VISIT_COUNT': '375',
                    'ck_price_range_filter': '1000-1999',
                    '_ga': 'GA1.2.1291350165.1720180102',
                    '_uetsid': '8c697960b5db11ef87fcf7108e1acc1d',
                    '_uetvid': '7f491e108d4911efbc785dcb0906df6b',
                    'cto_bundle': 'QoUEil92dXRidU8zZURHbkRUT20yYUZVc2VsUEFuczM4aEhHbzJ4SFJDdURSd1dLNzR4Q2RFWkxwMzVieTVLQXVGdWl4U3U4MTVVVER6SFRuQm5qYlhQcWE0TUlTTG1SSURmdXpDRjVFNnFFdnlhd1lOQlozaFhWQWJ4TXM2WGkzY2pKdGNPSVYxU2hhSk56a3lqUml0SEl1SVElM0QlM0Q',
                    '_ga_JQ1CQHSXRX': 'GS1.2.1733747202.45.1.1733751507.60.0.0',
                    '_ga_LKNEBVRZRG': 'GS1.1.1733747201.3.1.1733751508.54.0.0',
                    '_clsk': '9zimjo%7C1733751508973%7C6%7C0%7Cz.clarity.ms%2Fcollect',
                    'WZRK_S_656-WZ5-7K5Z': '%7B%22p%22%3A44%2C%22s%22%3A1733748766%2C%22t%22%3A1733751514%7D',
                }
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'cache-control': 'max-age=0',
                    # 'cookie': 'bcookie=acada8b9-f715-48e7-9dd8-0dc9a7cbceaf; EXP_NEW_SIGN_UP=DEFAULT; EXP_CART_LOGIN_SEGMENT=A; EXP_ADP_RV_REORDER=B; EXP_ADP_RV_SEGMENT=A; EXP_AB_AUTOFILL=B; EXP_ADP_RV_VIEW_SIMILAR_HLP=A; EXP_ADP_RV_PLP_CONFIGURABLE_NO_RESULTS=A; EXP_ADP_RV_PRODUCT_V3=CONTROL; EXP_AB_HLP_CARD_REVAMP=CONTROL; EXP_AB_WISHLIST=A; EXP_AB_PRICE_REVEAL_NEW=A; EXP_EDD_DELIVERY_WIDGET=A; EXP_ADP_RV_MULTI_COUPONS=A; EXP_AB_DWEB_MULTICOUPON=A; EXP_ADP_RV_SEARCH_BAR_NEW=A; EXP_AB_AUTH_PAGE=A; EXP_AB_AUTH_DWEB=CONTROL; EXP_INCORRECT_SLUG_REDIRECT=A; EXP_SLP_RELATED_SEARCHES=A; EXP_AB_HLP_CTA=A; EXP_AB_PDP_IMAGE=DEFAULT; EXP_AB_CALLOUT_NUDGE=A; EXP_AB_PRICE_REVAMP=A; EXP_AB_TRUECALLER=DEFAULT; EXP_AB_GOOGLE_ONE_TAP=DEFAULT; EXP_AB_HLP_PAGE=A; EXP_ORGANIC_GUIDES=A; EXP_AB_NEW_PLP=A; EXP_PDP_RATING_REVAMP=A; EXP_AB_BREADCRUMB_POSITION=A; EXP_PRODUCT_CARD_CTA=A; EXP_AB_MULTI_MRP=A; EXP_AB_BRAND_SEP_PDP=A; EXP_AB_TOP_NAV_CONFIG=CONTROL; EXP_QUERY_PARAM_EXP_DWEB=CONTROL; EXP_AB_BEAUTY_PORTFOLIO=A; EXP_AB_HAMBURGUR_BANNER=A; EXP_AB_HP_SEARCH_ANIMATION=CONTROL; EXP_AB_PDP_HAMBURGER=CONTROL; EXP_AB_RECO_PRODUCT_V4=A; EXP_AD_BRV=random; EXP_PDP_RELEVANT_CATEGORY=A; EXP_AB_PRODUCT_HIGHLIGHTS_CAROUSEL=A; EXP_AB_PR_FLASH_SALE_V5=A; EXP_AB_PRICE_FLUCTUATION=A; EXP_SNP_PRICE_FLUCTUATION_NUDGE=A; WZRK_G=8be39919e4284de1b38e70092d24204c; EXP_PLP_INLINE_FILTER=REVAMPED; EXP_AB_HLP_OFFERS=DEFAULT; EXP_AB_AUTO_FILL_OTP=A; EXP_AB_REMOVE_LOGIN_BOTTOMSHEET=DEFAULT; EXP_AB_HORIZONTAL_WIDGET_TYPE=CONTROL; EXP_AB_SOCIAL_PROOF_HLP=O_7; btIdentify=3e62843b-7afb-4714-b33a-680697756594; _bti=%7B%22bsin%22%3A%22%22%7D; unbxd.userId=uid-1723446894716-374; AMCV_FE9A65E655E6E38A7F000101%40AdobeOrg=2121618341%7CMCIDTS%7C19948%7CMCMID%7C92083031616342837933557661350989532064%7CMCAAMLH-1724051694%7C12%7CMCAAMB-1724051694%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1723454094s%7CNONE%7CMCAID%7CNONE; EXP_AB_ZENDESK_CHAT=A; EXP_ADP_RV_VIEW_SIMILAR=C; EXP_QUERY_PARAM_EXP=C; EXP_AB_DWEB_SHOPPING_BAG_URL=A; EXP_CART_GRATIFICATION_POPUP=B; EXP_EXP_MULTI_COUPONS_REVAMP=DEFAULT; EXP_AB_BEST_SELLER_PDP=DEFAULT; EXP_AB_PDP_HOME=B; EXP_AB_PRODUCT_VARIENTS_ORDER=A; EXP_APPSFLYER_DOWNLOAD_CTA=DEFAULT; N_S_B=1; S_S_B_S=0; EXP_SPECULATIVE_PRERENDERING=DEFAULT; EXP_ORDERS_REVAMP=DEFAULT; _gcl_au=1.1.461054102.1729253227; EXP_AB_WEB_AUTOREAD_OTP=DEFAULT; EXP_AB_IOC_CART_NUDGE=DEFAULT; EXP_ITEM_DISCOUNT=A; EXP_AB_ENABLE_HLP_NEW_API=DEFAULT; EXP_AB_PLP_PR_V5=A; EXP_AB_PDP_ACTION_CTA_V2=A; EXP_AB_CP_GAMES=A; EXP_AB_TAGS_RATING_ON_LISTING=ONLY_TAGS; run=86; EXP_REVIEW_COLLECTION=1; D_LST=1; D_PDP=1; PHPSESSID=r6p4Sym8gMYRGoe1732180080963; EXP_PLP_PINKBOX_CTA=CONTROL; EXP_SNP_BEST_PRICE=A; EXP_FULL_SCREEN_RECO_WIDGET=DEFAULT; EXP_SSR_CACHE=4a873da976d834a88328d8404e6ee3a3; head_data_react={"id":"","nykaa_pro":false,"group_id":""}; pro=false; _gid=GA1.2.965404068.1733714003; _ga_LKNEBVRZRG=deleted; _clck=gpws9u%7C2%7Cfrk%7C0%7C1752; _cfuvid=eD0jpKpH3rNndntBI5pATh782J5wgcgcLoK6BFG4580-1733744267857-0.0.1.1-604800000; ck_ptype=lst; ck_dir=desc; ck_order=popularity; ck_root=nav_2; EXP_UPDATED_AT=1731565381735; ck_id=1292; ck_redirectpath=slug; ck_page_no=1; ck_sort=popularity; ck_eq=desktop; __cf_bm=T9_dNvUZjhhwSA8Mwp3oalo4TbFAis3A3myrbp9xrh8-1733751228-1.0.1.1-xq2mLOWdWzE25EZ.ySf92_JNVv_hhLplEBJJNuMo7L50tjtz9IiXKX6JETGWUJKXseTFjvBSpmLcbwFdYI3CBA; cf_clearance=eU1fRV365FzlhUQxELF39eLDyJzn_g5DkA.ZZpq.KNI-1733751229-1.2.1.1-LeVrgyJjaMrxsZzzs0yE9bB.qe_uury_9DChenEAnHSadDnYXTL9pWqFNNiE6EEkgOrf6z1u.N0x6zrkxXkT0OxD3hM_a.aWBWiqsLWlkKAxtzTdMpz5VpncD2jLjHPzdC_PRruI3UENBzYRZNwLX4kvtKN_LsHZdelNs9EFh4H7kWwAwbulSZNKjg55FsJg_yo7bASAMtYhmCo5t46BtUjE71ilX3H_4Y92od2OFo7pcZkeoQIOUgOtd7..rRj1vtaDy9C4HmqMJmmCgJFWtx5H6JKvA.hFCUE99LtExufHxQ158SxppE3jV6dh3mN.kXY3V3ST0xFD_B9zPdRlEDUHKC9AhmLzTZKVR5XL_wO4T60kO5HdQAWNr525pUjk; SITE_VISIT_COUNT=375; ck_price_range_filter=1000-1999; _ga=GA1.2.1291350165.1720180102; _uetsid=8c697960b5db11ef87fcf7108e1acc1d; _uetvid=7f491e108d4911efbc785dcb0906df6b; cto_bundle=QoUEil92dXRidU8zZURHbkRUT20yYUZVc2VsUEFuczM4aEhHbzJ4SFJDdURSd1dLNzR4Q2RFWkxwMzVieTVLQXVGdWl4U3U4MTVVVER6SFRuQm5qYlhQcWE0TUlTTG1SSURmdXpDRjVFNnFFdnlhd1lOQlozaFhWQWJ4TXM2WGkzY2pKdGNPSVYxU2hhSk56a3lqUml0SEl1SVElM0QlM0Q; _ga_JQ1CQHSXRX=GS1.2.1733747202.45.1.1733751507.60.0.0; _ga_LKNEBVRZRG=GS1.1.1733747201.3.1.1733751508.54.0.0; _clsk=9zimjo%7C1733751508973%7C6%7C0%7Cz.clarity.ms%2Fcollect; WZRK_S_656-WZ5-7K5Z=%7B%22p%22%3A44%2C%22s%22%3A1733748766%2C%22t%22%3A1733751514%7D',
                    'priority': 'u=0, i',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                }
                # params = {
                #     'page_no': f'{page_no}',
                #     'sort': 'popularity',
                #     # 'id': f'{cat_id}',
                #     'redirectpath': 'slug',
                #     'eq': 'desktop',
                #     'price_range_filter': f'{price_range}'
                # }

                data_response = requests.get(url + f'?page_no={page_no}&sort=popularity&eq=desktop&price_range_filter={price_range}', cookies=cookies,
                                             headers=headers, timeout=60)

                data = json.loads(
                    data_response.text.split("window.__PRELOADED_STATE__ =")[-1].split(
                        "</script><script>window.__APP_DATA__ =")[0])

                # try:
                prd_lt = data.get('categoryListing', {}).get('listingData',{}).get('products',[])
                # except:
                #     print(f'{cat_id} Done')
                #     update_query = """
                #                       UPDATE new_cat_links SET status='Done' WHERE cat_id = %s and price_range = %s
                #                    """
                #     self.db.crsrSql.execute(update_query, (cat_id, price_range))
                #     self.db.connSql.commit()
                #     # curr.execute(update_query, (cat_id, price_range))
                #     # conn.commit()
                #     break

                # query = f"""CREATE TABLE IF NOT EXISTS`pdp_link_{datetime.now().strftime('%d_%m_%Y')}` (
                #                       `id` int NOT NULL AUTO_INCREMENT,
                #                       `prod_id` int UNIQUE,
                #                       `slug` text,
                #                       `cat_id` int DEFAULT NULL,
                #                       `hash_id` text,
                #                       `tags` text,
                #                       `status` varchar(11) DEFAULT 'pending',
                #                         PRIMARY KEY (`id`),
                #                         KEY `id` (`id`)
                #                     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
                #                 """
                # curr.execute(query)

                if prd_lt:
                    hash_id = str(
                        int(hashlib.md5(bytes(str(cat_id) + str(page_no) + str(price_range), "utf8")).hexdigest(),
                            16) % (10 ** 10))

                    with open(path + f'{hash_id}.json', 'wb') as f:
                        f.write(str.encode(json.dumps(data)))

                    for prod in prd_lt:
                        prod_id = prod.get('productId')
                        try:
                            prod_url = 'https://www.nykaa.com/' + prod.get('slug')
                        except:
                            prod_url = 'N/A'

                        tags = []
                        if prod.get('newTags'):
                            for tag_det in prod.get('newTags'):
                                tag = tag_det.get('title')
                                tags.append(tag)
                        cat_id = cat_id
                        hash_id = hash_id
                        try:
                            item = {
                                'main_cat_name': main_cat_name,
                                'cat_name': cat_name,
                                'sub_cat_name': sub_cat_name,
                                'prod_id': prod_id,
                                'prod_url': prod_url,
                                'cat_id': cat_id,
                                'hash_id': hash_id,
                                'tags': tags,
                            }
                            self.db2.insertItemToSql(item=item)
                        except Exception as e:
                            print(e)
                    print(f'{page_no}---------------')

                    page_no += 1
                else:
                    print(f'{cat_id}-------------{price_range}----------Done')
                    update_query = """
                                    UPDATE new_cat_links SET status='Done' WHERE cat_id = %s and price_range = %s 
                                   """
                    self.db.crsrSql.execute(update_query, (cat_id, price_range))
                    self.db.connSql.commit()
                    # curr.execute(update_query, (cat_id, price_range, segment))
                    # conn.commit()
                    break
            else:
                print(f'{cat_id}-------------{price_range}----------Partial_Done')
                update_query = """
                                   UPDATE new_cat_links SET status='Partial_Done' WHERE cat_id = %s and price_range = %s 
                               """
                self.db.crsrSql.execute(update_query, (cat_id, price_range))
                self.db.connSql.commit()


if __name__ == "__main__":
    execute(f'scrapy crawl {PdpLinkSpider.name} -a start=1 -a end=3238'.split())
    # todo: need to apply segment filter when the product count is more than 10000 or the page count is more than 500
    # todo:After applying the filter you need to take care of certain parameters example what will be the segment filter value, and need to create new table for that value with segment filter value
    # segment_filter=214440,153299,126127,126126,152823,219195,126125