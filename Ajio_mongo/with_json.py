# # import new_config
# # from curl_cffi import requests
# # from pymongo import MongoClient
# # import re
# # from datetime import datetime
# # import os
# # import json
# # import hashlib
# # from concurrent.futures import ThreadPoolExecutor, as_completed
# #
# #
# # # Initialize MongoDB client
# # client = MongoClient(new_config.MONGO_URI)
# # db = client[new_config.DB_NAME]
# # collection = db[new_config.COLLECTION_NAME]
# # collection_pdp = db[new_config.processed_collection_name]
# # html_save_path = 'D:/Jitendra Doriya/Probation/Ajio/HTMLs/IN/PDP'  # Path to save the JSON files
# # if not os.path.exists(html_save_path):
# #     os.makedirs(html_save_path)
# #
# # # Fetch product IDs from MongoDB
# # product_ids = list(collection.find({}, {"product_id": 1, "_id": 0}))
# # def process_product(product):
# #
# #         id_counter = 1
# #
# #         # Iterate through each product ID and fetch JSON
# #         for product in product_ids:
# #             product_id = product['product_id']
# #             product_url = f'https://www.ajio.com/p/{product_id}'
# #
# #             try:
# #                 response = requests.get(product_url, headers=new_config.HEADERS, cookies=new_config.COOKIES, timeout=60,impersonate="Chrome110")
# #                 if response.status_code == 200:
# #                     html_content = response.text
# #                     match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});\s*</script>', html_content, re.DOTALL)
# #                     if match:
# #                         json_str = match.group(1)
# #                         try:
# #                             data = json.loads(json_str)
# #                             file_name = f"{product_id}.json"
# #                             file_path = os.path.join(html_save_path, file_name)
# #                             with open(file_path, 'w', encoding='utf-8') as f:
# #                                 json.dump(data, f, ensure_ascii=False, indent=4)
# #                             products=data.get("product",{}).get("productDetails",{}).get("baseOptions",[])[0]
# #                             product_name=products.get("selected",{}).get("modelImage",{}).get("altText",None)
# #                             variantOptions=data.get("product",{}).get("productDetails",{}).get("brandName")
# #                             catalog_id=product_id
# #                             source="Ajio"
# #                             scraped_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #                             product_image=products.get("selected",{}).get("modelImage",{}).get("url",None)
# #                             #category_hierarchy
# #                             #arrival_date
# #                             #shipping_charges
# #                             is_sold_out=products.get("selected",{}).get("stock",{}).get("stockLevelStatus",None)
# #                             selling_price=products.get("selected",{}).get("priceData",{}).get("value",None)
# #                             url=product_url
# #                             avg_rating = data.get("product", {}).get("productDetails", {}).get("ratingsResponse", {}).get('aggregateRating', {}).get('averageRating')
# #                             ratings = data.get("product", {}).get("productDetails", {}).get("ratingsResponse", {}).get('aggregateRating', {}).get('numUserRatings')
# #                             country_code="IN"
# #                             rate=ratings
# #                             high_resolution_images = ""
# #                             images = data.get("product", {}).get("productDetails", {}).get("images", [])
# #                             for image in images:
# #                                 url = image.get("url")
# #                                 if url and re.search(r'-\d+Wx\d+H-', url):
# #                                     match = re.search(r'-(\d+)Wx(\d+)H-', url)
# #                                     if match:
# #                                         width = int(match.group(1))
# #                                         height = int(match.group(2))
# #                                         if width >= 1000:
# #                                             high_resolution_images += url + "|"
# #
# #                             high_resolution_images = high_resolution_images.rstrip("|")
# #                             description_data = data.get("product", {}).get("productDetails", {}).get("featureData", [])
# #                             descri_list = []
# #                             for desc in description_data:
# #                                 feature_values = desc.get("featureValues", [])
# #                                 for d in feature_values:
# #                                     descri = d.get("value", "")
# #                                     if descri:
# #                                         descri_list.append(descri)
# #                             description_text = " | ".join(descri_list)
# #                             product_details = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])
# #                             mandatory_info_list = []
# #                             for details in product_details:
# #                                 title = details.get("title", "")
# #                                 if title:
# #                                     mandatory_info_list.append(title)
# #                             mandatory_info_text = " | ".join(mandatory_info_list)
# #                             final_description = description_text + " | " + mandatory_info_text if description_text else mandatory_info_text
# #                             specification_data = data.get("product", {}).get("productDetails", {}).get("featureData", [])
# #                             specification_data_list = []
# #                             for desc in specification_data:
# #                                 feature_values = desc.get("featureValues", [])
# #                                 for d in feature_values:
# #                                     descri = d.get("value", "")
# #                                     if descri:
# #                                         specification_data_list.append(descri)
# #                             specification_text = " | ".join(descri_list)
# #
# #                             # sizes = data.get("product", {}).get("productDetails", {}).get("variantOptions", [])
# #                             # for size in sizes:
# #                             #     all_sizes = size.get("variantOptionQualifiers", [])[4]
# #                             #     get_size = all_sizes.get("value")
# #                             product_code=product_id
# #                             offers_data = ""
# #                             offers = data.get("product", {}).get("productDetails", {}).get("potentialPromotions", [])
# #                             if offers:
# #                                 for offer in offers:
# #                                     description = offer.get('description', '')
# #                                     clean_description = re.sub(r'<.*?>', '', description)
# #
# #                                     offer_details = f"Code: {offer.get('code')} | Description: {clean_description.strip()} | Details URL: {offer.get('detailsURL')} | Max Saving Price: {offer.get('maxSavingPrice')}"
# #
# #                                     offers_data += offer_details + "|"
# #                             else:
# #                                 print("❌ No offer data found.")
# #
# #                             offers_data = offers_data.rstrip("|")
# #                             available_sizes = ""
# #
# #                             sizes = data.get("product", {}).get("productDetails", {}).get("variantOptions", [])
# #                             for size in sizes:
# #                                 try:
# #                                     all_sizes = size.get("variantOptionQualifiers", [])[4]
# #                                     get_size = all_sizes.get("value") if all_sizes else None
# #                                     if get_size:
# #                                         available_sizes += get_size + "|"
# #                                 except IndexError:
# #                                     continue
# #
# #                             available_sizes = available_sizes.rstrip("|")
# #                             bank = data.get("product", {}).get("productDetails", {}).get("prepaidOffers", [])
# #
# #                             formatted_offers = ""
# #
# #                             for ban in bank:
# #                                 bank_id = ban.get("bankId", "")
# #                                 bank_name = ban.get("bankName", "")
# #                                 description = ban.get("description", "")
# #                                 offer_code = ban.get("offerCode", "")
# #                                 offer_amount = ban.get("offerAmount", 0)
# #                                 threshold_amount = ban.get("thresholdAmount", 0)
# #                                 tnc_url = ban.get("tncUrl", "")
# #                                 logo_url = ban.get("logo", "")
# #                                 start_date = ban.get("startDate", 0)
# #                                 end_date = ban.get("endDate", 0)
# #
# #                                 offer_detail = f"{bank_id}|{bank_name}|{description}|{offer_code}|{offer_amount}|{threshold_amount}|{tnc_url}|{logo_url}|{start_date}|{end_date}"
# #
# #                                 if formatted_offers:
# #                                     formatted_offers += "|"
# #                                 formatted_offers += offer_detail
# #
# #                             id_counter += 1
# #                             color_variant = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])[0]
# #                             color_var = color_variant.get("selected", {}).get("code")
# #                             more_color = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
# #                             colors_list = []
# #                             return_policies = []
# #                             return_policy = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
# #                             for policy in return_policy:
# #                                 for opt in policy.get("options", []):
# #                                     pol = opt.get("returnContent")
# #                                     if pol:
# #                                         return_policies.append(pol)
# #
# #                             # Step 2: Join the list into a single string (combine)
# #                             # You can choose separator: space / comma / newline
# #                             return_policies_string = " | ".join(return_policies)
# #
# #                             for color in more_color:
# #                                 colour_name = color.get("selected", {}).get("color")
# #                                 if colour_name:
# #                                     colors_list.append(colour_name)
# #
# #                             more_colors = "|".join(colors_list) if colors_list else None
# #                             manufacturing_info_countryOfOrigin = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])[3]
# #                             country=manufacturing_info_countryOfOrigin.get("title")
# #                             manufacturing_info_seller_name	=data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])[2]
# #                             name = manufacturing_info_seller_name.get("title")
# #                             discount_off = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
# #                             discount_value = None  # single value, not a list
# #
# #                             for options in discount_off:
# #                                 option = options.get("options", [])
# #                                 for offs in option:
# #                                     off = offs.get("priceData", {}).get("discountValue")
# #                                     if off is not None:
# #                                         discount_value = off
# #                                         break  # Exit inner loop
# #                                 if discount_value is not None:
# #                                     break
# #                             mrp = products.get("options", [])[0]
# #                             pricedata = mrp.get("wasPriceData", {}).get("value", "")
# #
# #                             # Check if pricedata exists and is not empty
# #                             # if pricedata:
# #                             #     # Extract only numeric part (using a filter to keep digits and remove other characters)
# #                             #     numeric_mrp = int(''.join(filter(str.isdigit, pricedata)))
# #                             #     print(numeric_mrp)
# #                             # else:
# #                             #     print("Price data not found.")
# #                             breadcrumbs = data.get("product", {}).get("productDetails", {}).get("rilfnlBreadCrumbList", {}).get("rilfnlBreadCrumb", [])
# #                             heirarchy_list = [category.get("name", "") for category in breadcrumbs]
# #                             heirarchy_joined = " | ".join(heirarchy_list)
# #                             manufacturing_info_seller_name = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])[2]
# #                             name = manufacturing_info_seller_name.get("title")
# #                             moq = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])[0]
# #                             moq_net = moq.get("title")
# #
# #                             product_details = {
# #                                 "product_id": product_id,
# #                                 "catalog_id": catalog_id,
# #                                 "Catalog name":product_name,
# #                                 "source": source,
# #                                 "scraped_date": scraped_date,
# #                                 "arrival_date":"N/A",
# #                                 "shipping_charges":"N/A",
# #                                 "page_url":"N/A",
# #                                 "product_url": product_url,
# #                                 "category_heirarchy":heirarchy_joined,
# #                                 "Brand":variantOptions,
# #                                 "product_name": product_name,
# #                                 "product_image": product_image,
# #                                 "is_sold_out": is_sold_out,
# #                                 "MRP":pricedata,
# #                                 'Discount':discount_value,
# #                                 "product_price": selling_price,
# #                                 "number_of_ratings": rate,
# #                                 "avg_rating": avg_rating,
# #                                 "MOQ":moq_net,
# #                                 "country_code": country_code,
# #                                 "rating":avg_rating,
# #                                 "Position":"N/A",
# #                                 "product_code": product_code,
# #                                 "high_resolution_images": high_resolution_images,
# #                                 "available_sizes": available_sizes,
# #                                 "best offers": offers_data,
# #                                 "Bank offer ": formatted_offers,
# #                                 "specifications	":specification_text,
# #                                 "description": final_description,
# #                                 "variation_id":color_var,
# #                                 "sellerPartnerId":"N/A",
# #                                 "manufacturing_info_packerInfo":"N/A",
# #                                 "manufacturing_info_manufacturerInfo": name,
# #                                 "manufacturing_info_seller_name":"N/A",
# #                                 "manufacturing_info_importerInfo":"N/A",
# #                                 "seller_return_policy":return_policies_string,
# #                                 "more_color":more_colors,
# #                                 "manufacturing_info_countryOfOrigin":country
# #                             }
# #
# #                             # json_file_path = os.path.join(html_save_path, f"{product_id}.json")
# #                             # with open(json_file_path, 'w', encoding='utf-8') as json_file:
# #                             #     json.dump(product_details, json_file, ensure_ascii=False, indent=4)
# #                             if discount_value:
# #                                 product_details["Discount"] = discount_value
# #                             else:
# #                                 product_details["Discount"] = None  # Or any default value you prefer (e.g., 0 or "N/A")
# #
# #                             # if return_policies:
# #                             #     product_details["seller_return_policy"] = return_policies
# #                             # else:
# #                             #     product_details[ "seller_return_policy"] = None  # Or any default value you prefer (e.g., "No Return Policy")
# #                             # Check if product with the same product_id exists
# #                             existing_product = collection_pdp.find_one({"product_id": product_id})
# #
# #                             if existing_product:
# #                                 # If the product already exists, print a message and skip the insertion
# #                                 print(f"Product with product_id {product_id} already exists. Skipping insertion.")
# #                             else:
# #                                 # If the product doesn't exist, insert the new product details
# #                                 collection_pdp.update_one(
# #                                     {"product_id": product_id},  # Search condition
# #                                     {"$set": product_details},  # Data to update or insert
# #                                     upsert=True  # If no document matches, insert a new one
# #                                 )
# #                                 print(f"Inserted product details for product_id {product_id} into MongoDB.")
# #
# #                         except json.JSONDecodeError as je:
# #                             print(f"❌ JSON decoding error for {product_id}: {je}")
# #                     else:
# #                         print(f"❌ Could not find JSON for {product_id}")
# #
# #                 else:
# #                     print(f"❌ Failed: {product_url} - Status: {response.status_code}")
# #
# #             except Exception as e:
# #                 print(f"❌ Exception for product ID {product_id}: {e}")
# #
# #         print("🎉 Done parsing all products!")
# #
# #
# # MAX_THREADS = 20
# #
# # with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
# #     futures = [executor.submit(process_product, product) for product in product_ids]
# #
# #     for future in as_completed(futures):
# #         try:
# #             future.result()
# #         except Exception as e:
# #             print(f"Thread error: {str(e)}")
# import math
#
# import re
# import time
# import json
# from curl_cffi import requests
#
# cookies = {
#     'f5_cspm': '1234',
#     '_gcl_au': '1.1.1713263269.1745559993',
#     'AB': 'B',
#     '_fbp': 'fb.1.1745559993302.793455710130750973',
#     '_fpuuid': 'OeCUQBjkK4ZtAdK6J0Orm',
#     'deviceId': 'OeCUQBjkK4ZtAdK6J0Orm',
#     '_scid': '8mP8_CIOGXaDjJdWULkIyu94uHqatyGI',
#     'V': '201',
#     'storeTypes': 'ajio',
#     '_gac_UA-68002030-1': '1.1745647257.Cj0KCQjw5azABhD1ARIsAA0WFUG5MFp4gx_TPa0rtF6clhH4WSSUR82ZWR0hAKRBID6nJXC41jWLFfYaAq2oEALw_wcB',
#     '_gcl_gs': '2.1.k1$i1745647255$u172147827',
#     '_gcl_aw': 'GCL.1745647265.Cj0KCQjw5azABhD1ARIsAA0WFUG5MFp4gx_TPa0rtF6clhH4WSSUR82ZWR0hAKRBID6nJXC41jWLFfYaAq2oEALw_wcB',
#     'th_external_id': 'e83785e592c249478419072ef01b27c3b705a69b905659ebe4a40bd0c01858f1',
#     'th_capi_ph': '4cecab59d94ac150fee4b9ee3c691357885cc8d0d7bff743f1cd872c49561901',
#     'th_capi_fn': '4cecab59d94ac150fee4b9ee3c691357885cc8d0d7bff743f1cd872c49561901',
#     'EI': 'XtwNySZwBS5lee%2FdeYIUm%2FLs4nUl6V6rKX85I42OGYpo0cXm5Oc8Pkb1WSyGgoeh',
#     'LS': 'LOGGED_IN',
#     'cohortSegment': '22,14,7,18',
#     'A': 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJjbGllbnQiLCJjbGllbnROYW1lIjoid2ViX2NsaWVudCIsInJvbGVzIjpbeyJuYW1lIjoiUk9MRV9UUlVTVEVEX0NMSUVOVCJ9XSwidGVuYW50SWQiOiJBSklPIiwiZXhwIjoxNzQ3NDQ1ODEzLCJpYXQiOjE3NDQ4NTM4MTN9.aQHWBAzy78NyYGQdZ8wtevNbGHOZ2LstpdOqN7BM7RiBHsqbEVyAR6O_VyJMTkI0ZQNvM9W5qOMPjXPNHBK2aRe_RCUOXHadkuD3-_5Hw-XabF4kWk7pQ_Kk25TbrKcjgvYn5JGG-DsEHNXHtc4PpVZvBtiEzS7HdWkRdFAw3TSKW1MZuj7qcaLVBFwIfaHkCftsEWhdU93djj4mw0eR93zM5RyeRlAYNKZo0ZAyqYPr4Zy9ANFvFBZfBE75xNBqmTnHO9rKSSBUpUaLVBjmo36XmdJanNoNsqBJoZe1yq8UCAn1ZNCdSyo4O0yHSfdJsx-o2sI5_aLBh25I5ie-og',
#     'U': 'anonymous',
#     'PC': '110001',
#     'CT': 'NEW%20DELHI',
#     'ST': 'DELHI',
#     'ZN': 'North',
#     'PG': 'PD40',
#     'bm_lso': '21B4CD97525E80906217E549B0D23857568E20205FE69E87E79E9E56D5B3068F~YAAQHDtAFy1diHqWAQAAmBT1fwMiILAhs58p/iNtCjbIeAZzbGF10fYCyCFvOOVtilL9I1nD1dqMNpkKN8mgUREzdn/vZiPj4nKa+/gEQWBtB4TEG1hQnadH6a2NDG1XyUfDDMEG+k+EJaqZRcp3FRFd2PGR3JFrlSWJGkSGLaZ43UBo0K4FXNfGzY7VjVhAGccTL7KoDQK8+C0mNYf7wb+szuAVlVPrTnIfQ0+wzOfSjZNKJFNlKMfCn7fwGR9iO+qkJVYQFG07ou2MWFS1q9/7icEqmQKfyFDfxP8TgsI/K8cKwXVACijmLW646HNg71vR3LlqVmpIO2e51T8DIdFncbdRuXtOC1ADIK0zeM7Q+UvGIvcbFcXAcDgojjq4cJ0uJGhMnKkAyOqGuFiv4XgsuynmJYDW60lrpMPbTLhcgQT0hJafLSpvxkmbrJjx/8Hcvyyfq9f3pWKS^1745903313205',
#     '_gid': 'GA1.2.1866336355.1747220901',
#     '_sctr': '1%7C1747161000000',
#     '_ScCbts': '%5B%5D',
#     'cdigiMrkt': 'utm_source%3Agoogle%7Cutm_medium%3Acpc%7Cdevice%3Adesktop%7Cexpires%3Amon%2C%2026%20may%202025%2010%3A25%3A54%20gmt%7Cexpires%3Asun%2C%2025%20may%202025%2012%3A44%3A17%20gmt%7Cexpires%3Asun%2C%2025%20may%202025%2012%3A57%3A21%20gmt%7Cexpires%3Asun%2C%2025%20may%202025%2012%3A44%3A22%20gmt%7Cexpires%3AMon%2C%2026%20May%202025%2012%3A44%3A33%20GMT%7C',
#     'bm_sz': '93F56D648358AA88FBE1B1E65058BEFD~YAAQjDtAFymLXq2WAQAAnexQ0hsAIcVJYcBw5bscNEvvLf+KUzx2LF2sP0DrLun6dWQRDBCZhGquqXG2izkAYr8QpbCWte58ZlTZUo2SlBgclD8wI0vyFWP+f6rQtNVGFTOKe4pvdiQMTPT2d4lT+4QteNJ/U7m7fFXEAv/Cz0Kn/lCeJfhj9bYdIrvo8VPbIGshkdeoRtsE/0hPwNMzU3VCDniim+nUzxrUxuiElKRbeNHyoIUP2NTP6N86h+oIPv+YHyhYvYHJ2oBOLg6tUXhmRJZt65OusQOzBnOt7ELoVvAarFYkAFOUbwakZihcmKL1q7oaNhWphkcxqob0e8CjfiBv7lk20X0C1AXSxw+EGNl1w1k=~4602165~4600641',
#     'TS01a68201': '015d0fa2262332c9dc25aef393254223958dd273ed0616372810ce6e40929f65d9d09a69abbd0b189fcc3630f97926b03278ec0e8537b2b0b6334e5069078819457f2bf291',
#     'ak_bmsc': '985B44EA064411FAB6E424BF7C60C3F7~000000000000000000000000000000~YAAQHfU3FzugLcWWAQAAaOgR0xt+5UTGWr1coUiRjRFbKPoSL2jQBVVHLOMM1zdtvgdw2kkq0+P2Jl9VsyJNPHHYnNqcJ/QclIzHLjnOinb8oWAxk0ZPB0gZxzZONBVMe48/SMb9WGNh5Au9ZJhZgaNy/EM6tWRs4RSmLb90I39ycB6BXrfa8Kysq3zfsBT5Ck3zs0Ep4njdcEHVSACWJ+PpLdXY/cf860KQDampLCI6iw2hL68rb8d5JlU3hIODKupyPwjF5g56/Y9BXSsqCh2+tXDdi/2u6ya4IIfFDNf2jj2OwOLMQDGuJK89s2IE/whCgTv2CnU4v4hqJhAIdk5RrKiDjCw/hGqqOR0+2y+YzVz+eWUGVqdZ/tKHSg==',
#     'recentlyViewed': '[{"id":"700228458_gold","store":0},{"id":"464075167_white","store":0}]',
#     '_abck': '00116242144627841D3E518AA3CD3857~0~YAAQHfU3Fz6gLcWWAQAAU+0R0w1yQGITcPZ6HURFuVdZhk1sPVMa0N0c4jq0XNLwbApL3MtmpFBBCfk1ZEzYSBCtk9Oz0PnIaG68RXjOwr3SMruu5N20Q535Tng1ja9mdXTQytKbTrs2zNoMW3bbhxb/b8qgik2xREN5lg75y9xJWWoKPsBoDm92WfUce9Rna31XJldaYGGJdDpgu3VkxMrq4NE6KCqUT7pLOa+TC/wGVgvYcMAOM7I2m+j8tAUDIpyenNRjyDlIJ5DtCFxC0SCMmg0fJNRLSV+kqbDICAYaOxojho569GOr5m2UzgaQmIBF4ol5X3jFjUbpvRKP1IEQO19Ef+cIe0h9wbWtmjEPcZpgmSQZtRG/uWzkwrpAm8nF5eTNUPCVnb6ipbi8SKX0id9FhXmYKiY8Ww2xbPcQ+oY2V//oj0pztmemVHTHvQaAF/giJU35EU9EeLLKhytosbU4eyYM0wW/dGWGMy3VbqI2Jp0sP0REiZQIaBcE4KoblrIWx/6qbfdg/XP+UrXQszclVxkonDojXhRwvZEp9wJFnaB6ttq+/xJPar3CIJCvZMEW9+bT5820aGgV7VqGKr5j7aFbIKPAI6wN8+ekmHewHjSXzNAwO+lAhbIqzkVc+qAAbTsC0Jo7k/+4V1JQVUy28MZAyAcgH0Xx9q2XTWen+VXmXQQY0Qgfrwk1IbC5MG4iDfuL+/VIEd7LxsTKEZIj9KB0O4PiBBVZm93L6aPtu2cAnuagQThgMAkDG9QhXz2RTAvJPsgHBUTS12MfSpaQRWEO59hazuNvhqTgS42eXTXv90+MhpFZrpjniJMa79dDOUQ8702XL+rpZ9jbyNKJzrhVZb6osrOhlEuygPFC7WOOCqGOcAMV8x4nidNNMKilvtFAsjsnC0lu4odMw4DYajKJLoPiUpZ6WD7rr+M7DNFYcFWc/x39q/+lk1/JQWjgNG4XsibzFLdAPAjOS4N5aJh0MfJ+w7EhVThlKjWP0QYgMVCXuZaigOGlxrwyQIm76/lcOHQ8/iy1Id68+A==~-1~-1~1747299867',
#     '_dc_gtm_UA-68002030-18': '1',
#     'sessionStatus': 'true|undefined',
#     'FirstPage': 'Thu May 15 2025 13:57:23 GMT+0530 (India Standard Time)',
#     '_dc_gtm_UA-68002030-1': '1',
#     '_gat_UA-68002030-18': '1',
#     'bm_ss': 'ab8e18ef4e',
#     '_scid_r': 'B-P8_CIOGXaDjJdWULkIyu94uHqatyGIG6EVnA',
#     'ADRUM_BT': 'R:35|i:5010|g:c317da98-0ee4-4ac2-9fd0-608096e5e1592016122|e:135|s:f|n:customer1_be12de70-87be-45ee-86d9-ba878ff9a400',
#     'TS01d405db': '015d0fa226c9438ab9fcc1846c0c2b9b4052475f7d14a7e1a8fe22ad93f23b8bee93757fc89844698c9e5f18068ea4a6591a004e52d0af85e0cee86a29a54ff8f8a5689ee51775c128498097c3c2a656a7bd3e0436dd5264330077e7685179f37c973e964d2a3aa9e8de4e063ef70c6ca818c1c2fa2a79acf3031faf248a13bb24c923a14a70c02b3fbd9a2133349e07faf1d2f0272f787e144b0806dd7a6aefff48f00125224d3ed6c857eb699c016ddcb4b62e391825d1ee2dafc29a2936131b0d4ee5fcaa34f8aa1811cd0a68b9990c5a7db4fbbdbc545710b08d343f1fb92c73bf8be79e3060d9c2dbfb688087a6da7a4903ba6b6a9bf07fa3d8ef6806f50dbbf5cbb964bf0033f254dd271ebcac2827b3f43ae5bf9720f85e32cc5a13b5443a59697a244da028cd92a206ef63be30bcc8188b74694293d753ace4d97d3752c6340dd5754a766c5d7cbc1744b7b646b7790232',
#     'TSae7facce027': '08dc579c15ab2000042b75bdfce30f7422cb192c810e1caaef9f50b46bbafdac6a4ce0bfc0b3c06608a9af4beb1130006036341d54c61184cd4a30a8daa76380929342b562775c034923057110c24839a9dafbbbb89b16d8f8ece9690e847ec6',
#     'bm_s': 'YAAQHfU3F0GgLcWWAQAAtfER0wPqHaFtGCtcuVGBdnsWX6+g88T94fA3V5ZnQQrZlfyQLoxpf/0nhwg+lO+3WeTFjaXwiGmAD7MhNZtD5Xv7bksHzSiM+B5wXI+88WGzZwPAy32zGe/IUtbx/xE5fRYcC/l+DCdCs+DJDh2N6iv5syYyBSGy1PMskmC6GWiGJrWdcIh08qeQlSsEJMrEXaRs9ojTz8i4owtMuAISM7o2k8tzi1jgzB6VIPBvgJRWJi18dZYTyo0o4E/CMKMHQ3xKUYvK8iOi6I+CUggkyJ/PoFZfqdyEs1NafKMF7ht3gdT5+bWU6HB/81FGjLUD8GrbOzueY/A0G4MuLaHMAQAVo3MLIKTN+MEHavBmMLjCztPe1/tOBEoJZxcazcEswJTKRNCux6sbu70vLDrpfTr8nEfbvHwKTQgrKGtDNJQVfWdWv2nEbwOfz7uDC83qCK4Ygw7o4q+pGQZoNkPw/qyW3uE/XCHbruThShHcmNt3qerkWx8pupbyUHyhKs22ovYyp4hn44NR0iuJXJAF9NHYFzdDXfedpQ==',
#     'bm_sv': 'D15AA891F1013CA464092B941D3D953D~YAAQHfU3F0KgLcWWAQAAtfER0xvRXh4xGYNSR8kQDTQ55/ZHGqpvg9hdv4jL6R9gf9GJIEues85GG2jbOGvqFGRoH7goQvLwqzo8ipGEHu6slOf7GwzfHmMfy5Jxvm3dgH8fXA9pshNE5cIsZf6kjyn3/qUOZZcONS+RprQKpTpsPH3g5Kqn6hnAwcvaHbxg55F6xpUdEPqZ7oQC1EY1PEzVL5CWWlCZFZwJ13TzEZue57JCc0TZJVa3ifoczA==~1',
#     '_ga': 'GA1.2.1924808953.1745559993',
#     '_gat_UA-68002030-1': '1',
#     'ImpressionCookie': '0',
#     'cto_bundle': 'YdrE0l8xMmlrb2RVJTJCaGVRVCUyRnQwdmNjNXZ2N3ZaYWhiaHhJRkhlMkpHUHhORjlaS3JXRDFWdnhaWUkyUjBuRjAySnl2Vk9WWk0wbE9tTjZINlQ0d3d3YWhTOExHTHRtQjd2bU1TNDBIaVNOTHBoN1hDTGx4Rm1ENlFVT3FialNVUk45YW56JTJCalpnRmY0b083YzNCM001bW5FMFElM0QlM0Q',
#     'f5avr0627051897aaaaaaaaaaaaaaaa_cspm_': 'ACIEAMFDEBHFJGGOCDNNIENHJDMNMFNMAFFOLAMHNDOFIALDHDJELDOKLHLBFGPIGEICGOGPBNBIJDHJENDACCGPBBLLDPILMGJLOGIAMGFEGBKDAPELMBJIFIILOIOB',
#     '_ga_X3MNHK0RVR': 'GS2.1.s1747297644$o23$g0$t1747297654$j50$l0$h0$di8Mv2InhZ-Nr7Osimzm47edgBcSWM0v2dQ',
# }
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'no-cache',
#     'pragma': 'no-cache',
#     'priority': 'u=0, i',
#     'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'none',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
#     # 'cookie': 'f5_cspm=1234; _gcl_au=1.1.1713263269.1745559993; AB=B; _fbp=fb.1.1745559993302.793455710130750973; _fpuuid=OeCUQBjkK4ZtAdK6J0Orm; deviceId=OeCUQBjkK4ZtAdK6J0Orm; _scid=8mP8_CIOGXaDjJdWULkIyu94uHqatyGI; V=201; storeTypes=ajio; _gac_UA-68002030-1=1.1745647257.Cj0KCQjw5azABhD1ARIsAA0WFUG5MFp4gx_TPa0rtF6clhH4WSSUR82ZWR0hAKRBID6nJXC41jWLFfYaAq2oEALw_wcB; _gcl_gs=2.1.k1$i1745647255$u172147827; _gcl_aw=GCL.1745647265.Cj0KCQjw5azABhD1ARIsAA0WFUG5MFp4gx_TPa0rtF6clhH4WSSUR82ZWR0hAKRBID6nJXC41jWLFfYaAq2oEALw_wcB; th_external_id=e83785e592c249478419072ef01b27c3b705a69b905659ebe4a40bd0c01858f1; th_capi_ph=4cecab59d94ac150fee4b9ee3c691357885cc8d0d7bff743f1cd872c49561901; th_capi_fn=4cecab59d94ac150fee4b9ee3c691357885cc8d0d7bff743f1cd872c49561901; EI=XtwNySZwBS5lee%2FdeYIUm%2FLs4nUl6V6rKX85I42OGYpo0cXm5Oc8Pkb1WSyGgoeh; LS=LOGGED_IN; cohortSegment=22,14,7,18; A=eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJjbGllbnQiLCJjbGllbnROYW1lIjoid2ViX2NsaWVudCIsInJvbGVzIjpbeyJuYW1lIjoiUk9MRV9UUlVTVEVEX0NMSUVOVCJ9XSwidGVuYW50SWQiOiJBSklPIiwiZXhwIjoxNzQ3NDQ1ODEzLCJpYXQiOjE3NDQ4NTM4MTN9.aQHWBAzy78NyYGQdZ8wtevNbGHOZ2LstpdOqN7BM7RiBHsqbEVyAR6O_VyJMTkI0ZQNvM9W5qOMPjXPNHBK2aRe_RCUOXHadkuD3-_5Hw-XabF4kWk7pQ_Kk25TbrKcjgvYn5JGG-DsEHNXHtc4PpVZvBtiEzS7HdWkRdFAw3TSKW1MZuj7qcaLVBFwIfaHkCftsEWhdU93djj4mw0eR93zM5RyeRlAYNKZo0ZAyqYPr4Zy9ANFvFBZfBE75xNBqmTnHO9rKSSBUpUaLVBjmo36XmdJanNoNsqBJoZe1yq8UCAn1ZNCdSyo4O0yHSfdJsx-o2sI5_aLBh25I5ie-og; U=anonymous; PC=110001; CT=NEW%20DELHI; ST=DELHI; ZN=North; PG=PD40; bm_lso=21B4CD97525E80906217E549B0D23857568E20205FE69E87E79E9E56D5B3068F~YAAQHDtAFy1diHqWAQAAmBT1fwMiILAhs58p/iNtCjbIeAZzbGF10fYCyCFvOOVtilL9I1nD1dqMNpkKN8mgUREzdn/vZiPj4nKa+/gEQWBtB4TEG1hQnadH6a2NDG1XyUfDDMEG+k+EJaqZRcp3FRFd2PGR3JFrlSWJGkSGLaZ43UBo0K4FXNfGzY7VjVhAGccTL7KoDQK8+C0mNYf7wb+szuAVlVPrTnIfQ0+wzOfSjZNKJFNlKMfCn7fwGR9iO+qkJVYQFG07ou2MWFS1q9/7icEqmQKfyFDfxP8TgsI/K8cKwXVACijmLW646HNg71vR3LlqVmpIO2e51T8DIdFncbdRuXtOC1ADIK0zeM7Q+UvGIvcbFcXAcDgojjq4cJ0uJGhMnKkAyOqGuFiv4XgsuynmJYDW60lrpMPbTLhcgQT0hJafLSpvxkmbrJjx/8Hcvyyfq9f3pWKS^1745903313205; _gid=GA1.2.1866336355.1747220901; _sctr=1%7C1747161000000; _ScCbts=%5B%5D; cdigiMrkt=utm_source%3Agoogle%7Cutm_medium%3Acpc%7Cdevice%3Adesktop%7Cexpires%3Amon%2C%2026%20may%202025%2010%3A25%3A54%20gmt%7Cexpires%3Asun%2C%2025%20may%202025%2012%3A44%3A17%20gmt%7Cexpires%3Asun%2C%2025%20may%202025%2012%3A57%3A21%20gmt%7Cexpires%3Asun%2C%2025%20may%202025%2012%3A44%3A22%20gmt%7Cexpires%3AMon%2C%2026%20May%202025%2012%3A44%3A33%20GMT%7C; bm_sz=93F56D648358AA88FBE1B1E65058BEFD~YAAQjDtAFymLXq2WAQAAnexQ0hsAIcVJYcBw5bscNEvvLf+KUzx2LF2sP0DrLun6dWQRDBCZhGquqXG2izkAYr8QpbCWte58ZlTZUo2SlBgclD8wI0vyFWP+f6rQtNVGFTOKe4pvdiQMTPT2d4lT+4QteNJ/U7m7fFXEAv/Cz0Kn/lCeJfhj9bYdIrvo8VPbIGshkdeoRtsE/0hPwNMzU3VCDniim+nUzxrUxuiElKRbeNHyoIUP2NTP6N86h+oIPv+YHyhYvYHJ2oBOLg6tUXhmRJZt65OusQOzBnOt7ELoVvAarFYkAFOUbwakZihcmKL1q7oaNhWphkcxqob0e8CjfiBv7lk20X0C1AXSxw+EGNl1w1k=~4602165~4600641; TS01a68201=015d0fa2262332c9dc25aef393254223958dd273ed0616372810ce6e40929f65d9d09a69abbd0b189fcc3630f97926b03278ec0e8537b2b0b6334e5069078819457f2bf291; ak_bmsc=985B44EA064411FAB6E424BF7C60C3F7~000000000000000000000000000000~YAAQHfU3FzugLcWWAQAAaOgR0xt+5UTGWr1coUiRjRFbKPoSL2jQBVVHLOMM1zdtvgdw2kkq0+P2Jl9VsyJNPHHYnNqcJ/QclIzHLjnOinb8oWAxk0ZPB0gZxzZONBVMe48/SMb9WGNh5Au9ZJhZgaNy/EM6tWRs4RSmLb90I39ycB6BXrfa8Kysq3zfsBT5Ck3zs0Ep4njdcEHVSACWJ+PpLdXY/cf860KQDampLCI6iw2hL68rb8d5JlU3hIODKupyPwjF5g56/Y9BXSsqCh2+tXDdi/2u6ya4IIfFDNf2jj2OwOLMQDGuJK89s2IE/whCgTv2CnU4v4hqJhAIdk5RrKiDjCw/hGqqOR0+2y+YzVz+eWUGVqdZ/tKHSg==; recentlyViewed=[{"id":"700228458_gold","store":0},{"id":"464075167_white","store":0}]; _abck=00116242144627841D3E518AA3CD3857~0~YAAQHfU3Fz6gLcWWAQAAU+0R0w1yQGITcPZ6HURFuVdZhk1sPVMa0N0c4jq0XNLwbApL3MtmpFBBCfk1ZEzYSBCtk9Oz0PnIaG68RXjOwr3SMruu5N20Q535Tng1ja9mdXTQytKbTrs2zNoMW3bbhxb/b8qgik2xREN5lg75y9xJWWoKPsBoDm92WfUce9Rna31XJldaYGGJdDpgu3VkxMrq4NE6KCqUT7pLOa+TC/wGVgvYcMAOM7I2m+j8tAUDIpyenNRjyDlIJ5DtCFxC0SCMmg0fJNRLSV+kqbDICAYaOxojho569GOr5m2UzgaQmIBF4ol5X3jFjUbpvRKP1IEQO19Ef+cIe0h9wbWtmjEPcZpgmSQZtRG/uWzkwrpAm8nF5eTNUPCVnb6ipbi8SKX0id9FhXmYKiY8Ww2xbPcQ+oY2V//oj0pztmemVHTHvQaAF/giJU35EU9EeLLKhytosbU4eyYM0wW/dGWGMy3VbqI2Jp0sP0REiZQIaBcE4KoblrIWx/6qbfdg/XP+UrXQszclVxkonDojXhRwvZEp9wJFnaB6ttq+/xJPar3CIJCvZMEW9+bT5820aGgV7VqGKr5j7aFbIKPAI6wN8+ekmHewHjSXzNAwO+lAhbIqzkVc+qAAbTsC0Jo7k/+4V1JQVUy28MZAyAcgH0Xx9q2XTWen+VXmXQQY0Qgfrwk1IbC5MG4iDfuL+/VIEd7LxsTKEZIj9KB0O4PiBBVZm93L6aPtu2cAnuagQThgMAkDG9QhXz2RTAvJPsgHBUTS12MfSpaQRWEO59hazuNvhqTgS42eXTXv90+MhpFZrpjniJMa79dDOUQ8702XL+rpZ9jbyNKJzrhVZb6osrOhlEuygPFC7WOOCqGOcAMV8x4nidNNMKilvtFAsjsnC0lu4odMw4DYajKJLoPiUpZ6WD7rr+M7DNFYcFWc/x39q/+lk1/JQWjgNG4XsibzFLdAPAjOS4N5aJh0MfJ+w7EhVThlKjWP0QYgMVCXuZaigOGlxrwyQIm76/lcOHQ8/iy1Id68+A==~-1~-1~1747299867; _dc_gtm_UA-68002030-18=1; sessionStatus=true|undefined; FirstPage=Thu May 15 2025 13:57:23 GMT+0530 (India Standard Time); _dc_gtm_UA-68002030-1=1; _gat_UA-68002030-18=1; bm_ss=ab8e18ef4e; _scid_r=B-P8_CIOGXaDjJdWULkIyu94uHqatyGIG6EVnA; ADRUM_BT=R:35|i:5010|g:c317da98-0ee4-4ac2-9fd0-608096e5e1592016122|e:135|s:f|n:customer1_be12de70-87be-45ee-86d9-ba878ff9a400; TS01d405db=015d0fa226c9438ab9fcc1846c0c2b9b4052475f7d14a7e1a8fe22ad93f23b8bee93757fc89844698c9e5f18068ea4a6591a004e52d0af85e0cee86a29a54ff8f8a5689ee51775c128498097c3c2a656a7bd3e0436dd5264330077e7685179f37c973e964d2a3aa9e8de4e063ef70c6ca818c1c2fa2a79acf3031faf248a13bb24c923a14a70c02b3fbd9a2133349e07faf1d2f0272f787e144b0806dd7a6aefff48f00125224d3ed6c857eb699c016ddcb4b62e391825d1ee2dafc29a2936131b0d4ee5fcaa34f8aa1811cd0a68b9990c5a7db4fbbdbc545710b08d343f1fb92c73bf8be79e3060d9c2dbfb688087a6da7a4903ba6b6a9bf07fa3d8ef6806f50dbbf5cbb964bf0033f254dd271ebcac2827b3f43ae5bf9720f85e32cc5a13b5443a59697a244da028cd92a206ef63be30bcc8188b74694293d753ace4d97d3752c6340dd5754a766c5d7cbc1744b7b646b7790232; TSae7facce027=08dc579c15ab2000042b75bdfce30f7422cb192c810e1caaef9f50b46bbafdac6a4ce0bfc0b3c06608a9af4beb1130006036341d54c61184cd4a30a8daa76380929342b562775c034923057110c24839a9dafbbbb89b16d8f8ece9690e847ec6; bm_s=YAAQHfU3F0GgLcWWAQAAtfER0wPqHaFtGCtcuVGBdnsWX6+g88T94fA3V5ZnQQrZlfyQLoxpf/0nhwg+lO+3WeTFjaXwiGmAD7MhNZtD5Xv7bksHzSiM+B5wXI+88WGzZwPAy32zGe/IUtbx/xE5fRYcC/l+DCdCs+DJDh2N6iv5syYyBSGy1PMskmC6GWiGJrWdcIh08qeQlSsEJMrEXaRs9ojTz8i4owtMuAISM7o2k8tzi1jgzB6VIPBvgJRWJi18dZYTyo0o4E/CMKMHQ3xKUYvK8iOi6I+CUggkyJ/PoFZfqdyEs1NafKMF7ht3gdT5+bWU6HB/81FGjLUD8GrbOzueY/A0G4MuLaHMAQAVo3MLIKTN+MEHavBmMLjCztPe1/tOBEoJZxcazcEswJTKRNCux6sbu70vLDrpfTr8nEfbvHwKTQgrKGtDNJQVfWdWv2nEbwOfz7uDC83qCK4Ygw7o4q+pGQZoNkPw/qyW3uE/XCHbruThShHcmNt3qerkWx8pupbyUHyhKs22ovYyp4hn44NR0iuJXJAF9NHYFzdDXfedpQ==; bm_sv=D15AA891F1013CA464092B941D3D953D~YAAQHfU3F0KgLcWWAQAAtfER0xvRXh4xGYNSR8kQDTQ55/ZHGqpvg9hdv4jL6R9gf9GJIEues85GG2jbOGvqFGRoH7goQvLwqzo8ipGEHu6slOf7GwzfHmMfy5Jxvm3dgH8fXA9pshNE5cIsZf6kjyn3/qUOZZcONS+RprQKpTpsPH3g5Kqn6hnAwcvaHbxg55F6xpUdEPqZ7oQC1EY1PEzVL5CWWlCZFZwJ13TzEZue57JCc0TZJVa3ifoczA==~1; _ga=GA1.2.1924808953.1745559993; _gat_UA-68002030-1=1; ImpressionCookie=0; cto_bundle=YdrE0l8xMmlrb2RVJTJCaGVRVCUyRnQwdmNjNXZ2N3ZaYWhiaHhJRkhlMkpHUHhORjlaS3JXRDFWdnhaWUkyUjBuRjAySnl2Vk9WWk0wbE9tTjZINlQ0d3d3YWhTOExHTHRtQjd2bU1TNDBIaVNOTHBoN1hDTGx4Rm1ENlFVT3FialNVUk45YW56JTJCalpnRmY0b083YzNCM001bW5FMFElM0QlM0Q; f5avr0627051897aaaaaaaaaaaaaaaa_cspm_=ACIEAMFDEBHFJGGOCDNNIENHJDMNMFNMAFFOLAMHNDOFIALDHDJELDOKLHLBFGPIGEICGOGPBNBIJDHJENDACCGPBBLLDPILMGJLOGIAMGFEGBKDAPELMBJIFIILOIOB; _ga_X3MNHK0RVR=GS2.1.s1747297644$o23$g0$t1747297654$j50$l0$h0$di8Mv2InhZ-Nr7Osimzm47edgBcSWM0v2dQ',
# }
# # response = requests.get('https://www.ajio.com/p/700410195002', cookies=cookies, headers=headers)
# url='https://www.ajio.com/p/701021402005'
# try:
#     # id_counter += 1
#
#     response = requests.get(url, headers=headers , impersonate="Chrome110")
#     if response.status_code == 200:
#         html_content = response.text
#         match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});\s*</script>', html_content, re.DOTALL)
#         time.sleep(2)  # Add 2 seconds delay after each retry
#
#         if match:
#             json_str = match.group(1)
#             try:
#                 data = json.loads(json_str)
#                 product_id = url.split('/')[-1]
#
#                 product_mrp = data.get("product", {}).get("productDetails", {}).get("variantOptions",[])
#                 mrp = "N/A"
#                 discount = "N/A"
#                 selling_price = "N/A"
#                 for m in product_mrp:
#                     code = m.get("code")
#                     if code == product_id:
#                         selling_price = m.get("priceData").get("value")
#                         discount_str = m.get("priceData").get("discountPercent", "")
#                         discount_match = re.search(r'\d+', discount_str)
#                         discount = int(discount_match.group()) if discount_match else "N/A"
#                         mrp = m.get("wasPriceData", {}).get("value")
#
#                 # product_name = products.get("selected", {}).get("modelImage", {}).get("altText", "N/A")
#                 # product_name = re.sub(r'\s+', ' ', product_name).strip()  # Replace multiple spaces with single space
#                 available_sizes_list = []
#
#                 sizes = data.get("product", {}).get("productDetails", {}).get("variantOptions", [])
#                 for size in sizes:
#                     try:
#                         qualifiers = size.get("variantOptionQualifiers", [])
#                         for qualifier in qualifiers:
#                             name = qualifier.get("name", "").lower()
#                             if name.startswith("size"):
#                                 value = qualifier.get("value")
#                                 if value:
#                                     available_sizes_list.append(value)
#                                 break  # Found size, skip other qualifiers in this variant
#                     except Exception:
#                         continue  # Catch-all in case of unexpected data issues
#                 seen = set()
#                 available_sizes_list = [s for s in available_sizes_list if not (s in seen or seen.add(s))]
#
#                 # Join with " | " if more than one, otherwise keep as single
#                 available_sizes = " | ".join(available_sizes_list) if available_sizes_list else "N/A"
#                 best_price = data.get("product", {}).get("productDetails", {}).get("potentialPromotions", [])[0]
#                 max_savings = best_price.get("maxSavingPrice")
#                 # Round up if max_savings is a number
#                 if max_savings is not None:
#                     best_price = round(max_savings)
#                 manufacturing_info_countryOfOrigin = data.get("product", {}).get("productDetails", {}).get(
#                     "mandatoryInfo", [])
#                 for item in manufacturing_info_countryOfOrigin:
#                     if item.get("key") == "Country Of Origin":
#                         country = item.get("title", "N/A")
#                         break
#
#                 mandatory_info = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])
#
#                 manufacturing_info = "N/A"
#
#                 for item in mandatory_info:
#                     if item.get("key") == "Marketed By":
#                         manufacturing_info = item.get("title")
#                 product_id_1 = url.split('/')[-1]
#                 discount = "N/A"
#                 selling_price = "N/A"
#                 for m in product_mrp:
#                     code = m.get("code")
#                     if code == product_id_1:
#                         selling_price = m.get("priceData").get("value")
#                         discount_str = m.get("priceData").get("discountPercent", "")
#                         discount_match = re.search(r'\d+', discount_str)
#                         discount = int(discount_match.group()) if discount_match else "N/A"
#                         mrp = m.get("wasPriceData", {}).get("value")
#
#                 import re
#
#                 products = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])[0]
#                 product_name = products.get("selected", {}).get("modelImage", {}).get("altText", "N/A")
#                 product_name = re.sub(r'\s+', ' ', product_name).strip()
#                 variantOptions = data.get("product", {}).get("productDetails", {}).get("brandName")
#                 productid = str(product_id)
#                 catalogid = productid
#                 source = "Ajio"
#
#                 # scraped_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#                 product_image = products.get("selected", {}).get("modelImage", {}).get("url", "N/A")
#
#                 high_resolution_images = ""
#                 images = data.get("product", {}).get("productDetails", {}).get("images", [])
#                 # product_image = data.get("product", {}).get("productDetails", {}).get("product_image", "")
#
#                 if not images:
#                     high_resolution_images = "N/A"
#                 else:
#                     seen_urls = set()
#
#                     for image in images:
#                         url = image.get("url")
#                         if not url:
#                             continue
#
#                         # Skip if same as product_image
#                         if url == product_image:
#                             continue
#
#                         # Skip any MODEL.jpg image
#                         if url.endswith("-MODEL.jpg"):
#                             continue
#
#                         # Skip duplicates
#                         if url in seen_urls:
#                             continue
#
#                         # Check resolution
#                         match = re.search(r'-(\d+)Wx(\d+)H-', url)
#                         if match:
#                             width = int(match.group(1))
#                             if width >= 1000:
#                                 seen_urls.add(url)
#                                 high_resolution_images += url + " | "
#
#                     high_resolution_images = high_resolution_images.rstrip(" | ")
#
#                     if not high_resolution_images:
#                         high_resolution_images = "N/A"
#
#                     description_data = data.get("product", {}).get("productDetails", {}).get("featureData", [])
#                     descri_list = []
#                     for desc in description_data:
#                         feature_values = desc.get("featureValues", [])
#                         attr_name = desc.get("catalogAttributeName", "").strip()  # e.g., 'length', 'neckline'
#
#                         for d in feature_values:
#                             value = d.get("value", "").strip()
#                             if value:
#                                 descri_list.append(f"{attr_name}: {value}")
#                     description_text = " | ".join(descri_list)
#
#                     product_deta = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])
#                     mandatory_info_list = []
#                     for details in product_deta:
#                         title = details.get("title", "")
#                         if title:
#                             mandatory_info_list.append(title)
#                     mandatory_info_text = " | ".join(mandatory_info_list)
#
#                     final_description = description_text + " | " + mandatory_info_text if description_text else mandatory_info_text
#
#                     specification_data = data.get("product", {}).get("productDetails", {}).get("featureData", [])
#                     specification_data_list = []
#                     for desc in specification_data:
#                         feature_values = desc.get("featureValues", [])
#                         for d in feature_values:
#                             descri = d.get("value", "")
#                             if descri:
#                                 specification_data_list.append(descri)
#                     specification_text = " | ".join(descri_list)
#
#                 print( "Mrp" , mrp,"selling price : ",selling_price,"Discount",discount,"Sizes",available_sizes,"Best Price",best_price,manufacturing_info,"Product Image",product_image,"images :",high_resolution_images)
#             except Exception as e:
#                 print(e)
# except Exception as e:
#     print(e)
