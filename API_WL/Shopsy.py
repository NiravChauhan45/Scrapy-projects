import json
import random
from shopsy_parse import ShopsyParse
import re
import requests
from datetime import datetime
from dateutil import tz

is_proxy = False
year = datetime.today().year
india_tz = tz.gettz('Asia/Kolkata')


def get_login_headers():
    headers = {
        'Accept-Encoding': 'gzip',
        'business': 'reseller',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'ud=7.FKluYsbjMSc0eLZOxg8Qng4DT3Dv2G95vZpWuM8JrNmF8Uvf97wlFN1ZH9XdvpGBRT0o7wPtOVPqxFRmHDIhe2LXNImUKUUMSwRJ3ZcFSRkKwgQH6_DV9jgNhs9kOjS45QRHVI8Y_b1oiEYmxEe5aROGfIqoZvsVbYNHSJmblXA; Max-Age=15552000; Domain=flipkart.net; Path=/; Secure; HttpOnly; vd=VIB13ED88ADE8942F1BBA47FEDF18C3AA8-1750411062799-2.1750416874.1750414049.158521277; Max-Age=15552000; Domain=flipkart.net; Path=/; Secure; HttpOnly; vd=VIB13ED88ADE8942F1BBA47FEDF18C3AA8-1750411062799-2.1750417925.1750414049.158496701',
        'FK-TENANT-ID': 'SHOPSY',
        'Host': '2.rome.api.flipkart.net',
        'newrelic': 'eyJ2IjpbMCwyXSwiZCI6eyJ0eSI6Ik1vYmlsZSIsImFjIjoiMzcwMjExMyIsImFwIjoiMTU4ODc1MDUxMSIsInRyIjoiYzRmM2JmZjZlYzNiNGViYThlNWI3YjhjOWNlZTBmYjgiLCJpZCI6IjBkYjA4MjU5MGViYjRmYjMiLCJ0aSI6MTc1MDQzNjM3ODA5MywidGsiOiI2Mjk1Mjg2In19',
        'secureCookie': 'd1t12PxpOPys/ID8/Wj1VZC4lP0InoWDt5orl963dAh6ik9QXpmkO5QW2JJo6Ifhw/toFavhLwK/rX49zpAc3RaeXag==',
        'secureToken': 'YJ++NolIi8Ifbhk50wnw2kZCxGRIMTLkbo0ism/ElrHduqIpP3M6x/o3iqBxTFadcB8xLUiPY7dm4wPnOQXDNw==',
        'sn': 'VIB13ED88ADE8942F1BBA47FEDF18C3AA8.TOK2E64AF8077C34C8981392FD87F047839.1750416899828.LI',
        'traceparent': '00-c4f3bff6ec3b4eba8e5b7b8c9cee0fb8-0db082590ebb4fb3-00',
        'tracestate': '6295286@nr=0-2-3702113-1588750511-0db082590ebb4fb3----1750436378092',
        'User-Agent': 'okhttp/4.9.2',
        'X-Layout-Version': '{"appVersion":"910000","frameworkVersion":"1.0"}',
        'X-NewRelic-ID': 'VwEHU1dSCxABUVlaAAQHU1UA',
        'X-PARTNER-CONTEXT': '{"source":"reseller"}',
        'X-User-Agent': 'Mozilla/5.0 (Linux; Android 9; G011A Build/PI) FKUA/Retail/2291122/Android/Mobile (google/G011A/0e3a95b2ba020f9ee84d42fd12dd960c)',
        'X-Visit-Id': '0e3a95b2ba020f9ee84d42fd12dd960c-1750430530424'
    }
    return headers


def get_proxy():
    px = json.loads(open('decodo.json').read())

    return {"https": random.choice(px)}


def extract_product_id(url):
    if 'flipkart.com' in url:
        return None
    match = re.search(r'[?&]pid=([A-Za-z0-9]+)', url)
    if match:
        return match.group(1)
    return None


def get_main_page_response(product_id, islogin):
    json_data = {
        'pageUri': f'/p/p/i?pid={product_id}',
        'pageContext': None,
        'locationContext': None,
        'requestContext': None,
    }
    headers = {
        'Accept-Encoding': 'gzip',
        'at': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFkOTYzYzUwLTM0YjctNDA1OC1iMTNmLWY2NDhiODFjYTBkYSJ9.eyJleHAiOjE3NTQzMTg5NzAsImlhdCI6MTc1MjU5MDk3MCwiaXNzIjoia2V2bGFyIiwianRpIjoiMmM3OTg2OTgtNmViNC00MjNjLWIwNzUtYzU2MDgxNWM3ZTZmIiwidHlwZSI6IkFUIiwiZElkIjoiMDZlYzYyMTAyYWZiNTY4Njk3ZmRkMzhhOTFlYzI5ZGYiLCJrZXZJZCI6IlZJMUQwMTIxRjUxREM5NDdDNTlCQzNFODU4MzY5NkUwN0EiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjF9.cZXnfrpuRLxn_0ro_OSgEuPfrGWWX9CXr41yEcP2Hv8',
        'business': 'reseller',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'vd=VI1D0121F51DC947C59BC3E8583696E07A-1752590970512-1.1752590970.1752590970.152540982; Max-Age=15552000; Domain=flipkart.net; Path=/; Secure; HttpOnly; ud=6.vlZgohnaUd0_DVPJq-kjat9Tae0RmvWAv4OpTmbeV5lgOh5Me6046fUHF3opPXdbmVEaOJ5ZDTtR2X_hC7iIAedZ78ETK3srzKS6Gzaicc3gqc4JGE0OF42advKm7XELhTX-xXw8fbUoTN5gk7vZoP6YtPaAhlMd0-fAarMoMNi5RaDYh0Ft2b_Gf7pi_7k6svjHglqM2Pp3TsOV6G8StapNpxLwoON_Wha0hKH262csf317un_-zTu6Ztwq8msk1He3_L1M3obP18bLDbfqpo5OkE3iHvW5fMcy4uAIk-drWQ_WdTUR8iSEmPrcHiSV; Max-Age=15552000; Domain=flipkart.net; Path=/; Secure; HttpOnly; ud=2.8s0eIJmQcL-uW1PpPTSXClNm-06ppdKgjuIu1mTNFF9OJ72PSGWXt6GU4S17jfKP0KeoITVKEtZWSqzURS9Vq9MRGvhMk2yF_0gR5DMVvcA; vd=VI1D0121F51DC947C59BC3E8583696E07A-1752590970512-1.1752591069.1752590970.152524598',
        'FK-TENANT-ID': 'SHOPSY',
        'Host': '2.rome.api.flipkart.net',
        'newrelic': 'eyJ2IjpbMCwyXSwiZCI6eyJ0eSI6Ik1vYmlsZSIsImFjIjoiMzcwMjExMyIsImFwIjoiMTU4ODc1MDUxMSIsInRyIjoiOTQ0MWRmNDk3OThlNDI0ZTgxOTY4YmI4NTQ0NzM1Y2IiLCJpZCI6IjI5MTYyMDM4MjI0YzQ4NTYiLCJ0aSI6MTc1MjU5MTAwNjQ2OSwidGsiOiI2Mjk1Mjg2In19',
        'secureCookie': 'd1t17Pz9ePxJLTG1AYD9NP0w/HD2Jf1pX4OysyKeB5N7XG+MRa09ph2IAzUVHdsnUGxEBTSwZxoHQ0In54XhcOm+eYA==',
        'secureToken': 'bNXOELx/xNOAUHSf0Kt6EERFLC2pi+aCDGwT5+Fo4kQ5p+e3xWHtEMwwa6Arl8lIcqIKalvD8gklrbDXwqSviQ==',
        'sn': 'VI1D0121F51DC947C59BC3E8583696E07A.TOKD05CC0E706EE40DDB2D3FBB8F5215BAB.1752591007376.LO',
        'traceparent': '00-9441df49798e424e81968bb8544735cb-29162038224c4856-00',
        'tracestate': '6295286@nr=0-2-3702113-1588750511-29162038224c4856----1752591006469',
        'User-Agent': 'okhttp/4.9.2',
        'X-Layout-Version': '{"appVersion":"910000","frameworkVersion":"1.0"}',
        'X-NewRelic-ID': 'VwEHU1dSCxABUVlaAAQHU1UA',
        'X-PARTNER-CONTEXT': '{"source":"reseller"}',
        'X-User-Agent': 'Mozilla/5.0 (Linux; Android 9; SM-N976N Build/QP1A.190711.020) FKUA/Retail/2291123/Android/Mobile (samsung/SM-N976N/06ec62102afb568697fdd38a91ec29df)',
        'X-Visit-Id': '06ec62102afb568697fdd38a91ec29df-1752518488771'
    }
    while True:
        response = None
        try:
            response = requests.post(
                url='https://2.rome.api.flipkart.net/4/page/fetch' if not int(
                    islogin) else 'https://2.rome.api.flipkart.net/4/page/fetch',
                headers=headers if not int(islogin) else get_login_headers(),
                data=json.dumps(json_data),
                proxies=get_proxy(), verify=False
            )
        except:
            pass
        print(response.status_code)
        if response.status_code in [404, 500]:
            return None
        if response and response.status_code == 200:
            break
    return response


def get_product_details_response(product_id):
    product_detail_url = f'https://www.shopsy.in/api/3/page/dynamic/product-details'
    payload = {'requestContext': {'productId': product_id, }, 'locationContext': {}, }
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-PARTNER-CONTEXT': '{"source":"reseller"}',
        'X-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 FKUA/msite/0.0.3/msite/Mobile',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    while True:
        response = None
        try:
            response = requests.post(
                url=product_detail_url,
                headers=headers,
                data=json.dumps(payload),
                proxies=get_proxy(), verify=False
            )
        except:
            pass
        if response and response.status_code == 200:
            break
    return response


def get_seller_response(product_id):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'X-PARTNER-CONTEXT': '{"source":"reseller"}',
        'X-user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 FKUA/msite/0.0.3/msite/Mobile',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    payload = {"requestContext": {"productId": product_id},
               "locationContext": {"pincode": '560001'}}
    while True:
        response = None
        try:
            response = requests.post(
                url='https://www.shopsy.in/api/3/page/dynamic/product-sellers',
                headers=headers,
                data=json.dumps(payload),
                proxies=get_proxy(), verify=False
            )
        except:
            pass
        if response and response.status_code == 200:
            break
    return response


def get_seller_response_2(product_id):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'T=cm05b24rp0j2u071331spisx3-BR1724332516261; _pxvid=936df67d-6088-11ef-a16c-426b3d7455d8; _ga=GA1.1.481542401.1724332520; _ga_MF2PJ1ME3R=deleted; _ga_MF2PJ1ME3R=GS1.1.1728617488.12.1.1728618503.58.0.0; DC_ID=2; ULSN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjb29raWUiLCJhdWQiOiJmbGlwa2FydCIsImlzcyI6ImF1dGguZmxpcGthcnQuY29tIiwiY2xhaW1zIjp7ImdlbiI6IjEiLCJ1bmlxdWVJZCI6IlVVSTI1MDEwNzE2MzMwODc1MzdFMVZNVU8iLCJma0RldiI6bnVsbH0sImV4cCI6MTc1MjAyNzc4OCwiaWF0IjoxNzM2MjQ3Nzg4LCJqdGkiOiJjMTRhODcwOC04ODA3LTQ3NDctYmMyNi1hNDdiOTA5OTcyZDMifQ.iK7_6uDTPMsLi-AuQTmKEVGVuHI5Va5ZYrvUgOJF_es; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20130%7CMCMID%7C26861789947323726860757072224267507474%7CMCAAMLH-1739284100%7C12%7CMCAAMB-1739775278%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1739177678s%7CNONE%7CMCAID%7CNONE; vw=302; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNhNzdlZTgxLTRjNWYtNGU5Ni04ZmRlLWM3YWMyYjVlOTA1NSJ9.eyJleHAiOjE3MzkyNTgzNDEsImlhdCI6MTczOTI1NjU0MSwiaXNzIjoia2V2bGFyIiwianRpIjoiNDBkMTlmYWUtNGZkYi00NTBkLTkyNTktM2RhZDBjMWFlMzYxIiwidHlwZSI6IkFUIiwiZElkIjoiY20wNWIyNHJwMGoydTA3MTMzMXNwaXN4My1CUjE3MjQzMzI1MTYyNjEiLCJiSWQiOiJNTlFaS0YiLCJrZXZJZCI6IlZJNTVCQzlENjA1MEZBNDY3RDgzMURBRDI0QThCNTE1NzkiLCJ0SWQiOiJtYXBpIiwiZWFJZCI6Im9ubFpGd1ZBWm1qSTJlUDN6dlcyVHRnLTJnLW9LWUxYbkxNdFZFRDZSUDktLXVjM1VteWQ5Zz09IiwidnMiOiJMSSIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjN9.fgAmu6g7KnnpLQKDJJ4_mVW73gOPgWGQy2gz7z5-l2Q; rt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhlM2ZhMGE3LTJmZDMtNGNiMi05MWRjLTZlNTMxOGU1YTkxZiJ9.eyJleHAiOjE3NTQ4OTQ5NDEsImlhdCI6MTczOTI1NjU0MSwiaXNzIjoia2V2bGFyIiwianRpIjoiNjVlM2M3YWEtMjg5Mi00NGEwLWIxZjItNjBiYmYxYTc5NzBlIiwidHlwZSI6IlJUIiwiZElkIjoiY20wNWIyNHJwMGoydTA3MTMzMXNwaXN4My1CUjE3MjQzMzI1MTYyNjEiLCJiSWQiOiJNTlFaS0YiLCJrZXZJZCI6IlZJNTVCQzlENjA1MEZBNDY3RDgzMURBRDI0QThCNTE1NzkiLCJ0SWQiOiJtYXBpIiwibSI6eyJ0eXBlIjoibiJ9LCJ2IjoiR1lVRVVPIn0.9DA9iPrUeLpoG_Ohyn6Aag9M2KhA3etSzvangcTc9GM; K-ACTION=null; s_sq=flipkartresellerprod%3D%2526pid%253DPagetype%25253A%252520ProductSeller%2526pidt%253D1%2526oid%253Dfunctiongr%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DDIV; gpv_pn=ProductViewPage%3AWomenWesternCore; gpv_pn_t=Product; ud=3.1YH-VQLXEJIPFTR2NXRbtrFBI1Ikpem14K1KL6owcdvxPdWNn6RKXtFugTRA_g_V0ckhvPtiWChcHCLMgblDq_MzmBmqNrGh_pGL_K1HxGjC34R1yX-kHrvgAlyqRhH8CmG8u6ZcPSB0rviuH6ycwlVXGY98mZChMLmLrTINYuM3A5w55krVTcxxtg8SiwQuHvMK_0LuO3ac1qUnfUKf7hkKED4asLWMpxcws7_785dQqKvkxHX4ZMd5Dgiintgqp4UEG7Rg952fWfEyzPjcGYS5m19Dwyir1G0iUYDDB755HenZvII9fmxlalvVd-cSa4PvLTI0XH9kbSY2gK_Wc_p_VO0wwKD2lp_4HQSUyq-LnJTTdnoqpn1DRpmMe_HD; _ga_MF2PJ1ME3R=GS1.1.1739254608.66.1.1739256676.8.0.0; vd=VI55BC9D6050FA467D831DAD24A8B51579-1736227742716-9.1739256720.1739254557.153839416; S=d1t10Pzc/VD8/Pz8/IG8/Pz9/YTTusEiD62EeV6fS1RNH9iMNCS0g4SbpnDTGnQqo4aCHn+SaywCJub0Kb3sjthRJGg==; SN=VI55BC9D6050FA467D831DAD24A8B51579.TOK43335B440C4E46C3BA6C1451206EA2EB.1739256720698.LI',
        'Origin': 'https://www.shopsy.in',
        'Referer': 'https://www.shopsy.in/oomph-casual-self-design-women-light-blue-top/p/itm4a6c194dcbefe?pid=TOPGRZMRR8YBCY5C',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
        'X-PARTNER-CONTEXT': '{"source":"reseller"}',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'x-user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 FKUA/msite/0.0.4/msite/Mobile',
    }

    params = {
        'cacheFirst': 'false',
    }

    json_data = {
        'pageUri': f'/sellers?pid={product_id}',
        'pageContext': {
            'fetchSeoData': True,
            'pageNumber': 1,
        },
        'trackingContext': {},
        'locationContext': {
            'pincode': '560001',
        },
    }

    while True:
        response = None
        try:
            response = requests.post(
                'https://www.shopsy.in/2.rome/api/4/page/fetch',
                params=params,
                headers=headers,
                json=json_data,
                proxies=get_proxy(),
                verify=False
            )
        except:
            pass
        if response and response.status_code == 200:
            break
    return response


def parse_main_page_response(product_id, response, islogin):
    item = dict()
    if int(islogin) == 1:
        status = 'login'
    else:
        status = 'logout'
    dataParser = ShopsyParse(response)
    product_name = dataParser.get_product_name()
    brand = dataParser.get_brand()
    image_url = dataParser.get_image_url()

    category_hierarchy = dataParser.get_category_hierarchy()
    if not category_hierarchy:
        category_hierarchy = dataParser.get_category_hierarchy_2()
    if not category_hierarchy:
        category_hierarchy = dataParser.get_category_hierarchy_3()
    if not category_hierarchy:
        category_hierarchy = 'N/A'

    product_url = dataParser.get_product_url()
    page_url = dataParser.get_page_url()

    product_price = dataParser.get_final_price()
    if not product_price:
        product_price = dataParser.get_final_price_SPECIAL_PRICE()
        if product_price:
            product_price = str(product_price)
    if not product_price:
        product_price = dataParser.get_final_price_FPS()
        if product_price:
            product_price = str(product_price)

    mrp = dataParser.get_mrp()
    if not mrp:
        mrp = dataParser.get_mrp_2()

    avg_rating = dataParser.get_avg_rating()
    if not avg_rating:
        avg_rating = dataParser.get_avg_rating_PRODUCT_PAGE_SUMMARY_V2()
    if not avg_rating:
        avg_rating = dataParser.get_avg_rating_2()
    if not avg_rating:
        avg_rating = dataParser.get_avg_rating_3()
    if not avg_rating:
        avg_rating = dataParser.get_avg_rating_4()
    if not avg_rating:
        avg_rating = dataParser.get_avg_rating_5()

    number_of_ratings = dataParser.get_number_of_ratings()
    if not number_of_ratings:
        number_of_ratings = dataParser.get_number_of_ratings_PRODUCT_PAGE_SUMMARY_V2()
    if not number_of_ratings:
        number_of_ratings = dataParser.get_number_of_ratings_2()
    if not number_of_ratings:
        number_of_ratings = dataParser.get_number_of_ratings_3()
    if not number_of_ratings:
        number_of_ratings = dataParser.get_number_of_ratings_4()
    if not number_of_ratings:
        number_of_ratings = dataParser.get_number_of_ratings_5()

    shipping_charges = dataParser.get_shipping_price()
    sold_out = dataParser.get_availablility()
    if sold_out == "true":
        sold_out = dataParser.get_availablility_2()
    if sold_out == "true":
        sold_out = dataParser.get_availablility_3()
    if sold_out == "false":
        arrival_date = str(dataParser.get_arrival_date())
    else:
        arrival_date = 'N/A'

    try:
        if mrp and product_price:
            discount_amount = float(mrp) - float(product_price)
            discount = int((discount_amount * 100) / int(mrp))
        else:
            discount = 'N/A'
    except:
        discount = dataParser.get_discount()

    other_data = dict()
    other_data['MOQ'] = dataParser.get_moq()
    if dataParser.get_brand():
        other_data['brand'] = dataParser.get_brand()

    if dataParser.get_itemid():
        other_data['item_id'] = dataParser.get_itemid()

    if dataParser.get_listing_id():
        other_data['listing_id'] = dataParser.get_listing_id()

    if dataParser.get_variations_list():
        other_data['variation_id'] = dataParser.get_variations_list()

    if dataParser.get_all_images():
        other_data['Images'] = dataParser.get_all_images()

    if dataParser.get_seller_return_policy():
        other_data['seller_return_policy'] = dataParser.get_seller_return_policy()
    elif dataParser.get_seller_return_policy_2():
        other_data['seller_return_policy'] = dataParser.get_seller_return_policy_2()

    if dataParser.get_coupons():
        other_data['coupon'] = dataParser.get_coupons()

    if dataParser.get_offers():
        other_data['offers'] = dataParser.get_offers()

    if dataParser.get_product_highlights():
        other_data['Product_highlights'] = dataParser.get_product_highlights()

    if dataParser.get_Highlights():
        other_data['Highlights'] = dataParser.get_Highlights()

    if dataParser.get_product_highlights_text():
        other_data['Product_highlights_text'] = dataParser.get_product_highlights_text()

    if dataParser.get_Cash_on_Delivery():
        other_data['cash_on_delivery'] = dataParser.get_Cash_on_Delivery()
    elif dataParser.get_Cash_on_Delivery_2():
        other_data['cash_on_delivery'] = dataParser.get_Cash_on_Delivery_2()

    if dataParser.get_replacement_policy():
        other_data['seller_replacement_policy'] = dataParser.get_replacement_policy()
    elif dataParser.get_replacement_policy_2():
        other_data['seller_replacement_policy'] = dataParser.get_replacement_policy_2()

    if dataParser.get_parameterRating():
        other_data['parameterized_rating'] = dataParser.get_parameterRating()
    elif dataParser.get_parameterRating_1():
        other_data['parameterized_rating'] = dataParser.get_parameterRating_1()
    try:
        if other_data['parameterized_rating']:
            filtered_data = [parameterized_loop for parameterized_loop in other_data.get('parameterized_rating') if
                             parameterized_loop.get("parameter") != "Seller rating"]
            if filtered_data:
                other_data['parameterized_rating'] = filtered_data
            else:
                other_data.pop('parameterized_rating')
    except:
        pass

    if dataParser.get_Cancellation_policy():
        other_data['seller_Cancellation_policy'] = dataParser.get_Cancellation_policy()
    seller_count = dataParser.get_seller_count()
    item['seller_count'] = seller_count
    item['main_seller_data'] = dataParser.get_main_seller()
    try:
        try:
            Moq_number = other_data['MOQ']
        except:
            Moq_number = 1
        try:
            main_seller_dict = dataParser.get_one_seller(Moq_number, product_price)
        except:
            main_seller_dict = {}
    except:
        main_seller_dict = {}
    item['main_seller_dict'] = main_seller_dict
    item['source'] = 'shopsy'
    item['country_code'] = 'IN'
    try:
        if seller_count:
            if int(seller_count) == 1:
                try:
                    Moq_number = other_data['MOQ']
                except:
                    Moq_number = 1
                other_data['Seller_List'] = dataParser.get_one_seller(Moq_number, product_price)

        else:
            seller_count = 1
            Moq_number = 1
            if dataParser.get_one_seller_data(Moq_number, product_price):
                try:
                    Moq_number = other_data['MOQ']
                except:
                    pass
                other_data['Seller_List'] = dataParser.get_one_seller_data(Moq_number, str(product_price))
            # if dataParser.get_one_seller_data():
            #     other_data['Seller_List'] = dataParser.get_one_seller_data()
    except:
        pass

    if dataParser.get_individual_ratings():
        other_data['individualRatingsCount'] = dataParser.get_individual_ratings()
    elif dataParser.get_individual_ratings_SHOPSY_PRODUCT_PAGE_SUMMARY():
        other_data['individualRatingsCount'] = dataParser.get_individual_ratings_SHOPSY_PRODUCT_PAGE_SUMMARY()
    elif dataParser.get_individual_ratings_1():
        other_data['individualRatingsCount'] = dataParser.get_individual_ratings_1()
    elif dataParser.get_individual_ratings_2():
        other_data['individualRatingsCount'] = dataParser.get_individual_ratings_2()
    elif dataParser.get_individual_ratings_3():
        other_data['individualRatingsCount'] = dataParser.get_individual_ratings_3()

    if dataParser.get_isbn():
        other_data['ISBN'] = dataParser.get_isbn()
    if mrp:
        get_Maximum_Retail_Price = dataParser.get_Maximum_Retail_Price()
        if get_Maximum_Retail_Price:
            try:
                other_data['Maximum Retail Price'] = int(float(dataParser.get_Maximum_Retail_Price()))
            except:
                other_data['Maximum Retail Price'] = dataParser.get_Maximum_Retail_Price()
        else:
            try:
                other_data['Maximum Retail Price'] = int(float(mrp))
            except:
                other_data['Maximum Retail Price'] = mrp
    if product_price:
        get_Selling_Price = dataParser.get_Selling_Price()
        if get_Selling_Price:
            try:
                other_data['Selling Price'] = int(float(dataParser.get_Selling_Price()))
            except:
                other_data['Selling Price'] = dataParser.get_Selling_Price()
        elif not get_Selling_Price:
            get_Selling_Price = dataParser.get_final_price_FPS()
            if get_Selling_Price:
                try:
                    other_data['Selling Price'] = int(float(get_Selling_Price))
                except:
                    other_data['Selling Price'] = get_Selling_Price

    SPECIAL_PRICE = dataParser.get_Special_price()

    if not SPECIAL_PRICE:
        SPECIAL_PRICE = dataParser.get_final_price_SPECIAL_PRICE()

    if SPECIAL_PRICE:
        try:
            other_data['Special Price'] = int(float(SPECIAL_PRICE))
        except:
            other_data['Special Price'] = SPECIAL_PRICE
    if dataParser.get_product_details_from_pdp():
        other_data['product_detail'] = dataParser.get_product_details_from_pdp()

    if dataParser.get_coupon_off():
        other_data[f'coupon_status_{status}'] = True
        other_data[f'coupon_description_{status}'] = dataParser.get_coupon_off()
    elif dataParser.get_coupon_off_2():
        other_data[f'coupon_status_{status}'] = True
        other_data[f'coupon_description_{status}'] = dataParser.get_coupon_off_2()
    else:
        other_data[f'coupon_status_{status}'] = False
    ordered_tag = dataParser.get_ordered_tag()
    if ordered_tag:
        other_data['ordered_tag'] = ordered_tag
    product_Tag = dataParser.get_product_Tag()
    print(product_Tag)
    if product_Tag:
        other_data[product_Tag] = True

    item['position'] = 'N/A'
    item['product_id'] = product_id
    item['catalog_id'] = product_id
    item['product_name'] = product_name.replace(' ()', '').strip()
    item['catalog_name'] = product_name.replace(' ()', '').strip()
    item['image_url'] = image_url
    if category_hierarchy:
        item['category_hierarchy'] = category_hierarchy
    try:
        item['product_price'] = int(float(product_price)) if product_price else 'N/A'
    except:
        item['product_price'] = str(product_price)
    item['arrival_date'] = str(arrival_date)
    try:
        item['shipping_charges'] = int(float(shipping_charges))
    except:
        item['shipping_charges'] = str(shipping_charges)
    item['is_sold_out'] = sold_out
    try:
        item['discount'] = int(float(discount)) if discount else 'N/A'
    except:
        item['discount'] = str(discount)
    try:
        item['mrp'] = int(float(mrp)) if mrp else 'N/A'
    except:
        item['mrp'] = str(mrp)
    item['page_url'] = page_url
    item['product_url'] = product_url.replace('flipkart.com', 'shopsy.in')
    try:
        item['number_of_ratings'] = int(float(number_of_ratings))
    except:
        item['number_of_ratings'] = "N/A"
    try:
        item['avg_rating'] = float(avg_rating)
    except:
        item['avg_rating'] = "N/A"
    item['others'] = other_data
    item['scraped_date'] = (datetime.now(tz=india_tz)).strftime("%Y-%m-%d %H:%M:%S")

    return item


def parse_product_detail_response(response, other_data):
    dataParser = ShopsyParse(response)
    if 'ISBN' not in other_data:
        if dataParser.get_isbn():
            other_data['ISBN'] = dataParser.get_isbn()
    if dataParser.get_key_features():
        other_data['keyFeatures'] = dataParser.get_key_features()
    if dataParser.get_product_description():
        other_data['description'] = dataParser.get_product_description()
    if dataParser.get_detail_component():
        other_data['detailedComponents'] = dataParser.get_detail_component()
    if dataParser.get_specification():
        other_data['product_specification'] = dataParser.get_specification()
    if 'MOQ' not in other_data:
        other_data['MOQ'] = 1
    return other_data


def parse_seller_data(response, product_price, other_data, main_seller_data, main_seller_dict):
    dataParser = ShopsyParse(response)
    # other_data['Seller_List'] = dataParser.get_seller_list(main_seller_data)
    other_data['Seller_List'] = dataParser.get_seller_list(main_seller_data, main_seller_dict, product_price)
    return other_data


def main(input_value, islogin):
    # try:
    if input_value.startswith("http"):
        product_id = extract_product_id(input_value)
    else:
        product_id = input_value
    if product_id is None:
        return {"Error": "Invalid URL."}
    islogin = int(islogin)
    main_page_response = get_main_page_response(product_id, islogin)
    if main_page_response.status_code == 404:
        return {"Error": "404 - Page Not Found."}
    item = parse_main_page_response(product_id, main_page_response, islogin)
    main_seller_dict = item.pop('main_seller_dict')
    product_price = item.get('product_price')
    product_details_response = get_product_details_response(product_id)
    other_data = item.pop('others')
    other_data = parse_product_detail_response(product_details_response, other_data)
    seller_count = item.pop('seller_count')
    main_seller_data = item.pop('main_seller_data')
    if seller_count:
        if seller_count > 1:
            seller_response = get_seller_response(product_id)
            other_data = parse_seller_data(seller_response, product_price, other_data, main_seller_data,
                                           main_seller_dict)
            # other_data['Seller_List'] = dataParser.get_seller_list(main_seller_data, main_seller_dict, product_price)

    other_data['data_vendor'] = 'Actowiz'
    item['others'] = other_data

    return item


if __name__ == '__main__':
    # url = 'https://www.shopsy.in/ayur-herbals-skin-toner-enrished-rose-aloe-mint-glowing-men-women/p/itm1143af799023d?pid=XSQGZV74Z7FEQNWY'
    product_id = 'EOEGA9XZHAJ4XCFW'
    islogin = 0
    item = main(product_id, islogin)
    print(json.dumps(item, ensure_ascii=False))
    # main(product_id)
