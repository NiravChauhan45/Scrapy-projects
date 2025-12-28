from curl_cffi import requests
from pymongo import MongoClient
import re
from datetime import datetime
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import OrderedDict
import config as db

client = MongoClient(db.MONGO_URI)
db_name = client[db.DB_NAME]
collection = db_name[db.COLLECTION_NAME]
collection_pdp = db_name[db.processed_collection_name]
# html_save_path = rf'E:\Nirav\Project_page_save\Ajio_nua\{db.TODAY}'
html_save_path = rf'D:\Nirav Chauhan\Pagesave\Ajio_nua\{db.TODAY}'
os.makedirs(html_save_path, exist_ok=True)

if not os.path.exists(html_save_path):
    os.makedirs(html_save_path)

product_ids = list(collection.find({"status":"pending"}, {"product_id": 1, "_id": 0}))
# product_ids = list(collection.find({"product_id": 701108835015}, {"product_id": 1, "_id": 0}))


# unprocessed_products = []


def process_product(product):
    # id_counter = 0
    product_id = product['product_id']
    # id_counter += 1

    product_url = f'https://www.ajio.com/p/{product_id}'
    try:
        response = requests.get(product_url, headers=db.HEADERS, timeout=150, impersonate="Chrome110")
        if response.status_code == 200:
            html_content = response.text
            match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});\s*</script>', html_content, re.DOTALL)
            time.sleep(2)
            if match:
                json_str = match.group(1)
                try:
                    main_data = json.loads(json_str)
                    file_name = f"{product_id}.json"
                    file_path = os.path.join(html_save_path, file_name)

                    if os.path.exists(file_path):
                        print(f"File already exists: {file_path}")
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)  # Todo: existing_data already usable
                    else:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(main_data, f, ensure_ascii=False, indent=4)
                        print(f"Saved new file: {file_path}")
                        data = main_data

                    products = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])[0]
                    product_name = products.get("selected", {}).get("modelImage", {}).get("altText", "N/A")
                    product_name = re.sub(r'\s+', ' ', product_name).strip()
                    brand_name = data.get("product", {}).get("productDetails", {}).get("brandName")
                    if brand_name:
                        brand_name = brand_name.upper()
                    productid = str(product_id)
                    catalogid = productid
                    source = "Ajio"

                    scraped_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    product_image = products.get("selected", {}).get("modelImage", {}).get("url", "N/A")

                    stock_status = products.get("selected", {}).get("stock", {}).get("stockLevelStatus", "").lower()
                    is_sold_out = "True" if "outofstock" in stock_status else "False"

                    # selling_price = products.get("selected", {}).get("priceData", {}).get("value", "N/A")

                    avg_rating = data.get("product", {}).get("productDetails", {}).get("ratingsResponse", {}).get(
                        'aggregateRating', {}).get('averageRating')

                    ratings = data.get("product", {}).get("productDetails", {}).get("ratingsResponse", {}).get(
                        'aggregateRating', {}).get('numUserRatings')

                    country_code = "IN"

                    rate = ratings

                    high_resolution_images = ""
                    images = data.get("product", {}).get("productDetails", {}).get("images", [])
                    # product_image = data.get("product", {}).get("productDetails", {}).get("product_image", "")

                    if not images:
                        high_resolution_images = "N/A"
                    else:
                        seen_urls = set()

                        for image in images:
                            url = image.get("url")
                            if not url:
                                continue

                            # Skip if same as product_image
                            if url == product_image:
                                continue

                            # Skip any MODEL.jpg image
                            if url.endswith("-MODEL.jpg"):
                                continue

                            # Skip duplicates
                            if url in seen_urls:
                                continue

                            # Check resolution
                            match = re.search(r'-(\d+)Wx(\d+)H-', url)
                            if match:
                                width = int(match.group(1))
                                if width >= 1000:
                                    seen_urls.add(url)
                                    high_resolution_images += url + " | "

                        high_resolution_images = high_resolution_images.rstrip(" | ")

                        if not high_resolution_images:
                            high_resolution_images = "N/A"

                    description_data = data.get("product", {}).get("productDetails", {}).get("featureData", [])
                    descri_list = []
                    for desc in description_data:
                        feature_values = desc.get("featureValues", [])
                        attr_name = desc.get("catalogAttributeName", "").strip()  # e.g., 'length', 'neckline'

                        for d in feature_values:
                            value = d.get("value", "").strip()
                            if value:
                                descri_list.append(f"{attr_name}: {value}")
                    description_text = " | ".join(descri_list)

                    product_deta = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])
                    mandatory_info_list = []
                    for details in product_deta:
                        key = details.get("key", "")
                        title = details.get("title", "")
                        if title and key:
                            mandatory_info_list.append(f"{key}: {title}")
                    mandatory_info_text = " | ".join(mandatory_info_list)

                    # final_description = description_text + " | " + mandatory_info_text if description_text else mandatory_info_text
                    final_description = description_text if description_text else "N/A"
                    # else:
                    #     final_description = mandatory_info_text

                    # Todo: Specification data
                    # specification_data = data.get("product", {}).get("productDetails", {}).get("featureData", [])
                    # specification_data_list = []
                    # for desc in specification_data:
                    #     feature_values = desc.get("featureValues", [])
                    #     for d in feature_values:
                    #         descri = d.get("value", "")
                    #         if descri:
                    #             specification_data_list.append(descri)
                    # specification_text = " | ".join(descri_list)
                    specification_text = mandatory_info_text

                    product_code = product_id

                    offers_data = ""
                    offers = data.get("product", {}).get("productDetails", {}).get("potentialPromotions", [])
                    if offers:
                        for offer in offers:
                            description = offer.get('description', '')
                            clean_description = re.sub(r'<.*?>', '', description)
                            offer_details = f"Code: {offer.get('code')} | Description: {clean_description.strip()} | Details URL: {offer.get('detailsURL')} | Max Saving Price: {offer.get('maxSavingPrice')}"
                            offers_data += offer_details + " | "
                    # else:
                    #     print("❌ No offer data found.")
                    offers_data = offers_data.rstrip(" | ")

                    try:
                        best_price = data.get("product", {}).get("productDetails", {}).get("potentialPromotions", [])[0]
                        max_savings = best_price.get("maxSavingPrice")
                        # Round up if max_savings is a number
                        if max_savings is not None:
                            best_price = round(max_savings)
                    except:
                        best_price = "N/A"

                    available_sizes_list = []

                    sizes = data.get("product", {}).get("productDetails", {}).get("variantOptions", [])
                    for size in sizes:
                        try:
                            qualifiers = size.get("variantOptionQualifiers", [])
                            for qualifier in qualifiers:
                                name = qualifier.get("name", "").lower()
                                if name.startswith("size"):
                                    value = qualifier.get("value")
                                    if value:
                                        available_sizes_list.append(value)
                                    break
                        except Exception:
                            continue

                    seen = set()
                    available_sizes_list = [s for s in available_sizes_list if not (s in seen or seen.add(s))]

                    # Join with " | " if more than one, otherwise keep as single
                    available_sizes = " | ".join(available_sizes_list) if available_sizes_list else "N/A"

                    bank = data.get("product", {}).get("productDetails", {}).get("prepaidOffers", [])
                    formatted_offers = ""
                    for ban in bank:
                        bank_id = ban.get("bankId", "")
                        bank_name = ban.get("bankName", "")
                        description = ban.get("description", "")
                        offer_code = ban.get("offerCode", "")
                        offer_amount = ban.get("offerAmount", 0)
                        threshold_amount = ban.get("thresholdAmount", 0)
                        tnc_url = ban.get("tncUrl", "")
                        logo_url = ban.get("logo", "")
                        start_date = ban.get("startDate", 0)
                        end_date = ban.get("endDate", 0)
                        offer_detail = f"{bank_id} | {bank_name} | {description} | {offer_code} | {offer_amount} | {threshold_amount} | {tnc_url} | {logo_url} | {start_date} | {end_date}"

                        if formatted_offers:
                            formatted_offers += " | "
                        formatted_offers += offer_detail

                    color_variant = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])[0]
                    color_var = color_variant.get("selected", {}).get("code")
                    more_color = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
                    colors_list = []
                    for color in more_color:
                        colour_name = color.get("selected", {}).get("color")
                        if colour_name:
                            colors_list.append(colour_name)
                    more_colors = " | ".join(colors_list) if colors_list else "N/A"

                    return_policies = []
                    return_policy = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
                    for policy in return_policy:
                        for opt in policy.get("options", []):
                            pol = opt.get("returnContent")
                            if pol:
                                return_policies.append(pol)

                    return_policies_string = " | ".join(return_policies)

                    country = "N/A"  # default fallback
                    manufacturing_info_countryOfOrigin = data.get("product", {}).get("productDetails", {}).get(
                        "mandatoryInfo", [])
                    for item in manufacturing_info_countryOfOrigin:
                        if item.get("key") == "Country Of Origin":
                            country = item.get("title", "N/A")
                            break

                    # manufacturing_info_seller_name = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])[2]
                    # name = manufacturing_info_seller_name.get("title")

                    # discount_off = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
                    # discount_value = "N/A"
                    # for options in discount_off:
                    #     option = options.get("options", [])
                    #     for offs in option:
                    #         off = offs.get("priceData", {}).get("discountValue")
                    #         if off is not None:
                    #             discount_value = off
                    #             break  # Exit inner loop
                    #     if discount_value is not None:
                    #         break

                    # mrp = products.get("options", [])[0]
                    # pricedata = mrp.get("wasPriceData", {}).get("value", "")

                    breadcrumbs = data.get("product", {}).get("productDetails", {}).get("rilfnlBreadCrumbList", {}).get(
                        "rilfnlBreadCrumb", [])
                    heirarchy_list = [category.get("name", "") for category in breadcrumbs]
                    heirarchy_joined = " | ".join(heirarchy_list)

                    mandatory_info = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])

                    manufacturing_info_info = "N/A"

                    for item in mandatory_info:
                        if item.get("key") == "Marketed By":
                            manufacturing_info_info = item.get("title")

                    mandatory_info = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])
                    net_qty = None
                    for info in mandatory_info:
                        if info.get("key") == "Net Qty":
                            net_qty = info.get("title")
                            break
                    product_mrp = data.get("product", {}).get("productDetails", {}).get("variantOptions", [])
                    product_id_1 = product_url.split('/')[-1]

                    mrp = "N/A"
                    discount = "N/A"
                    selling_price = "N/A"
                    for m in product_mrp:
                        code = m.get("code")
                        if code == product_id_1:
                            selling_price = m.get("priceData").get("value")
                            discount_str = m.get("priceData").get("discountPercent", "")
                            discount_match = re.search(r'\d+', discount_str)
                            discount = int(discount_match.group()) if discount_match else "N/A"
                            mrp = m.get("wasPriceData", {}).get("value")

                    no_of_review = 'N/A'

                    product_details = OrderedDict([
                        ("product_id", str(productid)),
                        ("catalog_name", product_name),
                        ("catalog_id", catalogid),
                        ("source", source),
                        ("scraped_date", scraped_date),
                        ("product_name", product_name),
                        ("image_url", product_image),
                        ("product_price", selling_price),
                        ("is_sold_out", is_sold_out),
                        ('discount', discount if discount else "N/A"),
                        ("mrp", mrp),
                        ("product_url", product_url),
                        ("number_of_ratings", rate if rate else "N/A"),
                        ("avg_rating", avg_rating if avg_rating else "N/A"),
                        ("No of reviews", no_of_review if no_of_review else "N/A"),
                        ("images", high_resolution_images),
                        ("product_details", final_description),
                        ("specifications", specification_text),
                        ("Seller Name", "N/A"),
                        ("Brand", brand_name),
                        ("product_code", str(productid)),

                        # ("category_heirarchy", heirarchy_joined),
                        # ("arrival_date", "N/A"),
                        # ("shipping_charges", "N/A"),
                        # ("page_url", "N/A"),
                        # ("position", "N/A"),
                        # ("country_code", country_code),
                        # ("Best_Price", best_price if best_price else "N/A"),
                        # ("Best_offers", offers_data if offers_data else "N/A"),
                        # ("bank_offer ", formatted_offers),
                        # ("rating", avg_rating if avg_rating else "N/A"),
                        # ("MOQ", net_qty),
                        # ("product_code", str(product_code)),
                        # ("Available_sizes", available_sizes),
                        # ("sellerPartnerId", "N/A"),
                        # ("seller_return_policy", return_policies_string),
                        # ("manufacturing_info_packerInfo", "N/A"),
                        # ("manufacturing_info_importerInfo", "N/A"),
                        # ("manufacturing_info_countryOfOrigin", country),
                        # ("manufacturing_info_manufacturerInfo", manufacturing_info_info),
                        # ("More_colours", more_colors),
                        # ("Variation Id", color_var),
                    ])
                    # Todo: set unique column
                    collection_pdp.update_one(
                        {"product_id": product_details["product_id"]},  # Match by product_id
                        {"$set": product_details},  # Update with full data
                        upsert=True
                    )

                    # Todo: set status done
                    collection.update_one(
                        {"product_id": int(productid)},
                        {"$set": {"status": "done"}}
                    )
                    print(f"Inserted details for product_id {product_id} in MongoDB.")
                except json.JSONDecodeError as je:
                    print(f"❌ JSON decoding error for {product_id}: {je}")
            else:
                print(f"❌ Could not find JSON for {product_id}")
        else:
            print(f"❌ Failed: {product_url} - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception for product ID {product_id}: {e}")


# MAX_THREADS = 1
MAX_THREADS = 30
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = [executor.submit(process_product, product) for product in product_ids]
    for future in as_completed(futures):
        future.result()
