import json
import re
import time
import json_repair
import requests
from bs4 import BeautifulSoup
from loguru import logger
from parsel import Selector
from datetime import datetime


def get_place_id(pincode):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://www.croma.com',
        'priority': 'u=1, i',
        'referer': 'https://www.croma.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }

    response = requests.get(
        f'https://api.croma.com/pwagoogle/v1/getgeocode/{pincode}?components=%27country:IN|postal_code:{pincode}%27',
        headers=headers,
    )
    return response


def get_star_review_count(product_id):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
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

    response = requests.get(f'https://api.croma.com/productdetails/allchannels/v1/reviewcount/{product_id}',
                            headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return json_data


def get_delivery_date(pincode, product_id):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'oms-apim-subscription-key': '1131858141634e2abe2efb2b3a2a2a5d',
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
                        'categoryType': 'mobile',
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
                        'categoryType': 'mobile',
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
                        'categoryType': 'mobile',
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

    if response.status_code == 200:
        json_data = response.json()

        j_data_list = ''
        try:
            j_data_list = json_data.get('promise').get('suggestedOption').get('option').get('promiseLines').get(
                'promiseLine')
        except Exception as e:
            logger.error(e)

        # Todo: get delivery date
        delivery_date = ''
        try:
            for data in j_data_list:
                assiment_list = data.get('assignments')
                if assiment_list:
                    for delivery_date in assiment_list.get('assignment'):
                        delivery_date = delivery_date.get('deliveryDate')
                        if delivery_date:
                            break
                if delivery_date:
                    break
            return delivery_date
        except Exception as e:
            logger.error(e)


def get_product_response(pincode, product_id, retries=5, delay=2):
    cookies = {
        'localStoragePincode': f'"{pincode}"',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }
    url = f'https://www.croma.com/%20/p/{product_id}'

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
            response.raise_for_status()  # raise error for bad status codes
            return response
        except requests.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)  # wait before retrying
            else:
                raise  # re-raise the last exception if all retries fail


def get_delivery_date_response(pincode, product_id):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'oms-apim-subscription-key': '1131858141634e2abe2efb2b3a2a2a5d',
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
                        'categoryType': 'mobile',
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
                        'categoryType': 'mobile',
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
                        'categoryType': 'mobile',
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

    if response.status_code == 200:
        json_data = response.json()

        j_data_list = ''
        try:
            j_data_list = json_data.get('promise').get('suggestedOption').get('option').get('promiseLines').get(
                'promiseLine')
        except Exception as e:
            logger.error(e)

        # Todo: get delivery date
        delivery_date = ''
        try:
            for data in j_data_list:
                assiment_list = data.get('assignments')
                if assiment_list:
                    for delivery_date in assiment_list.get('assignment'):
                        delivery_date = delivery_date.get('deliveryDate')
                        if delivery_date:
                            break
                if delivery_date:
                    break
            return delivery_date
        except Exception as e:
            logger.error(e)


def get_emi_options(price):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
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
        'fields': 'FULL',
        'amount': str(price),
    }

    response = requests.get('https://api.croma.com/product/allchannels/v1/emidata', params=params, headers=headers)
    json_data = response.json()
    if response.status_code == 200:
        bank_list = json_data.get('bankDetails')

        main_dict = dict()
        for bank_data in bank_list:
            # bank_details_list = []
            bank_lst = bank_data.get('bankList')
            if bank_lst:
                offer_list = list()
                bank_name = ''
                for bank_d in bank_lst:
                    item = dict()
                    bank_name = bank_d.get('name')
                    item['intrest'] = bank_d.get('annualIntRate')
                    item['total_cost'] = bank_d.get('totalPayment')
                    item['InterestAmount'] = bank_d.get('bankInterestAmount')
                    item['montly_emi_plan'] = bank_d.get('tenure')
                    offer_list.append(item)
                main_dict[bank_name] = offer_list
    return main_dict


# -----------------------------------------Product-Details-------------------------------------------------


def get_product_details(response, pincode, delivery_date, get_star_review_count):
    json_data = ''
    try:
        selector = Selector(text=response.text)
        json_data = selector.xpath("//script[contains(text(),'__INITIAL_DATA__')]/text()").get()
        json_data = json_data.split("__INITIAL_DATA__=")[-1]
    except Exception as e:
        logger.error(e)

    if not json_data or not json_data.strip():
        print("No JSON data found")
    else:
        try:
            json_data = json.loads(json_data)
        except:
            json_data = json_repair.loads(json_data)

    if json_data:
        item = dict()
        other_dict = dict()

        # Todo: product_id
        try:
            item['product_id'] = product_id
        except:
            item['product_id'] = "N/A"

        # Todo: seller_name
        try:
            seller_name = ""
            if seller_name:
                item['seller_name'] = seller_name
            else:
                item['seller_name'] = "N/A"
        except:
            item['seller_name'] = "N/A"

        # Todo: platform
        item['platform'] = "Chroma"

        # Todo: SKU
        item['sku'] = product_id

        # Todo: specifications
        specification_main_list = []
        try:
            specification_list = json_data.get('pdpReducer').get('pdpData').get('classifications')
            if specification_list:
                s_dict = dict()
                for data in specification_list:
                    features_dict = dict()
                    key_s = data.get('name')
                    for features_name in data.get('features'):
                        key = features_name.get('name')
                        value = features_name.get('featureValues')[0].get('value')
                        features_dict[key] = value
                    s_dict[key_s] = features_dict
                # print(json.dumps(s_dict))
                specification_main_list.append(s_dict)
        except Exception as e:
            logger.error(e)

        # Todo:brand
        try:
            for brand in specification_main_list:
                if "Brand" in brand.keys():
                    item["brand_name"] = brand.get('Brand')
                    break
        except Exception as e:
            logger.error(e)

        # Todo: link
        try:
            url = json_data.get('pdpReducer').get('pdpData').get('url')
            if url:
                item['link'] = "https://www.croma.com" + url
        except:
            logger.error(e)

        # Todo: Pincode
        try:
            item['pincode'] = pincode
        except Exception as e:
            logger.error(e)

        # Todo:Category-Path
        try:
            category_path_list = json_data.get("pdpReducer").get("pdpData").get("pdpBreadcrumbs")
            category_path_list = [breadcrumbs.get('name') for breadcrumbs in category_path_list if breadcrumbs]
            try:
                item['category_path'] = " > ".join(category_path_list[:3])
            except:
                item['category_path'] = " > ".join(category_path_list)
        except Exception as e:
            logger.error(e)

        # Todo:date_time_of_crawling
        try:
            date_time_of_crawling = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item['date_time_of_crawling'] = date_time_of_crawling
        except Exception as e:
            logger.error(e)

        # Todo: model_name_number
        try:
            for model_number in specification_main_list:
                if "Model Number" in model_number.keys():
                    item["model_name_number"] = model_number.get('Model Number')
                    break
        except Exception as e:
            print(e)

        # Todo: image_url
        image_url_list = []
        try:
            try:
                image_url_list = json_data.get('pdpReducer').get('pdpData').get('imageInfo')
            except:
                image_url_list = []
            if image_url_list:
                image_url_list = [image.get('url') for image in image_url_list if image]
                if image_url_list:
                    item['image_url'] = image_url_list[0]
        except:
            item['image_url'] = "N/A"

        # Todo: Name
        try:
            item['product_name'] = json_data.get('pdpReducer').get('pdpData').get('name')
        except:
            item['product_name'] = "N/A"

        # Todo:rating
        try:
            rating = json_data.get('pdpReducer').get('pdpData').get('averageRating')
            if rating:
                item['rating'] = rating
            else:
                item['rating'] = "N/A"
        except Exception as e:
            logger.error(e)

        # Todo:number_of_ratings
        try:
            number_of_ratings = json_data.get('pdpReducer').get('pdpData').get('numberOfRatings')
            if number_of_ratings:
                item['number_of_ratings'] = number_of_ratings
            else:
                item['number_of_ratings'] = "N/A"
        except Exception as e:
            logger.error(e)

        # Todo: star rating
        try:
            for key, value in star_review_count.items():
                key = f"{key}_star"
                item[key] = value
        except Exception as e:
            print(e)

        # Todo:coupon
        try:
            coupon = ""
            if coupon:
                item['coupon'] = coupon
            else:
                item['coupon'] = "N/A"
        except Exception as e:
            logger.error(e)

        # Todo:promotions
        try:
            promotions = ""
            if promotions:
                item['promotions'] = promotions
            else:
                item['promotions'] = "N/A"
        except Exception as e:
            logger.error(e)

        # Todo:bestseller
        try:
            bestseller = ""
            if bestseller:
                item['bestseller'] = bestseller
            else:
                item['bestseller'] = "N/A"
        except Exception as e:
            logger.error(e)

        # Todo:stock
        try:
            stock = ""
            if stock:
                item['stock'] = stock
            else:
                item['stock'] = "N/A"
        except Exception as e:
            logger.error(e)

        # Todo: delivery_date
        try:
            item['delivery_date'] = delivery_date
        except Exception as e:
            logger.error(e)

        # Todo: min_delivery_days
        try:
            item['min_delivery_days'] = delivery_date
        except Exception as e:
            logger.error(e)

        # Todo: max_delivery_days
        try:
            item['max_delivery_days'] = delivery_date
        except Exception as e:
            logger.error(e)

        # Todo: mrp
        mrp = ''
        try:
            mrp = json_data.get('pdpPriceReducer').get('pdpPriceData').get('mrp')
            mrp = mrp.get('value') if mrp else "N/A"
            item['mrp'] = float(mrp)
        except Exception as e:
            logger.error(e)

        # Todo: selleing price
        try:
            offer_price = json_data.get('pdpPriceReducer').get('pdpPriceData').get('sellingPrice')
            offer_price = offer_price.get('value') if offer_price else mrp
            item['offer_price'] = float(offer_price)
        except Exception as e:
            logger.error(e)

        # Todo:max_operating_price
        item['max_operating_price'] = item['mrp']

        # Todo: discount_percent
        try:
            discount_percent = json_data.get('pdpReducer').get('pdpData').get('discount')
            if discount_percent:
                item['discount_percent'] = float(discount_percent)
            else:
                item['discount_percent'] = "N/A"
        except:
            item['discount_percent'] = "N/A"

        # Todo: variation_info
        variation_info_list = []
        try:
            variation_info_lst = json_data.get('pdpReducer').get('pdpData').get('consolidatedVariantsInfo')
            if variation_info_lst:
                for data in variation_info_lst:
                    variation_info_list.append(data)
                other_dict['variation_info'] = variation_info_list
        except Exception as e:
            logger.error(e)

        # Todo: overview
        overview_dict = ''
        try:
            overview_html_text = json_data.get('pdpReducer').get('pdpData').get('description')
            if overview_html_text:
                soup = BeautifulSoup(overview_html_text, "html.parser")
                result = {}
                strong_tags = soup.find_all("strong")

                for strong in strong_tags:
                    key = strong.get_text(strip=True)
                    value_parts = []

                    for sib in strong.next_siblings:
                        if getattr(sib, "name", None) == "strong":
                            break
                        if sib.name == "br":  # skip <br> tags
                            continue
                        text = str(sib).strip()
                        if text:
                            value_text = BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
                            value_text = re.sub("\\s+", " ", value_text).strip()
                            value_parts.append(value_text)
                    result[key] = " ".join(value_parts).strip()
                    overview_dict = result
        except Exception as e:
            logger.error(e)

        # Todo: key features
        key_features = []
        try:
            key_features = json_data.get('pdpReducer').get('pdpData').get('quickviewdesc')
            selector = Selector(text=key_features)
            key_features = selector.xpath("//li/text()").getall()
            # other_dict['key_features'] = key_features
            # for data in key_features:
            #     key_feature_dict = dict()
            #     data_text = data.strip()
            #     if ":" in data_text:
            #         key, value = data_text.split(":", 1)
            #         key = re.sub("\\s+", " ", key).strip()
            #         value = re.sub("\\s+", " ", value).strip()
            #         key_feature_dict[key] = value
            #         key_feature_list.append(key_feature_dict)
            # print(key_feature_list)
        except Exception as e:
            logger.error(e)

        # Todo: emi_option
        emi_option = ''
        try:
            emi_option = get_emi_options(offer_price)
        except Exception as e:
            print(e)
        # Todo: other dict
        try:
            # Todo: image list
            if image_url_list:
                other_dict['images'] = image_url_list

            # Todo: specification_main_list
            if specification_main_list:
                other_dict['specification'] = specification_main_list

            # Todo:variation_info
            if variation_info_list:
                other_dict['variation_info'] = variation_info_list

            # Todo: overview_dict
            if other_dict:
                other_dict['overview'] = overview_dict

            # Todo: key features
            if other_dict:
                other_dict['key_features'] = key_features

            # Todo: emi_option
            if emi_option:
                other_dict['emi_option'] = emi_option
            item['other'] = other_dict
        except Exception as e:
            logger.error(e)
        return item


if __name__ == '__main__':
    pincode = "700017"
    product_id = "316053"
    # product_id = "314881"
    place_id = get_place_id(pincode)
    get_delivery_date = get_delivery_date_response(pincode, product_id)
    star_review_count = get_star_review_count(product_id)
    response = get_product_response(pincode, product_id)
    product_details = get_product_details(response, pincode, get_delivery_date, star_review_count)
    print(json.dumps(product_details))
