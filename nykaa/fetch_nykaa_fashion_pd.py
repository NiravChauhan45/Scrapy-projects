import requests
import pandas as pd
import traceback
import csv
import re
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed

df = pd.read_excel('client_inputs/Nykaa.xlsx', sheet_name='Nykaa', engine='openpyxl')
now = datetime.now()
collection_name = f"products_details_{now.strftime('%d_%m_%Y_%H_%M')}"
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['nykaa']
collection = db[collection_name]

cookies = {
    'bcookie': '435726bd-c2e1-4ef5-a0d3-9a91ed2b8c75',
    'EXP_new-relic-client': 'variant1',
    'EXP_UPDATED_AT': '1745214663407',
    'EXP_SSR_CACHE': '52ba23c55fac75d79f01d839bfc9a25e',
    'tm_stmp': '1745823335847',
    'rum_abMwebSort': '48',
    'PHPSESSID': '958f74f251c74f278af9002d0d766822',
    'EXP_prod': 'prod-a',
    'EXP_size-inventory-nudge-ab': 'size-inventory-nudge-a',
    'EXP_checkout-ssr-mweb': 'variant-pci',
    'EXP_checkout-ssr-dweb': 'variant-pci',
    'EXP_login-nudge-plp': 'Variant1',
    'EXP_speculation-rule-cart-ab': 'speculation-rule-cart-a',
    '_gcl_gs': '2.1.k1$i1745823334$u8179629',
    '_gcl_au': '1.1.1591618574.1745823337',
    'NYK_VISIT': '435726bd-c2e1-4ef5-a0d3-9a91ed2b8c75~1745823336786',
    'EXP_postorder_variant_ab': 'postorder_default_A',
    'EXP_gamification-nudge': 'gamification-nudge-a',
    '_ga': 'GA1.1.54183066.1745823337',
    'WZRK_G': 'ddfedeedabdc446cadf9d596ae062ab9',
    '_clck': '1wx5esj%7C2%7Cfvg%7C0%7C1944',
    '_gcl_aw': 'GCL.1745823347.EAIaIQobChMIlcip5JL6jAMVYGQPAh2iBSwSEAAYASAAEgKMt_D_BwE',
    'NF_LN': 'true',
    'mp_0cd3b66d1a18575ebe299806e286685f_mixpanel': '%7B%22distinct_id%22%3A%22%24device%3Ae6ff34aa-e2d9-4bd1-a04b-c83e5e848268%22%2C%22%24device_id%22%3A%22e6ff34aa-e2d9-4bd1-a04b-c83e5e848268%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2F%3Fptype%3Dhomepage%26utm_content%3Dads%26utm_source%3DGooglePaid%26utm_medium%3DSearch%26utm_campaign%3DSearch_NykaaFashion%26utm_term%3DBrand_Core%26gad_source%3D1%26gbraid%3D0AAAAAC968R0mi1qWYYL1h_HGeSM3kXvZg%26gclid%3DEAIaIQobChMIlcip5JL6jAMVYGQPAh2iBSwSEAAYASAAEgKMt_D_BwE%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2F%3Fptype%3Dhomepage%26utm_content%3Dads%26utm_source%3DGooglePaid%26utm_medium%3DSearch%26utm_campaign%3DSearch_NykaaFashion%26utm_term%3DBrand_Core%26gad_source%3D1%26gbraid%3D0AAAAAC968R0mi1qWYYL1h_HGeSM3kXvZg%26gclid%3DEAIaIQobChMIlcip5JL6jAMVYGQPAh2iBSwSEAAYASAAEgKMt_D_BwE%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22entry_page_product_id%22%3A%2218176745%22%7D',
    'bm_sz': '405DC64DABA000BC8279F5483B4149B9~YAAQrfXSF4nCU0qWAQAA+EJNexvfuWMkZDstkzs8c76j0IAmmRuCJr60EvHxEA9O8/hgxVtQQ8Jm9dWSshGK1AesFoUmIQ3nUv1gv+Z6jk+wCdFx+MujkKD1N5/mOVIWWcmSjm0NHfYxLz8GvjnaAzZKWEAMmmPKdNehj6MoL7+328pJmEbLPAq6we6uXD/eC7ckWoBr17KuB1Ab/UwQFutyB7ZKCc3oWKmavqwYbtTIh/UvTS7/Qw4bHk9IKNVQKu/l4qPSYYwBJhXuYo7rC/FUx9ITvI/cN4ppqdmw6h76WVBBJyqRIUTwESCi3rMiNWP+kDdTpUBwMJLzkpeTB2FKHw/Jahnd+gfiDr9uabMC0B8JHrDVmaSR6Dj9Ff7fkZCMZZHHlwQ8Zuq6Xp7eFFvkg56whVMfL9xsb07y0Gw6b7kfnJ+S8kmAKSd5a1utV39WRdjClz41YBKyTcxgcGf0fq5P9UwdeuGAb1B8jUksz7tm553uU0a70DsUaadYG2W2VrJb6Nx5a1hKnD/1i2N++jPa+yt7S/hmkzOt1sYrRImAgJEQjKBtFgYr~3159606~4536371',
    '_abck': '423BCA2EB3CC09A1B8741B7AB8B5F07C~0~YAAQrfXSF5fCU0qWAQAAkUNNew21LNNidc+DU6dPrzJDCLn3slIEPolYHmBdAkzH4JGgfnofgYF0Jy4sp+STekc1uO7/Ku9GiW6FyGB80kCgULevJJeQ58/8/qo9qLju3V7gqTQjekIDHsdWxt1qZEiCfezb/Lm9YfR3yf35tk81zyvqpoxtV2HzD0u+XdgY9I3Nj+m+KGl6zFU/yRSZ8Y6xnHakl9VGUsmwW9bxmP5M4oD81WXl6ZLPNHfO6DubdJjt2L5/Eq0XLToxJ1mHPBXQFVYKNIPdyq5kkaOUTs4O51hXGS7lSruRnFKxdSnBSo6Ofs02LEGanSF7g00tL47Ap73jZhJnS219Ew4gwpVnJmiTMsU5Xj80XqAefQa+MF9spZ/rBdRCeqhWE/xD46iY3RjcLxF24NYMMstBb2JaUMoRZW3gwxpTreZyr8m0C+0AV8RkBLrC9bSbPA+c1v/NXRBjUuTxhL7j/mpjkShyGlDTBgryZ9r7UuG3Cc0TJ7AkQjmJHyQC8IRQxf8FHvoV6afN/Iz58nLhlCAP20HDR2hrdehPO5yXQqNPaS2OvO1X4N4zQA2IQ/OWHE/3oRu7YC9TUj35U8AasEu2ZusUANlSN0G1cwGlpxiGR0vfKuL6ThaT/LSerguXPG/nqVmxdDL2KNqjbisKLCmnJEFb9A==~-1~-1~1745826953',
    '_ga_DZ4MXZBLKH': 'GS1.1.1745823337.1.1.1745825367.59.0.0',
    '_clsk': '1o1nffb%7C1745825367556%7C18%7C0%7Cu.clarity.ms%2Fcollect',
    'NYK_PCOUNTER': '25',
    'NYK_ECOUNTER': '162',
    'WZRK_S_WRK-4W9-R55Z': '%7B%22p%22%3A17%2C%22s%22%3A1745823353%2C%22t%22%3A1745825386%7D',
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
    # 'cookie': 'bcookie=435726bd-c2e1-4ef5-a0d3-9a91ed2b8c75; EXP_new-relic-client=variant1; EXP_UPDATED_AT=1745214663407; EXP_SSR_CACHE=52ba23c55fac75d79f01d839bfc9a25e; tm_stmp=1745823335847; rum_abMwebSort=48; PHPSESSID=958f74f251c74f278af9002d0d766822; EXP_prod=prod-a; EXP_size-inventory-nudge-ab=size-inventory-nudge-a; EXP_checkout-ssr-mweb=variant-pci; EXP_checkout-ssr-dweb=variant-pci; EXP_login-nudge-plp=Variant1; EXP_speculation-rule-cart-ab=speculation-rule-cart-a; _gcl_gs=2.1.k1$i1745823334$u8179629; _gcl_au=1.1.1591618574.1745823337; NYK_VISIT=435726bd-c2e1-4ef5-a0d3-9a91ed2b8c75~1745823336786; EXP_postorder_variant_ab=postorder_default_A; EXP_gamification-nudge=gamification-nudge-a; _ga=GA1.1.54183066.1745823337; WZRK_G=ddfedeedabdc446cadf9d596ae062ab9; _clck=1wx5esj%7C2%7Cfvg%7C0%7C1944; _gcl_aw=GCL.1745823347.EAIaIQobChMIlcip5JL6jAMVYGQPAh2iBSwSEAAYASAAEgKMt_D_BwE; NF_LN=true; mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%22%24device%3Ae6ff34aa-e2d9-4bd1-a04b-c83e5e848268%22%2C%22%24device_id%22%3A%22e6ff34aa-e2d9-4bd1-a04b-c83e5e848268%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2F%3Fptype%3Dhomepage%26utm_content%3Dads%26utm_source%3DGooglePaid%26utm_medium%3DSearch%26utm_campaign%3DSearch_NykaaFashion%26utm_term%3DBrand_Core%26gad_source%3D1%26gbraid%3D0AAAAAC968R0mi1qWYYL1h_HGeSM3kXvZg%26gclid%3DEAIaIQobChMIlcip5JL6jAMVYGQPAh2iBSwSEAAYASAAEgKMt_D_BwE%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2F%3Fptype%3Dhomepage%26utm_content%3Dads%26utm_source%3DGooglePaid%26utm_medium%3DSearch%26utm_campaign%3DSearch_NykaaFashion%26utm_term%3DBrand_Core%26gad_source%3D1%26gbraid%3D0AAAAAC968R0mi1qWYYL1h_HGeSM3kXvZg%26gclid%3DEAIaIQobChMIlcip5JL6jAMVYGQPAh2iBSwSEAAYASAAEgKMt_D_BwE%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22entry_page_product_id%22%3A%2218176745%22%7D; bm_sz=405DC64DABA000BC8279F5483B4149B9~YAAQrfXSF4nCU0qWAQAA+EJNexvfuWMkZDstkzs8c76j0IAmmRuCJr60EvHxEA9O8/hgxVtQQ8Jm9dWSshGK1AesFoUmIQ3nUv1gv+Z6jk+wCdFx+MujkKD1N5/mOVIWWcmSjm0NHfYxLz8GvjnaAzZKWEAMmmPKdNehj6MoL7+328pJmEbLPAq6we6uXD/eC7ckWoBr17KuB1Ab/UwQFutyB7ZKCc3oWKmavqwYbtTIh/UvTS7/Qw4bHk9IKNVQKu/l4qPSYYwBJhXuYo7rC/FUx9ITvI/cN4ppqdmw6h76WVBBJyqRIUTwESCi3rMiNWP+kDdTpUBwMJLzkpeTB2FKHw/Jahnd+gfiDr9uabMC0B8JHrDVmaSR6Dj9Ff7fkZCMZZHHlwQ8Zuq6Xp7eFFvkg56whVMfL9xsb07y0Gw6b7kfnJ+S8kmAKSd5a1utV39WRdjClz41YBKyTcxgcGf0fq5P9UwdeuGAb1B8jUksz7tm553uU0a70DsUaadYG2W2VrJb6Nx5a1hKnD/1i2N++jPa+yt7S/hmkzOt1sYrRImAgJEQjKBtFgYr~3159606~4536371; _abck=423BCA2EB3CC09A1B8741B7AB8B5F07C~0~YAAQrfXSF5fCU0qWAQAAkUNNew21LNNidc+DU6dPrzJDCLn3slIEPolYHmBdAkzH4JGgfnofgYF0Jy4sp+STekc1uO7/Ku9GiW6FyGB80kCgULevJJeQ58/8/qo9qLju3V7gqTQjekIDHsdWxt1qZEiCfezb/Lm9YfR3yf35tk81zyvqpoxtV2HzD0u+XdgY9I3Nj+m+KGl6zFU/yRSZ8Y6xnHakl9VGUsmwW9bxmP5M4oD81WXl6ZLPNHfO6DubdJjt2L5/Eq0XLToxJ1mHPBXQFVYKNIPdyq5kkaOUTs4O51hXGS7lSruRnFKxdSnBSo6Ofs02LEGanSF7g00tL47Ap73jZhJnS219Ew4gwpVnJmiTMsU5Xj80XqAefQa+MF9spZ/rBdRCeqhWE/xD46iY3RjcLxF24NYMMstBb2JaUMoRZW3gwxpTreZyr8m0C+0AV8RkBLrC9bSbPA+c1v/NXRBjUuTxhL7j/mpjkShyGlDTBgryZ9r7UuG3Cc0TJ7AkQjmJHyQC8IRQxf8FHvoV6afN/Iz58nLhlCAP20HDR2hrdehPO5yXQqNPaS2OvO1X4N4zQA2IQ/OWHE/3oRu7YC9TUj35U8AasEu2ZusUANlSN0G1cwGlpxiGR0vfKuL6ThaT/LSerguXPG/nqVmxdDL2KNqjbisKLCmnJEFb9A==~-1~-1~1745826953; _ga_DZ4MXZBLKH=GS1.1.1745823337.1.1.1745825367.59.0.0; _clsk=1o1nffb%7C1745825367556%7C18%7C0%7Cu.clarity.ms%2Fcollect; NYK_PCOUNTER=25; NYK_ECOUNTER=162; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A17%2C%22s%22%3A1745823353%2C%22t%22%3A1745825386%7D',
}


def get_future_date(days_after_today):
    today = datetime.today()
    # Start counting from tomorrow
    future_date = today + timedelta(days=days_after_today)
    return future_date.strftime("%Y-%m-%d")


def clean_html_description(html_text):
    # Replace bold label tags with formatted label:
    html_text = re.sub(r'<b>([^<]+?)\s*:\s*</b>', r'\1: ', html_text)

    # Replace paragraph tags with newlines
    html_text = re.sub(r'</?p>', '\n', html_text)

    # Remove any other HTML tags if present
    html_text = re.sub(r'<[^>]+>', '', html_text)

    # Collapse multiple newlines and strip whitespace
    html_text = re.sub(r'\n+', '\n', html_text).strip()

    cleaned_text = re.sub(r'\s{2,}', ' ', html_text.strip())

    return cleaned_text

def fetch_and_parse_product(product_id):
    try:
        url = f"https://www.nykaafashion.com/red-tape-etpu-men-colorblocked-white-and-black-athleisure-walking-shoes/p/{product_id}"
        response = requests.get(url, cookies=cookies, headers=headers, timeout=15)

        # store HTML data here

        with open(f"Product Pages/{product_id}.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        match = re.search(r'<script id="__PRELOADED_STATE__" type="application/json">({.*?})</script>', response.text,
                          re.DOTALL)
        if not match:
            print("Match not found in data")
            return default_na_product(product_id)

        data = json.loads(match.group(1))
        print("product id:", product_id)
        product_data = data.get("details", {}).get("skuData", {}).get("product", {})
        category_data = product_data.get("primary_categories_json_all", {})
        # Filter and sort keys like 'l0_Category', 'l1_Category', ..., 'lN_Category'
        sorted_category_keys = sorted(
            (k for k in category_data.keys() if re.match(r"l\d+_Category", k)),
            key=lambda x: int(re.search(r"\d+", x).group())
        )

        category_hierarchy = " > ".join(
            category_data.get(key, {}).get("name", "N/A") for key in sorted_category_keys
        )
        if product_data.get("id") == str(product_id):
            print("fetched PID:", product_data.get("id"))

            offer_cookies = {
                'tm_stmp': '1747230874251',
                'bcookie': 'd95a561a-77aa-417a-a0b9-84cd44728f1a',
                '_gcl_au': '1.1.2097519378.1747230875',
                'WZRK_G': '8897d9798f3646df9d3fa53c11a0bb8c',
                '_ga': 'GA1.1.800417472.1747230876',
                'rum_abMwebSort': '92',
                'PHPSESSID': '876692f58c1d4c5ca7e1d2a86501d3cf',
                '_fbp': 'fb.1.1750059475211.894453321715247054',
                'EXP_rating-review-v2': 'rating-review-v2-c',
                'EXP_UPDATED_AT': '1750333959062',
                'EXP_SSR_CACHE': '50605be3484a1621ed9656d50322e59d',
                '_clck': '8jh87y%7C2%7Cfx4%7C0%7C1960',
                'mp_0cd3b66d1a18575ebe299806e286685f_mixpanel': '%7B%22distinct_id%22%3A%22%24device%3Aadc1084d-bc93-4be2-b210-bcf12708e367%22%2C%22%24device_id%22%3A%22adc1084d-bc93-4be2-b210-bcf12708e367%22%2C%22entry_page_product_id%22%3A%2219140254%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2Ffabindia-lime-green-cotton-silk-embroidery-chikankari-dupatta%2Fp%2F14946206%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2Ffabindia-lime-green-cotton-silk-embroidery-chikankari-dupatta%2Fp%2F14946206%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22entry_page_type%22%3A%22pdp%22%2C%22network_bandwidth%22%3A%224g%22%2C%22user_agent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F137.0.0.0%20Safari%2F537.36%22%2C%22%24search_engine%22%3A%22google%22%7D',
                'NYK_PCOUNTER': '1',
                'NYK_ECOUNTER': '2',
                '_ga_DZ4MXZBLKH': 'GS2.1.s1751015580$o21$g1$t1751016085$j60$l0$h0',
                'bm_sz': '74DBFE11CB8DAD35B951A7EBF406400A~YAAQSCTDFxbnH86XAQAAHSI25BzoEL25Y3UKPB66QvTU1pvTmxeW8CWp9YHId9g4H9/Zr4e0kGKKR4HTOSPw+spRvERUnCljfeDkv5+CAqTOKwxQYdNmH4Goz5ZZA/2JABnSKZrQ2jHflqP7pMaWncd5RCzRGvU14ulhhyyQhRaDLI2M6QctpG+/Gj0p6YJZSkVA4FvJUzhSMzG+16VHtnI66ZuVQcREZhVOTnzkUJ/rHK2DrDAl/mTPA+INT4RmJjaBwO42J8F1lsr60Gykhkl/P/5VNizEd9AxnbDTITPB5S6o5iRRConz4iGKvMFdzSRLw64Jy0BNcovDGpuq5nwSNdCasa8dcYt9lKcS3pkKAwMPhx1RmICUp/XnHupdDO0RvObB/z9l0ePU9EBUVuD19uIMSpiGhVpvVar5T2yF8EPf2RqE~3556402~4273217',
                '_abck': '2B8A3A2A5E1A4A94BDDF7AB6DD3082C9~0~YAAQSCTDF1bnH86XAQAAsyQ25A4a4DUQUQlpXxCHT1QvV9FpQ1+EmkhtYkUY5NFIYyOtH6Nn6SwjjXLr9z7KBs1owAJTgnW6dR19cJnNJpXdK3aTKcyUUFBhFlHuunJrStk/aoLYOqpCxZq/wFnMDy6nBL5rl59ciaIKfwih8VA1Oj8rEXWkmv/WEY9oDMAsA2FcaSDWNyxIT/gpKV30EBYozjZE153uzn5qXLNGGnymIexLu1cqTN4WH2aOCrUdpu9Jh53aEf3MPbvGJuJVWH6jEjd/+GtyI28tsrrCc33bCl+C+IPqFYqnIpj6ClJeRF/FcZPSftLxkS++B/uRbLcCZePU1L5ZRWmYeu+6E2glYzUg4yNkP/SodyU4MCe3UvGLsvuIYQbcXB5uPaiwpF623FjHunCQ89I3cX/eLL5U15Q/lx26RpQrMMJWCL2HEEzHqVEGsPdag1hn+oC9CEpARek7BzYQ0MTVdCMCeUjuw+CB5vNE+tUqxZtc8m+SlPoQXiEZ07MT3PmVwILIj8LlCuQvCo82kW/tp0heoHMropofOFdZUKmfJ+5N96Wtl7E6rBPJI3pQ9rt7nrEt1AjSWvr2v6kiye504v6MrObkabziovKwRDUKdVmmofCgGzmgDEbmpA9bbY43nmgt7oaFncM/To3Ljh7K3SYGrWEE9A==~-1~-1~1751883740',
            }

            offer_headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'priority': 'u=1, i',
                'referer': 'https://www.nykaafashion.com/fabindia-brass-mehnoor-antiqued-oil-lamp/p/16738502',
                'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                # 'cookie': 'tm_stmp=1747230874251; bcookie=d95a561a-77aa-417a-a0b9-84cd44728f1a; _gcl_au=1.1.2097519378.1747230875; WZRK_G=8897d9798f3646df9d3fa53c11a0bb8c; _ga=GA1.1.800417472.1747230876; rum_abMwebSort=92; PHPSESSID=876692f58c1d4c5ca7e1d2a86501d3cf; _fbp=fb.1.1750059475211.894453321715247054; EXP_rating-review-v2=rating-review-v2-c; EXP_UPDATED_AT=1750333959062; EXP_SSR_CACHE=50605be3484a1621ed9656d50322e59d; _clck=8jh87y%7C2%7Cfx4%7C0%7C1960; mp_0cd3b66d1a18575ebe299806e286685f_mixpanel=%7B%22distinct_id%22%3A%22%24device%3Aadc1084d-bc93-4be2-b210-bcf12708e367%22%2C%22%24device_id%22%3A%22adc1084d-bc93-4be2-b210-bcf12708e367%22%2C%22entry_page_product_id%22%3A%2219140254%22%2C%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2Ffabindia-lime-green-cotton-silk-embroidery-chikankari-dupatta%2Fp%2F14946206%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%2C%22__mps%22%3A%7B%7D%2C%22__mpso%22%3A%7B%22%24initial_referrer%22%3A%22https%3A%2F%2Fwww.nykaafashion.com%2Ffabindia-lime-green-cotton-silk-embroidery-chikankari-dupatta%2Fp%2F14946206%22%2C%22%24initial_referring_domain%22%3A%22www.nykaafashion.com%22%7D%2C%22__mpus%22%3A%7B%7D%2C%22__mpa%22%3A%7B%7D%2C%22__mpu%22%3A%7B%7D%2C%22__mpr%22%3A%5B%5D%2C%22__mpap%22%3A%5B%5D%2C%22entry_page_type%22%3A%22pdp%22%2C%22network_bandwidth%22%3A%224g%22%2C%22user_agent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F137.0.0.0%20Safari%2F537.36%22%2C%22%24search_engine%22%3A%22google%22%7D; NYK_PCOUNTER=1; NYK_ECOUNTER=2; _ga_DZ4MXZBLKH=GS2.1.s1751015580$o21$g1$t1751016085$j60$l0$h0; bm_sz=74DBFE11CB8DAD35B951A7EBF406400A~YAAQSCTDFxbnH86XAQAAHSI25BzoEL25Y3UKPB66QvTU1pvTmxeW8CWp9YHId9g4H9/Zr4e0kGKKR4HTOSPw+spRvERUnCljfeDkv5+CAqTOKwxQYdNmH4Goz5ZZA/2JABnSKZrQ2jHflqP7pMaWncd5RCzRGvU14ulhhyyQhRaDLI2M6QctpG+/Gj0p6YJZSkVA4FvJUzhSMzG+16VHtnI66ZuVQcREZhVOTnzkUJ/rHK2DrDAl/mTPA+INT4RmJjaBwO42J8F1lsr60Gykhkl/P/5VNizEd9AxnbDTITPB5S6o5iRRConz4iGKvMFdzSRLw64Jy0BNcovDGpuq5nwSNdCasa8dcYt9lKcS3pkKAwMPhx1RmICUp/XnHupdDO0RvObB/z9l0ePU9EBUVuD19uIMSpiGhVpvVar5T2yF8EPf2RqE~3556402~4273217; _abck=2B8A3A2A5E1A4A94BDDF7AB6DD3082C9~0~YAAQSCTDF1bnH86XAQAAsyQ25A4a4DUQUQlpXxCHT1QvV9FpQ1+EmkhtYkUY5NFIYyOtH6Nn6SwjjXLr9z7KBs1owAJTgnW6dR19cJnNJpXdK3aTKcyUUFBhFlHuunJrStk/aoLYOqpCxZq/wFnMDy6nBL5rl59ciaIKfwih8VA1Oj8rEXWkmv/WEY9oDMAsA2FcaSDWNyxIT/gpKV30EBYozjZE153uzn5qXLNGGnymIexLu1cqTN4WH2aOCrUdpu9Jh53aEf3MPbvGJuJVWH6jEjd/+GtyI28tsrrCc33bCl+C+IPqFYqnIpj6ClJeRF/FcZPSftLxkS++B/uRbLcCZePU1L5ZRWmYeu+6E2glYzUg4yNkP/SodyU4MCe3UvGLsvuIYQbcXB5uPaiwpF623FjHunCQ89I3cX/eLL5U15Q/lx26RpQrMMJWCL2HEEzHqVEGsPdag1hn+oC9CEpARek7BzYQ0MTVdCMCeUjuw+CB5vNE+tUqxZtc8m+SlPoQXiEZ07MT3PmVwILIj8LlCuQvCo82kW/tp0heoHMropofOFdZUKmfJ+5N96Wtl7E6rBPJI3pQ9rt7nrEt1AjSWvr2v6kiye504v6MrObkabziovKwRDUKdVmmofCgGzmgDEbmpA9bbY43nmgt7oaFncM/To3Ljh7K3SYGrWEE9A==~-1~-1~1751883740',
            }

            offer_params = {
                'customerGroupId': '0',
                'domain': 'fashion',
                'deviceType': 'WEBSITE',
                'isLoyal': '1',
                'productId': str(product_id),
                'mrp': product_data.get("price"),
                'sp': product_data.get("price"),
                'fetchUniversalOffers': 'true',
                'fetchCouponOffers': 'true',
                'fetchPaymentMethodOffers': 'true',
                'fetchTradeOffers': 'true',
                'fetchBestOffers': 'true',
            }

            offer_response = requests.get(
                'https://www.nykaafashion.com/gateway-api/offer/api/v1/product/customer/offer',
                params=offer_params,
                cookies=offer_cookies,
                headers=offer_headers,
            )

            response_data = offer_response.json().get('data')

            best_offer = None
            if response_data.get('bestOffers'):
                best_offer = response_data['bestOffers'][0]  # Take the first best offer
                best_offer_text = best_offer.get('title')
            else:
                best_offer_text = None

            # 2. Best Price
            best_price = response_data.get('offerBestPrice')

            # 3. Bank Offer (from `paymentOffers`)
            bank_offers = response_data.get('paymentOffers', [])
            bank_offer_texts = [offer.get('title') for offer in bank_offers if offer.get('title')]

            return {
                "product_id": product_data.get("id", "N/A"),
                "catalog_name": f"{product_data.get('title', '')} {product_data.get('subTitle', '')}",
                "catalog_id": product_data.get("id", "N/A"),
                "source": "Nykaa",
                "scraped_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "product_name": f"{product_data.get('title', '')} {product_data.get('subTitle', '')}",
                "image_url": product_data.get("meta_data", {}).get("imgUrl", "N/A"),
                "category_hierarchy": category_hierarchy,
                "product_price": product_data.get("discountedPrice", "N/A"),
                    "arrival_date": get_future_date(int(product_data.get("shipsIn", "N/A"))),
                "shipping_charges": "N/A",
                "is_sold_out": product_data.get("isOutOfStock", 0) != 0,
                "discount": product_data.get("discount", "N/A") if product_data.get("discount", "N/A") != 0 else "N/A",
                "mrp": product_data.get("price", "N/A"),
                "page_url": product_data.get("meta_data", {}).get("productUrl", "N/A"),
                "product_url": product_data.get("meta_data", {}).get("productUrl", "N/A"),
                "number_of_ratings": product_data.get("review_rating_json", {}).get("star_rating_count", "N/A"),
                "avg_rating": product_data.get("review_rating_json", {}).get("star_rating", "N/A"),
                "position": 1,
                "country_code": "IN",
                "images": " | ".join([media['url'] for media in product_data.get('productMedia', [])]) or "N/A",
                "Best_price": best_price if best_price else "N/A",
                "Best_offers": best_offer_text if best_offer_text else "N/A",
                "bank_offers": bank_offer_texts or "N/A",
                "product_details": clean_html_description(" | ".join(
                    [f"{section.get('value', "N/A")}"
                     for section in product_data.get('pdp_sections', [])
                     if section.get('widget_type') == 'plain_collapsable_widget' and section.get(
                        'title') == 'Know your product']
                ) or "N/A"),
                "specifications": " | ".join(
                        # From attribute_columnize_widget
                        [f"{attr.get('label', 'N/A')}: {attr.get('value', 'N/A')}"
                         for section in product_data.get('pdp_sections', [])
                         if section.get('title') == 'Product details'
                         for widget in section.get('child_widgets', [])
                         if widget.get('widget_type') == 'attribute_columnize_widget'
                         for attr in widget.get('attributes', [])]
                        +
                        # From plain_widget
                        [f"{widget.get('title', 'N/A')}: {widget.get('value', 'N/A')}"
                         for section in product_data.get('pdp_sections', [])
                         if section.get('title') == 'Product details'
                         for widget in section.get('child_widgets', [])
                         if widget.get('widget_type') == 'plain_widget']
                    ) or "N/A",
                "rating": product_data.get("review_rating_json", {}).get("star_rating", "N/A"),
                "MOQ": 1,  # product_data.get("max_allowed_qty", "N/A"),
                "brand": product_data.get("title", "N/A"),
                "product_code": product_data.get("sku", "N/A"),
                "Available_sizes": " | ".join(
                    [s.get('sizeName') for s in product_data.get("sizeOptions", {}).get('options', [])]
                ) or "N/A",
                "sellerPartnerId": product_data.get("sku", "N/A"),
                "seller_return_policy": next(
                    (section.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                     if section.get('title') == 'Return and exchange policy'), "N/A"),
                "manufacturing_info_packerInfo": next(
                    (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                     if section.get('widget_type') == 'attribute_widget'
                     for attr in section.get('attributes', [])
                     if 'Address of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A"),
                "manufacturing_info_seller_name": next(
                    (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                     if section.get('widget_type') == 'attribute_widget'
                     for attr in section.get('attributes', [])
                     if 'Name of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A"),
                "manufacturing_info_importerInfo": next(
                    (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                     if section.get('widget_type') == 'attribute_widget'
                     for attr in section.get('attributes', [])
                     if 'Address of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A"),
                "manufacturing_info_countryOfOrigin": next(
                    (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                     if section.get('widget_type') == 'attribute_widget'
                     for attr in section.get('attributes', [])
                     if 'Country of Origin' in attr.get('label', '')), "N/A"),
                "manufacturing_info_manufacturerInfo": next(
                    (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                     if section.get('widget_type') == 'attribute_widget'
                     for attr in section.get('attributes', [])
                     if 'Address of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A"),
                "More_colours": " | ".join(
                    [color.get('name', '').lower() for color in product_data.get('colorOptions', [])]
                ) or "N/A",
                "variation_id": " | ".join(
                    [f"{color.get('name', '').lower()} : {color.get('sku')}" for color in
                     product_data.get('colorOptions', [])]
                ) or "N/A",
            }

        else:
            print("store default value")
            return default_na_product(product_id)
    except Exception as e:
        traceback.print_exc()
        print(f"Error processing product {product_id}: {e}")
        return default_na_product(product_id)


def default_na_product(product_id):
    return {
        "product_id": str(product_id),
        "catalog_name": "N/A",
        "catalog_id": "N/A",
        "source": "Nykaa",
        "scraped_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "product_name": "N/A",
        "image_url": "N/A",
        "category_hierarchy": "N/A",
        "product_price": "N/A",
        "arrival_date": "N/A",
        "shipping_charges": "N/A",
        "is_sold_out": "N/A",
        "discount": "N/A",
        "mrp": "N/A",
        "page_url": "N/A",
        "product_url": "N/A",
        "number_of_ratings": "N/A",
        "avg_rating": "N/A",
        "position": "N/A",
        "country_code": "IN",
        "images": "N/A",
        "Best_price": "N/A",
        "Best_offers": "N/A",
        "bank_offers": "N/A",
        "product_details": "N/A",
        "specifications": "N/A",
        "rating": "N/A",
        "MOQ": "N/A",
        "brand": "N/A",
        "product_code": "N/A",
        "Available_sizes": "N/A",
        "sellerPartnerId": "N/A",
        "seller_return_policy": "N/A",
        "manufacturing_info_packerInfo": "N/A",
        "manufacturing_info_seller_name": "N/A",
        "manufacturing_info_importerInfo": "N/A",
        "manufacturing_info_countryOfOrigin": "N/A",
        "manufacturing_info_manufacturerInfo": "N/A",
        "More_colours": "N/A",
        "variation_id": "N/A",
    }


# Thread pool for concurrent execution
all_products = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_and_parse_product, int(row['Nykaa Fashion'])): row for index, row in df.iterrows()}

    for idx, future in enumerate(as_completed(futures)):
        result = future.result()
        if result:
            result["Id"] = idx + 1 # Assign ID during collection
            all_products.append(result)

if all_products:
    collection.insert_many(all_products)
    print("✅ Data inserted into MongoDB")

data = list(collection.find({}))

# Remove "_id" field from each document
for doc in data:
    doc.pop("_id", None)  # Safely remove '_id' if it exists

# Convert to DataFrame
df = pd.DataFrame(data)
if 'Id' in df.columns:
    cols = ['Id'] + [col for col in df.columns if col != 'Id']
    df = df[cols]

# Save to Excel
df.to_excel(f"nykaa_fashion_{collection_name}.xlsx", index=False, engine='openpyxl')

print(f"✅ Data exported to nykaa_fashion_{collection_name}.xlsx without '_id' field.")


# Save final data
# final_df = pd.DataFrame(all_products)
# final_df.to_csv("nykaa_products_deta.csv", index=False)
# print("✅ All data written to nykaa_products_threaded.csv")
