import requests
import re
import csv
import json
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

cookies = {
    'bcookie': '3615be7e-317a-488a-8cd2-4863fe7de37a',
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
    'EXP_AB_DWEB_MULTICOUPON': 'A',
    'EXP_ADP_RV_SEARCH_BAR_NEW': 'A',
    'EXP_AB_AUTH_DWEB': 'A',
    'EXP_INCORRECT_SLUG_REDIRECT': 'A',
    'EXP_PLP_INLINE_WIDGETS': 'A',
    'EXP_PLP_PINKBOX_CTA': 'CONTROL',
    'EXP_SLP_RELATED_SEARCHES': 'A',
    'EXP_QUERY_PARAM_EXP': 'C',
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
    'EXP_AD_BRV': 'random',
    'EXP_PDP_RELEVANT_CATEGORY': 'CONTROL',
    'EXP_AB_REMOVE_LOGIN_BOTTOMSHEET': 'DEFAULT',
    'EXP_AB_ZENDESK_CHAT': 'A',
    'EXP_AB_ACCOUNT_REVAMP': 'DEFAULT',
    'EXP_AB_HORIZONTAL_WIDGET_TYPE': 'CONTROL',
    'EXP_AB_IOC_CART_NUDGE': 'DEFAULT',
    'EXP_APPSFLYER_DOWNLOAD_CTA': 'DEFAULT',
    'EXP_AB_PDP_SIMILAR_PRODUCT_SHEET': 'DEFAULT',
    'EXP_FULL_SCREEN_RECO_WIDGET': 'DEFAULT',
    'EXP_AB_BEST_SELLER_PDP': 'CONTROL',
    'EXP_AB_ENABLE_HLP_NEW_API': 'DEFAULT',
    'EXP_SPECULATIVE_PRERENDERING': 'A',
    'EXP_AB_TAGS_RATING_ON_LISTING': 'ONLY_TAGS',
    'EXP_SEARCH_INP_ON_CART': 'CONTROL',
    'EXP_AB_NEW_TAGS_ON_PDP': 'DEFAULT',
    'EXP_REVIEW_SUBMIT': 'A',
    'EXP_AB_GUIDES_V2': 'CONTROL',
    'EXP_AB_OFFER_DELTA_COMMUNICATION': 'DEFAULT',
    'EXP_AB_HLP_COUPON_OFFERS': 'A',
    'EXP_AB_NEW_GC_PAGE': 'A',
    'EXP_PLP_DNW_DWEB': 'A',
    'EXP_UPDATED_AT': '1745591203545',
    'EXP_SSR_CACHE': '5639a8a22b34af4817be8d00a18e0468',
    'run': '23',
    'EXP_REVIEW_COLLECTION': '1',
    'D_LST': '1',
    'D_PDP': '1',
    'PHPSESSID': 'EEF02kw9axSt1f31745814411674',
    'head_data_react': '{"id":"","nykaa_pro":false,"group_id":""}',
    'pro': 'false',
    '_gcl_gs': '2.1.k1$i1745814396$u269731310',
    '_gcl_au': '1.1.1433646885.1745814401',
    'utm_source': 'GooglePaid',
    'utm_medium': 'search',
    'utm_campaign': 'Search_Nykaa',
    '_gcl_aw': 'GCL.1745814402.EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE',
    'deduplication_cookie': 'GooglePaid',
    'deduplication_cookie': 'GooglePaid',
    'WZRK_G': '4acc75a4be874dc2b698b5f1fde88289',
    '_gid': 'GA1.2.1791180062.1745814402',
    '_gac_UA-31866293-9': '1.1745814402.EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE',
    '_clck': '1fhl761%7C2%7Cfvg%7C0%7C1944',
    '_ttgclid': 'EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE',
    '_ttgclid': 'EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE',
    '_ttgclid': 'EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE',
    'tt_deduplication_cookie': 'GooglePaid',
    'tt_deduplication_cookie': 'GooglePaid',
    'tt_deduplication_cookie': 'GooglePaid',
    'countryCode': 'IN',
    'storeId': 'nykaa',
    'SITE_VISIT_COUNT': '2',
    '_ga_LKNEBVRZRG': 'GS1.1.1745818270.2.1.1745818274.56.0.0',
    'WZRK_S_656-WZ5-7K5Z': '%7B%22p%22%3A1%2C%22s%22%3A1745818291%2C%22t%22%3A1745818274%7D',
    '_ga': 'GA1.2.756707784.1745814402',
    '_gat_UA-31866293-9': '1',
    '_uetsid': 'fca325d023e811f0a3d5c733dcee03e5',
    '_uetvid': 'fca3a29023e811f0b3ffbbddf2b059f7',
    'cto_bundle': 'Pauek190ZndiQ1FhclVFWVNQRjFLNmtHUlRNTiUyQlFHZGZvRFdMN2xzeHdQSlRRNTdrV3FxRVA2Nm1lWm52elJFWkdWZ1hySDRKVkdkSiUyQks4T2hkQVBIbTBBUTlKSGdTTHFKUHlFYVJSdUpIUVdvYVJXQU5NQSUyRm52QiUyQlNlYjFMbVpKbnhMaTlOa25PVzBmTWJrcCUyRkpLT3E2SGF3JTNEJTNE',
    '_clsk': 'gtx7zf%7C1745818275315%7C1%7C1%7Cu.clarity.ms%2Fcollect',
    '_ga_JQ1CQHSXRX': 'GS1.2.1745818275.2.0.1745818275.60.0.0',
    'pinCodeDel': '380025',
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
    # 'cookie': 'bcookie=3615be7e-317a-488a-8cd2-4863fe7de37a; EXP_AB_DWEB_SHOPPING_BAG_URL=A; EXP_NEW_SIGN_UP=DEFAULT; EXP_CART_GRATIFICATION_POPUP=B; EXP_ITEM_DISCOUNT=A; EXP_ORDERS_REVAMP=A; EXP_AB_PDP_ACTION_CTA_V2=A; EXP_CART_LOGIN_SEGMENT=A; EXP_ADP_RV_REORDER=A; EXP_AB_CP_GAMES=A; EXP_ADP_RV_SEGMENT=A; EXP_AB_AUTOFILL=B; EXP_ADP_RV_VIEW_SIMILAR_HLP=A; EXP_ADP_RV_VIEW_SIMILAR=A; EXP_ADP_RV_PLP_CONFIGURABLE_NO_RESULTS=A; EXP_ADP_RV_PRODUCT_V3=CONTROL; EXP_AB_HLP_CARD_REVAMP=CONTROL; EXP_AB_WISHLIST=A; EXP_AB_PRICE_REVEAL_NEW=A; EXP_PLP_INLINE_FILTER=REVAMPED; EXP_EDD_DELIVERY_WIDGET=A; EXP_ADP_RV_MULTI_COUPONS=A; EXP_AB_DWEB_MULTICOUPON=A; EXP_ADP_RV_SEARCH_BAR_NEW=A; EXP_AB_AUTH_DWEB=A; EXP_INCORRECT_SLUG_REDIRECT=A; EXP_PLP_INLINE_WIDGETS=A; EXP_PLP_PINKBOX_CTA=CONTROL; EXP_SLP_RELATED_SEARCHES=A; EXP_QUERY_PARAM_EXP=C; EXP_AB_HLP_CTA=A; EXP_AB_PDP_IMAGE=DEFAULT; EXP_AB_CALLOUT_NUDGE=A; EXP_AB_TRUECALLER=DEFAULT; EXP_AB_GOOGLE_ONE_TAP=DEFAULT; EXP_AB_HLP_PAGE=A; EXP_ORGANIC_GUIDES=A; EXP_AB_NEW_PLP=A; EXP_AB_BREADCRUMB_POSITION=A; EXP_PRODUCT_CARD_CTA=A; EXP_AB_SIZE_MINI_PRODUCT=A; EXP_AB_TOP_NAV_CONFIG=CONTROL; EXP_AB_PRODUCT_HIGHLIGHTS=A; EXP_QUERY_PARAM_EXP_DWEB=CONTROL; EXP_AB_BEAUTY_PORTFOLIO=A; EXP_AB_HP_SEARCH_ANIMATION=CONTROL; EXP_AB_PDP_HAMBURGER=CONTROL; EXP_AB_HLP_OFFERS=DEFAULT; EXP_AB_WEB_AUTOREAD_OTP=DEFAULT; EXP_AD_BRV=random; EXP_PDP_RELEVANT_CATEGORY=CONTROL; EXP_AB_REMOVE_LOGIN_BOTTOMSHEET=DEFAULT; EXP_AB_ZENDESK_CHAT=A; EXP_AB_ACCOUNT_REVAMP=DEFAULT; EXP_AB_HORIZONTAL_WIDGET_TYPE=CONTROL; EXP_AB_IOC_CART_NUDGE=DEFAULT; EXP_APPSFLYER_DOWNLOAD_CTA=DEFAULT; EXP_AB_PDP_SIMILAR_PRODUCT_SHEET=DEFAULT; EXP_FULL_SCREEN_RECO_WIDGET=DEFAULT; EXP_AB_BEST_SELLER_PDP=CONTROL; EXP_AB_ENABLE_HLP_NEW_API=DEFAULT; EXP_SPECULATIVE_PRERENDERING=A; EXP_AB_TAGS_RATING_ON_LISTING=ONLY_TAGS; EXP_SEARCH_INP_ON_CART=CONTROL; EXP_AB_NEW_TAGS_ON_PDP=DEFAULT; EXP_REVIEW_SUBMIT=A; EXP_AB_GUIDES_V2=CONTROL; EXP_AB_OFFER_DELTA_COMMUNICATION=DEFAULT; EXP_AB_HLP_COUPON_OFFERS=A; EXP_AB_NEW_GC_PAGE=A; EXP_PLP_DNW_DWEB=A; EXP_UPDATED_AT=1745591203545; EXP_SSR_CACHE=5639a8a22b34af4817be8d00a18e0468; run=23; EXP_REVIEW_COLLECTION=1; D_LST=1; D_PDP=1; PHPSESSID=EEF02kw9axSt1f31745814411674; head_data_react={"id":"","nykaa_pro":false,"group_id":""}; pro=false; _gcl_gs=2.1.k1$i1745814396$u269731310; _gcl_au=1.1.1433646885.1745814401; utm_source=GooglePaid; utm_medium=search; utm_campaign=Search_Nykaa; _gcl_aw=GCL.1745814402.EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE; deduplication_cookie=GooglePaid; deduplication_cookie=GooglePaid; WZRK_G=4acc75a4be874dc2b698b5f1fde88289; _gid=GA1.2.1791180062.1745814402; _gac_UA-31866293-9=1.1745814402.EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE; _clck=1fhl761%7C2%7Cfvg%7C0%7C1944; _ttgclid=EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE; _ttgclid=EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE; _ttgclid=EAIaIQobChMI_dKKvfH5jAMV8fIWBR15yyTKEAAYASAAEgJOKvD_BwE; tt_deduplication_cookie=GooglePaid; tt_deduplication_cookie=GooglePaid; tt_deduplication_cookie=GooglePaid; countryCode=IN; storeId=nykaa; SITE_VISIT_COUNT=2; _ga_LKNEBVRZRG=GS1.1.1745818270.2.1.1745818274.56.0.0; WZRK_S_656-WZ5-7K5Z=%7B%22p%22%3A1%2C%22s%22%3A1745818291%2C%22t%22%3A1745818274%7D; _ga=GA1.2.756707784.1745814402; _gat_UA-31866293-9=1; _uetsid=fca325d023e811f0a3d5c733dcee03e5; _uetvid=fca3a29023e811f0b3ffbbddf2b059f7; cto_bundle=Pauek190ZndiQ1FhclVFWVNQRjFLNmtHUlRNTiUyQlFHZGZvRFdMN2xzeHdQSlRRNTdrV3FxRVA2Nm1lWm52elJFWkdWZ1hySDRKVkdkSiUyQks4T2hkQVBIbTBBUTlKSGdTTHFKUHlFYVJSdUpIUVdvYVJXQU5NQSUyRm52QiUyQlNlYjFMbVpKbnhMaTlOa25PVzBmTWJrcCUyRkpLT3E2SGF3JTNEJTNE; _clsk=gtx7zf%7C1745818275315%7C1%7C1%7Cu.clarity.ms%2Fcollect; _ga_JQ1CQHSXRX=GS1.2.1745818275.2.0.1745818275.60.0.0; pinCodeDel=380025',
}

df = pd.read_csv('Nykaa.csv')

for index, row in df.iterrows():
    print(f"Row {index}: {int(row['Nykaa Fashion'])}")  # Each row is a Series, can access with row['column_name']

    product_id = int(row['Nykaa Fashion'])

    print("Product Id:", product_id)

    params = {
        'productId': str(product_id),
        'pps': '1',
    }

    response = requests.get(
        f'https://www.nykaa.com/fabindia-brown-solid-wallet/p/{product_id}',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    print("Data fetching started")
    # create html file from page source

    with open(f"Product Pages/{product_id}.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    #
    print("HTML file created")
    script_content = response.text
    match = re.search(r'window\.__PRELOADED_STATE__ = ({.*?})</script>', script_content, re.DOTALL)

    if match:
        json_str = match.group(1)
        data = json.loads(json_str)
        # print(data)
        file_name = f"Product Json/{product_id}.json"

        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print("Json file created")

        if data.get("dataLayer", {}).get("product", {}).get("id"):

            product_info = {
                "Id": data.get("dataLayer", {}).get("product", {}).get("id"),
                # Example: Generate an ID or fetch from the data if applicable
                "product_id": data.get("dataLayer", {}).get("product", {}).get("id"),
                "catalog_name": data.get("dataLayer", {}).get("product", {}).get("name", "NA"),  # Example value
                "catalog_id": data.get("dataLayer", {}).get("product", {}).get("id"),  # Example value
                "source": "Nykaa",  # Example value
                "scraped_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Current timestamp
                "product_name": data.get("dataLayer", {}).get("product", {}).get("name", "NA"),
                "image_url": data.get("dataLayer", {}).get("product", {}).get("image", "NA"),
                "category_hierarchy": " > ".join([
                    data.get("dataLayer", {}).get("product", {}).get("categoryLevel", {}).get("l1", {}).get("name", "NA"),
                    data.get("dataLayer", {}).get("product", {}).get("categoryLevel", {}).get("l2", {}).get("name", "NA"),
                    data.get("dataLayer", {}).get("product", {}).get("categoryLevel", {}).get("l3", {}).get("name", "NA")
                ]),
                "product_price": data.get("dataLayer", {}).get("product", {}).get("offerPrice", "NA"),
                "arrival_date": "NA",  # Example value
                "shipping_charges": "NA",  # Example value
                "is_sold_out": not data.get("dataLayer", {}).get("product", {}).get("inStock"),  # Example value
                "discount": data.get("dataLayer", {}).get("product", {}).get("discount", "NA"),
                "mrp": data.get("dataLayer", {}).get("product", {}).get("mrp", "NA"),
                "page_url": "https://www.nykaa.com/" + data.get("dataLayer", {}).get("product", {}).get("slug", "NA"),
                "product_url": "https://www.nykaa.com/" + data.get("dataLayer", {}).get("product", {}).get("slug", "NA"),
                "number_of_ratings": data.get("dataLayer", {}).get("product", {}).get("ratingCount", "NA"),
                "avg_rating": data.get("dataLayer", {}).get("product", {}).get("rating", "NA"),
                "position": 1,  # Example value
                "country_code": "IN",  # Example value
                "images": [data.get("dataLayer", {}).get("product", {}).get("image", "NA")],
                "Best_offers": "No special offers",  # Example value
                "bank_offers": "No bank offers",  # Example value
                "product_details": data.get("productPage", {}).get("product", {}).get("description", "NA"),
                "specifications": data.get("dataLayer", {}).get("product", {}).get("specifications", "NA"),
                # Example value
                "rating": data.get("dataLayer", {}).get("product", {}).get("rating", "NA"),
                "MOQ": 1,  # Example value
                "brand": data.get("dataLayer", {}).get("product", {}).get("brandName", "NA"),
                "product_code": data.get("dataLayer", {}).get("product", {}).get("sku", "NA"),
                "Available_sizes": data.get("dataLayer", {}).get("product", {}).get("packSize", "NA"),  # Example value
                "sellerPartnerId": data.get("dataLayer", {}).get("product", {}).get("sku", "NA"),  # Example value
                "seller_return_policy": data.get("productPage", {}).get("product", {}).get("returnMessage", "NA"),
                "manufacturing_info_packerInfo": data.get("productPage", {}).get("product", {}).get("manufacturerName", "NA"),
                # Example value
                "manufacturing_info_seller_name": data.get("productPage", {}).get("product", {}).get("manufacturerName", "NA"),
                # Example value
                "manufacturing_info_importerInfo": data.get("productPage", {}).get("product", {}).get("manufacture", "NA"),
                # Example value
                "manufacturing_info_countryOfOrigin": data.get("productPage", {}).get("product", {}).get(
                    "originOfCountryName", "NA"),  # Example value
                "manufacturing_info_manufacturerInfo": data.get("productPage", {}).get("product", {}).get(
                    "manufacturerName", "NA"),
                "More_colours": data.get("productPage", {}).get("product", {}).get("variants", "NA"),  # Example value
                "variation_id": data.get("productPage", {}).get("product", {}).get("variants", "NA")  # Example value
            }

            csv_file = f"Product CSV/{product_id}.csv"
            csv_columns = product_info.keys()

            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerow(product_info)

            client = MongoClient('mongodb://localhost:27017/')
            db = client['nykaa']
            collection = db['products']
            collection.insert_one(product_info)

            print(f"{product_id} Data stored in CSV and MongoDB successfully.")
        else:
            continue
