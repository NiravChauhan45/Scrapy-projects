import re
import json
import datetime
from html import unescape
from parsel import Selector


def get_data_pl(response):
    list_of_links = list()
    selector = Selector(response)
    data_load = json.loads(
        selector.xpath('//script[contains(text(), "window.__myx = {")]//text()').get("").replace("window.__myx =",
                                                                                                 "").strip())

    for data in data_load['searchData']['results']['products']:
        list_of_links.append("https://www.myntra.com/" + data['landingPageUrl'])

    return list_of_links

# def get_data_pl(response):
#     list_of_links = list()
#     selector = Selector(text=response)
#     json_data = selector.xpath("//script[contains(text(),'searchData')]/text()").get()
#     if json_data:
#         json_data = json_data.replace("window.__myx =", "").strip()
#         json_data = json.loads(json_data)
#     else:
#         json_data = json.loads(response)
#     results = json_data.get('searchData').get('results').get('products')
#     if not results:
#         results = results.get('products')
#
#     if results:
#         for index, result in enumerate(results):
#             # Todo: Break Loop If Index Count: 25
#             if index >= 25:
#                 break
#             index += 1
#             product_url = result.get('landingPageUrl')
#             if product_url:
#                 product_url = f"https://www.myntra.com/{product_url}"
#             list_of_links.append(product_url)
#
#         return list_of_links


def get_data_pdp(response,product_url):
    selector = Selector(text=response)

    # Extracting the product data embedded in a script tag
    data = selector.xpath(
        "//script[contains(text(), 'window.__myx') and contains(text(), 'pdpData') and contains(text(), 'discountedPrice')]/text()"
    ).get()

    if not data:
        return {
            "HTTP Status Code": 404,
            "Error Code": "NOT_FOUND",
            "Description": f"The requested product {product_url} or resource could not be found",
            "Error Message": "The requested resource was not found."
        }

    # Clean and parse the extracted data
    try:
        data = data.split('window.__myx = ')[1].strip()
        if data.endswith(';'):
            data = data[:-1]
    except:
        data = data.split('window.__myx = ')[0].strip()
        if data.endswith(';'):
            data = data[:-1]

    try:
        parsed_data = json.loads(data)  # Convert string to Python dict
    except json.JSONDecodeError as e:
        return {"statusCode": 500, "status": "error", "message": f"Failed to parse JSON data: {e}"}

    pdp_data = parsed_data.get('pdpData', {})
    product_id = pdp_data.get('id', "N/A")

    # Initializing the result dictionary
    result = {
        # 'date_given': datetime.now().strftime("%Y-%m-%d"),
        'product_name': pdp_data.get('name', "N/A").strip(),
        'product_id': product_id,  # Placeholder, adjust as needed
        # 'scrap_date_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'scrap_date_and_time': str(datetime.datetime.now()).replace(" ", "T")[:-3] + "Z",
        'image_urls': [],
        'brand': pdp_data.get('brand', "NA").get('name'),
        'product_details': {},
        'product_specifications': "N/A",
        'seller_info': "N/A",
        'product_url': product_url,
        'mrp': "",
        "available_sizes": "",
        'selling_price': pdp_data.get('price', {}).get('discounted', "N/A"),
        'discount': "N/A",
        'color_list': [],
        'in_stock_out_of_stock_status': "",
        'colour': "N/A",
        'size_list': "N/A",
        'size_chart': "N/A",
        'product_rating': round(pdp_data.get('ratings', {}).get('averageRating', 0), 1),
        'total_rating_count': pdp_data.get('ratings', {}).get('totalCount', 0),
        'individual_ratings_count': "N/A",
        'category': "N/A",
    }

    try:
        result['variant'] = [variant['displayText'] for variant in pdp_data.get('relatedStyles')]
    except:
        pass

    # TODO : discount: need to set when no price
    try:
        result['discount'] = pdp_data.get('discounts', [{}])[0].get('discountPercent', "N/A")
    except:
        result['discount'] = "N/A"
    try:
        # Initialize the 'image_links': [], list in the result dictionary
        result['image_urls'] = []

        # Loop through the albums in the 'media' key
        for album in pdp_data.get('media', {}).get('albums', []):
            for image in album.get('images', []):
                result['image_urls'].append(image.get('imageURL', "NA").strip())

    except Exception as e:
        result['image_urls'] = "N/A"
        print(f"Error: {e}")

    desc_text = {}

    for item in pdp_data.get('productDetails', []):
        title = item.get('title', 'Unknown Title')
        description = item.get('description', '')

        if "<b>" in description:
            html_text = unescape(description)

            # ✅ Handle free text before first <b>
            first_b_match = re.search(r"<b>", html_text)
            if first_b_match:
                initial_text = html_text[:first_b_match.start()].strip()
                initial_text = re.sub(r'<br\s*/?>', '\n', initial_text, flags=re.IGNORECASE)
                initial_text = re.sub(r'<[^>]+>', '', initial_text).strip()
                if initial_text:
                    if title == 'Product Details':
                        desc_text['text'] = initial_text
                    else:
                        desc_text[title.lower().replace(" ", "_")] = initial_text

            # ✅ Now handle all <b>...</b> blocks
            matches = list(re.finditer(r"<b>(.*?)</b>(.*?)(?=<b>|$)", html_text, re.DOTALL))
            for match in matches:
                key = match.group(1).strip().lower().replace(" ", "_")
                content = match.group(2).strip()

                if '<ul>' in content:
                    items = re.findall(r"<li>(.*?)</li>", content)
                    desc_text[key] = [item.strip() for item in items]
                else:
                    text = re.sub(r'<[^>]+>', '', content).strip()
                    desc_text[key] = text

        else:
            clean_description = re.sub(r'<br\s*/?>', '\n', description, flags=re.IGNORECASE)
            # Clean the description (remove unwanted escape characters and format text)
            clean_description = re.sub(r'\\\"', '', clean_description)  # Remove escaped quotes

            # Ensure there is a space before "Machine Wash"

            # If the title is 'product_details', change it to 'text'
            if title == 'Product Details':
                title = 'text'

            # For the 'SIZE & FIT', format it more clearly
            if title == 'SIZE & FIT':
                clean_description = re.sub(r'(\d+)"', r'\1 inches', clean_description)  # Convert height in inches
                clean_description = clean_description.replace('MChest', 'Chest').replace('Height',
                                                                                         'Height:')  # Readable formatting
            clean_description = re.sub("<.*?>", "", clean_description).replace('&nbsp;', ' ')
            title = title.lower().replace(" ", "_")
            desc_text[title] = [part.strip() for part in clean_description.split('\n') if part.strip()]

    try:
        result['product_details'] = desc_text
    except Exception as e:
        print(f"Error in Description json dumps :: {e}")
        result['product_details'] = "N/A"

    # Extracting product specifications
    try:
        def strip_html(text):
            return re.sub(r'<[^>]+>', '', text).strip()

        specification = pdp_data.get('articleAttributes', {})
        result['product_specifications'] = {
            key.lower().replace("-", "_").replace(" ", "_"): strip_html(value)
            for key, value in specification.items()
            if value.strip() not in ['N/A', '']
        }
    except:
        pass

    try:
        def lower_keys(obj):
            if isinstance(obj, dict):
                return {k.lower(): lower_keys(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [lower_keys(item) for item in obj]
            else:
                return obj

        sellers = pdp_data.get('sellers', [])

        if isinstance(sellers, list):
            if len(sellers) >= 1:
                sellers = sellers[0]

        result['seller_info'] = lower_keys(sellers)
    except KeyError as e:
        print(f"KeyError: Missing expected key seller info - {e}")
        result['seller_info'] = "N/A"
    except Exception as e:
        print(f"An unexpected error occurred seller info: {e}")
        result['seller_info'] = "N/A"

    try:
        # Extract only the 'label' (size) for each entry
        size_labels = [size.get("label") for size in pdp_data.get('sizes', [])]
        result['size_list'] = size_labels
    except KeyError as e:
        print(f"KeyError: Missing expected key - {e}")
        result['size_list'] = "N/A"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result['size_list'] = "N/A"

    try:
        Tag = []
        for available_sizes in pdp_data.get('sizes'):
            size_seller_data = available_sizes.get('sizeSellerData', [])

            if size_seller_data:
                left_item_count = size_seller_data[0].get('availableCount', 0)

                left_size = available_sizes.get('label', 'Unknown Size')

                if left_item_count:  # "tagText": "Only Few Left!","skuThreshold": 5,
                    Tag.append(f"{left_size}")
        if Tag:
            result['available_sizes'] = Tag
        else:
            result['available_sizes'] = "N/A"
    except:
        result['available_sizes'] = "N/A"

    try:
        # Extract only the 'label' (size) for each entry
        colors = pdp_data.get('baseColour', "N/A")

        result['colour'] = colors
    except KeyError as e:
        print(f"KeyError: Missing expected key - {e}")
        result['colour'] = "N/A"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result['colour'] = "N/A"

    result['mrp'] = pdp_data.get('mrp', "N/A")

    try:
        out_of_stock = pdp_data.get('flags', {}).get('outOfStock', None)

        if out_of_stock is False:
            instock_status = True  # Item is in stock
        else:
            instock_status = False  # Out of stock or unknown status

    except Exception as e:
        instock_status = False  # Default to False in case of an error
        print(f"Error: {str(e)}")  # Log the error for debugging

    result['in_stock_out_of_stock_status'] = instock_status

    # tODO  : size_chart
    all_sizes = pdp_data.get('sizes', [])
    size_chart = []

    for allsize in all_sizes:
        size_data = {}
        size_data["size_list"] = allsize.get("label", "N/A").strip()

        for m in allsize.get("measurements", []):
            name = m.get("name", "").strip()
            name = name.lower().replace(" ", "_")
            value = m.get("value", "").strip()
            size_data[name] = value
            size_data['unit'] = m.get("unit", "").strip()

        size_chart.append(size_data)

    try:
        result['size_chart'] = size_chart
    except Exception as e:
        print(f"Errorn in size_chart json dumps :{str(e)}")


    try:
        # Extract only the 'label' (size) for each entry
        rating_info = pdp_data.get('ratings', {}).get('ratingInfo', [])
        # Filter and sort the ratings by rating value (as integers)
        # sorted_rating_info = sorted(
        #     [item for item in rating_info if item['count'] > 0],
        #     key=lambda x: int(x['rating'])
        # )
        #
        # result['individual_ratings_count'] = {
        #     str(item['rating']): item['count'] for item in sorted_rating_info
        # }
        result['individual_ratings_count'] = rating_info
    except KeyError as e:
        result['individual_ratings_count'] = "N/A"

    try:
        cat = selector.xpath('//script[contains(text(), "BreadcrumbList")]/text()').get()
        clean_data = re.sub(r'\s+', ' ', cat).strip()
        clean_data = json.loads(clean_data)
        categories = clean_data['itemListElement']

        # Create the desired category mapping
        category_map = {}

        # Iterate over the list and assign each category to the L1, L2, L3, etc.
        for i, category1 in enumerate(categories):
            category_name = category1['item']['name']
            category_map[f'l{i + 1}'] = category_name

        result['category'] = category_map
    except Exception as e:
        print(f"Exception in category: {e}")
        result['category'] = "N/A"

    try:
        color_list = []
        veriation_ids = [veria_id for veria_id in pdp_data.get('colours', [])]
        for varia in veriation_ids:
            if 'label' in varia:
                varia['url'] = "https://www.myntra.com/" + varia.get('url')
                varia['colour'] = varia.pop('label')
                color_list.append(varia['colour'])
        result['color_list'] = color_list
        result['variant_level'] = veriation_ids
    except Exception as e:
        result['variant_level'] = "N/A"

    try:
        result['discount'] = str(round((1 - float(result['selling_price']) / float(result['mrp'])) * 100))
    except:
        result['discount'] = "N/A"

    result['individual_ratings_count'] = result['individual_ratings_count'] if result[
        'individual_ratings_count'] else "N/A"

    if result['discount'] != 'N/A':
        result['discount'] = int(result['discount'])

    if result['discount'] == 0 or result['discount'] == str(0):
        result['discount'] = 'N/A'

    return result


def get_data_similar(response):
    result = dict()
    try:
        try:
            data1 = json.loads(response)
        except Exception:
            return {}

        product_list = []
        for products in data1.get('related'):
            if products.get('type') == 'Similar':
                for item in products.get('products'):
                    name = item.get('name', "N/A")
                    MRP = item.get('price').get('mrp', "N/A")
                    product_price = item.get('price').get('discounted', "N/A")
                    image_url = item.get('defaultImage').get('src')
                    product_url = "https://www.myntra.com/" + item.get('landingPageUrl')
                    discount = item.get('price').get('discount').get('label').strip('(').strip(')')
                    try:
                        rating = round(item.get('rating'))
                    except:
                        rating = "N/A"

                    if discount:
                        discount_list = re.findall(r"\d+", discount)
                        discount = "".join([discount.strip() for discount in discount_list if discount])
                        discount = int(discount)
                    else:
                        discount = "N/A"

                    product_list.append({
                        "name": name,
                        "mrp": MRP,
                        "product_rice": product_price,
                        "product_url": product_url,
                        "image_url": image_url,
                        "discount": discount,
                        "rating": rating
                    })

        result['similar_product'] = product_list
    except Exception:
        result['similar_product'] = []

    return result


def get_data_review(response):
    return response