import requests
from parsel import Selector
from loguru import logger
import json
import re
from fastapi import FastAPI
import uvicorn

app = FastAPI()


def get_response(product_url, max_retries=5, delay=1):
    cookies = {
        '_gcl_au': '1.1.2034444316.1765174144',
        'FPID': 'FPID2.2.JqBFpWlx8Ekcz3iivvFRlqcmkZXaNhTR1odHNrfELAQ%3D.1765172366',
        'FPLC': 'Tgv8faj59G%2Fs2vAEWMgW8vlAJf1tqz5uqERFFNc0qipK56IK0ebK82aaixE8dDrUAoE4j%2F3cMFs6ZBfHH8ue01jSH3D0RTjAcsx2H4%2ByIuPZ8VYnq0KTRgRW5zOzWQ%3D%3D',
        '__cq_uuid': 'bcb2VLigA8O6GGagVDLLm9ZwYo',
        '__stripe_mid': '364fab9e-cd15-4a1a-8689-6915eeb3abb4362c1b',
        '__stripe_sid': 'ad39290e-9bbc-493e-94ff-722b1a165360c3b05c',
        'dwac_0644a165d42080eb78142cac75': 'PcLMlrgDgQOmvI1Uq89CACFtNCyEhEpeVnM%3D|dw-only|||USD|false|US%2FPacific|true',
        'cqcid': 'absH9el6oYZpmGsfkYuC88SOGV',
        'cquid': '||',
        'sid': 'PcLMlrgDgQOmvI1Uq89CACFtNCyEhEpeVnM',
        'newCustomer': 'new',
        'dwpersonalization_914668167e2805280fee994f0c25aa1b': '9770b5c81785d7c175a3a6665420260206030000000',
        'dwanonymous_914668167e2805280fee994f0c25aa1b': 'absH9el6oYZpmGsfkYuC88SOGV',
        '__cq_dnt': '0',
        'dw_dnt': '0',
        'dwsid': '_an4FA-iNIk1-i40Qb_pFuEGAK4zJf_UxTXGtPRpEUHPzrgBG7H-a9I81-wbjFPkay9klIVQEartJ9BtiDBrLA==',
        '_cfuvid': '7udDs59UoYGvJo8RsuUThOCjqgKxt8JrWnAwTWJUwl8-1765174147227-0.0.1.1-604800000',
        'capi_lift_channel': 'Referral',
        'lux_uid': '176517415395246616',
        '_pin_unauth': 'dWlkPU0yRmlOelF6TVdNdE1EWmhaaTAwTWpNeUxUZzVZV0V0TUdZeVpqQTJNelkwT1RObA',
        '__attentive_id': 'f6703669f0bd4067ae6ec5f189ad0c0b',
        '__attentive_session_id': '6d8282add846483fb475c095f02eda53',
        '_attn_': 'eyJ1Ijoie1wiY29cIjoxNzY1MTc0MTYwODI0LFwidW9cIjoxNzY1MTc0MTYwODI0LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImY2NzAzNjY5ZjBiZDQwNjdhZTZlYzVmMTg5YWQwYzBiXCJ9In0=',
        '__attentive_cco': '1765174160829',
        '_fbp': 'fb.1.1765174161078.535208241593282659',
        '_gid': 'GA1.2.2105813566.1765174162',
        '_gat_UA-26305999-1': '1',
        '__cq_bc': '%7B%22bhcn-reformation-us%22%3A%5B%7B%22id%22%3A%220103940%22%2C%22type%22%3A%22vgroup%22%2C%22alt_id%22%3A%220103940CVD%22%7D%5D%7D',
        '_tt_enable_cookie': '1',
        '_ttp': '01KBY98C91CNX92R0Q9SV00FR9_.tt.1',
        'scarab.visitor': '%224C1967A116946649%22',
        'scarab.profile': '%22g%252F0103940%7C1765174161%22',
        '__attentive_ss_referrer': 'ORGANIC',
        '__attentive_dv': '1',
        'GlobalE_CT_Data': '%7B%22CUID%22%3A%7B%22id%22%3A%22956473441.525640755.1008%22%2C%22expirationDate%22%3A%22Mon%2C%2008%20Dec%202025%2006%3A39%3A28%20GMT%22%7D%2C%22CHKCUID%22%3Anull%2C%22GA4SID%22%3A789853891%2C%22GA4TS%22%3A1765174168494%2C%22Domain%22%3A%22www.thereformation.com%22%7D',
        'GlobalE_Full_Redirect': 'false',
        'refWelcomeModal': 'true',
        'GlobalE_Data': '%7B%22countryISO%22%3A%22MP%22%2C%22cultureCode%22%3A%22en-GB%22%2C%22currencyCode%22%3A%22USD%22%2C%22apiVersion%22%3A%222.1.4%22%7D',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Mon+Dec+08+2025+11%3A39%3A37+GMT%2B0530+(India+Standard+Time)&version=202503.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=c248c6b8-836a-4d5b-adf1-bdb0638f4603&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false',
        '__cq_seg': '0~0.44!1~-0.06!2~-0.20!3~0.37!4~-0.43!5~0.41!6~0.09!7~0.25!8~0.42!9~-0.15!f0~15~5!n0~1',
        '_ga': 'GA1.1.1770795153.1765172366',
        '_ga_7BLG0E10ZJ': 'GS2.1.s1765172365$o1$g1$t1765174177$j60$l0$h2108608928',
        '_ga_M3XP66ENNS': 'GS2.1.s1765170575$o4$g1$t1765174177$j60$l0$h0',
        '_uetsid': '704e4890d3fc11f0895d4fb241cc7599',
        '_uetvid': '704ec140d3fc11f0bdeaa3384ac3eec6',
        'fs_lua': '1.1765174177439',
        'fs_uid': '#o-19Y02A-na1#2c2a9058-359d-40e0-96ed-a5cfc93d1eed:668d2fb8-9414-4890-8db0-53728125add3:1765170568835::17#/1796283716',
        '__attentive_pv': '2',
        'GlobalE_Analytics': '%7B%22merchantId%22%3A1008%2C%22shopperCountryCode%22%3A%22MP%22%2C%22cdn%22%3A%22https%3A%2F%2Fwebservices.global-e.com%2F%22%2C%22clientId%22%3A%2205405c73-750d-4dbe-8208-c72281860390%22%2C%22sessionId%22%3A%223e236b97-f78b-4e94-ae37-959ff74ac328%22%2C%22sessionIdExpiry%22%3A1765175980680%2C%22configurations%22%3A%7B%22eventSendingStrategy%22%3A0%7D%2C%22featureToggles%22%3A%7B%22FT_3DA%22%3Afalse%2C%22FT_3DA_UTM_SOURCE_LIST%22%3A%5B%5D%2C%22FT_3DA_STORAGE_LIFETIME%22%3A4320%2C%22FT_BF_GOOGLE_ADS%22%3Afalse%2C%22FT_BF_GOOGLE_ADS_LIFETIME%22%3A30%2C%22isOperatedByGlobalE%22%3Afalse%7D%2C%22lockBrowsingStartOnSessionId%22%3A%223e236b97-f78b-4e94-ae37-959ff74ac328%22%2C%22dataUpdatedAt%22%3A1765174180680%7D',
        'ttcsid': '1765174161724::T1OdTvpuds_IIf8MOw-l.1.1765174186364.0',
        'ttcsid_C9J3CFRC77U92U7NNRQG': '1765174178236::ZhwaXRnGPhFGvpdcF2JQ.1.1765174186364.1',
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
                selector = Selector(text=response.text)
                return selector

            print(f"[{attempt}/{max_retries}] Status {response.status_code}, retrying in {delay}s...")

        except requests.RequestException as e:
            print(f"[{attempt}/{max_retries}] Request failed: {e}. Retrying in {delay}s...")

        time.sleep(delay)

    print("❌ Failed after max retries.")
    return None


def cleanText(text):
    text = re.sub("\s+", " ", text)
    text = re.sub("[\n\t]", "", text)
    text = text.strip("-")
    return text.strip()


def getPname(json_data, response):
    name = json_data.get('name')
    if name:
        name = cleanText(name)
        return name
    else:
        name = response.xpath('//meta[@property="og:title"]/@content').get()
        if name:
            name = cleanText(name)
            return name
        else:
            return "N/A"


def getImageUrl(response):
    image_url_list = response.xpath('//button[@class="product-gallery__button set--w-100"]/img/@data-srcset').getall()
    if image_url_list:
        for image in image_url_list:
            image_url = image.split('500w')[-1]
            image_url = image_url.replace('2x', '').strip("',").strip()
            return image_url
    else:
        return "N/A"


def getSku(product_url, json_data):
    try:
        sku = json_data.get('sku')
    except:
        sku = ''

    if sku:
        return sku
    else:
        return product_url.split('%20/')[-1].replace('.html', '')


def getPID(sku):
    try:
        pid = sku[:-3] if len(sku) == 10 else sku
        return pid
    except:
        return "N/A"


def getInStock(response):
    if 'InStock' in response._text:
        return "True"
    else:
        return "False"


def getSalePrice(response):
    sale_price = response.xpath(
        '//div[@class="pdp__header"]//div[contains(@class,"price__sales sales")]//@content').getall()
    if sale_price:
        if len(sale_price) == 2:
            sale_price = sale_price[-1]
        sale_price = "".join(sale_price)
        sale_price = sale_price.replace('null', '')
        if sale_price:
            return cleanText(sale_price).replace("$", "").replace(".00", '')
        else:
            return None
    else:
        sale_price = response.xpath(
            '//div[@class="pdp__header"]//div[contains(@class,"price__sales sales")]//span[@class="price--formated"]/text()').getall()
        if sale_price:
            sale_price = "".join(sale_price)
            return cleanText(sale_price).replace("$", "").replace(".00", '')
        else:
            return None


def getPrice(response):
    price = response.xpath(
        '//div[@class="pdp__header"]//span[@class="price__original text-decoration--strike strike-through list is-sale"]/span[@class="price--formated"]/text()').getall()
    if price:
        price = "".join(price).replace("$", "").replace(".00", "")
        return cleanText(price)
    else:
        price = response.xpath(
            '//div[@class="pdp__header"]//span[@class="price__original text-decoration--strike strike-through list is-sale"]/span[@class="price--reduced"]/text()').getall()
        if price:
            price = "".join(price).replace("$", "").replace(".00", "")
            return cleanText(price)
        else:
            price = response.xpath('//span[@itemprop="highprice"]/@content').get()
            if price:
                return price
            else:
                price = response.xpath('//span[@itemprop="highprice"]/span[@class="price--formated"]/text()').get(
                    '').strip()
                price = price.replace('$', '')
                if price:
                    return price.replace(".00", "")
                else:
                    return None


def getDiscount(mrp, price):
    if 'N/A' not in str(mrp) and 'N/A' not in price:
        discount = float(mrp) - float(price)
        if discount == 0.0:
            return "N/A"
        return int(discount)
    else:
        return "N/A"


def getBrand(json_data):
    if json_data:
        brand = json_data.get('brand')
        if brand:
            brand_name = brand.get('name')
            return cleanText(brand_name)
        else:
            return "N/A"
    else:
        return "N/A"


def getColour(response):
    colour_name = response.xpath('//span[@class="product-attribute__selected-value"]/text()').get()
    if colour_name:
        colour_name = cleanText(colour_name)
        return colour_name
    else:
        colour_name = response.xpath(
            '//label[@class="product-attribute__label product-attribute__label--color font-size--12 margin-b--8"]//span[@class="product-attribute__selected-value"]/text()').getall()
        if colour_name:
            colour_name = "".join(colour_name)
            colour_name = cleanText(colour_name)
            return colour_name
        else:
            return "N/A"


def getAlternateImageUrls(response):
    image_url_list = response.xpath(
        '//button[@class="product-gallery__button set--w-100"]/img/@data-srcset | //button[@class="pdp__get-the-look-thumbnail-image"]/img/@src').getall()
    if image_url_list:
        image_url_lst = []
        for image in image_url_list:
            if image:
                image_url = image.split('500w')[-1]
                image_url = image_url.replace('2x', '').strip("',").strip()
                image_url_lst.append(image_url)
        return " | ".join(image_url_lst[1:])
    else:
        image_urls = response.xpath(
            '//div[@class="cloudinary-data-container d-none visually-hidden"]/@data-cloudinary').get()
        if image_urls:
            image_url_lst = []
            json_data = json.loads(image_urls)
            for image in json_data.get('images').get('imageURLs'):
                image_url = image.get('url')
                if image_urls:
                    image_url_lst.append(image_url)
            if image_url_lst:
                return " | ".join(image_url_lst[1:])
            else:
                return "N/A"
        else:
            return "N/A"


def getCategory(response, name):
    category_list = response.xpath('//a[@class="breadcrumbs__anchor link link--secondary"]//text()').getall()
    category_list = [cleanText(category).replace("/", "") for category in category_list if
                     'Home' != cleanText(category) and name not in cleanText(category)]
    category_list = [cat.strip() for cat in category_list if cat.strip()]
    if category_list:
        return "/".join(category_list)
    else:
        return "N/A"


def getDescription(response):
    description_list = []

    # Todo: Description
    long_description = response.xpath('//div[@data-product-component="long-description"]//text()').getall()
    if long_description:
        long_description = "".join(long_description)
        long_description = cleanText(long_description)
        description_list.append(long_description)

    # Todo: Fit & Details
    fit_and_details = response.xpath('//div[@data-product-component="details-accordion"]')
    if fit_and_details:
        # Todo: Title
        fit_and_details_title = fit_and_details.xpath("./button//text()").getall()
        if fit_and_details_title:
            fit_and_details_title = "".join(fit_and_details_title)
            fit_and_details_title = cleanText(fit_and_details_title)

        # Todo: Description
        fit_and_details_description = fit_and_details.xpath(
            './/div[@class="pdp__product-accordion__content-inner"]//text()').getall()
        if fit_and_details_description:
            fit_and_details_description = "".join(fit_and_details_description)
            fit_and_details_description = cleanText(fit_and_details_description)

        fit_and_details_dict = f"{fit_and_details_title}: {fit_and_details_description}"
        if fit_and_details_dict:
            description_list.append(fit_and_details_dict)

    # Todo: Material & care
    material_and_care = response.xpath('//div[@data-product-component="materials-accordion"]')
    if material_and_care:
        # Todo: Title
        material_and_care_title = material_and_care.xpath("./button//text()").getall()
        if material_and_care_title:
            material_and_care_title = "".join(material_and_care_title)
            material_and_care_title = cleanText(material_and_care_title)

        # Todo: Description
        material_and_care_description = material_and_care.xpath(
            './/div[@class="pdp__product-accordion__content-inner"]//text()').getall()
        if material_and_care_description:
            material_and_care_description = "".join(material_and_care_description)
            material_and_care_description = cleanText(material_and_care_description)

        material_and_care_dict = f"{material_and_care_title}: {material_and_care_description}"
        if material_and_care_dict:
            description_list.append(material_and_care_dict)

    # Todo: sustainability impact
    sustainability_impact = response.xpath('//div[@data-product-component="sustainability-accordion"]')
    if sustainability_impact:
        # Todo: Title
        sustainability_impact_title = sustainability_impact.xpath("./button//text()").getall()
        if sustainability_impact_title:
            sustainability_impact_title = "".join(sustainability_impact_title)
            sustainability_impact_title = cleanText(sustainability_impact_title)

        # Todo: Description
        sustainability_impact_description = sustainability_impact.xpath(
            './/div[@class="pdp__product-accordion__content-inner"]//text()').getall()
        if sustainability_impact_description:
            sustainability_impact_description = "".join(sustainability_impact_description)
            sustainability_impact_description = cleanText(sustainability_impact_description)

        sustainability_impact_dict = f"{sustainability_impact_title}: {sustainability_impact_description}"
        if sustainability_impact_dict:
            description_list.append(sustainability_impact_dict)

    if description_list:
        return " | ".join(description_list)
    else:
        return "N/A"


def getSize(response, json_data):
    offer_data = json_data.get('offers')
    try:
        if offer_data:
            size_list = []
            for variant in offer_data:
                size = variant.get('size')
                size_list.append(size)
            return " | ".join(size_list)
        else:
            size_list = response.xpath('//div[@class="pdp_sizepicker"]//span[@data-sizepicker-value]/text()').getall()
            if size_list:
                return " | ".join(size_list)
            else:
                return "N/A"
    except:
        return "N/A"


def getVariantPrice(sale_price, response):
    size_list = response.xpath('//div[@class="pdp_sizepicker"]//span[@data-sizepicker-value]/text()').getall()
    variant_price_lst = []
    if size_list:
        for size in size_list:
            variant_price = f"{size}-{sale_price}"
            variant_price_lst.append(variant_price)
        return " | ".join(variant_price_lst)
    else:
        return "N/A"


def getVariantData(sale_price, mrp, colour, json_data):
    offer_data = json_data.get('offers')
    variant_data_list = []
    try:
        if offer_data:
            for offer in offer_data:
                variant_data_dict = dict()
                variant_data_dict['available'] = True if 'InStock' in offer.get('availability') else False
                variant_data_dict['Price'] = int(sale_price)
                variant_data_dict['Mrp'] = mrp
                variant_data_dict['size'] = offer.get('size')
                variant_data_dict['colour'] = colour
                variant_data_dict['sku'] = offer.get('sku')
                variant_data_list.append(variant_data_dict)
            return variant_data_list
        else:
            return variant_data_list
    except:
        return variant_data_list


@app.get("/items")
def product_details(product_url: str):
    item = dict()

    # Todo: Get Response
    response = ''
    try:
        response = get_response(product_url)
    except Exception as error:
        logger.exception(error)

    # Todo: json_data
    json_data = ''
    try:
        json_data = response.xpath('//script[@type="application/ld+json"]/text()').get('').strip()
        json_data = json.loads(json_data)
    except Exception as error:
        logger.error(error)

    # Todo: Name
    item['Name'] = getPname(json_data, response)

    # Todo: Image URL
    item['Image URL'] = getImageUrl(response)

    # Todo: SKU
    sku = getSku(product_url, json_data)
    item['SKU'] = sku

    # Todo: PID
    item['PID'] = getPID(sku)

    # Todo: IsInStock
    item['IsInStock'] = getInStock(response)

    # Todo: Price Currency
    item['Price Currency'] = ""

    # Todo: Sale Price
    item['Sale Price'] = getSalePrice(response) if getSalePrice(response) else "N/A"

    # Todo: Final Price
    item['Final Price'] = getSalePrice(response) if getSalePrice(response) else "N/A"

    # Todo: Mrp
    if getPrice(response):
        if isinstance(getPrice(response), str):
            if "." in getPrice(response):
                item['Mrp'] = float(getPrice(response))
            else:
                item['Mrp'] = int(getPrice(response))
    else:
        if 'N/A' not in getSalePrice(response):
            item['Mrp'] = int(getSalePrice(response))
        else:
            item['Mrp'] = "N/A"

    # Todo: Price Currency
    item['Price Currency'] = "USD" if 'N/A' not in str(item['Mrp']) else "N/A"

    # Todo: Discount
    item['Discount'] = getDiscount(item['Mrp'], item['Sale Price'])

    # Todo: Manufacturer
    item['Manufacturer'] = "N/A"

    # Todo: Brand
    item['Brand'] = getBrand(json_data)

    # Todo: Colour
    item['Colour'] = getColour(response)

    # Todo:Num Ratings
    item['Num Ratings'] = "N/A"

    # Todo: Average Ratings
    item['Average Ratings'] = "N/A"

    # Todo: Gender
    item['Gender'] = "N/A"

    # Todo: Alternate Image URLs
    item['Alternate Image URLs'] = getAlternateImageUrls(response)

    # Todo: Link URL
    item['Link URL'] = product_url

    # Todo: Category
    item['Category'] = getCategory(response, item['Name'])

    # Todo: Description
    item['Description'] = getDescription(response)

    # Todo: Size
    item['Size'] = getSize(response, json_data)

    # Todo: Varint_Price
    item['Varint_Price'] = getVariantPrice(item['Sale Price'], response)

    # Todo: Variant_data
    item['Variant_data'] = getVariantData(item['Sale Price'], item['Mrp'], item['Colour'], json_data)

    # Todo: policy
    item['policy'] = []

    item_json = cleanText(json.dumps(item, indent=4))
    return item


if __name__ == '__main__':
    # product_url = 'https://www.thereformation.com/products/%20/1314728.html'
    # product_url = "https://www.thereformation.com/products/%20/1317018OPW.html"
    # product_url = "https://www.thereformation.com/products/%20/1317184CRM.html"
    # product_url = "https://www.thereformation.com/products/%20/1311588BIU.html"
    # item = product_details(product_url)
    uvicorn.run("pdp_api:app", host="127.0.0.1", port=8000)
