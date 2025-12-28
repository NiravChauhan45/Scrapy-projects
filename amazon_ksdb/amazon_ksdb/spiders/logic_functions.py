import json
import re
from datetime import datetime

from loguru import logger


# Todo: clean extra space
def clean_space(text):
    if isinstance(text, str):
        text = re.sub("\\s+", " ", text)
    return text.strip()


# Todo: Product Name
def get_product_name(response):
    try:
        product_name = response.xpath("//h1[@id='title']/span[@id='productTitle']/text()").get()
        if product_name:
            product_name = clean_space(product_name)
    except:
        product_name = "N/A"
    return product_name


# Todo: Product Id
def get_product_id(product_url):
    if "/dp/" in product_url:
        product_id = ""
        try:
            product_id = product_url.split('/dp/')[-1]
        except Exception as e:
            print(e)
        return product_id


# Todo: Scraped_date (YYYY-MM-DD H:M:S)
def get_scraped_date():
    scraped_date = ''
    try:
        scraped_date = datetime.now().strftime("%Y_%m_%d %H:%M:%S")
    except Exception as e:
        logger.error(e)
    return scraped_date


# Todo: Main Image Url
def get_main_image_url(response):
    image_list = list()
    videos_list = list()
    image_json = re.findall(b"jQuery.parseJSON\(\'(.*?)\'\);", response.body)
    image_json2 = response.xpath('//script[contains(text(),"ImageBlockATF")]//text()').get()

    try:
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

                # if 'hiRes' in img:
                #     image_list.append(img['hiRes'])
                # elif 'large' in img:
                #     image_list.append(img['large'])
                # else:
                #     image_list.append(img['thumb'])
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

        if image_list:
            image_url = image_list[0]
            return image_url
        else:
            image_url = '//*[@class="imgTagWrapper"]/img/@src|//*[@class="image-wrapper"]/img/@src'
            if not image_url:
                image_url = '//*[@id="ebooks-img-canvas"]//img[@id="ebooksImgBlkFront"]/@src|//*[@id="img-wrapper"]//img/@src'
            return image_url

    except:
        pass
