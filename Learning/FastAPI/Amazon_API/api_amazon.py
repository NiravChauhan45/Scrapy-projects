import json
import re

from parsel import selector, Selector

from curl_cffi import requests

cookies = {
    'csm-sid': '438-5519700-8111034',
    'session-id': '262-9182643-2277461',
    'i18n-prefs': 'INR',
    'lc-acbin': 'en_IN',
    'ubid-acbin': '261-2268315-9543000',
    'session-token': 'nvjiqxoRuudeJOpXZ9N4eFcSkBsgjdb5Xg6gHwBWgnrNl24Fskl2FrO1zXClmOLFANWTXEluHn6kcCAU6+71Yo8YNaVUudQ+Y3mjLUQKsrP3+LNfwzkKNUVxJUXInfzMcypR+iPhP75jRE2jnezuYMg1u0+3TTXg+rSJEnogW5KqzdGfNA/hsh9C07XKYKU49mW7OrYjBOkXdkphxouspnCDX0dJxTkxHVNPXY5BaOzEE6/RKyO+y6lom9NGH6yUdSnjzAyKRYE0OD+9PNZJVrdcQVyAdeK/myulYflWYBjHxeh9mzTMmW3ICuzwFAITclwze0zKZRbwoxfaJ5C+1ckUdVuOkNdZ',
    'csm-hit': 'tb:XRBZ3SP0APBVDZGREP6R+s-XRBZ3SP0APBVDZGREP6R|1755076349398&t:1755076349398&adb:adblk_no',
    'session-id-time': '2082787201l',
    'rxc': 'AGFKW8NBYN5mDdPvDZk',
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
    'rtt': '100',
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
    # 'cookie': 'csm-sid=438-5519700-8111034; session-id=262-9182643-2277461; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=261-2268315-9543000; session-token=nvjiqxoRuudeJOpXZ9N4eFcSkBsgjdb5Xg6gHwBWgnrNl24Fskl2FrO1zXClmOLFANWTXEluHn6kcCAU6+71Yo8YNaVUudQ+Y3mjLUQKsrP3+LNfwzkKNUVxJUXInfzMcypR+iPhP75jRE2jnezuYMg1u0+3TTXg+rSJEnogW5KqzdGfNA/hsh9C07XKYKU49mW7OrYjBOkXdkphxouspnCDX0dJxTkxHVNPXY5BaOzEE6/RKyO+y6lom9NGH6yUdSnjzAyKRYE0OD+9PNZJVrdcQVyAdeK/myulYflWYBjHxeh9mzTMmW3ICuzwFAITclwze0zKZRbwoxfaJ5C+1ckUdVuOkNdZ; csm-hit=tb:XRBZ3SP0APBVDZGREP6R+s-XRBZ3SP0APBVDZGREP6R|1755076349398&t:1755076349398&adb:adblk_no; session-id-time=2082787201l; rxc=AGFKW8NBYN5mDdPvDZk',
}

params = {
    'th': '1',
}
url = 'https://www.amazon.in/dp/B08GZ6QNTC'
response = requests.get(url, params=params, cookies=cookies, headers=headers)
new_selector = Selector(text=response.text)

item = dict()

try:
    item['product_id'] = url.split("/dp/")[-1]
    item['product url'] = f"https://www.amazon.in/dp/{item['product_id']}"
except:
    item['product_id'] = "N/A"
    item['product_url'] = "N/A"

product_name = ''
try:
    item['product_name'] = new_selector.xpath("//h1[@id='title']//text()").get('').strip()
    if not item['product_name']:
        product_name = new_selector.xpath('//span[@id="productTitle"]//text()').get('').strip()
        item['product_name'] = re.sub("\\s+", " ", product_name).strip()
except:
    item['product_name'] = "N/A"

try:
    item['avg_rating'] = new_selector.xpath("//*[@id='acrPopover']/@title").get()
except:
    item['avg_rating'] = "N/A"

try:
    item['number_of_ratings'] = new_selector.xpath('//*[@id="acrCustomerReviewText"]/text()').get('')
except:
    item['number_of_ratings'] = "N/A"

try:
    item['price'] = new_selector.xpath(
        "//div[@class='a-section a-spacing-none aok-align-center aok-relative']//span[@class='a-price-whole']/text()").get()
    if item['price']:
        item['price'] = item['price'].replace(",", "")
except:
    item['price'] = "N/A"

try:
    mrp_list = new_selector.xpath("//div[@class='centerColAlign']//span[@class='a-offscreen']/text()").getall()
    if mrp_list:
        mrp = [mrp.strip() for mrp in mrp_list if mrp.strip()]
        item['mrp'] = "".join(mrp).replace("₹", "").replace(",", "")
except:
    item['mrp'] = "N/A"

try:
    discount_list = new_selector.xpath(
        "//div[@class='centerColAlign']//span[contains(@class,'savingsPercentage')]/text()").getall()
    discount = "".join(
        [discount.strip().replace("-", "").replace("%", "") for discount in discount_list if discount.strip()])
    item['discount'] = discount
except:
    item['discount'] = "N/A"
# Todo: Brand Name
try:
    brand_name = new_selector.xpath("//a[@id='bylineInfo']/text() | //a[contains(text(),'Brand')]/text()").get()
    if brand_name:
        brand_name = brand_name.replace("Brand:", "").strip()
    item['brand_name'] = brand_name
except:
    item['brand_name'] = "N/A"

# Todo: about_this_item
try:
    about_this_list = []
    about_this_dict = {}
    li_list = new_selector.xpath('//*[contains(text(),"About this item")]//parent::div[@id="feature-bullets"]//li')
    if not li_list:
        li_list = new_selector.xpath('//*[contains(text(),"About this item")]//parent::div//li')
    if not li_list:
        li_list = new_selector.xpath('//div[@id="feature-bullets"]//li')
    for li in li_list:
        li_text = li.xpath(".//text()").get('').strip()
        if li_text:
            about_this_list.append(li_text)
    # if about_this_list:
    #     for index, item in enumerate(about_this_list, start=1):
    #         about_this_dict[f'Bullet Point - {index}'] = item
    item['about_this_item'] = about_this_list
except:
    item['about_this_item'] = "N/A"

try:
    if isinstance(product_name, str):
        if "women" in product_name.lower():
            target_gender = "Women"
        elif "men" in product_name.lower():
            target_gender = "Men"
except:
    target_gender = "N/A"

try:
    image_list = list()
    videos_list = list()
    image_json = re.findall("jQuery.parseJSON\(\'(.*?)\'\);", response._text)
    image_json2 = new_selector.xpath('//script[contains(text(),"ImageBlockATF")]//text()').get()

    if image_json:
        image_dict = list()
        try:
            image_json = json.loads(image_json[0])
        except:
            image_json = json.loads(image_json[0].replace(b'\\\'', b''))
        if 'colorToAsin' in image_json:
            asin = re.findall(r',&quot;url&quot;:&quot;https://www.amazon.in/dp/(.*?)&quot;,&quot;',
                              response.text)
            asin = asin[0].split('?')[0]
            for key in image_json['colorToAsin']:
                # if response.meta['asin'] in image_json['colorToAsin'][key]['asin'] and key in image_json[
                if asin in image_json['colorToAsin'][key]['asin'] and key in image_json[
                    'colorImages']:
                    image_dict = image_json['colorImages'][key]
                    break

        for img in image_dict:

            hiRes = img.get('hiRes')
            large = img.get('large')
            thumb = img.get('thumb')

            if hiRes:
                image_list.append(hiRes)
            elif large:
                image_list.append(large)
            elif thumb:
                image_list.append(thumb)

        try:
            vid_ls = image_json['videos']
        except:
            vid_ls = []

        if vid_ls:
            for vurl in vid_ls:
                vid_link = vurl.get('url')
                if vid_link:
                    videos_list.append(vid_link)
    if image_json2 and not image_list:
        try:
            # image_json2=image_json2.split('var data =')[1].split("'colorToAsin")[0].replace('\\n','').replace('\\t','').replace('\\r','').strip().replace("'colorImages'",'"colorImages"').replace("'initial'",'"initial"')
            image_json2 = image_json2.split("{ 'initial':")[1].split("'colorToAsin")[0].replace('\\n',
                                                                                                '').replace(
                '\\t', '').replace('\\r', '').strip()
            if image_json2.endswith('},'):
                image_json2 = image_json2[:-2]
            # forimg=json.loads(image_json2)

            image_list_d = json.loads(image_json2)

            for img in image_list_d:
                hiRes = img.get('hiRes')
                large = img.get('large')
                thumb = img.get('thumb')

                if hiRes:
                    image_list.append(hiRes)
                elif large:
                    image_list.append(large)
                elif thumb:
                    image_list.append(thumb)

        except:
            ...

except:
    image_list = "N/A"

try:
    item['image_url'] = image_list[0]
    item['images'] = image_list
except:
    item['image_url'] = "N/A"
    item['images'] = "N/A"

try:
    additional_services = dict()
    if new_selector.xpath('//div[@id="ppdBundlesEnhancedBox"]//span[@id="ppdBundlesHeading"]'):
        for bundle in new_selector.xpath('//div[@id="ppdBundlesEnhancedBox"]//span[@id="ppdBundlesHeading"]'):
            bundle_text = bundle.xpath('./b/text()').get()
            bundle_price = bundle.xpath(
                './..//following-sibling::div//span[@id="ppdBundlesPriceValueId"]/text()').get()
            if bundle_text and bundle_price:
                additional_services['service_name'] = bundle_text.strip()
                additional_services['service_price'] = bundle_price.strip()

    if additional_services:
        item['additional_services'] = additional_services
except:
    item['additional_services'] = "N/A"

try:
    is_sold_out = ""
    if ' In stock ' in new_selector._text or 'In stock' in new_selector._text:
        item['is_sold_out'] = "False"
    else:
        item['is_sold_out'] = "True"
except:
    item['is_sold_out'] = "N/A"

print(json.dumps(item))
