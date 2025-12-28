# main.py
import requests
from fastapi import FastAPI, HTTPException
from parsel import Selector
import uvicorn
import amazon_logic  # Make sure this file is correctly named
from typing import Dict

app = FastAPI(
    title="Amazon Product API",
    description="Fetch product details from Amazon India using product_id (ASIN).",
    version="1.0.0"
)


def get_response(product_id: str) -> str:
    """Fetch Amazon product page HTML synchronously."""
    url = f"https://www.amazon.in/dp/{product_id}"
    cookies = {
        'session-id': '257-8197099-3389816',
        'i18n-prefs': 'INR',
        'lc-acbin': 'en_IN',
        'ubid-acbin': '261-8449377-2614061',
        'x-amz-captcha-1': '1753007490286758',
        'x-amz-captcha-2': 'sVMDHN3I/qrnn/xSWtXxrA==',
        'session-token': 'CrsoZOCSuPedImNHFE0ZYqFoR7m1I9xPiQNJ40CJogBhHdIbQouGe59195UStshqJrc+tOwW5VW9cdQKzgua4N3tT4EC2stFl9czmMQsTFj4jWXUFawYMNQs53MdMHOJVa5fFnWmO80RV4xsuZx0q0nbKRJs84SLhmNOOd9dKMn2JXAXdqoGmYr4HP77txdnFW4tGb7V0ObdP2ERPxUriXpkmiB2XSl0zs6YCwpJMIhBisV6CwM+7u+xSB9VL+O9zdxjMM4PikOnaKc4EkKsFzZZCgVh8jS1vTXt9oYRMWeAu8lKyriS5RNMuZ34WjSG9fTzWj8zXvoEpHtXDPaHV2el+XbT1jkD',
        'session-id-time': '2082787201l',
        'csm-hit': 'tb:7PSPBTSJS99GSY7685MW+s-JQ37GEG9BR9K64TMRTZ8|1755075390145&t:1755075390145&adb:adblk_no',
        'rxc': 'AKsPUdgK58TXiy9gjLM',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'device-memory': '8',
        'downlink': '10',
        'dpr': '1',
        'ect': '4g',
        'priority': 'u=0, i',
        'rtt': '50',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-viewport-width': '1920',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'viewport-width': '1920',
        # 'cookie': 'session-id=257-8197099-3389816; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=261-8449377-2614061; x-amz-captcha-1=1753007490286758; x-amz-captcha-2=sVMDHN3I/qrnn/xSWtXxrA==; session-token=CrsoZOCSuPedImNHFE0ZYqFoR7m1I9xPiQNJ40CJogBhHdIbQouGe59195UStshqJrc+tOwW5VW9cdQKzgua4N3tT4EC2stFl9czmMQsTFj4jWXUFawYMNQs53MdMHOJVa5fFnWmO80RV4xsuZx0q0nbKRJs84SLhmNOOd9dKMn2JXAXdqoGmYr4HP77txdnFW4tGb7V0ObdP2ERPxUriXpkmiB2XSl0zs6YCwpJMIhBisV6CwM+7u+xSB9VL+O9zdxjMM4PikOnaKc4EkKsFzZZCgVh8jS1vTXt9oYRMWeAu8lKyriS5RNMuZ34WjSG9fTzWj8zXvoEpHtXDPaHV2el+XbT1jkD; session-id-time=2082787201l; csm-hit=tb:7PSPBTSJS99GSY7685MW+s-JQ37GEG9BR9K64TMRTZ8|1755075390145&t:1755075390145&adb:adblk_no; rxc=AKsPUdgK58TXiy9gjLM',
    }
    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="Request timed out")
    except requests.RequestException as exc:
        raise HTTPException(status_code=500, detail=f"Request error: {exc}")


def product_logics(html_content, product_id):
    """Extract product details from HTML."""
    response = Selector(text=html_content)

    item = dict()
    # Todo: asin_no
    try:
        asin_no = product_id
        item['asin_no'] = asin_no
    except:
        item['asin_no'] = "N/A"

    # Todo: amazon_fulfilled
    try:
        if response.xpath('//div[@data-feature-name="shippingMessageInsideBuyBox"]//*[@aria-label="Fulfilled"]'):
            item['amazon_fulfilled'] = True
        else:
            item['amazon_fulfilled'] = False
    except Exception as e:
        print(e)

    # Todo: seller_name
    try:
        product_name = response.xpath("//h1[@id='title']//text() | //span[@id='productTitle']//text()").get('').strip()
    except:
        seller_name = "N/A"

    # Todo: Product Rating
    try:
        product_rating = response.xpath("//*[@id='acrPopover']/@title").get()
        # pattern = "(.*)out of 5 stars"
        # match = re.search(pattern, product_rating)
        # if match:
        #     rating = match.group(1).strip()
        # else:
        #     rating = "N/A"
    except:
        product_rating = 'N/A'

    # todo: product total rating
    try:
        no_of_rating_list = response.xpath("//*[@id='acrCustomerReviewText']/text()").getall()
        no_of_rating_lst = "".join(list(set(no_of_rating_list)))
        no_of_rating = no_of_rating_lst.replace(",", "").replace("ratings", "").strip()
    except:
        no_of_rating = "N/A"

    # Todo: seller_feedback
    try:
        seller_name = response.xpath(
            "//span[contains(text(),'Sold by')]/../../following-sibling::div//a/text()").get()
        seller_feedback = get_seller_feedback(seller_name)
    except:
        seller_feedback = "N/A"

    # Todo: item_link
    try:
        item_link = response.url
    except:
        item_link = "N/A"

    # Todo: price
    try:
        price = response.xpath(
            "//div[@class='a-section a-spacing-none aok-align-center aok-relative']//span[@class='a-price-whole']/text()").get()
    except:
        price = "N/A"

    # Todo: Item Name
    try:
        item_lst = []
        item_name_list = response.xpath("//h1[@id='title']//text() | //span[@id='productTitle']//text()").getall()
        for item in item_name_list:
            if item:
                item_lst.append(item.strip())
        item_name = "".join(item_lst)
    except:
        item_name = 'N/A'

    # Todo: Brand Name
    try:
        brand_name = response.xpath("//a[@id='bylineInfo']/text() | //a[contains(text(),'Brand')]/text()").get()
        if brand_name:
            brand_name = brand_name.replace("Brand:", "").strip()
    except:
        brand_name = "N/A"

    # Todo: about_this_item
    try:
        about_this_list = []
        about_this_dict = {}
        li_list = response.xpath('//*[contains(text(),"About this item")]//parent::div[@id="feature-bullets"]//li')
        if not li_list:
            li_list = response.xpath('//*[contains(text(),"About this item")]//parent::div//li')
        if not li_list:
            li_list = response.xpath('//div[@id="feature-bullets"]//li')
        for li in li_list:
            li_text = li.xpath(".//text()").get('').strip()
            if li_text:
                about_this_list.append(li_text)
        if about_this_list:
            for index, item in enumerate(about_this_list, start=1):
                about_this_dict[f'Bullet Point - {index}'] = item
        print(about_this_dict)
    except:
        about_this_item = "N/A"

    # Todo: target gender
    try:
        if isinstance(item_name, str):
            if "women" in item_name.lower():
                target_gender = "Women"
            elif "men" in item_name.lower():
                target_gender = "Men"
    except:
        target_gender = "N/A"

    # Todo:product details
    try:
        product_detail = dict()
        key_list = response.xpath("//*[@id='detailBullets_feature_div']//li//span[@class='a-text-bold']/text()")
        value_list = response.xpath(
            "//*[@id='detailBullets_feature_div']//li//span[@class='a-text-bold']/following-sibling::span/text()").getall()

        # for detail in response.xpath('//*[@id="detailBullets_feature_div"]//li'):
        #     key_list = [re.sub(r'[\n\u200f\u200e]+', '', i).strip() for i in
        #            detail.xpath('.//span[@class="a-text-bold"]/text()').getall() if i.strip()]
        #     key = "".join(key_list).strip()
        #     key = key.replace(":", "").strip()
        #     value_list = detail.xpath('./span[@class="a-text-bold"]/following-sibling::span/text()')
        #     if key and value:
        #         product_detail[key] = value
    except:
        ''


if __name__ == '__main__':
    product_id = "B08GZ6QNTC"
    html_content = get_response(product_id)
    product_data = product_logics(html_content, product_id)
    print(product_data)
# @app.get("/amazon/{product_id}", summary="Get Amazon product details")
# def get_product_details(product_id: str):
#     html_content = get_response(product_id)
#     return product_logics(html_content, product_id)
#

# if __name__ == "__main__":
#     # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
