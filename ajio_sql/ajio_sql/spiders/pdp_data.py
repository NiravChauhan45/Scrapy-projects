import gzip
import json
import os
import random
import re
import time
from datetime import datetime
from parsel import Selector
import pymysql
import ajio_sql.db_config as db
from ajio_sql.items import AjioSqlItem
from typing import Any

import json_repair

from ajio_sql.config.database_config import ConfigDatabase
import scrapy
from scrapy import cmdline


def pagesave(page_save_path, product_id, response):
    # page save
    try:
        if not os.path.exists(page_save_path):
            os.makedirs(page_save_path)
        main_path = f'{page_save_path}{str(product_id)}.html.gz'
        if not os.path.exists(main_path):
            with gzip.open(main_path, 'wb') as f:
                f.write(response.text.encode('utf-8'))
            print(f"page save for this {product_id}")
    except Exception as e:
        print(e)


def make_pagesave(response, self_PAGE_SAVE_PATH, pagesave_path, product_id, cur, conn):
    if response.status == 200:
        if not os.path.exists(pagesave_path):
            os.makedirs(self_PAGE_SAVE_PATH, exist_ok=True)
            with gzip.open(pagesave_path, mode="wb") as file:
                file.write(response.body)
        else:
            print("Path already exists..!!")
    else:
        update_query = f"""UPDATE {db.input_name}_inputs SET status = %s WHERE product_id = %s"""
        data = (response.status, product_id)  # set age=30 for user with id=1
        cur.execute(update_query, data)
        conn.commit()
        print(f"❌ Failed: {product_url} - Status: {response.status}")


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"
    allowed_domains = ["www.ajio.com"]
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    conn = pymysql.connect(
        database="ajio",
        user="root",
        password="actowiz",
        host="localhost"
    )
    cur = conn.cursor()

    def __init__(self, start, end, **kwargs: Any):
        super().__init__(**kwargs)
        self.start_id = start
        self.end = end
        self.today_date = datetime.now().strftime('%d_%m_%Y')
        # self.page_save_path = f"D:\\Nirav Chauhan\\Pagesave\\Ajio\\{self.today_date}\\"
        self.page_save_path = f"E:\\Nirav\\Project_page_save\\Ajio\\{self.today_date}\\"
        self.db = ConfigDatabase(database="ajio", table=f"{db.input_name}_inputs")
        # self.db = ConfigDatabase(database="ajio", table=f'osm_nsm_inputs')
        self.headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    handle_httpstatus_list = [404, 500, 401]

    def start_requests(self):
        results = self.db.fetchResultsfromSql(conditions={'status': 'Pending'}, start=self.start_id, end=self.end)
        for result in results:
            product_id = result['product_id']
            product_url = f'https://www.ajio.com/p/{product_id}'

            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            main_path = f'{self.page_save_path}{str(product_id)}.html.gz'
            if os.path.exists(main_path):
                yield scrapy.Request(url=f'file:///{main_path}',
                                     dont_filter=True,
                                     callback=self.parse,
                                     meta={"impersonate": self.browser,
                                           'product_url': product_url, 'product_id': product_id
                                           })
            else:
                yield scrapy.Request(url=product_url, headers=headers,
                                     meta={"impersonate": self.browser, "product_id": product_id,
                                           "product_url": product_url}, dont_filter=True)

    def parse(self, response, **kwargs):
        product_id = response.meta.get('product_id')
        product_url = response.meta.get('product_url')

        pagesave_path = f"{self.page_save_path}{product_id}.html.gz"

        if not os.path.exists(pagesave_path):
            if response.status == 200 and str(product_id) in response.text:
                pagesave_path = f"{self.page_save_path}{product_id}.html.gz"
                make_pagesave(response, self.page_save_path, pagesave_path, product_id, self.cur, self.conn)
        else:
            response = gzip.decompress(response.body)
            response = response.decode('utf-8')
            response = Selector(text=response)

        try:

            try:
                html_content = response.text
            except:
                html_content = response._text

            match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});\s*</script>', html_content,
                              re.DOTALL)
            time.sleep(1)
            if match:
                json_str = match.group(1)
                try:
                    data = json.loads(json_str)
                    # file_name = f"{product_id}.json.gz"
                    #
                    # os.makedirs(self.page_save_path, exist_ok=True)
                    # file_path = os.path.join(self.page_save_path, file_name)
                    #
                    # if os.path.exists(file_path):
                    #     print(f"File already exists: {file_path}")
                    #     with open(file_path, 'r', encoding='utf-8') as f:
                    #         # Todo: existing_data already usable
                    #         try:
                    #             data = json.load(f)
                    #         except json.JSONDecodeError as e:
                    #             data = json_repair.loads(f)
                    # else:
                    #     with open(file_path, 'w', encoding='utf-8') as f:
                    #         json.dump(main_data, f, ensure_ascii=False, indent=4)
                    #     print(f"Saved new file: {file_path}")
                    #     data = main_data

                    products = ''
                    try:
                        products = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])[0]
                    except Exception as e:
                        print(e)

                    product_name = ''
                    # Todo: product_name
                    try:
                        product_name = products.get("selected", {}).get("modelImage", {}).get("altText", "N/A")
                        product_name = re.sub(r'\s+', ' ', product_name).strip()
                    except:
                        product_name = 'N/A'

                    # Todo:brandName
                    brandName = ''
                    try:
                        brandName = data.get("product", {}).get("productDetails", {}).get("brandName")
                    except:
                        brandName = "N/A"

                    # Todo : productid & catalogid
                    productid = ''
                    catalogid = ''
                    try:
                        productid = str(product_id)
                        catalogid = productid
                    except:
                        productid = 'N/A'
                        catalogid = 'N/A'

                    # Todo: source
                    source = "Ajio"

                    # Todo: scraped_date
                    scraped_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Todo: product_image
                    product_image = ""
                    try:
                        product_image = products.get("selected", {}).get("modelImage", {}).get("url", "N/A")
                    except:
                        product_image = "N/A"

                    # Todo: stock_status
                    try:
                        stock_status = products.get("selected", {}).get("stock", {}).get("stockLevelStatus",
                                                                                         "").lower()
                    except:
                        stock_status = "N/A"

                    # Todo: is_sold_out
                    is_sold_out = ''
                    try:
                        is_sold_out = "True" if "outofstock" in stock_status else "False"
                    except:
                        is_sold_out = "N/A"

                    # selling_price = products.get("selected", {}).get("priceData", {}).get("value", "N/A")

                    # Todo: avg_rating
                    try:
                        avg_rating = data.get("product", {}).get("productDetails", {}).get("ratingsResponse",
                                                                                           {}).get(
                            'aggregateRating', {}).get('averageRating')
                    except:
                        avg_rating = "N/A"

                    # Todo: ratings
                    try:
                        ratings = data.get("product", {}).get("productDetails", {}).get("ratingsResponse", {}).get(
                            'aggregateRating', {}).get('numUserRatings')
                    except:
                        ratings = "N/A"

                    country_code = "IN"

                    rate = ratings

                    high_resolution_images = ""
                    # Todo: Images
                    try:
                        images = data.get("product", {}).get("productDetails", {}).get("images", [])

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
                    except:
                        high_resolution_images = "N/A"

                    # Todo: description_text
                    description_text = ""
                    try:
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
                    except:
                        description_text = "N/A"

                    # Todo: mandatory_info_text
                    mandatory_info_text = ""
                    try:
                        product_deta = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])
                        mandatory_info_list = []
                        p_json_data = response.xpath("//script[contains(text(),'hasVariant')]/text()").get()
                        if p_json_data:
                            j_data = json.loads(p_json_data)
                            product_code_list = j_data.get('hasVariant')
                            for product_code in product_code_list:
                                product_code = product_code.get('sku')
                                mandatory_info_list.append(f"product code: {product_code}")
                                if product_code:
                                    break
                        for details in product_deta:
                            title = details.get("title", "")
                            key = details.get("key", "")
                            if title:
                                mandatory_info_list.append(f"{key}: {title}")
                        mandatory_info_text = " | ".join(mandatory_info_list)
                    except:
                        mandatory_info_text = "N/A"

                    final_description = description_text + " | " + mandatory_info_text if description_text else mandatory_info_text

                    # Todo: specification_data
                    specification_text = ""
                    try:
                        specification_data = data.get("product", {}).get("productDetails", {}).get("featureData",
                                                                                                   [])
                        specification_data_list = []
                        for desc in specification_data:
                            feature_values = desc.get("featureValues", [])
                            for d in feature_values:
                                descri = d.get("value", "")
                                if descri:
                                    specification_data_list.append(descri)
                        specification_text = " | ".join(specification_data_list)
                    except:
                        specification_text = "N/A"

                    product_code = product_id

                    # Todo:offers_data
                    offers_data = ""
                    try:
                        offers = data.get("product", {}).get("productDetails", {}).get("potentialPromotions", [])
                        if offers:
                            for offer in offers:
                                description = offer.get('description', '')
                                clean_description = re.sub(r'<.*?>', '', description).replace("ViewAll Products",
                                                                                              "").replace(
                                    "ViewAll Products>", "").replace(".>", "")
                                clean_description = clean_description.replace("View All Products", "").replace(
                                    ". >", "")
                                offer_details = f"Code: {offer.get('code')} | Description: {clean_description.strip()} | Max Saving Price: {offer.get('maxSavingPrice')}"  # Details URL: {offer.get('detailsURL')}
                                offers_data += offer_details + " | "
                        offers_data = offers_data.rstrip(" | ")
                    except:
                        offers_data = "N/A"

                    # Todo: best_price = ""
                    best_price = ""
                    try:
                        best_price = \
                            data.get("product", {}).get("productDetails", {}).get("potentialPromotions", [])[0]
                        max_savings = best_price.get("maxSavingPrice")
                        # Round up if max_savings is a number
                        if max_savings is not None:
                            # best_price = round(max_savings)
                            best_price = max_savings
                    except:
                        best_price = "N/A"

                    # Todo: available_sizes_list
                    available_sizes_list = []
                    try:
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
                    except:
                        available_sizes_list = "N/A"

                    # Todo: available_sizes
                    available_sizes = ''
                    try:
                        seen = set()
                        available_sizes_list = [s for s in available_sizes_list if not (s in seen or seen.add(s))]
                        available_sizes = " | ".join(available_sizes_list) if available_sizes_list else "N/A"
                    except:
                        available_sizes = "N/A"

                    formatted_offers = ""
                    # Todo: formatted_offers
                    try:
                        bank = data.get("product", {}).get("productDetails", {}).get("prepaidOffers", [])
                        for ban in bank:
                            bank_id = ban.get("bankId", "")
                            bank_name = ban.get("bankName", "")
                            description = ban.get("description", "")
                            offer_code = ban.get("offerCode", "")
                            offer_amount = ban.get("offerAmount", 0)
                            threshold_amount = ban.get("thresholdAmount", 0)
                            # tnc_url = ban.get("tncUrl", "")
                            # logo_url = ban.get("logo", "")
                            start_date = ban.get("startDate", 0)
                            end_date = ban.get("endDate", 0)
                            # offer_detail = f"{bank_id} | {bank_name} | {description} | {offer_code} | {offer_amount} | {threshold_amount} | {tnc_url} | {logo_url} | {start_date} | {end_date}"
                            offer_detail = f"{bank_id} | {bank_name} | {description} | {offer_code} | {offer_amount} | {threshold_amount} | {start_date} | {end_date}"

                            if formatted_offers:
                                formatted_offers += " | "
                            formatted_offers += re.sub("\\s+", " ", offer_detail)
                    except:
                        formatted_offers = "N/A"

                    # Todo: more_colors
                    more_colors = ""
                    color_var = ""
                    try:
                        color_variant = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])[0]
                        color_var = color_variant.get("selected", {}).get("code")
                        more_color = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
                        colors_list = []
                        for color in more_color:
                            colour_name = color.get("selected", {}).get("color")
                            if colour_name:
                                colors_list.append(colour_name)
                        more_colors = " | ".join(colors_list) if colors_list else "N/A"
                    except:
                        more_colors = "N/A"

                    # Todo: return_policies_string
                    return_policies_string = ""
                    try:
                        return_policies = []
                        return_policy = data.get("product", {}).get("productDetails", {}).get("baseOptions", [])
                        for policy in return_policy:
                            for opt in policy.get("options", []):
                                pol = opt.get("returnContent")
                                if pol:
                                    return_policies.append(pol)

                        return_policies_string = " | ".join(return_policies)
                    except:
                        return_policies_string = "N/A"

                    country = "N/A"  # default fallback
                    try:
                        manufacturing_info_countryOfOrigin = data.get("product", {}).get("productDetails", {}).get(
                            "mandatoryInfo", [])
                        for item in manufacturing_info_countryOfOrigin:
                            if item.get("key") == "Country Of Origin":
                                country = item.get("title", "N/A")
                                break
                    except:
                        country = "N/A"

                    # Todo: category_heirarchy
                    heirarchy_joined = ""
                    try:
                        breadcrumbs = data.get("product", {}).get("productDetails", {}).get("rilfnlBreadCrumbList",
                                                                                            {}).get(
                            "rilfnlBreadCrumb", [])
                        heirarchy_list = [category.get("name", "") for category in breadcrumbs]
                        heirarchy_joined = " | ".join(heirarchy_list)
                    except:
                        heirarchy_joined = "N/A"

                    mandatory_info = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])

                    manufacturing_info_info = "N/A"
                    try:
                        for item in mandatory_info:
                            if item.get("key") == "Marketed By":
                                manufacturing_info_info = item.get("title")
                    except:
                        manufacturing_info_info = "N/A"

                    # Todo: net_qty
                    net_qty = "N/A"
                    try:
                        mandatory_info = data.get("product", {}).get("productDetails", {}).get("mandatoryInfo", [])
                        net_qty = None
                        for info in mandatory_info:
                            if info.get("key") == "Net Qty":
                                net_qty = info.get("title")
                                break
                    except:
                        net_qty = "N/A"

                    mrp = "N/A"
                    discount = "N/A"
                    selling_price = "N/A"
                    product_mrp = data.get("product", {}).get("productDetails", {}).get("variantOptions", [])
                    for m in product_mrp:
                        selling_price = m.get("priceData").get("value")
                        discount_str = m.get("priceData").get("discountPercent", "")
                        discount_match = re.search(r'\d+', discount_str)
                        discount = int(discount_match.group()) if discount_match else "N/A"
                        mrp = m.get("wasPriceData", {}).get("value")
                        break

                    item = AjioSqlItem()
                    item['product_id'] = str(productid)
                    item['catalog_name'] = product_name
                    item['catalog_id'] = str(catalogid)
                    item['source'] = "Ajio"
                    item['scraped_date'] = re.sub("\\s+", " ", scraped_date).strip()
                    item['product_name'] = product_name
                    item['image_url'] = product_image
                    item['category_hierarchy'] = heirarchy_joined
                    item['product_price'] = selling_price
                    item['arrival_date'] = "N/A"
                    item['shipping_charges'] = "N/A"
                    item['is_sold_out'] = is_sold_out
                    item['discount'] = discount if discount else "N/A"
                    item['mrp'] = mrp
                    item['page_url'] = "N/A"
                    item['product_url'] = product_url
                    item['number_of_ratings'] = rate if rate else "N/A"
                    item['avg_rating'] = avg_rating if avg_rating else "N/A"
                    item["position"] = "N/A"
                    item["country_code"] = country_code
                    item["images"] = high_resolution_images
                    item["Best_price"] = best_price if best_price else "N/A"
                    item["Best_offers"] = offers_data if offers_data else "N/A"
                    item["bank_offers"] = formatted_offers
                    item["product_details"] = final_description
                    item["specifications"] = specification_text
                    item["rating"] = avg_rating if avg_rating else "N/A"
                    item["MOQ"] = "1"  # net_qty if net_qty else "N/A"
                    item["brand"] = brandName if brandName else "N/A"
                    item["product_code"] = str(product_code)
                    item["Available_sizes"] = available_sizes if available_sizes else "N/A"
                    item["sellerPartnerId"] = "N/A"
                    item["seller_return_policy"] = return_policies_string if return_policies_string else "N/A"
                    item["manufacturing_info_packerInfo"] = "N/A"
                    item["manufacturing_info_seller_name"] = "N/A"
                    item[
                        "manufacturing_info_importerInfo"] = manufacturing_info_info if "Imported By" in response.text else "N/A"
                    item["manufacturing_info_countryOfOrigin"] = country if country else "N/A"
                    item[
                        "manufacturing_info_manufacturerInfo"] = manufacturing_info_info if manufacturing_info_info else "N/A"
                    item["More_colours"] = more_colors if more_colors else "N/A"
                    item["variation_id"] = color_var if color_var else "N/A"
                    yield item
                except json.JSONDecodeError as je:
                    print(f"❌ JSON decoding error for {product_id}: {je}")
            else:
                print(f"❌ Could not find JSON for {product_id}")
        except Exception as e:
            print(f"❌ Exception for product ID {product_id}: {e}")


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpDataSpider.name} -a start=6503 -a end=6503".split())
