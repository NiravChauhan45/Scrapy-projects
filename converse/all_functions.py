import json
import os
from datetime import datetime
import requests
import time
import gzip

from duckdb.duckdb import description
from parsel import Selector
import re
import hashlib
import db_config as db
from loguru import logger


def get_response(product_url, max_retries=5, delay=1):
    cookies = {
        'bm_sv': '74784A9F2937C7073D5C385C987E34DF~YAAQsiTDF+YKQKqaAQAAZTOQvx1NdY4Hew7u7hU99vgf3cp66qUvKmT8A5SiPvz616Uktx4yx6FgyhB1OxVaAHf2qjy2NQ6j/ItshcHmMgohB0yr/qoov59k1JpP4X+NSvMS0fnJJCbno4DgnZ+OeVO1akNfCJmpATsFxOL0VM2TI0oyQTh6sYCd5xm7XHoUwu4SNihMYNYVikjCCJNXOsS4Ytl9GcQEb+PLjDte60llCRHHAJNx7AJCItqv8nFVpP4J~1',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(product_url, cookies=cookies, headers=headers, timeout=10)

            if response.status_code == 200:
                return response

            print(f"[{attempt}/{max_retries}] Status {response.status_code}, retrying in {delay}s...")

        except requests.RequestException as e:
            print(f"[{attempt}/{max_retries}] Request failed: {e}. Retrying in {delay}s...")

        time.sleep(delay)

    print("❌ Failed after max retries.")
    return None


def make_pagesave(response, hash_id, current_date):
    pagesave_path = fr"E:\Nirav\Project_page_save\converse\{current_date}"
    full_path = fr"{pagesave_path}\{hash_id}.html.gz"
    if response:
        if not os.path.exists(pagesave_path):
            os.makedirs(pagesave_path, exist_ok=True)
            with gzip.open(full_path, mode="wb") as file:
                file.write(response.content)
        else:
            os.makedirs(pagesave_path, exist_ok=True)
            with gzip.open(full_path, mode="wb") as file:
                file.write(response.content)


def parseResponse(response):
    selector = Selector(text=response.text)
    return selector


def getWebName():
    return "Converse"


def getPid(json_data, product_url):
    # product_id = json_data.get('product_id')
    # product_id = json_data.get('product_master_id')
    product_id = json_data.get('product_sku_id')
    if product_id:
        product_id = "".join(product_id).strip()
        return product_id
    else:
        product_id = product_url.split("?")
        product_id = product_id[0]
        product_id = product_id.split("/")[-1]
        product_id = product_id.split(".")[0]
        return product_id.strip()


def cleanText(text):
    try:
        text = re.sub("\s+", " ", text)
        text = re.sub("[\n\t]", "", text)
        return text.strip()
    except Exception as e:
        print(e)


def getPname(json_data, response):
    product_name = json_data.get("page_context_title")
    if product_name:
        product_name = cleanText(product_name)
        return product_name
    else:
        product_name = response.xpath("//h1[contains(@class,'pdp-primary-information__product-name')]/text()").get()
        product_name = cleanText(product_name)
        return product_name


def getShorDescription(response):
    short_description = response.xpath(
        '//div[@class="pdp-primary-information__short-description-container"]//p/text()').get()
    if short_description:
        short_description = cleanText(short_description)
        return short_description
    else:
        return None


def getDescription(response):
    # description_list = response.xpath('//div[@id="pdp-more-info"]//text()').getall()
    # if description_list:
    #     description_list = [cleanText(description).strip() for description in description_list if
    #                         cleanText(description).strip()]
    # if description_list:
    #     description = "".join(description_list)
    #     description = cleanText(description)
    #     description = description.replace("More Info + Less Info -", "")
    #     return description.replace("  ", " ").strip()
    # else:
    #     return None

    head_title = response.xpath('//h2[@class="pdp-tab__title text-align--sm-center"]//text()').getall()
    if head_title:
        head_title = "".join(head_title)
        head_title = cleanText(head_title)
    else:
        head_title = ''

    pdp_content = response.xpath('//div[@class="pdp-tab__content text-align--sm-center"]//text()').getall()
    if pdp_content:
        pdp_content = "".join(pdp_content)
        pdp_content = cleanText(pdp_content)
    else:
        pdp_content = ""

    main_text = f"{head_title}: {pdp_content}"

    author_title = response.xpath('//div[@id="pdp-more-info__model-info-anchor"]//text()').getall()
    if author_title:
        author_title = "".join(author_title)
        author_title = cleanText(author_title)
    else:
        author_title = ""

    listing_text = response.xpath('//li[@class="pdp-tab__list-item pdp__list-item--bulleted"]//text()').getall()
    if listing_text:
        listing_text = "".join(listing_text)
        listing_text = cleanText(listing_text)
    else:
        listing_text = ""

    list_text = f"{author_title}: {listing_text}"

    # Todo: what are model
    what_title = response.xpath("//div[contains(text(),'What Our Models Are Wearing')]/text()").get()
    if what_title:
        what_title = cleanText(what_title)

    product_content = response.xpath('//div[@class="pdp-tab__content"]//text()').getall()
    p_content = []
    if product_content:
        product_content = [p_content.append(pro_con) for pro_con in product_content if pro_con not in p_content]
        product_content = [cleanText(con).strip() for con in p_content if cleanText(con).strip()]
        product_content = " ".join(product_content)
        product_content = cleanText(product_content)
    else:
        product_content = ""

    what_text = f"{what_title}: {product_content}"

    # Todo: converse essentials
    pdp_header = response.xpath("//div[contains(@class,'pdp-tab--origin-header')]//text()").getall()
    if pdp_header:
        pdp_header = "".join(pdp_header)
        pdp_header = cleanText(pdp_header)
    else:
        pdp_header = ""

    pdp_collab = response.xpath('//div[contains(@class,"pdp-tab--origin-collaboration")]/text()').getall()
    if pdp_collab:
        pdp_collab = "".join(pdp_collab)
        pdp_collab = cleanText(pdp_collab)
    else:
        pdp_collab = ""

    converse_essentials = f"{pdp_header}: {pdp_collab}"

    description = [main_text, list_text, what_text, converse_essentials]
    if description:
        description = [cleanText(des).strip() for des in description if cleanText(des).strip()]

    description = " | ".join(description)
    return description.strip('| :')


def getCategory(json_data):
    l1 = json_data.get('page_category_l1')
    l2 = json_data.get('page_category_l2')
    l3 = json_data.get('page_category_l3')

    category = ''
    if l1:
        category = l1
    if l2:
        category = f"{category}/{l2}"
    if l3:
        category = f"{category}/{l3}"
    if category:
        return category
    else:
        return None


def getImageurl(json_data, response):
    image_url = response.xpath("//meta[@property='og:image']/@content").get()
    if image_url:
        image_url = "".join(image_url)
        return image_url
    else:
        image_url = json_data.get('product_image_url')
        if image_url:
            return image_url
        else:
            image_url = response.xpath('//div[@class="pdp-images__primary-image display--small-up"]/img/@src').get()
            return image_url


def getPrice(json_data, response):
    price = json_data.get('product_msrp_price')
    if price:
        price = "".join(price)
        return price if price else None
    else:
        price_list = response.xpath('//div[@class="product-price"]//text()').getall()
        if price_list:
            price_list = [cleanText(price).strip().replace("$", "") for price in price_list if cleanText(price).strip()]
            return price_list[0]
        else:
            return None


def getPriceCurrency(json_data, response):
    price_currency = json_data.get('region_currency')
    if price_currency:
        return price_currency
    else:
        price_currency = response.xpath('//meta[@itemprop="priceCurrency"]/@content').get()
        return price_currency


def salePrice(json_data, response):
    sale_price = json_data.get("product_display_price")
    if sale_price:
        sale_price = "".join(sale_price)
        return float(sale_price)
    else:
        sale_price_list = response.xpath('//div[@class="product-price"]//text()').getall()
        sale_price_list = [cleanText(price).strip().replace("$", "") for price in sale_price_list if
                           cleanText(price).strip()]
        if sale_price_list:
            return float(sale_price_list[0])
        else:
            return float(0)


def getDiscount(mrp, price):
    discount = float(mrp) - float(price)
    return int(discount)


# https://www.converse.com/shop/p/chuck-taylor-all-star-lift-xxhi-platform-womens-high-top-shoe/A16571C.html?dwvar_A16571C_color=black%2Fblack%2Fblack&dwvar_A16571C_width=standard&styleNo=A16571C&cgid=de-luxe-styles-1
# def getVIsinStock(json_data, response, size):
#     stock_detail = response.xpath('//div[@class="variations__notify-stock-details"]//text()').getall()
#     if stock_detail:
#         stock_detail = [cleanText(stock).strip() for stock in stock_detail if cleanText(stock).strip()]
#         stock_detail = "".join(stock_detail)
#     else:
#         stock_detail = ''
#
#     condition_text = 'product is coming soon'  # The product is sold out.
#     condition_text1 = size
#     try:
#         if condition_text in response.text or 'sold out' in condition_text1.lower() or 'sold out' in stock_detail:
#             return "False"
#         else:
#             return "True"
#     except:
#         if condition_text in response._text or 'sold out' in condition_text1.lower():
#             return "False"
#         else:
#             return "True"


def getIsinStock(json_data, response, size):
    stock_detail = response.xpath('//div[@class="variations__notify-stock-details"]//text()').getall()
    if stock_detail:
        stock_detail = [cleanText(stock).strip() for stock in stock_detail if cleanText(stock).strip()]
        stock_detail = "".join(stock_detail)
    else:
        stock_detail = ''

    condition_text = 'product is coming soon'  # The product is sold out.
    condition_text1 = size
    try:
        if condition_text in response.text or 'sold out' in condition_text1.lower() or 'sold out' in stock_detail:
            return "False"
        else:
            return "True"
    except:
        if condition_text in response._text or 'sold out' in condition_text1.lower() or 'sold out' in stock_detail:
            return "False"
        else:
            return "True"


def getBrand(json_data, response):
    brand = json_data.get("product_brand")
    if brand:
        brand = "".join(brand)
        return brand.strip()
    else:
        brand = response.xpath('//meta[@itemprop="brand"]/@content').get()
        return brand


def getSKU(json_data, product_id):
    sku = json_data.get('product_sku_id')
    if sku:
        sku = "".join(sku)
        return sku.strip()
    else:
        if '_' in product_id:
            sku = product_id.split('_')[0]
            return sku
        else:
            sku = product_id
            return sku


def getColour(json_data, response):
    color = response.xpath('//meta[@itemprop="color"]/@content').get()
    if color:
        return cleanText(color)
    else:
        color = response.xpath('//span[@class="variations__label-value"]/text()').get()
        if color:
            return cleanText(color)
    # color = json_data.get('product_color_family')
    # if color:
    #     color = "".join(color)
    #     return color.strip()
    # else:
    #     color = json_data.get("colorFamily")
    #     if color:
    #         color = "".join(color)
    #         return color.strip()
    #     else:
    #         return None


def getGender(json_data, response):
    condition_text = response.xpath(
        "//p[contains(@class,'pdp-primary-information__badge text--bold text')]/text()").get()
    condition_text = "".join(condition_text)
    condition_text = cleanText(condition_text)
    if 'unisex' in condition_text.lower():
        return "UNISEX"
    elif "women" in condition_text.lower():
        return "FEMALE"
    elif "men" in condition_text.lower():
        return "MALE"
    else:
        return None

    # gender = json_data.get('product_gender_group')
    # if gender:
    #     color = "".join(gender)
    #     return color.strip()
    # else:
    #     gender = json_data.get('product_gender_class')
    #     if gender:
    #         color = "".join(gender)
    #         return color.strip()
    #     else:
    #         return None


def getAlternateImage(response):
    images_url = response.xpath(
        '//img[@class="pdp-images-gallery__media pdp-images-gallery__media--main opacity-up lazyload"]/@data-src').getall()
    if images_url:
        images_url = " | ".join(images_url)
        return images_url
    else:
        short_id = response.xpath('//div[@class="custom-builder custom-builder-hidden"]/@data-converse-custom').get()
        if short_id:
            j_data = json.loads(short_id)
            inspiration_id = j_data.get('inspirationID')
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9',
                'nike-api-caller-id': 'com.converse:commerce.idpdp.desktop',
                'origin': 'https://www.converse.com',
                'priority': 'u=1, i',
                'referer': 'https://www.converse.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            }
            response = requests.get(
                f'https://api.nike.com/customization/consumer_designs/v1?filter=shortId({inspiration_id})',
                headers=headers)
            json_data = json.loads(response.text)
            image_lst = []
            for data in json_data.get('objects'):
                image_list = data.get('imagery')
                for image in image_list:
                    image = image.get('imageSourceURL')
                    image_lst.append(image)
            if image_lst:
                images_url = " | ".join(image_lst[1:])
                return images_url


def getNumRatings(response):
    number_of_rating = response.xpath('//span[@itemprop="reviewCount"]/@data-count').get()
    if number_of_rating:
        return number_of_rating
    else:
        return None


def getSize(response):
    size_list = response.xpath(
        '//select[@id="variationDropdown-size"]//option/text() | //select[@id="variation-dropdown-size"]//option/text()').getall()
    if size_list:
        size_list = [cleanText(size) for size in size_list if 'Pick a Size' not in size]
        return size_list
    else:
        return None


def getAvgRatings(response):
    avg_ratings = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
    if avg_ratings:
        avg_ratings = cleanText(avg_ratings)
        return avg_ratings
    else:
        return None


#
# def getVHashId(product_url, sku, colour, size):
#     hash_id = int(hashlib.md5(bytes(str(product_url) + str(sku) + str(size) + str(colour), "utf8")).hexdigest(), 16) % (
#             10 ** 18)
#     return hash_id


def getHashId(product_url, sku, colour, size):
    hash_id = int(hashlib.md5(bytes(str(product_url) + str(sku) + str(size) + str(colour), "utf8")).hexdigest(), 16) % (
            10 ** 18)
    return hash_id


def insertItemToSql(item, product_url, connection, cursor):
    try:
        # Convert dicts, lists, tuples → JSON
        value_list = [
            json.dumps(v) if isinstance(v, (dict, list, tuple)) else v
            for v in item.values()
        ]

        # Build query dynamically
        field_list = [f"`{field}`" for field in item.keys()]
        placeholders = ["%s"] * len(item)

        fields = ",".join(field_list)
        placeholders_str = ",".join(placeholders)

        insert_db = (
            f"INSERT IGNORE INTO {db.pdp_data} "
            f"({fields}) VALUES ({placeholders_str})"
        )

        # Debug (optional)
        # print("SQL:", insert_db)
        # print("VALUES:", value_list)

        cursor.execute(insert_db, value_list)
        connection.commit()
        logger.info("Item Successfully Inserted...")

        # # Update link status
        # update_sql = f"UPDATE {db.pdp_links} SET status = %s WHERE product_url = %s"
        # update_values = ('Done', product_url)
        # db.cursor.execute(update_sql, update_values)
        # db.connection.commit()
        #
        # logger.success("Item Successfully Updated...")

    except Exception as e:
        logger.error(f"SQL Insert Error: {e}")
