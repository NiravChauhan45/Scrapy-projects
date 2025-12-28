import json
from datetime import datetime
from distutils.command.clean import clean
from itertools import product, zip_longest
from typing import Iterable, Any
import scrapy
from duckdb.duckdb import description
import requests
import nykaa_saller.db_config as db
from nykaa_saller.config.database_config import ConfigDatabase
from scrapy import cmdline
import random
import os
import gzip
from parsel import Selector
import re
from nykaa_saller.items import NykaaSallerPdpItem


def make_pagesave(response, self_PAGE_SAVE_PATH, pagesave_path):
    if response.status == 200:
        if not os.path.exists(pagesave_path):
            os.makedirs(self_PAGE_SAVE_PATH, exist_ok=True)
            with gzip.open(pagesave_path, mode="wb") as file:
                file.write(response.body)
        else:
            print("Path already exists..!!")


def cleanText(text):
    text = re.sub("\s+", " ", text)
    text = re.sub("[\n\t]", "", text)
    # text = text.strip("-")
    return text.strip()


def getCategory(json_data, response):
    category_list = json_data.get('appReducer').get('breadCrumb')
    if category_list:
        category_lst = []
        for category in category_list:
            category_name = category.get('key')
            category_name = cleanText(category_name)
            if 'Home' not in category_name:
                category_lst.append(category_name)
        return category_lst
    else:
        category_list = json_data.get('dataLayer').get('product').get('categoryLevel')
        if category_list:
            category_lst = []
            for key, value in category_list.items():
                category_name = value.get('name')
                if category_name:
                    if 'Home' not in category_name:
                        category_lst.append(category_name)
            return category_lst


def getSellerName(json_data, response):
    seller_name = json_data.get('productPage').get('product').get('sellerName')
    if seller_name:
        return cleanText(seller_name)
    else:
        seller_name = response.xpath("//span[contains(text(),'Sold by')]/following-sibling::span/text()").get()
        if seller_name:
            return cleanText(seller_name)
        else:
            return None


def getProductId(json_data, product_id):
    product_id = json_data.get('productPage').get('product').get('id')
    if product_id:
        return product_id
    else:
        return product_id


def getProductName(json_data, response):
    product_name = response.xpath('//h1[@class="css-1gc4x7i"]/text()').get()
    if product_name:
        return cleanText(product_name)
    else:
        product_name = json_data.get('productPage').get('product').get('name')
        if product_name:
            return cleanText(product_name)
        else:
            return None


def getImageUrls(json_data, response):
    image_url_list = json_data.get('productPage').get('product').get('parentMedia')
    image_url_lst = []
    if image_url_list:
        for image_data in image_url_list:
            image_url = image_data.get('url')
            image_url_lst.append(image_url)
        return " | ".join(image_url_lst)
    else:
        image_url_list = response.xpath(
            '//div[@class="slide-view-container"]//img[@alt="product-thumbnail"]/@src').getall()
        image_url_lst = []
        if image_url_list:
            for image_url in image_url_list:
                image_url_lst.append(image_url)
            return " | ".join(image_url_lst)
        else:
            return None


def getProductRating(json_data, response):
    rating = json_data.get('productPage').get('product').get('rating')
    if rating:
        return rating
    else:
        rating = response.xpath('//div[@class="css-m6n3ou"]/text()').get()
        if rating:
            return rating
        else:
            return None


def getProductRatingCount(json_data, response):
    rating_count = json_data.get('productPage').get('product').get('ratingCount')
    if rating_count:
        return rating_count
    else:
        rating_count = response.xpath('//div[@class="css-1hvvm95"]/text()').get()
        if rating_count:
            return rating_count
        else:
            return None


def getProductReviewCount(json_data, response):
    review_count = json_data.get('productPage').get('product').get('reviewCount')
    if review_count:
        return review_count
    else:
        review_count = response.xpath('//div[@class="css-1hvvm95"]/text()').getall()
        review_count = re.findall(r'\d+', ' '.join(review_count))
        if review_count:
            return review_count[-1]
        else:
            return None


def getProductRatingCountMap(json_data, response):
    rating_list = json_data.get('productPage').get('product').get('reviewSplitUp')
    key_list = ["Poor", "Average", "Good", "Very Good", "Excellent"]
    rating_count_dict = dict()
    if rating_list:
        rating_list = rating_list[::-1]
        for key, value in zip_longest(key_list, rating_list):
            value = value.get("count")
            rating_count_dict[key] = value
        return json.dumps(rating_count_dict)
    else:
        rating_list = response.xpath('//span[@class="css-11lfsnj"]/text()').getall()
        if rating_list:
            rating_list = rating_list[::-1]
            for key, value in zip_longest(key_list, rating_list):
                rating_count_dict[key] = value
            return json.dumps(rating_count_dict)
        else:
            return None


def getProductSize(json_data, response):
    size = json_data.get('productPage').get('product').get('packSize')
    if size:
        return size
    else:
        size_list = response.xpath('//span[@class="css-1ctpgu6"]/text()').getall()
        if size_list:
            size = "".join(size_list)
            size = re.sub(r"[()]", "", size)
            return size


def remove_html(text):
    text = re.sub(r"<[^>]+>", "", text)
    return cleanText(text)


def getProductDetails(json_data, response):
    # Todo: description
    description_data = json_data.get('productPage').get('product').get('description')
    description_data = remove_html(description_data)
    expiry_date = f"Expiry Date: {json_data.get('productPage').get('product').get('expiry')}" if json_data.get(
        'productPage').get('product').get('expiry') else ''
    country_of_origin = f"Country of Origin: {json_data.get('productPage').get('product').get('originOfCountryName')}" if json_data.get(
        'productPage').get('product').get('originOfCountryName') else ''

    manufacturerName = f"Manufacturer: {json_data.get('productPage').get('product').get('manufacturerName')}" if json_data.get(
        'productPage').get('product').get('manufacturerName') else ''

    manufacturerAddress = f"Address: {json_data.get('productPage').get('product').get('manufacturerAddress')}" if json_data.get(
        'productPage').get('product').get('manufacturerAddress') else ''

    description_data = f"{description_data} {expiry_date} {country_of_origin} {manufacturerName} {manufacturerAddress}"
    description_data = cleanText(description_data)

    # Todo: Ingredients
    ingredients = json_data.get('productPage').get('product').get('ingredients')
    if ingredients:
        ingredients = remove_html(ingredients)

    # Todo: howToUse
    howToUse = json_data.get('productPage').get('product').get('howToUse')
    if howToUse:
        howToUse = remove_html(howToUse)

    product_details = f"{description_data} {ingredients} {howToUse}"
    product_details = cleanText(product_details)
    return product_details


def getProductPrice(json_data, response):
    price = json_data.get('productPage').get('product').get('offerPrice')
    if price:
        return price
    else:
        price = response.xpath('//span[@class="css-1jczs19"]/text()').get()
        if price:
            return price.replace('₹', '')


def getDeliveryCharges(Product_Price):
    if int(Product_Price) < 299:
        return '79'
    else:
        return 'N/A'


def getStatus(json_data, response):
    in_stock = json_data.get('productPage').get('product').get('inStock')
    if in_stock:
        return "TRUE"
    else:
        return "FALSE"


def getMRP(json_data, response):
    mrp = json_data.get('productPage').get('product').get('mrp')
    if mrp:
        return mrp
    else:
        mrp = response.xpath('//span[@class="css-u05rr"]//text()').get()
        if mrp:
            mrp = mrp.replace('₹', '')
            return mrp
        else:
            return None


def getDiscount(json_data, response):
    discount = json_data.get('productPage').get('product').get('discount')
    if discount:
        return discount
    else:
        discount = response.xpath('//span[@class="css-bhhehx"]/text()').get()
        if discount:
            discount = discount.replace('% Off', '')
            return discount
        else:
            return None


def getSKU(json_data):
    try:
        # productPage.product.id
        product_id = json_data['productPage']['product']['id']
        SKU = [s['sku'] for s in json_data['productPage']['product']['variants']]
        type_1 = 'configurable'
        if not SKU:
            SKU = [json_data['productPage']['product']['sku']]
            type_1 = 'simple'
        return SKU, type_1
    except:
        SKU = [json_data['productPage']['product']['sku']]
        type_1 = 'simple'
        return SKU, type_1


def getDeliveryDate(cookies, headers, sku, type_1, pagesave_path):
    if not isinstance(sku, list):
        sku = [sku]

    json_data = ''
    if not os.path.exists(pagesave_path):
        json_data = {
            'skus': sku,
            'type': type_1,
            'domain': 'nykaa',
            'source': 'pdp',
            'fetchDarkstoreDetails': False,
            'pincode': '781001',
        }

        response = requests.post('https://www.nykaa.com/edd/product/edd/default/fetch', cookies=cookies,
                                 headers=headers,
                                 json=json_data)
        with open(pagesave_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        json_data = response.json()
    else:
        with open(pagesave_path, "r", encoding="utf-8") as f:
            json_data = f.read()
        try:
            json_data = json.loads(json_data)
        except:
            pass

    if json_data:
        if isinstance(sku, list):
            sku = sku[0]

        delivery_date = json_data.get('data').get('details').get(sku).get('message')
        return delivery_date
    else:
        return None


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"
    allowed_domains = ["www.nykaa.com"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    def __init__(self, start_id, end, **kwargs):
        super().__init__(**kwargs)
        self.PAGE_SAVE_PATH = f"E:\\Nirav\\Project_page_save\\{db.database_name}\\{db.current_date}"
        os.makedirs(self.PAGE_SAVE_PATH, exist_ok=True)
        self.cookies = {
            'EXP_AB_PARTIAL_CHECKOUT': 'A',
            'EXP_PLP_PINKBOX_CTA': 'CONTROL',
            'EXP_AB_OFFER_DELTA_COMMUNICATION': 'A',
            'EXP_AB_MWEB_FILTERS_PLP': 'DEFAULT',
            'EXP_AB_VISUAL_FILTERS_PLP': 'DEFAULT',
            'EXP_SPECIAL_DEALS': 'CONTROL2',
            'EXP_UPDATED_AT': '1764827066518',
            'EXP_SSR_CACHE': 'f032ac255142bb326894a1ed3b8b018f',
            'PHPSESSID': 'WkLvEJdCmkZieaf1765804070763',
            '_gcl_au': '1.1.2125019929.1765804075',
            'run': '19',
            'EXP_REVIEW_COLLECTION': '1',
            'D_LST': '1',
            'D_PDP': '1',
            'bcookie': 'dc0c7d85-4401-48a6-a9e4-39829898a990',
            'PRIVE_TIER': 'null',
            'head_data_react': '{"id":"","nykaa_pro":false,"group_id":""}',
            'pro': 'false',
            '_gid': 'GA1.2.1989546305.1765804084',
            'EXP_OL': 'DEFAULT',
            'EXP_AB_NEW_SHOPPING_BAG': 'A',
            'EXP_H_F_M_M_S_P': '1',
            '_clck': '1vs35x8%5E2%5Eg1w%5E0%5E2175',
            'storeId': 'nykaa',
            'pinCodeDel': '781001',
            'countryCode': 'IN',
            '_gat_UA-31866293-9': '1',
            'bm_sz': '67DBE8C51C7743CDE41EC6F602959FC3~YAAQNxzFF96nX6+aAQAAhqHTJR6uTMhI66aU+QyaQMtH8FxKqmxuG/EZ/js7n7cdR3psq1lf1c89WdGGkpui2O/kDfNaCmxCsV6QS5jh/cXL3Lk6FgiLILiTE1dkMqR+nJbiUjVT4fexoo+pFpUKAn1cNsmrkmZKgRIaeLU4dOPQ9rkiO4n/GntyXXDmDBKaKp+sY7SQ2Hn5xlaHqvSeNBxcsue40+M1A7Nf8JRccnYMdBhvMOWCoxxLABrren4FxhQ+d9Q/HDwjzGFPX79YUiXjDVb4qT3R0imDoHYfKFq40aMareAH+4G4vqlPKaXNVsBeMScB9WFv4CcOI1EoqhAOw4cJPSWWI22grO4W6XGcXAVXPyZv8oIfLQoIFf6/0jlsuggDhpzWImY2HuMUj0vHN0agSEFbwSXbez7coeZkcdroQHdc8omxCyt1WyP8uG9zoU8kZeSiePDk~4342321~3486022',
            'SITE_VISIT_COUNT': '152',
            'WZRK_S_656-WZ5-7K5Z': '%7B%22p%22%3A3%7D',
            '_ga_LKNEBVRZRG': 'GS2.1.s1765864900$o4$g1$t1765866188$j52$l0$h0',
            '_ga': 'GA1.2.1967898466.1765804084',
            '_uetsid': '17409a50d9b711f0b01cbd2fd05a20c8',
            '_uetvid': '17448100d9b711f0aa9ac5f95dc3180d',
            '_ga_JQ1CQHSXRX': 'GS2.2.s1765864900$o3$g1$t1765866188$j56$l0$h0',
            'cto_bundle': '-C2cQ19RSTBtVWFqNnZ2elZuRXdLaXZoTTNtOHRQOUpTWExkSGpPRzQxUEJnYVlQZHBUdUZNUGlSYyUyQmQlMkJFeFlRSzZWWklBaTJFcXZtJTJCeVo0clVLZWVTak9zWDdNYnRueWdWUnNnQ1NmbEkyJTJCZktiaGJjQmR4SFdTYVNqYTF2TUx6TDhqaXBtbmxMYmxNSDAlMkJYUXpEJTJGSkV4QnclM0QlM0Q',
            '_clsk': '1wl41pi%5E1765866188920%5E4%5E1%5El.clarity.ms%2Fcollect',
            '_abck': 'D86A1358FBB8EAD57F4F3C3A8D0CA530~0~YAAQNxzFFxXPX6+aAQAA1U/UJQ/rrhgjR5mLHS+roCru7o/k0Qr7WxNDUHbLHuUgmX5kDPRyQeHN9LcfBoBhgajZ3Z/qOR2iDIh3YILVBXk6FGMTq96pMRXHBi13Dq6xiCKfhm4N+KXPS0Rab0YmIHSbG81SFu1fv6g5U3I1XoXgq/if9hA7d174sh0/3/CFxtqTae+k/3+crM2WLMkMDs0ryO20OKG+0a+sAgmLjgvXF0Tzj/5xLW5I8NEj9NolDmK1cBDcXdPwP6BxNF4KQpV+hLoHpRUm4BOYELLDJG6pkSrK1oE9uqg9LT/LPh7D9Yqd9la1PbyIbsQTnr3OnCL9XNKjHG9yAbm0S25sKhJ2r2Yj5hklb0sUUVH4LyjoujRxmOyGft1BF1w4kg+7AZkrb/JVSOI4roY1WrTCDQl1MKw8gclKWGXt0l6JzdDpi6MKXb8c+uYcLZv4CoDolplwBlL4Euwp8yzkQ3yZ/PZ5W56ufxb7aPO2qI7r6TjkpU0JEbFOiBDp+n0HeW6PRzIDjsUVxfn4qrys+PS8t1dVQYeumx3nOy/WvWV7Af/r1d1/LKXsjARJfPU1AbYkdL+Ns94abW3kqk2tJq5yIM3hGpwB1g7PZbzdlI9j3Hiy1dVrnn50iHntKvuFhVSuZs5vk+34fnS07Ikh1SFrh+mtGiH2yLdyaWccPprKL8f8EPBRCvTJzs+WsjhXjeNz83LfU2L+24GkiwAq3OM/Mew2y4oR+0UVmlmIp6qhyAsiH67qxX9WNoVPo3XUXw6hmEyShuuJFdTvvKH+nJymKxByv2WoEnIGLQsfxEuu2lJqXInwDWAxo1k0yr2R0DLdT4IZ9qBZoGB9by6c5tbGpnkwNK5BTQ8h2BQ8uAsnIp2miJRvwnWfYvecoy7VqRfa/r2jLBA/yJqYBKtQCg9TZ/aGbN8N4QwUEXIzvzaeDWBfhA==~-1~-1~1765866433~AAQAAAAE%2f%2f%2f%2f%2f2kwCtaTw1IwAHN99TFfVXdDX41gt%2fy1fwANWNnyK3pRui64%2fjQoOiymrZkOkXOHyryhomTyeI5HOgHQq6e71ihrh9z3M7felQETv6Uh9Sj%2fjkYlKf50skBYtUgkdDx26Yt8oJ0hUE7ptnZ%2fKUjeL6H1uY0C894%2f3ehrm+VStg%3d%3d~-1',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            # 'cookie': 'EXP_AB_PARTIAL_CHECKOUT=A; EXP_PLP_PINKBOX_CTA=CONTROL; EXP_AB_OFFER_DELTA_COMMUNICATION=A; EXP_AB_MWEB_FILTERS_PLP=DEFAULT; EXP_AB_VISUAL_FILTERS_PLP=DEFAULT; EXP_SPECIAL_DEALS=CONTROL2; EXP_UPDATED_AT=1764827066518; EXP_SSR_CACHE=f032ac255142bb326894a1ed3b8b018f; PHPSESSID=WkLvEJdCmkZieaf1765804070763; _gcl_au=1.1.2125019929.1765804075; run=19; EXP_REVIEW_COLLECTION=1; D_LST=1; D_PDP=1; bcookie=dc0c7d85-4401-48a6-a9e4-39829898a990; PRIVE_TIER=null; head_data_react={"id":"","nykaa_pro":false,"group_id":""}; pro=false; _gid=GA1.2.1989546305.1765804084; EXP_OL=DEFAULT; EXP_AB_NEW_SHOPPING_BAG=A; EXP_H_F_M_M_S_P=1; _clck=1vs35x8%5E2%5Eg1w%5E0%5E2175; storeId=nykaa; pinCodeDel=781001; countryCode=IN; _gat_UA-31866293-9=1; bm_sz=67DBE8C51C7743CDE41EC6F602959FC3~YAAQNxzFF96nX6+aAQAAhqHTJR6uTMhI66aU+QyaQMtH8FxKqmxuG/EZ/js7n7cdR3psq1lf1c89WdGGkpui2O/kDfNaCmxCsV6QS5jh/cXL3Lk6FgiLILiTE1dkMqR+nJbiUjVT4fexoo+pFpUKAn1cNsmrkmZKgRIaeLU4dOPQ9rkiO4n/GntyXXDmDBKaKp+sY7SQ2Hn5xlaHqvSeNBxcsue40+M1A7Nf8JRccnYMdBhvMOWCoxxLABrren4FxhQ+d9Q/HDwjzGFPX79YUiXjDVb4qT3R0imDoHYfKFq40aMareAH+4G4vqlPKaXNVsBeMScB9WFv4CcOI1EoqhAOw4cJPSWWI22grO4W6XGcXAVXPyZv8oIfLQoIFf6/0jlsuggDhpzWImY2HuMUj0vHN0agSEFbwSXbez7coeZkcdroQHdc8omxCyt1WyP8uG9zoU8kZeSiePDk~4342321~3486022; SITE_VISIT_COUNT=152; WZRK_S_656-WZ5-7K5Z=%7B%22p%22%3A3%7D; _ga_LKNEBVRZRG=GS2.1.s1765864900$o4$g1$t1765866188$j52$l0$h0; _ga=GA1.2.1967898466.1765804084; _uetsid=17409a50d9b711f0b01cbd2fd05a20c8; _uetvid=17448100d9b711f0aa9ac5f95dc3180d; _ga_JQ1CQHSXRX=GS2.2.s1765864900$o3$g1$t1765866188$j56$l0$h0; cto_bundle=-C2cQ19RSTBtVWFqNnZ2elZuRXdLaXZoTTNtOHRQOUpTWExkSGpPRzQxUEJnYVlQZHBUdUZNUGlSYyUyQmQlMkJFeFlRSzZWWklBaTJFcXZtJTJCeVo0clVLZWVTak9zWDdNYnRueWdWUnNnQ1NmbEkyJTJCZktiaGJjQmR4SFdTYVNqYTF2TUx6TDhqaXBtbmxMYmxNSDAlMkJYUXpEJTJGSkV4QnclM0QlM0Q; _clsk=1wl41pi%5E1765866188920%5E4%5E1%5El.clarity.ms%2Fcollect; _abck=D86A1358FBB8EAD57F4F3C3A8D0CA530~0~YAAQNxzFFxXPX6+aAQAA1U/UJQ/rrhgjR5mLHS+roCru7o/k0Qr7WxNDUHbLHuUgmX5kDPRyQeHN9LcfBoBhgajZ3Z/qOR2iDIh3YILVBXk6FGMTq96pMRXHBi13Dq6xiCKfhm4N+KXPS0Rab0YmIHSbG81SFu1fv6g5U3I1XoXgq/if9hA7d174sh0/3/CFxtqTae+k/3+crM2WLMkMDs0ryO20OKG+0a+sAgmLjgvXF0Tzj/5xLW5I8NEj9NolDmK1cBDcXdPwP6BxNF4KQpV+hLoHpRUm4BOYELLDJG6pkSrK1oE9uqg9LT/LPh7D9Yqd9la1PbyIbsQTnr3OnCL9XNKjHG9yAbm0S25sKhJ2r2Yj5hklb0sUUVH4LyjoujRxmOyGft1BF1w4kg+7AZkrb/JVSOI4roY1WrTCDQl1MKw8gclKWGXt0l6JzdDpi6MKXb8c+uYcLZv4CoDolplwBlL4Euwp8yzkQ3yZ/PZ5W56ufxb7aPO2qI7r6TjkpU0JEbFOiBDp+n0HeW6PRzIDjsUVxfn4qrys+PS8t1dVQYeumx3nOy/WvWV7Af/r1d1/LKXsjARJfPU1AbYkdL+Ns94abW3kqk2tJq5yIM3hGpwB1g7PZbzdlI9j3Hiy1dVrnn50iHntKvuFhVSuZs5vk+34fnS07Ikh1SFrh+mtGiH2yLdyaWccPprKL8f8EPBRCvTJzs+WsjhXjeNz83LfU2L+24GkiwAq3OM/Mew2y4oR+0UVmlmIp6qhyAsiH67qxX9WNoVPo3XUXw6hmEyShuuJFdTvvKH+nJymKxByv2WoEnIGLQsfxEuu2lJqXInwDWAxo1k0yr2R0DLdT4IZ9qBZoGB9by6c5tbGpnkwNK5BTQ8h2BQ8uAsnIp2miJRvwnWfYvecoy7VqRfa/r2jLBA/yJqYBKtQCg9TZ/aGbN8N4QwUEXIzvzaeDWBfhA==~-1~-1~1765866433~AAQAAAAE%2f%2f%2f%2f%2f2kwCtaTw1IwAHN99TFfVXdDX41gt%2fy1fwANWNnyK3pRui64%2fjQoOiymrZkOkXOHyryhomTyeI5HOgHQq6e71ihrh9z3M7felQETv6Uh9Sj%2fjkYlKf50skBYtUgkdDx26Yt8oJ0hUE7ptnZ%2fKUjeL6H1uY0C894%2f3ehrm+VStg%3d%3d~-1',
        }
        self.start_id = start_id
        self.end = end
        self.db = ConfigDatabase(database=db.database_name, table=db.link_table)

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'pending'}, start=self.start_id, end=self.end)
        for result in results:
            product_url = result.get('product_url').strip()
            product_id = product_url.split('/p/')[-1]
            pagesave_path = self.PAGE_SAVE_PATH + "\\" + product_id + ".html.gz"
            if os.path.exists(pagesave_path):
                with gzip.open(pagesave_path, 'rb') as f:
                    html_content = f.read().decode('utf-8', errors='ignore')

                yield scrapy.Request(
                    url=f'file:///{pagesave_path}',
                    body=html_content,
                    cb_kwargs={
                        "product_url": product_url, "product_id": product_id,
                    },
                    dont_filter=True,
                    callback=self.parse
                )
            else:
                yield scrapy.Request(url=product_url, headers=self.headers, cookies=self.cookies,
                                     cb_kwargs={"product_url": product_url, "product_id": product_id},
                                     meta={'impersonate': self.browser})

    def parse(self, response, **kwargs):
        product_id = kwargs.get('product_id')
        product_id = product_id.replace('\r\n', '')
        product_url = kwargs.get('product_url')
        pagesave_path = self.PAGE_SAVE_PATH + "\\" + product_id + ".html.gz"

        if not os.path.exists(pagesave_path):
            if response.status == 200:
                make_pagesave(response, self.PAGE_SAVE_PATH, pagesave_path)
        else:
            with gzip.open(pagesave_path, mode="rb") as file:
                response = file.read()
            # response = gzip.decompress(response.body)
            response = response.decode('utf-8')
            response = Selector(text=response)

        json_data = response.xpath("//script[contains(text(),'__PRELOADED_STATE__ ')]/text()").get()
        if json_data:
            json_data = json_data.replace("window.__PRELOADED_STATE__ =", "").strip()
            json_data = json.loads(json_data)

            item = NykaaSallerPdpItem()

            # Todo: Categories
            category_list = getCategory(json_data, response)
            item['Super_Category_Name'] = ''
            item['Category_name'] = ''
            item['Sub_Category_Name'] = ''
            if category_list:
                try:
                    item['Super_Category_Name'] = category_list[0]
                except:
                    item['Super_Category_Name'] = None
                try:
                    item['Category_name'] = category_list[1]
                except:
                    item['Category_name'] = None
                try:
                    item['Sub_Category_Name'] = category_list[2]
                except:
                    item['Sub_Category_Name'] = None
            # Todo: Seller Name
            item['Seller_Data_Name'] = getSellerName(json_data, response)

            # Todo: Product_Sku_Id
            item['Product_Sku_Id'] = getProductId(json_data, product_id)

            # Todo: Product_Sku_Name
            item['Product_Sku_Name'] = getProductName(json_data, response)

            # Todo: Product_Sku_Url
            item['Product_Sku_Url'] = product_url.strip()

            # Todo: Product_Images_Urls
            item['Product_Images_Urls'] = getImageUrls(json_data, response)

            # Todo: Product_Count_of_Images
            item['Product_Count_of_Images'] = len(item['Product_Images_Urls'].split(" | ")) if item[
                'Product_Images_Urls'] else None

            # Todo: Product_Rating
            item['Product_Rating'] = getProductRating(json_data, response)

            # Todo: Product_Rating_Count
            item['Product_Rating_Count'] = getProductRatingCount(json_data, response)

            # Todo: Product_Review_Count
            item['Product_Review_Count'] = getProductReviewCount(json_data, response)

            # Todo:Product_Rating_Count_Map
            item['Product_Rating_Count_Map'] = getProductRatingCountMap(json_data, response)

            # Todo: Product_Size
            item['Product_Size'] = getProductSize(json_data, response)

            # Todo: Product_Variation_Price
            item['Product_Variation_Price'] = "N/A"

            # Todo: Product_Variation_Min_Price
            item['Product_Variation_Min_Price'] = "N/A"

            # Todo: Product_Variation_Max_Price
            item['Product_Variation_Max_Price'] = "N/A"

            # Todo:Product_Details
            item['Product_Details'] = getProductDetails(json_data, response)

            # Todo: Product_Price
            item['Product_Price'] = getProductPrice(json_data, response)

            # Todo: Product_Delivery_Charges
            item['Product_Delivery_Charges'] = getDeliveryCharges(item['Product_Price'])

            # Todo: Product_In_Stock_Status
            item['Product_In_Stock_Status'] = getStatus(json_data, response)

            # Todo: Product_Mrp
            item['Product_Mrp'] = getMRP(json_data, response)

            # Todo: Product_Discounted_Price
            item['Product_Discounted_Price'] = item['Product_Price']

            # Todo: Product_Discount_Percent
            item['Product_Discount_Percent'] = getDiscount(json_data, response)

            # Todo: Seller_Id
            item['Seller_Id'] = '30855'

            # Todo: Seller_Name
            item['Seller_Name'] = item['Seller_Data_Name']

            # Todo: Seller_Url
            item['Seller_Url'] = 'https://www.nykaa.com/brands/rhe-cosmetics/c/30855'

            # Todo: Seller_Rating
            item['Seller_Rating'] = "N/A"

            # Todo: Seller_Rating_Count
            item['Seller_Rating_Count'] = "N/A"

            # Todo: Seller_Followers_Count
            item['Seller_Followers_Count'] = "N/A"

            # Todo: Seller_Product_Count
            item['Seller_Product_Count'] = 'N/A'

            # Todo:Product_Delivery_Date
            sku, type_1 = getSKU(json_data)
            if len(sku) == 1:
                sku = "".join(sku)
            PAGE_SAVE_PATH = f"E:\\Nirav\\Project_page_save\\{db.database_name}\\{db.current_date}\\delivery"
            os.makedirs(PAGE_SAVE_PATH, exist_ok=True)
            pagesave_path = PAGE_SAVE_PATH + "\\" + product_id + ".json"

            item['Product_Delivery_Date'] = getDeliveryDate(self.cookies, self.headers, sku, type_1, pagesave_path)

            # Todo:Product_Pincode
            item['Product_Pincode'] = '781001'

            # Todo: City
            item['City'] = "GUWAHATI"

            # Todo:Scrape_Date
            item['Scrape_Date'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            yield item
        else:
            print("json_data not found")


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpDataSpider.name} -a start_id=1 -a end=100".split())
