import requests
import json
import re


cookies = {
    'countryCode': 'IN',
    'storeId': 'nykaa',
    'bcookie': '4b0e13c6-a95b-4504-9557-1f9f126157d5',
    'EXP_AB_DWEB_SHOPPING_BAG_URL': 'A',
    'EXP_NEW_SIGN_UP': 'DEFAULT',
    'EXP_CART_GRATIFICATION_POPUP': 'B',
    'EXP_ITEM_DISCOUNT': 'A',
    'EXP_ORDERS_REVAMP': 'A',
    'EXP_AB_PDP_ACTION_CTA_V2': 'A',
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
    'EXP_AB_AUTH_DWEB': 'CONTROL',
    'EXP_INCORRECT_SLUG_REDIRECT': 'A',
    'EXP_PLP_PINKBOX_CTA': 'CONTROL',
    'EXP_SLP_RELATED_SEARCHES': 'A',
    'EXP_QUERY_PARAM_EXP': 'B',
    'EXP_AB_HLP_CTA': 'A',
    'EXP_AB_PDP_IMAGE': 'DEFAULT',
    'EXP_AB_CALLOUT_NUDGE': 'A',
    'EXP_AB_TRUECALLER': 'DEFAULT',
    'EXP_AB_GOOGLE_ONE_TAP': 'DEFAULT',
    'EXP_AB_HLP_PAGE': 'A',
    'EXP_ORGANIC_GUIDES': 'A',
    'EXP_AB_NEW_PLP': 'A',
    'EXP_AB_BREADCRUMB_POSITION': 'A',
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
    'EXP_PDP_RELEVANT_CATEGORY': 'CONTROL',
    'EXP_AB_REMOVE_LOGIN_BOTTOMSHEET': 'DEFAULT',
    'EXP_AB_ZENDESK_CHAT': 'A',
    'EXP_AB_ACCOUNT_REVAMP': 'A',
    'EXP_AB_HORIZONTAL_WIDGET_TYPE': 'CONTROL',
    'EXP_AB_IOC_CART_NUDGE': 'DEFAULT',
    'EXP_APPSFLYER_DOWNLOAD_CTA': 'DEFAULT',
    'EXP_AB_PDP_SIMILAR_PRODUCT_SHEET': 'DEFAULT',
    'EXP_FULL_SCREEN_RECO_WIDGET': 'DEFAULT',
    'EXP_AB_BEST_SELLER_PDP': 'CONTROL',
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
    'EXP_UPDATED_AT': '1745404603647',
    'EXP_SSR_CACHE': '9bcc03dcd3d7d85407c1e3b821a84c9f',
    '_gcl_gs': '2.1.k1$i1745500432$u269731310',
    '_gcl_au': '1.1.1977710893.1745500448',
    'utm_source': 'GooglePaid',
    'utm_medium': 'search',
    'utm_campaign': 'Search_Nykaa',
    '_gid': 'GA1.2.745219525.1745500449',
    '_gac_UA-31866293-9': '1.1745500449.EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE',
    '_clck': 'q7ip8s%7C2%7Cfvc%7C0%7C1940',
    'deduplication_cookie': 'GooglePaid',
    'deduplication_cookie': 'GooglePaid',
    '_ttgclid': 'EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE',
    '_ttgclid': 'EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE',
    '_ttgclid': 'EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE',
    'tt_deduplication_cookie': 'GooglePaid',
    'tt_deduplication_cookie': 'GooglePaid',
    'tt_deduplication_cookie': 'GooglePaid',
    'run': '69',
    'EXP_REVIEW_COLLECTION': '1',
    'D_LST': '1',
    'D_PDP': '1',
    'PHPSESSID': '7L6O867pULKZT4m1745500626041',
    'head_data_react': '{"id":"","nykaa_pro":false,"group_id":""}',
    'pro': 'false',
    'EXP_PLP_DNW_DWEB': 'DEFAULT',
    'WZRK_G': '8574852850384dc0824e34ba2cd62c2c',
    '_gcl_aw': 'GCL.1745500479.EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE',
    'ck_transaction_id': '8e5cf601287714c478b7e761e0056de9',
    'ck_intcmp': 'nykaa:sp:hair-clp-desktop:hair:l3:SLIDING_WIDGET_V2:3:Shampoos:-1:8e5cf601287714c478b7e761e0056de9',
    '_gat_UA-31866293-9': '1',
    'SITE_VISIT_COUNT': '10',
    'ck_ptype': 'lst',
    'ck_id': '316',
    'ck_root': 'nav_3',
    'ck_dir': 'desc',
    'ck_order': 'popularity',
    '_ga_LKNEBVRZRG': 'GS1.1.1745500448.1.1.1745500630.11.0.0',
    '_ga': 'GA1.2.1974991255.1745500449',
    'WZRK_S_656-WZ5-7K5Z': '%7B%22p%22%3A9%2C%22s%22%3A1745500629%2C%22t%22%3A1745500630%7D',
    '_ga_JQ1CQHSXRX': 'GS1.2.1745500449.1.1.1745500630.52.0.0',
    '_uetsid': '01b77a20210e11f0baac374ccab89430',
    '_uetvid': '01b7aef0210e11f0a981bfb5ef97145a',
    '_clsk': '1mgluka%7C1745500630931%7C8%7C1%7Cu.clarity.ms%2Fcollect',
    'cto_bundle': 'sCesSV8wa1p6eDBLY1VBWGVvRWpmYnIlMkZZb05Nbm5jSTJZS0ZUQ1NFSW13OTBzbk1Fa0laV2RDQXh4Mkd2Z2oxQ3FUSGQ1ZEZnUDRtaHhmWll5YkF2SHV4JTJGRko3NHNKVXRYWWhlVUVqcWJEYmxkZnV1TzB2Wld6bGJWVHlOT2pCcTdyZmRFYnVGY0F6cyUyRnlIMjhXRTlIWGQxdnclM0QlM0Q',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'countryCode=IN; storeId=nykaa; bcookie=4b0e13c6-a95b-4504-9557-1f9f126157d5; EXP_AB_DWEB_SHOPPING_BAG_URL=A; EXP_NEW_SIGN_UP=DEFAULT; EXP_CART_GRATIFICATION_POPUP=B; EXP_ITEM_DISCOUNT=A; EXP_ORDERS_REVAMP=A; EXP_AB_PDP_ACTION_CTA_V2=A; EXP_CART_LOGIN_SEGMENT=A; EXP_ADP_RV_REORDER=A; EXP_AB_CP_GAMES=A; EXP_ADP_RV_SEGMENT=A; EXP_AB_AUTOFILL=B; EXP_ADP_RV_VIEW_SIMILAR_HLP=A; EXP_ADP_RV_VIEW_SIMILAR=A; EXP_ADP_RV_PLP_CONFIGURABLE_NO_RESULTS=A; EXP_ADP_RV_PRODUCT_V3=CONTROL; EXP_AB_HLP_CARD_REVAMP=CONTROL; EXP_AB_WISHLIST=A; EXP_AB_PRICE_REVEAL_NEW=A; EXP_PLP_INLINE_FILTER=REVAMPED; EXP_EDD_DELIVERY_WIDGET=A; EXP_ADP_RV_MULTI_COUPONS=A; EXP_ADP_RV_SEARCH_BAR_NEW=A; EXP_AB_AUTH_DWEB=CONTROL; EXP_INCORRECT_SLUG_REDIRECT=A; EXP_PLP_PINKBOX_CTA=CONTROL; EXP_SLP_RELATED_SEARCHES=A; EXP_QUERY_PARAM_EXP=B; EXP_AB_HLP_CTA=A; EXP_AB_PDP_IMAGE=DEFAULT; EXP_AB_CALLOUT_NUDGE=A; EXP_AB_TRUECALLER=DEFAULT; EXP_AB_GOOGLE_ONE_TAP=DEFAULT; EXP_AB_HLP_PAGE=A; EXP_ORGANIC_GUIDES=A; EXP_AB_NEW_PLP=A; EXP_AB_BREADCRUMB_POSITION=A; EXP_PRODUCT_CARD_CTA=A; EXP_AB_SIZE_MINI_PRODUCT=A; EXP_AB_TOP_NAV_CONFIG=CONTROL; EXP_AB_PRODUCT_HIGHLIGHTS=A; EXP_QUERY_PARAM_EXP_DWEB=CONTROL; EXP_AB_BEAUTY_PORTFOLIO=A; EXP_AB_HP_SEARCH_ANIMATION=CONTROL; EXP_AB_PDP_HAMBURGER=CONTROL; EXP_AB_HLP_OFFERS=DEFAULT; EXP_AB_WEB_AUTOREAD_OTP=DEFAULT; EXP_AD_BRV=variant1; EXP_PDP_RELEVANT_CATEGORY=CONTROL; EXP_AB_REMOVE_LOGIN_BOTTOMSHEET=DEFAULT; EXP_AB_ZENDESK_CHAT=A; EXP_AB_ACCOUNT_REVAMP=A; EXP_AB_HORIZONTAL_WIDGET_TYPE=CONTROL; EXP_AB_IOC_CART_NUDGE=DEFAULT; EXP_APPSFLYER_DOWNLOAD_CTA=DEFAULT; EXP_AB_PDP_SIMILAR_PRODUCT_SHEET=DEFAULT; EXP_FULL_SCREEN_RECO_WIDGET=DEFAULT; EXP_AB_BEST_SELLER_PDP=CONTROL; EXP_AB_ENABLE_HLP_NEW_API=DEFAULT; EXP_SPECULATIVE_PRERENDERING=DEFAULT; EXP_AB_TAGS_RATING_ON_LISTING=ONLY_TAGS; EXP_SEARCH_INP_ON_CART=B; EXP_AB_NEW_TAGS_ON_PDP=DEFAULT; EXP_REVIEW_SUBMIT=A; EXP_AB_GUIDES_V2=A; EXP_AB_OFFER_DELTA_COMMUNICATION=DEFAULT; EXP_AB_HLP_COUPON_OFFERS=A; EXP_AB_NEW_GC_PAGE=A; EXP_UPDATED_AT=1745404603647; EXP_SSR_CACHE=9bcc03dcd3d7d85407c1e3b821a84c9f; _gcl_gs=2.1.k1$i1745500432$u269731310; _gcl_au=1.1.1977710893.1745500448; utm_source=GooglePaid; utm_medium=search; utm_campaign=Search_Nykaa; _gid=GA1.2.745219525.1745500449; _gac_UA-31866293-9=1.1745500449.EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE; _clck=q7ip8s%7C2%7Cfvc%7C0%7C1940; deduplication_cookie=GooglePaid; deduplication_cookie=GooglePaid; _ttgclid=EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE; _ttgclid=EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE; _ttgclid=EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE; tt_deduplication_cookie=GooglePaid; tt_deduplication_cookie=GooglePaid; tt_deduplication_cookie=GooglePaid; run=69; EXP_REVIEW_COLLECTION=1; D_LST=1; D_PDP=1; PHPSESSID=7L6O867pULKZT4m1745500626041; head_data_react={"id":"","nykaa_pro":false,"group_id":""}; pro=false; EXP_PLP_DNW_DWEB=DEFAULT; WZRK_G=8574852850384dc0824e34ba2cd62c2c; _gcl_aw=GCL.1745500479.EAIaIQobChMIz83uteDwjAMVqzh7Bx3TKzc2EAAYASAAEgI5QPD_BwE; ck_transaction_id=8e5cf601287714c478b7e761e0056de9; ck_intcmp=nykaa:sp:hair-clp-desktop:hair:l3:SLIDING_WIDGET_V2:3:Shampoos:-1:8e5cf601287714c478b7e761e0056de9; _gat_UA-31866293-9=1; SITE_VISIT_COUNT=10; ck_ptype=lst; ck_id=316; ck_root=nav_3; ck_dir=desc; ck_order=popularity; _ga_LKNEBVRZRG=GS1.1.1745500448.1.1.1745500630.11.0.0; _ga=GA1.2.1974991255.1745500449; WZRK_S_656-WZ5-7K5Z=%7B%22p%22%3A9%2C%22s%22%3A1745500629%2C%22t%22%3A1745500630%7D; _ga_JQ1CQHSXRX=GS1.2.1745500449.1.1.1745500630.52.0.0; _uetsid=01b77a20210e11f0baac374ccab89430; _uetvid=01b7aef0210e11f0a981bfb5ef97145a; _clsk=1mgluka%7C1745500630931%7C8%7C1%7Cu.clarity.ms%2Fcollect; cto_bundle=sCesSV8wa1p6eDBLY1VBWGVvRWpmYnIlMkZZb05Nbm5jSTJZS0ZUQ1NFSW13OTBzbk1Fa0laV2RDQXh4Mkd2Z2oxQ3FUSGQ1ZEZnUDRtaHhmWll5YkF2SHV4JTJGRko3NHNKVXRYWWhlVUVqcWJEYmxkZnV1TzB2Wld6bGJWVHlOT2pCcTdyZmRFYnVGY0F6cyUyRnlIMjhXRTlIWGQxdnclM0QlM0Q',
}

params = {
    'ptype': 'lst',
    'id': '316',
    'root': 'nav_3',
    'dir': 'desc',
    'order': 'popularity',
}

response = requests.get('https://www.nykaa.com/hair-care/hair/shampoo/c/316', params=params, cookies=cookies, headers=headers)

# print(response.text)
script_content = response.text
match = re.search(r'window\.__PRELOADED_STATE__ = ({.*?})</script><script id="__LOADABLE_REQUIRED_CHUNKS__"', script_content, re.DOTALL)

# print(match)

if match:
    # Extract the matched JSON content
    json_str = match.group(1)
    print("Captured JSON string:")
    # print(json_str)

    # Ensure no extra characters and parse the JSON
    try:
        preloaded_state = json.loads(json_str[:274163])  # Convert JSON string to Python dictionary
        print(preloaded_state)

        file_name = "data.json"

        # Open the file in write mode and write the dictionary as a JSON object
        with open(file_name, 'w') as json_file:
            json.dump(preloaded_state, json_file, indent=4)

        breadcrumb = preloaded_state.get('appReducer', {}).get('breadCrumb', [])

        for item in breadcrumb:
            print(item)
            # print(f"Key: {item['key']}, Value: {item['value']}")

        # print("Page Type:", preloaded_state.get('appReducer', {}).get('pageType'))
        # print("Region:", preloaded_state.get('appReducer', {}).get('region', {}).get('regionHeader'))

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
else:
    print("No match found for the preloaded state.")