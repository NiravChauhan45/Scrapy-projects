import base64
import json
import re
import time

import logger
from curl_cffi import requests
from parsel import Selector

from datetime import datetime, timedelta


def remove_extra_space(text):
    text = re.sub("\\s+", " ", text).strip()
    return text


def get_place_id(pincode):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'common-client-static-version': '101',
        'content-type': 'application/json',
        'osmos-enabled': 'true',
        'priority': 'u=1, i',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }

    params = {
        "inputText": pincode,  # Pass pincode or search text
        "token": "5036f45b-a066-499c-ba68-ff23fd46a2b2",
    }

    try:
        response = requests.get(
            "https://www.bigbasket.com/places/v1/places/autocomplete/",
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()  # Raise error if bad HTTP status
        json_data = response.json()

        predictions = json_data.get("predictions", [])
        if predictions:
            return predictions[0].get("placeId")  # first match
        return None

    except requests.RequestException as e:
        print(f"HTTP Error: {e}")
        return None
    except ValueError:
        print("Error parsing JSON")
        return None


def get_lat_long(place_id: str) -> str | None:
    headers = {
        "sec-ch-ua-platform": '"Windows"',
        "common-client-static-version": "101",
        "yArmour": "246",
        "Referer": "https://www.bigbasket.com/",
        "X-Integrated-FC-Door-Visible": "false",
        "X-Tracker": "bwb-a54130d5-84da-4c74-8b36-b54d0addb883",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "xArmour": "1074",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/139.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/json",
        "X-Entry-Context": "bbnow",
        "X-Entry-Context-Id": "10",
        "X-Channel": "BB-WEB",
    }

    params = {"placeId": place_id}

    try:
        response = requests.get(
            "https://www.bigbasket.com/places/v1/places/details/",
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        json_data = response.json()

        geometry = json_data.get("geometry", {})
        location = geometry.get("location")
        if location:
            lat = location.get("lat")
            lng = location.get("lng")
            if lat is not None and lng is not None:
                coords = f"{lat}|{lng}"
                encoded = base64.b64encode(coords.encode()).decode()
                return encoded

        return None

    except requests.RequestException as e:
        print(f"HTTP error: {e}")
        return None
    except ValueError:
        print("Error parsing JSON")
        return None


def get_pdp_response(product_id, pincode, encoded_id, retries=5, backoff=2):
    if "https" in product_id or "http" in product_id:
        url = product_id
    else:
        url = f"https://www.bigbasket.com/pd/{product_id}"  # fixed f-string
    cookies = {
        '_bb_vid': 'ODY3Mzk5Njc5MzUxNzQzMjE0',
        '_bb_lat_long': encoded_id,
        '_bb_aid': '"Mjk1MzkxMjU3Mw=="',
        '_bb_pin_code': pincode,
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        # 'cookie': '_bb_locSrc=default; x-channel=web; _bb_vid=ODY3Mzk5Njc5MzUxNzQzMjE0; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=FWgeWnmFOOuolD09qdUmNNAR7qbLjwIp5PKaPCTo8YEMNldsb3IbI9D3FnBRw9W7; _bb_bb2.0=1; _is_tobacco_enabled=0; _is_bb1.0_supported=0; bb2_enabled=true; bm_ss=ab8e18ef4e; csurftoken=8m-FdA.ODY3Mzk5Njc5MzUxNzQzMjE0.1755768251970.zYQwpiNAVpa6Yx8OKa3My+ouTs+GeI9hXBZ945C+sOM=; ufi=1; bigbasket.com=f51d4352-d622-43c0-aa58-33d623d65e38; _gcl_au=1.1.384881824.1755768254; jarvis-id=283cd44c-a1d6-4a40-9403-6faec96f4deb; _gid=GA1.2.519655507.1755768254; _gat_UA-27455376-1=1; adb=0; _fbp=fb.1.1755768254773.76079300477097255; _bb_lat_long=MjMuMDI2NDI1OXw3Mi41ODQzNDE0; _bb_cid=15; _bb_aid="Mjk1MzkxMjU3Mw=="; xentrycontext=bb-b2c; xentrycontextid=100; jentrycontextid=100; isintegratedsa=false; is_global=0; _bb_addressinfo=MjMuMDI2NDI1OXw3Mi41ODQzNDE0fEJoYXR0YXwzODAwMDF8QWhtZWRhYmFkfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=380001; _bb_sa_ids=17182; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xNzE4Mg==; is_integrated_sa=0; bm_s=YAAQHkPHF7/8zKyYAQAA+P/xywMgq1v/gXfwV6j6bGdix9j2/1LUryyUFGgx1zttOCDBEf64bi/IABwpNTzos+vBRyxF07Q6VB+PCnFUb9b1uUlHG7aNC0qSiuOXrqp0RWRyAYljI1SKqxGaMc8j9uAw24boe5uaXs8EFAX2F5FiEnSP16lzD9IFKOvyctrn+O5ijB2i4p+euV09bCsTdWp72N6MdI1Ly358q3h9IENHWKfPVft6JX+c5/dbh3fyUiIULAtGCjk/fn/rZKwL4ni2QqHt/xZaxDJP2xX9NBEcNP0M4/QKy5YOVoAWhYOrytEgxfqwhrakfZ8DX8RjQuP2mZlxSZIpJGtH6ToLUf1mp+Kp8JH4UmoAGOXleE8YaUGhu/oqvETiDWD0KbuxdS9oJJVvtfvloUZBTVDrBnDAykCsqbO+8HpekRWItZ2/PGDU9EodrLXenZATVc/UKs3Fmsw0ZyP4KcMutRFC2b2EKxM4RM4u/I5awCKhyfsIdk0YJEwx6/egOzGkr4l0L8wDPbQDp0EBpl1gR0aY5IcrGiQe1ZC1NuziK59ufw9s9Qqk93HZgQ==; bm_so=2295633B862E00C1C57D0CE322269B9CC6C82A1F9951CE4AE4D83635D4A37805~YAAQHkPHF8D8zKyYAQAA+P/xywQVDFpu5hgZ3nweGoQZ2qzJ2aDZKyyWZvFoBxcGzHkHdW/6GZHN6ggyv8OKx6G79Argf4jvfvl3S7n+1+Z9UTVuNVWd2+zx5O/3I/yhPcHP8eP/ZDJ8IpfL/vRSRhPc0mIc4pBKVk2WcB96m0j5ROBADmExx7VXcgu+7DKwxwGXXEnzD8aAEJCi2YFgwaz1jqb4gSQbo8GncjNBVmnhcrbkFfkeNjSIGKWhn7N23TtSsQLSZpnnu311i/qZzQ1B4xGdwCONf4vt85VI2sIJRba1DGInI0jC09Hjh7Mz8Tv6B24kTcWrDmTaNCbv8Uct/R58S9xcvXfbHLkFa33L9zTvp0n4pmTsyNh1xMQsC8yGEJ3WxBE1OYlIT7qbZjm6DQB30Pvg8gmdwingFJB8nqcxNwXukxCcVKdkB0A7ACiXFDWTwToiH+PmWi14Ow==; ts=2025-08-21%2014:54:51.799; _ga_FRRYG5VKHX=GS2.1.s1755768254$o1$g1$t1755768291$j23$l0$h0; _ga=GA1.2.2075497224.1755768254; bm_lso=2295633B862E00C1C57D0CE322269B9CC6C82A1F9951CE4AE4D83635D4A37805~YAAQHkPHF8D8zKyYAQAA+P/xywQVDFpu5hgZ3nweGoQZ2qzJ2aDZKyyWZvFoBxcGzHkHdW/6GZHN6ggyv8OKx6G79Argf4jvfvl3S7n+1+Z9UTVuNVWd2+zx5O/3I/yhPcHP8eP/ZDJ8IpfL/vRSRhPc0mIc4pBKVk2WcB96m0j5ROBADmExx7VXcgu+7DKwxwGXXEnzD8aAEJCi2YFgwaz1jqb4gSQbo8GncjNBVmnhcrbkFfkeNjSIGKWhn7N23TtSsQLSZpnnu311i/qZzQ1B4xGdwCONf4vt85VI2sIJRba1DGInI0jC09Hjh7Mz8Tv6B24kTcWrDmTaNCbv8Uct/R58S9xcvXfbHLkFa33L9zTvp0n4pmTsyNh1xMQsC8yGEJ3WxBE1OYlIT7qbZjm6DQB30Pvg8gmdwingFJB8nqcxNwXukxCcVKdkB0A7ACiXFDWTwToiH+PmWi14Ow==^1755768292879',
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            response.raise_for_status()  # raise if not 2xx
            return response
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                wait_time = backoff ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("Max retries reached. Request failed.")
                return None


def clean_price(price_text):
    price_text = price_text.replace("₹", "").replace(",", "")
    price_text = re.sub("\\s+", " ", price_text)
    return price_text.strip()


def calculate_discount(price, mrp):
    discount = ((float(mrp) - float(price)) / float(mrp)) * 100
    return round(discount, 2)  # round to 2 decimal places


def big_basket_pdp_page(response, old_product_id, pincode):
    selector = Selector(text=response.text)
    json_data = selector.xpath("//script[@id='__NEXT_DATA__']/text()").get()
    json_data = json.loads(json_data)
    item = dict()

    try:
        product_data_list = json_data.get('props').get('pageProps').get('productDetails').get('children')
    except:
        product_data_list = ''

    if product_data_list:
        for product_data in product_data_list:
            if old_product_id == product_data.get('id'):
                # Todo: product_id
                try:
                    item['product_id'] = product_data.get('id')
                except:
                    item['product_id'] = "N/A"

                # Todo: seller_name
                try:
                    item['seller_name'] = "N/A"
                except:
                    item['seller_name'] = "N/A"

                # Todo: platform
                try:
                    item['platform'] = "Big Basket"
                except:
                    item['platform'] = "N/A"

                # Todo: SKU
                try:
                    item['SKU'] = item['product_id']
                except:
                    item['SKU'] = "N/A"

                # Todo: brand
                try:
                    item['brand_name'] = product_data.get('brand').get('name')
                except:
                    brand = selector.xpath("//a[@class='Description___StyledLink-sc-82a36a-1 gePjxR']/text()").get()
                    item['brand_name'] = re.sub("\\s+", " ", brand) if brand else "N/A"

                # Todo: link
                try:
                    product_url = "https://www.bigbasket.com" + product_data.get(
                        'absolute_url') if product_data.get(
                        'absolute_url') else "N/A"
                    item['link'] = product_url
                except:
                    item['link'] = "N/A"

                # Todo:
                item['pincode'] = pincode

                # Todo: Todo:category_path
                try:
                    category_hierarchy_lst = []
                    category_hierarchy_lst.append("Home")
                    category_hierarchy_list = product_data.get('breadcrumb')
                    for category in category_hierarchy_list:
                        category = category.get('name')
                        if "home" not in category.lower():
                            category_hierarchy_lst.append(category)
                    item['category_path'] = " / ".join(
                        category_hierarchy_lst) if category_hierarchy_lst else "N/A"
                except:
                    item['category_path'] = "N/A"

                # Todo: date_time_of_crawling
                try:
                    item['date_time_of_crawling'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                except:
                    item['date_time_of_crawling'] = "N/A"

                # Todo:model_name_number
                try:
                    item['model_name_number'] = "N/A"
                except:
                    item['model_name_number'] = "N/A"

                # Todo: Images
                try:
                    image_list = []
                    for image in product_data.get('images'):
                        image = image.get("l")
                        image_list.append(image)
                    # item['images'] = image_list
                except:
                    pass
                    # item['images'] = "N/A"

                # Todo: image_url
                try:
                    item['image_url'] = image_list[0]
                except:
                    item['image_url'] = "N/A"

                # Todo: product_name
                try:
                    product_name = selector.xpath(
                        "//h1[@class='Description___StyledH-sc-82a36a-2 bofYPK']/text()").get()
                    item['product_name'] = re.sub("\\s+", " ", product_name) if product_name else "N/A"
                except:
                    item['product_name'] = "N/A"

                # Todo: rating
                try:
                    item['rating'] = float(product_data.get('rating_info').get('avg_rating')) if product_data.get(
                        'rating_info').get('avg_rating') else "N/A"
                except:
                    item['rating'] = "N/A"

                # Todo: number_of_rating
                try:
                    item['number_of_ratings'] = product_data.get('rating_info').get(
                        'rating_count') if product_data.get(
                        'rating_info').get('rating_count') else "N/A"
                except:
                    item['number_of_ratings'] = "N/A"

                # Todo: star-rating
                try:
                    item['1_star'] = json_data.get('props').get('pageProps').get('dySectionsData').get('rnrData').get(
                        'rating_stats').get('ratings_count_1')
                    item['2_star'] = json_data.get('props').get('pageProps').get('dySectionsData').get('rnrData').get(
                        'rating_stats').get('ratings_count_2')
                    item['3_star'] = json_data.get('props').get('pageProps').get('dySectionsData').get('rnrData').get(
                        'rating_stats').get('ratings_count_3')
                    item['4_star'] = json_data.get('props').get('pageProps').get('dySectionsData').get('rnrData').get(
                        'rating_stats').get('ratings_count_4')
                    item['5_star'] = json_data.get('props').get('pageProps').get('dySectionsData').get('rnrData').get(
                        'rating_stats').get('ratings_count_5')
                except:
                    item['1_star'], item['2_star'], item['3_star'], item['4_star'], item['5_star'] = "N/A"

            # Todo:coupon
            try:
                item['coupon'] = 'N/A'
            except:
                item['coupon'] = "N/A"

            # Todo:promotions
            try:
                item['promotions'] = "N/A"
            except:
                item['promotions'] = "N/A"

            # Todo:bestseller
            try:
                item['bestseller'] = "N/A"
            except:
                item['bestseller'] = "N/A"

            # Todo:stock
            try:
                if product_data.get('availability').get('avail_status'):
                    if product_data.get('availability').get('avail_status') == "001":
                        item['stock'] = True
                    else:
                        item['stock'] = False
            except:
                item['stock'] = False

            # Todo:delivery_date
            try:
                delivery_date = product_data.get('availability').get('short_eta') if product_data.get(
                    'availability') else "N/A"

                if "min" in delivery_date.lower():
                    new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    item['delivery_date'] = new_date

                if "days" in delivery_date.lower():
                    digits = re.findall(r'\d+', delivery_date)
                    delivery_date = ''.join(digits)
                    # get current datetime
                    current_date = datetime.now()

                    # extract number of days
                    days_to_add = int(re.findall(r'\d+', delivery_date)[0])

                    # add days
                    new_date = current_date + timedelta(days=days_to_add)

                    item['delivery_date'] = new_date.strftime("%Y-%m-%d %H:%M:%S")
            except:
                item['delivery_date'] = "N/A"

            # Todo:min_delivery_days
            try:
                item['min_delivery_days'] = item['delivery_date']
            except:
                item['min_delivery_days'] = "N/A"

            # Todo:max_delivery_days
            try:
                item['max_delivery_days'] = item['delivery_date']
            except:
                item['max_delivery_days'] = "N/A"

            # Todo: mrp
            try:
                mrp = product_data.get('pricing').get('discount').get('mrp')
                item['mrp'] = float(mrp) if mrp else "N/A"
            except:
                item['mrp'] = 'N/A'

            # Todo: price
            try:
                price = product_data.get('pricing').get('discount').get('prim_price').get('sp')
                item['offer_price'] = float(price) if price else item['mrp']
            except:
                item['offer_price'] = item['mrp']

            # Todo: max_operating_price
            try:
                mrp = product_data.get('pricing').get('discount').get('mrp')
                item['max_operating_price'] = float(mrp) if mrp else "N/A"
            except:
                item['max_operating_price'] = 'N/A'

            # Todo: discount-percent
            try:
                discount = product_data.get('pricing').get('discount').get('d_text')
                if "%" in discount:
                    discount = discount.replace("%", "").replace("OFF", "").strip()
                    item['discount_percent'] = float(discount) if discount else "N/A"
                else:
                    if item['mrp'] != "N/A" and item['mrp']:
                        discount_percent = calculate_discount(item['price'], item['mrp'])
                        item['discount_percent'] = discount_percent
            except:
                item['discount_percent'] = "N/A"
            # -----------------------------------other dict--------------------------------------------------------
            other_dict = dict()

            # Todo: product_url
            try:
                product_url = "https://www.bigbasket.com" + product_data.get('absolute_url') if product_data.get(
                    'absolute_url') else "N/A"
                other_dict['url'] = product_url
            except:
                other_dict['url'] = "N/A"

            # Todo: Images
            try:
                image_list = []
                for image in product_data.get('images'):
                    image = image.get("l")
                    image_list.append(image)
                other_dict['images'] = image_list
            except:
                other_dict['images'] = "N/A"

            # Todo:weight
            try:
                other_dict['weight'] = product_data.get("w")
            except:
                other_dict['weight'] = "N/A"

            # Todo: number_of_review
            try:
                other_dict['number_of_review'] = product_data.get('rating_info').get(
                    'review_count') if product_data.get(
                    'rating_info').get('review_count') else "N/A"
            except:
                other_dict['number_of_review'] = "N/A"

            # Todo: is_vage
            try:
                is_vage = product_data.get('additional_attr').get('info')[0]
                is_vage = is_vage.get("label")
                if is_vage == "veg":
                    other_dict['is_veg'] = True
                else:
                    other_dict['is_veg'] = False
            except:
                other_dict['is_veg'] = True

            # # Todo:availability
            try:
                if product_data.get('availability').get('avail_status'):
                    if product_data.get('availability').get('avail_status') == "001":
                        other_dict['availability'] = True
                    else:
                        other_dict['availability'] = False
            except:
                other_dict['availability'] = False

            # Todo: about this item
            try:
                about_this_item = product_data.get('tabs')
                for about in about_this_item:
                    if "About the Product" in about.get("title"):
                        about_this_item_text = about.get('content')
                        ss = Selector(text=about_this_item_text)
                        about_this_item_text = " ".join(ss.xpath("//p//text()").getall())
                        other_dict['about_this_item'] = remove_extra_space(about_this_item_text)
            except:
                item['about_this_item'] = "N/A"

            # Todo: ingredients
            try:
                ingredients_list = product_data.get('tabs')
                for ingredients in ingredients_list:
                    if "Ingredients" in ingredients.get("title"):
                        ingredients_text = ingredients.get('content')
                        ss = Selector(text=ingredients_text)
                        ingredients_text = " ".join(ss.xpath("//p//text()").getall())
                        other_dict['ingredients'] = remove_extra_space(ingredients_text)
            except:
                other_dict['ingredients'] = "N/A"

            # Todo: Other Product Info
            try:
                other_product_info = product_data.get('tabs')
                for other_product in other_product_info:
                    if "Other Product Info" in other_product.get("title"):
                        other_product_info = other_product.get('content')
                        ss = Selector(text=other_product_info)
                        other_product_text = " ".join(ss.xpath("//p//text()").getall())
                        other_dict['other_product_info'] = remove_extra_space(other_product_text)
            except:
                other_dict['other_product_info'] = "N/A"

            # Todo: From the Brand
            try:
                from_the_brand = product_data.get('tabs')
                for other_product in from_the_brand:
                    if "From the Brand" in other_product.get("title"):
                        from_the_brand = other_product.get('content')
                        ss = Selector(text=from_the_brand)
                        from_the_brand_text = " ".join(ss.xpath("//p//text()").getall())
                        other_dict['from_the_brand'] = remove_extra_space(from_the_brand_text)
            except:
                other_dict['from_the_brand'] = "N/A"

            # Todo: how_to_use
            try:
                how_to_use = product_data.get('tabs')
                for other_text in how_to_use:
                    if "How to Use" in other_text.get("title"):
                        how_to_use_text = other_text.get('content')
                        ss = Selector(text=how_to_use_text)
                        how_to_use_text = " ".join(ss.xpath("//p//text()|//li/text()").getall())
                        other_dict['how_to_use'] = remove_extra_space(how_to_use_text) if how_to_use_text else "N/A"
            except:
                other_dict['how_to_use'] = "N/A"

            # Todo: feature
            try:
                feature = product_data.get('tabs')
                for other_text in feature:
                    if "Features" in other_text.get("title"):
                        feature_text = other_text.get('content')
                        ss = Selector(text=feature_text)
                        feature_text = " ".join(ss.xpath("//p//text()|//li/text()").getall())
                        other_dict['feature'] = remove_extra_space(feature_text) if feature_text else "N/A"
            except:
                other_dict['feature'] = "N/A"

            # Todo: Nutritional Facts
            try:
                nutritional_facts_list = product_data.get('tabs')
                for nutritional_facts in nutritional_facts_list:
                    if "Nutritional Facts" in nutritional_facts.get("title"):
                        nutritional_facts_text = nutritional_facts.get('content')
                        ss = Selector(text=nutritional_facts_text)
                        nutritional_facts_text = " ".join(ss.xpath("//p//text()|//li/text()").getall())
                        other_dict['nutritional_facts'] = remove_extra_space(
                            nutritional_facts_text) if nutritional_facts_text else "N/A"
            except:
                other_dict['nutritional_facts'] = "N/A"

            item['other'] = other_dict
            return item

    else:
        logger.error("Product data not found")


if __name__ == '__main__':
    pincode = "110001"
    product_id = "1212518"
    place_id = get_place_id(pincode=pincode)
    encoded_id = get_lat_long(place_id)
    response = get_pdp_response(product_id=product_id, pincode=pincode, encoded_id=encoded_id)
    pdp_data = big_basket_pdp_page(response=response, old_product_id=product_id, pincode=pincode)
    print(json.dumps(pdp_data))
