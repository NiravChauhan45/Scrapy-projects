import json
import re
import time
from datetime import datetime

import requests
from parsel import Selector


def get_delivery_date(product_id, pincode):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'oms-apim-subscription-key': '1131858141634e2abe2efb2b3a2a2a5d',
        'origin': 'https://www.croma.com',
        'priority': 'u=1, i',
        'referer': 'https://www.croma.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }
    json_data = {
        'promise': {
            'allocationRuleID': 'SYSTEM',
            'checkInventory': 'Y',
            'organizationCode': 'CROMA',
            'sourcingClassification': 'EC',
            'promiseLines': {
                'promiseLine': [
                    {
                        'fulfillmentType': 'HDEL',
                        'mch': '',
                        'itemID': product_id,
                        'lineId': '1',
                        'categoryType': 'nonMobile',
                        'reEndDate': '2500-01-01',
                        'reqStartDate': '',
                        'requiredQty': '1',
                        'shipToAddress': {
                            'company': '',
                            'country': '',
                            'city': '',
                            'mobilePhone': '',
                            'state': '',
                            'zipCode': pincode,
                            'extn': {
                                'irlAddressLine1': '',
                                'irlAddressLine2': '',
                            },
                        },
                        'extn': {
                            'widerStoreFlag': 'N',
                        },
                    },
                    {
                        'fulfillmentType': 'STOR',
                        'mch': '',
                        'itemID': product_id,
                        'lineId': '2',
                        'categoryType': 'nonMobile',
                        'reqEndDate': '',
                        'reqStartDate': '',
                        'requiredQty': '1',
                        'shipToAddress': {
                            'company': '',
                            'country': '',
                            'city': '',
                            'mobilePhone': '',
                            'state': '',
                            'zipCode': pincode,
                            'extn': {
                                'irlAddressLine1': '',
                                'irlAddressLine2': '',
                            },
                        },
                        'extn': {
                            'widerStoreFlag': 'N',
                        },
                    },
                    {
                        'fulfillmentType': 'SDEL',
                        'mch': '',
                        'itemID': product_id,
                        'lineId': '3',
                        'categoryType': 'nonMobile',
                        'reqEndDate': '',
                        'reqStartDate': '',
                        'requiredQty': '1',
                        'shipToAddress': {
                            'company': '',
                            'country': '',
                            'city': '',
                            'mobilePhone': '',
                            'state': '',
                            'zipCode': pincode,
                            'extn': {
                                'irlAddressLine1': '',
                                'irlAddressLine2': '',
                            },
                        },
                        'extn': {
                            'widerStoreFlag': 'N',
                        },
                    },
                ],
            },
        },
    }

    response = requests.post('https://api.croma.com/inventory/oms/v2/tms/details-pwa/', headers=headers, json=json_data)
    json_data = response.json()
    try:
        promise_line_list = json_data.get('promise').get('suggestedOption').get('option').get('promiseLines')
    except:
        pass

    delivery_date = ''
    try:
        for data in promise_line_list.get('promiseLine'):
            delivery_date_list = data.get('assignments')
            for data in delivery_date_list.get('assignment'):
                delivery_date = data.get('deliveryDate')
                if delivery_date:
                    break

            # Regex to extract yyyy-mm-dd
            match = re.search(r"\d{4}-\d{2}-\d{2}", delivery_date)
            if match:
                date_str = match.group()  # "2025-09-01"
                current_time = datetime.now().strftime("%H:%M:%S")
                # Combine properly
                datetime_str = f"{date_str} {current_time}"
                return datetime_str  # Example: 2025-09-01 14:49:10
    except Exception as e:
        print(e)


def get_response_pl(keyword, pincode, page_no, retries=5, backoff=2):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'httpsagent': '[object Object]',
        'origin': 'https://www.croma.com',
        'priority': 'u=1, i',
        'referer': 'https://www.croma.com/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }
    params = {
        'currentPage': page_no,
        'query': f"{keyword}:relevance",
        'fields': 'FULL',
        'channel': 'WEB',
        'channelCode': pincode,
        'spellOpt': 'DEFAULT',
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                'https://api.croma.com/searchservices/v1/search',
                params=params,
                headers=headers,
                timeout=10  # always good to have a timeout
            )

            # Return if successful
            if response.status_code == 200:
                return response

            print(f"Attempt {attempt}: Failed with status {response.status_code}")

        except requests.RequestException as e:
            print(f"Attempt {attempt}: Exception occurred - {e}")

        # Wait before retrying
        if attempt < retries:
            sleep_time = backoff ** attempt
            print(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)

    # Todo: If all attempts fail, return None
    return None


def chroma_pl_page(response, search_keyword):
    json_data = response.json()
    try:
        product_data_list = json_data.get("products")
    except:
        product_data_list = ""
    item_list = []
    if product_data_list:
        for index, product_data in enumerate(product_data_list, start=1):
            item = dict()

            # Todo: Product Id
            try:
                product_id = product_data.get("code") if product_data.get("code") else "N/A"
                item['product_id'] = product_id
            except:
                item['product_id'] = "N/A"

            # Todo: Product url
            try:
                product_url = f"https://www.croma.com{product_data.get('url')}" if product_data.get(
                    'url') else "N/A"
                item['product_url'] = product_url
            except:
                item['product_url'] = "N/A"

            # Todo:search keyword
            try:
                item['search_keyword'] = search_keyword
            except:
                item['search_keyword'] = "N/A"

            # Todo:onsite keyword
            try:
                item['onsite_keyword'] = json_data.get('freeTextSearch')
            except:
                item['onsite_keyword'] = "N/A"

            item['platform'] = "Big Basket"

            # Todo: sku
            try:
                item['sku'] = item['product_id']
            except:
                item['sku'] = "N/A"

            # Todo: Product Name
            try:
                product_name = product_data.get("name") if product_data.get("name") else "N/A"
                item['name'] = product_name
            except:
                item['name'] = "N/A"

            # Todo: Mrp
            try:
                mrp = product_data.get("mrp").get("value") if product_data.get("mrp").get("value") else "N/A"
                item['mrp'] = mrp
            except:
                item['mrp'] = "N/A"

            # Todo: Price
            try:
                price = product_data.get("price").get("value") if product_data.get("price").get("value") else item[
                    'mrp']
                item['price'] = price
            except:
                item['price'] = item['mrp']

            # Todo:Avg Rating
            try:
                avg_rating = round(product_data.get('averageRating'), 2) if product_data.get(
                    'averageRating') else "N/A"
                item['avg_rating'] = avg_rating
            except:
                item['avg_rating'] = "N/A"

            # Todo:total_rating
            try:
                total_rating = product_data.get('numberOfRatings') if product_data.get(
                    'numberOfRatings') else "N/A"
                item['total_rating'] = total_rating
            except:
                item['total_rating'] = "N/A"

            # Todo: Discount
            try:
                discount = product_data.get("discountValue") if product_data.get("discountValue") else "N/A"
                discount = discount.replace("%", "")
                item['discount'] = int(discount)
            except:
                item['discount'] = "N/A"

            # Todo: image url
            try:
                image_url = product_data.get('plpImage') if product_data.get('plpImage') else "N/A"
                item['image_url'] = image_url
            except:
                item['image_url'] = "N/A"

            # Todo: search_rank
            try:
                search_rank = index
                item['search_rank'] = search_rank
            except:
                item['search_rank'] = "N/A"

            # Todo: bought_past_month
            # try:
            #     bought_past_month = "N/A"
            #     item['bought_past_month'] = bought_past_month
            # except:
            #     item['bought_past_month'] = "N/A"

            # Todo: limited_time_deal
            # try:
            #     limited_time_deal = "N/A"
            #     item['limited_time_deal'] = limited_time_deal
            # except:
            #     item['limited_time_deal'] = "N/A"

            # Todo: pincode
            try:
                item['pincode'] = pincode
            except:
                pass

            # Todo:delivery date
            try:
                delivery_date = get_delivery_date(product_id, pincode)
                item['delivery_date'] = delivery_date
            except:
                item['delivery_date'] = 'N/A'

            # # Todo: free_delivery
            # try:
            #     free_delivery = "N/A"
            #     item['free_delivery'] = free_delivery if
            # except:
            #     item['free_delivery'] = "N/A"

            # Todo: fastest_delivery
            # try:
            #     fastest_delivery = "N/A"
            #     item['fastest_delivery'] = fastest_delivery
            # except:
            #     item['fastest_delivery'] = "N/A"

            # Todo: stock_left
            # try:
            #     stock_left = "N/A"
            #     item['stock_left'] = stock_left
            # except:
            #     item['stock_left'] = "N/A"

            # Todo: prime_product
            # try:
            #     prime_product = "N/A"
            #     item['prime_product'] = prime_product
            # except:
            #     item['prime_product'] = "N/A"

            # Todo: sponsored
            # try:
            #     sponsored = "N/A"
            #     item['sponsored'] = sponsored
            # except:
            #     item['sponsored'] = "N/A"

            # # Todo:numberOfReviews
            try:
                if product_data.get('numberOfReviews') == 0 or product_data.get('numberOfReviews') == "0":
                    item['numberOfReviews'] = "N/A"
                else:
                    item['numberOfReviews'] = product_data.get('numberOfReviews')
            except:
                item['numberOfReviews'] = "N/A"

            # Todo:manufacturer
            try:
                manufacturer = product_data.get('manufacturer')
                if manufacturer:
                    item['manufacturer'] = manufacturer
            except:
                pass

            # Todo: product detail
            try:
                product_detail = product_data.get('quickViewDesc') if product_data.get('quickViewDesc') else ""
                if product_detail:
                    product_detail_dict = dict()
                    selector = Selector(text=product_detail)
                    for data_text in selector.xpath("//li/text()").getall():
                        if ":" in data_text:
                            key, value = data_text.split(":")
                            if key:
                                key = re.sub("\\s+", " ", key).strip()

                            if value:
                                value = re.sub("\\s+", " ", value).strip()
                            product_detail_dict[key] = value
                    item['product_detail'] = product_detail_dict
            except:
                pass
            item_list.append(item)

        return item_list


if __name__ == '__main__':
    search_keyword = "ac"
    pincode = "110001"
    page_no = 0

    response = get_response_pl(keyword=search_keyword, pincode=pincode, page_no=page_no)
    pl_data = chroma_pl_page(response=response, search_keyword=search_keyword)
    print(json.dumps(pl_data))
