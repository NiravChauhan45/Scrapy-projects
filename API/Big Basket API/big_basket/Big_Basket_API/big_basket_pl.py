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
        'referer': 'https://www.bigbasket.com/ps/?q=drink&nc=as',
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


def get_pl_response_1(keyword, page_number, pincode, encoded_id, retries=5, backoff=2):
    cookies = {
        '_bb_locSrc': 'default',
        'x-channel': 'web',
        '_bb_vid': 'ODc1ODEwOTU4NTIyMDkwMjIy',
        '_bb_nhid': '7427',
        '_bb_dsid': '7427',
        '_bb_dsevid': '7427',
        '_bb_bhid': '',
        '_bb_loid': '',
        'csrftoken': '0HNDSDuE30ju1c7Lw0rZSGitrI8EzY2ccDZcozGH9VHrr7L1MtHHlAlBXzv6Q83l',
        '_bb_bb2.0': '1',
        '_is_bb1.0_supported': '0',
        'bb2_enabled': 'true',
        'bm_ss': 'ab8e18ef4e',
        'ufi': '1',
        'csurftoken': 'X0C1Xw.ODc1ODEwOTU4NTIyMDkwMjIy.1756269604192.0ojgnsIOQzUqWAdVhWTLkDz70b5pcEZkzDm86o9/rlc=',
        'adb': '0',
        '_gcl_au': '1.1.221030583.1756269607',
        'jarvis-id': '7bd7dce4-7216-43cc-84e8-95a687d20601',
        'bigbasket.com': '06207061-9b56-48ed-8aca-d28a4747b8b6',
        '_gid': 'GA1.2.593051270.1756269608',
        '_fbp': 'fb.1.1756269607983.538986682753390781',
        'is_global': '0',
        '_is_tobacco_enabled': '1',
        '_bb_lat_long': encoded_id,
        '_bb_cid': '18',
        '_bb_aid': '"Mjk4MDU5Mjk0Ng=="',
        'xentrycontext': 'bb-b2c',
        'xentrycontextid': '100',
        'jentrycontextid': '100',
        'isintegratedsa': 'false',
        '_bb_addressinfo': 'MjguNjMyNzQyNnw3Ny4yMTk1OTY5fENvbm5hdWdodCBQbGFjZXwxMTAwMDF8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==',
        '_bb_pin_code': pincode,
        '_bb_sa_ids': '10260',
        '_bb_cda_sa_info': 'djIuY2RhX3NhLjEwMC4xMDI2MA==',
        'is_integrated_sa': '0',
        'bm_s': 'YAAQFYR7XPr1LdSYAQAAwoPV6QP+oUv+zfTvxAYz8pmtZNcnh6bGvYn2n3saLayFSzOxQh3yfMyzW9D1x/QTQUyN+Q43mfphwvojMOMbp0X13z8UvhJc/eFlHvVhhYZvGO2df5Hk31ZWyOYcBDUaxXB7p+97XFmh0c51F9ETePvJ4Y0Te5m0SCp5+EIW3yorEg9xL1cee3nEr8Z/3LFmoFJxXBkHRBiREBprJM6trmnPH6fRo6tG0ITYcyxQhYUEMKofbJSDofEm8ksS21nQw9ZK+9psaQQ52lXFv0aILt2ZUvvdVHbtVKhWKELrGYH38kDO9HSteOR3yID94FnL1XyCV9JYK4RbAGc4bARyh25OZQYBoaSnuWj4dv2d42Fzou0HfvXbVpBhyhw/S4uQpqn36E9Vi8VTBIy5i/gPTf2lPxeUzOryvhUu68T+XbBk/5/g6vSk88QfayiUVlNmydQ+Q9H2k4HmKgA+0LI84v7Un2aef83fQubg9t7D62D7nxzTib5DhnyMJ64/YyiuZGQxRYM02/M0X++JW4E6xJwJTIFOdvy0SThUhFyAQGFfcSNMbtM0Bdg=',
        'bm_so': 'D7B57A58B736F8D961848CA18696416CD66DBA94612E8240ABCBE31F1CC45564~YAAQFYR7XPv1LdSYAQAAwoPV6QT6dMoQ5qvAt3/RTJfTkJvffB+bquialnKdCh5tGLgHmoMzTEObvkAbhpsEN32vx/5YnS0Jk6vNk1xqiL3RJTBJD0bwR9//nnWkbj0sNGimY2a5SJXwYtJ3IZ265QQSJbjTetS5lteN8ZjBtvG4EAxcZRR1ZUgRemZAdTZCu5vnQ9V1hqgaDcJ7Syp0XWRwJ4Ra97w49VCJ/Sd05oHayPTKgOfnveniPtcrywYE0VjGn1gK716dOcD+EJnX5pFB0YhWJMcn9Mw+xitclMT74PiQFcir0EaQwziJhXf+XnXY7oGWO7N8seIbxv1oNldv+7p/vESV0n0OWeDBQz2nyUumC+MpI5w1bLnGlQcknwZhxCoOTdjU+ecBoH9XA7sRUpLYTV5/B1cCWupt4XIYsLi6iaBcfdOksOSc6a2HUrT/3CtU1gUqkE7UtHdF2ew=',
        'ts': '2025-08-27%2010:12:22.058',
        '_ga_FRRYG5VKHX': 'GS2.1.s1756269607$o1$g1$t1756269743$j40$l0$h0',
        '_ga': 'GA1.2.1773956655.1756269607',
        'bm_lso': 'D7B57A58B736F8D961848CA18696416CD66DBA94612E8240ABCBE31F1CC45564~YAAQFYR7XPv1LdSYAQAAwoPV6QT6dMoQ5qvAt3/RTJfTkJvffB+bquialnKdCh5tGLgHmoMzTEObvkAbhpsEN32vx/5YnS0Jk6vNk1xqiL3RJTBJD0bwR9//nnWkbj0sNGimY2a5SJXwYtJ3IZ265QQSJbjTetS5lteN8ZjBtvG4EAxcZRR1ZUgRemZAdTZCu5vnQ9V1hqgaDcJ7Syp0XWRwJ4Ra97w49VCJ/Sd05oHayPTKgOfnveniPtcrywYE0VjGn1gK716dOcD+EJnX5pFB0YhWJMcn9Mw+xitclMT74PiQFcir0EaQwziJhXf+XnXY7oGWO7N8seIbxv1oNldv+7p/vESV0n0OWeDBQz2nyUumC+MpI5w1bLnGlQcknwZhxCoOTdjU+ecBoH9XA7sRUpLYTV5/B1cCWupt4XIYsLi6iaBcfdOksOSc6a2HUrT/3CtU1gUqkE7UtHdF2ew=^1756269747433',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'common-client-static-version': '101',
        'content-type': 'application/json',
        'osmos-enabled': 'true',
        'priority': 'u=1, i',
        'referer': 'https://www.bigbasket.com/ps/?q=wafer&nc=as',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'x-channel': 'BB-WEB',
        'x-entry-context': 'bb-b2c',
        'x-entry-context-id': '100',
        'x-integrated-fc-door-visible': 'true',
        'x-tracker': 'd7ac2f90-70c6-4269-9c27-388d0bcfc062',
        # 'cookie': '_bb_locSrc=default; x-channel=web; _bb_vid=ODc1ODEwOTU4NTIyMDkwMjIy; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=0HNDSDuE30ju1c7Lw0rZSGitrI8EzY2ccDZcozGH9VHrr7L1MtHHlAlBXzv6Q83l; _bb_bb2.0=1; _is_bb1.0_supported=0; bb2_enabled=true; bm_ss=ab8e18ef4e; ufi=1; csurftoken=X0C1Xw.ODc1ODEwOTU4NTIyMDkwMjIy.1756269604192.0ojgnsIOQzUqWAdVhWTLkDz70b5pcEZkzDm86o9/rlc=; adb=0; _gcl_au=1.1.221030583.1756269607; jarvis-id=7bd7dce4-7216-43cc-84e8-95a687d20601; bigbasket.com=06207061-9b56-48ed-8aca-d28a4747b8b6; _gid=GA1.2.593051270.1756269608; _fbp=fb.1.1756269607983.538986682753390781; is_global=0; _is_tobacco_enabled=1; _bb_lat_long=MjguNjMyNzQyNnw3Ny4yMTk1OTY5; _bb_cid=18; _bb_aid="Mjk4MDU5Mjk0Ng=="; xentrycontext=bb-b2c; xentrycontextid=100; jentrycontextid=100; isintegratedsa=false; _bb_addressinfo=MjguNjMyNzQyNnw3Ny4yMTk1OTY5fENvbm5hdWdodCBQbGFjZXwxMTAwMDF8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=110001; _bb_sa_ids=10260; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xMDI2MA==; is_integrated_sa=0; bm_s=YAAQFYR7XPr1LdSYAQAAwoPV6QP+oUv+zfTvxAYz8pmtZNcnh6bGvYn2n3saLayFSzOxQh3yfMyzW9D1x/QTQUyN+Q43mfphwvojMOMbp0X13z8UvhJc/eFlHvVhhYZvGO2df5Hk31ZWyOYcBDUaxXB7p+97XFmh0c51F9ETePvJ4Y0Te5m0SCp5+EIW3yorEg9xL1cee3nEr8Z/3LFmoFJxXBkHRBiREBprJM6trmnPH6fRo6tG0ITYcyxQhYUEMKofbJSDofEm8ksS21nQw9ZK+9psaQQ52lXFv0aILt2ZUvvdVHbtVKhWKELrGYH38kDO9HSteOR3yID94FnL1XyCV9JYK4RbAGc4bARyh25OZQYBoaSnuWj4dv2d42Fzou0HfvXbVpBhyhw/S4uQpqn36E9Vi8VTBIy5i/gPTf2lPxeUzOryvhUu68T+XbBk/5/g6vSk88QfayiUVlNmydQ+Q9H2k4HmKgA+0LI84v7Un2aef83fQubg9t7D62D7nxzTib5DhnyMJ64/YyiuZGQxRYM02/M0X++JW4E6xJwJTIFOdvy0SThUhFyAQGFfcSNMbtM0Bdg=; bm_so=D7B57A58B736F8D961848CA18696416CD66DBA94612E8240ABCBE31F1CC45564~YAAQFYR7XPv1LdSYAQAAwoPV6QT6dMoQ5qvAt3/RTJfTkJvffB+bquialnKdCh5tGLgHmoMzTEObvkAbhpsEN32vx/5YnS0Jk6vNk1xqiL3RJTBJD0bwR9//nnWkbj0sNGimY2a5SJXwYtJ3IZ265QQSJbjTetS5lteN8ZjBtvG4EAxcZRR1ZUgRemZAdTZCu5vnQ9V1hqgaDcJ7Syp0XWRwJ4Ra97w49VCJ/Sd05oHayPTKgOfnveniPtcrywYE0VjGn1gK716dOcD+EJnX5pFB0YhWJMcn9Mw+xitclMT74PiQFcir0EaQwziJhXf+XnXY7oGWO7N8seIbxv1oNldv+7p/vESV0n0OWeDBQz2nyUumC+MpI5w1bLnGlQcknwZhxCoOTdjU+ecBoH9XA7sRUpLYTV5/B1cCWupt4XIYsLi6iaBcfdOksOSc6a2HUrT/3CtU1gUqkE7UtHdF2ew=; ts=2025-08-27%2010:12:22.058; _ga_FRRYG5VKHX=GS2.1.s1756269607$o1$g1$t1756269743$j40$l0$h0; _ga=GA1.2.1773956655.1756269607; bm_lso=D7B57A58B736F8D961848CA18696416CD66DBA94612E8240ABCBE31F1CC45564~YAAQFYR7XPv1LdSYAQAAwoPV6QT6dMoQ5qvAt3/RTJfTkJvffB+bquialnKdCh5tGLgHmoMzTEObvkAbhpsEN32vx/5YnS0Jk6vNk1xqiL3RJTBJD0bwR9//nnWkbj0sNGimY2a5SJXwYtJ3IZ265QQSJbjTetS5lteN8ZjBtvG4EAxcZRR1ZUgRemZAdTZCu5vnQ9V1hqgaDcJ7Syp0XWRwJ4Ra97w49VCJ/Sd05oHayPTKgOfnveniPtcrywYE0VjGn1gK716dOcD+EJnX5pFB0YhWJMcn9Mw+xitclMT74PiQFcir0EaQwziJhXf+XnXY7oGWO7N8seIbxv1oNldv+7p/vESV0n0OWeDBQz2nyUumC+MpI5w1bLnGlQcknwZhxCoOTdjU+ecBoH9XA7sRUpLYTV5/B1cCWupt4XIYsLi6iaBcfdOksOSc6a2HUrT/3CtU1gUqkE7UtHdF2ew=^1756269747433',
    }

    params = {
        'type': 'ps',
        'slug': keyword,
        'page': page_number,
        'bucket_id': '92',
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(
                'https://www.bigbasket.com/listing-svc/v2/products',
                params=params,
                cookies=cookies,
                headers=headers,
                timeout=10  # avoid hanging forever
            )

            # If status is OK (200), return the response
            if response.status_code == 200:
                return response
            else:
                print(f"Attempt {attempt}: Status {response.status_code}")

        except requests.RequestException as e:
            print(f"Attempt {attempt}: Error {e}")

        # If not last attempt, wait before retrying
        if attempt < retries:
            sleep_time = backoff * (2 ** (attempt - 1))  # exponential backoff
            print(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)

        # If all retries fail, return None
    return None


def big_basket_pl_page(response, search_keyword):
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
                    onsite_keyword = tabs.get('search_info').get('query_term')

                    for index, products_data in enumerate(products_data_list, start=1):
                        item = dict()
                        if products_data:
                            # Todo: Product_ID
                            try:
                                item['product_id'] = products_data.get("id") if products_data.get("id") else "N/A"
                            except:
                                item['product_id'] = "N/A"

                            # Todo: Product_url
                            try:
                                item['product_url'] = "https://www.bigbasket.com" + products_data.get(
                                    "absolute_url") if products_data.get("absolute_url") else "N/A"
                            except:
                                item['product_url'] = "N/A"

                            # Todo: search_keyword
                            try:
                                item['search_keyword'] = search_keyword
                            except:
                                item['search_keyword'] = "N/A"

                            # Todo: onsite_keyword
                            try:
                                item['onsite_keyword'] = onsite_keyword
                            except:
                                item['onsite_keyword'] = "N/A"

                            # Todo: platform
                            item['platform'] = "Big Basket"

                            # Todo: SKU
                            try:
                                item['SKU'] = products_data.get("id") if products_data.get("id") else "N/A"
                            except:
                                item['SKU'] = "N/A"

                            # Todo: product Name
                            try:
                                item['product_name'] = products_data.get("desc") if products_data.get("desc") else "N/A"
                            except:
                                item['product_name'] = "N/A"

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

                            # Todo: avg_rating
                            try:
                                avg_rating = products_data.get('rating_info').get('avg_rating')
                                item['avg_rating'] = float(avg_rating) if avg_rating else "N/A"
                            except:
                                item['avg_rating'] = "N/A"

                            # Todo: total_rating
                            try:
                                total_rating = products_data.get('rating_info').get('rating_count')
                                item['total_rating'] = total_rating if total_rating else "N/A"
                            except:
                                item['total_rating'] = "N/A"

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
                                # item['images'] = image_list
                                image_lst = image_list
                            except:
                                item['images'] = "N/A"

                            # Todo: image
                            try:
                                # item['image'] = item['images'][0]
                                item['image'] = image_lst[0]
                            except:
                                item['image'] = "N/A"

                            # Todo: search_rank
                            try:
                                item['search_rank'] = index
                            except:
                                item['search_rank'] = "N/A"

                            # # Todo: bought_past_month
                            # try:
                            #     item['bought_past_month'] = "N/A"
                            # except:
                            #     item['bought_past_month'] = "N/A"

                            # # Todo: limited_time_deal
                            # try:
                            #     item['limited_time_deal'] = "N/A"
                            # except:
                            #     item['limited_time_deal'] = "N/A"

                            # # Todo: free_delivery
                            # try:
                            #     item['free_delivery'] = "N/A"
                            # except:
                            #     item['free_delivery'] = "N/A"

                            # # Todo: fastest_delivery
                            # try:
                            #     item['fastest_delivery'] = "N/A"
                            # except:
                            #     item['fastest_delivery'] = "N/A"

                            # # Todo: stock_left
                            # try:
                            #     item['stock_left'] = "N/A"
                            # except:
                            #     item['stock_left'] = "N/A"

                            # # Todo: prime_product
                            # try:
                            #     item['prime_product'] = "N/A"
                            # except:
                            #     item['prime_product'] = "N/A"

                            # # Todo: sponsored
                            # try:
                            #     item['sponsored'] = "N/A"
                            # except:
                            #     item['sponsored'] = "N/A"

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
    keyword = "lays"
    page_no = 1
    pincode = "560001"
    place_id_list = get_place_id(pincode=pincode)
    for place_id in place_id_list:
        encoded_id = get_lat_long(place_id)
        if encoded_id:
            response = get_pl_response(keyword=keyword, page_number=page_no, pincode=pincode, encoded_id=encoded_id)
            if response.status_code == 200:
                pl_data = big_basket_pl_page(response=response, search_keyword=keyword)
                print(json.dumps(pl_data))
                break
            else:
                response = get_pl_response_1(keyword=keyword, page_number=page_no, pincode=pincode,
                                             encoded_id=encoded_id)
                if response.status_code == 200:
                    pl_data = big_basket_pl_page(response=response, search_keyword=keyword)
                    print(json.dumps(pl_data))
                    break
