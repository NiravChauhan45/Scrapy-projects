import base64
import requests
import json
import time


def calculate_discount(price, mrp):
    discount = ((float(mrp) - float(price)) / float(mrp)) * 100
    return round(discount, 2)  # round to 2 decimal places


def get_place_id(pincode):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }
    params = {
        'inputText': pincode,
        'token': '9b1c36d7-a7a4-4aee-8c0d-a0ec74787fd0',
    }

    try:
        response = requests.get(
            "https://www.bigbasket.com/places/v1/places/autocomplete/",
            params=params,
            headers=headers,
        )
        response.raise_for_status()  # Raise error if bad HTTP status
        json_data = response.json()

        predictions_list = json_data.get("predictions", [])
        predictions_lst = []
        for predictions in predictions_list:
            if predictions:
                predictions = predictions.get("placeId")
                predictions_lst.append(predictions)
        return predictions_lst  # first match


    except requests.RequestException as e:
        print(f"HTTP Error: {e}")
        return None
    except ValueError:
        print("Error parsing JSON")
        return None


def get_lat_long(place_id):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    }
    params = {
        'placeId': place_id,
        'token': '9ff8eed2-e6bc-49bb-9747-8ad49b1897b2'
    }

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


def get_pl_response(keyword, page_number, pincode, encoded_id, retries=5, backoff=2):
    url = f"https://www.bigbasket.com/listing-svc/v2/products"
    params = {
        'type': 'ps',
        'slug': keyword,
        'page': page_number,
    }

    cookies = {
        '_bb_locSrc': 'default',
        'x-channel': 'web',
        '_bb_nhid': '7427',
        '_bb_dsid': '7427',
        '_bb_dsevid': '7427',
        'isintegratedsa': 'true',
        '_bb_vid': 'ODc0NzA0MTY3MzI4NzE1NzU4',
        'jentrycontextid': '10',
        'xentrycontextid': '10',
        '_bb_lat_long': encoded_id,
        '_bb_pin_code': pincode,
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'common-client-static-version': '101',
        'content-type': 'application/json',
        'osmos-enabled': 'true',
        'referer': f'https://www.bigbasket.com/ps/?q={keyword}&nc=as',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'x-channel': 'BB-WEB',
        'x-entry-context': 'bbnow',
        'x-entry-context-id': '10',
        'x-integrated-fc-door-visible': 'false',
        'x-tracker': '9f95121f-29cf-4586-b625-2474eda94fb4',
    }
    # Todo: retry
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=10)
            response.raise_for_status()  # raise error for non-200 responses
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


def big_basket_pl_page(response):
    json_data = response.json()
    item_list = []
    try:
        if json_data.get("tabs"):
            try:
                tabs = json_data.get("tabs")[0]
            except:
                tabs = ''
        else:
            print("Tabs Not Found..")

        if tabs:
            if tabs.get("product_info"):
                product_info = tabs.get('product_info')
                if product_info.get("products"):
                    products_data_list = product_info.get("products")
                    for products_data in products_data_list:
                        item = dict()
                        if products_data:
                            # Todo: Product_ID
                            try:
                                item['ID'] = products_data.get("id") if products_data.get("id") else "N/A"
                            except:
                                item['ID'] = "N/A"

                            # Todo: product Name
                            try:
                                item['product_name'] = products_data.get("desc") if products_data.get("desc") else "N/A"
                            except:
                                item['product_name'] = "N/A"

                            # Todo: Product_url
                            try:
                                item['product_url'] = "https://www.bigbasket.com" + products_data.get(
                                    "absolute_url") if products_data.get("absolute_url") else "N/A"
                            except:
                                item['product_url'] = "N/A"

                            # Todo: mrp
                            try:
                                mrp = products_data.get('pricing').get('discount').get('mrp')
                                item['mrp'] = float(mrp) if mrp else "N/A"
                            except:
                                item['mrp'] = 'N/A'

                            # Todo: price
                            try:
                                price = products_data.get('pricing').get('discount').get('prim_price').get('sp')
                                item['price'] = float(price) if price else item['mrp']
                            except:
                                item['price'] = item['mrp']

                            # Todo: discount
                            try:
                                discount = products_data.get('pricing').get('discount').get('d_text')
                                if "%" in discount:
                                    discount = discount.replace("%", "").replace("OFF", "").strip()
                                    item['discount'] = float(discount) if discount else "N/A"
                                else:
                                    if item['mrp'] != "N/A" and item['mrp']:
                                        discount_percent = calculate_discount(item['price'], item['mrp'])
                                        item['discount'] = discount_percent
                            except:
                                item['discount'] = "N/A"

                            # Todo: Images
                            try:
                                image_list = []
                                for image in products_data.get('images'):
                                    image = image.get("l")
                                    image_list.append(image)
                                item['images'] = image_list
                            except:
                                item['images'] = "N/A"

                            # Todo: image
                            try:
                                item['image'] = item['images'][0]
                            except:
                                item['image'] = "N/A"

                            # Todo: sku_max_quantity
                            try:
                                item['sku_max_quantity'] = products_data.get("sku_max_quantity") if products_data.get(
                                    "sku_max_quantity") else "N/A"
                            except:
                                item['sku_max_quantity'] = "N/A"

                            # Todo: Product weight
                            try:
                                item['weight'] = products_data.get("w") if products_data.get("w") else "N/A"
                            except:
                                item['weight'] = "N/A"
                            # Todo: cart_count
                            try:
                                item['cart_count'] = products_data.get('cart_count') if products_data.get(
                                    'cart_count') else "N/A"
                            except:
                                item['cart_count'] = "N/A"

                            # Todo:availability
                            try:
                                if products_data.get('availability').get('avail_status'):
                                    if products_data.get('availability').get('avail_status') == "001":
                                        item['availability'] = True
                                    else:
                                        item['availability'] = False
                            except:
                                item['availability'] = False

                            # Todo: brand
                            try:
                                brand = products_data.get('brand').get('name')
                                item['brand'] = brand if brand else "N/A"
                            except:
                                item['brand'] = "N/A"

                            # Todo: category_hierarchy
                            try:
                                category_hierarchy_lst = []
                                category_hierarchy_lst.append("Home")
                                category_hierarchy_list = products_data.get('category')
                                for key, value in category_hierarchy_list.items():
                                    if 'name' in key and "home" not in value.lower():
                                        category_hierarchy_lst.append(value)
                                item['category_hierarchy'] = " > ".join(
                                    category_hierarchy_lst) if category_hierarchy_lst else "N/A"
                            except:
                                item['category_hierarchy'] = "N/A"

                            # Todo: avg_rating
                            try:
                                avg_rating = products_data.get('rating_info').get('avg_rating')
                                item['avg_rating'] = float(avg_rating) if avg_rating else "N/A"
                            except:
                                item['avg_rating'] = "N/A"

                            # Todo: rating
                            try:
                                number_of_rating = products_data.get('rating_info').get('rating_count')
                                item['number_of_rating'] = number_of_rating if number_of_rating else "N/A"
                            except:
                                item['number_of_rating'] = "N/A"

                            try:
                                number_of_review = products_data.get('rating_info').get('review_count')
                                item['number_of_review'] = number_of_review if number_of_review else "N/A"
                            except:
                                item['number_of_review'] = "N/A"

                            item_list.append(item)
                        else:
                            print("Product data not found..")
                    return item_list
                    # print(json.dumps(item_list))
                else:
                    print("products Not Found..")
            else:
                print("Product_info Not Found..")
        else:
            print("Tabs not found..")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    keyword = "wafer"
    page_no = 1
    pincode = "110001"
    place_id_list = get_place_id(pincode=pincode)
    for place_id in place_id_list:
        encoded_id = get_lat_long(place_id)
        if encoded_id:
            response = get_pl_response(keyword=keyword, page_number=page_no, pincode=pincode, encoded_id=encoded_id)
            if response.status_code == 200:
                pl_data = big_basket_pl_page(response=response)
                print(json.dumps(pl_data))
                break
            else:
                print("response can not get properly")
