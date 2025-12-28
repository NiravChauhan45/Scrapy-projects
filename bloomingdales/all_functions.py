import json
import os
from datetime import datetime
from tkinter.messagebox import RETRY

import requests
import time
import gzip
from json_repair import repair_json
from dns.asyncresolver import resolve
from parsel import Selector
import re
import hashlib
import db_config as db
from loguru import logger


def get_response(product_url, max_retries=5, delay=1):
    # Todo: Old Cookies & headers
    cookies = {
        'SignedIn': '0',
        'GCs': 'CartItem1_92_03_87_UserName1_92_4_02_',
        'mercury': 'true',
        'rxVisitor': '1764333272601KSDCSVE14FB76TMT4BK84COMF36P1G7K',
        'BVBRANDID': '26f7a7a7-9c16-4bcb-8823-e599d049f266',
        'BVBRANDSID': 'f3bea4f9-8791-4cd1-95dc-5926433f804f',
        'OptanonAlertBoxClosed': '2025-11-28T12:34:32.863Z',
        'RTD': '0ff60a00ff91c00ff81600ffa2200ffc3600ff70a00ffcc800ff2a90',
        'MISCGCs': '',
        'ak_bmsc': 'FDE09A0ECB3E68A79A8DBD043604388C~000000000000000000000000000000~YAAQB+scuJpbpaSaAQAANkJ1yh3gcv9ZjV9pakYYKFfB/wnPnUq3wl7TwyM7bIMLZ664ZJBoTimQb7gPreDHjl1FY9CghI6srgN3Xc+zUQuz7J/dI/3xpjrt1JqHQaLOLry2UuRyDodRv/AjK0BLdjQsuw08UmocGrGrlObyg2CZ7+44M8Zj0pIanl8ksvSEIwBcRTbps1QaQxzLqodM8iWvhigorlO3qQE/nv4mUaPxiLj1s/N6/gAO2LwyLdWHey8SCW5XbnyNpgkZ3uPmjlPyvNzCsNySvM8rMGXqEM34X455tt5AiHrKwyDwa46P+77yVFjHmMcbItU7HmQ5zTa+Lm9J/ke5UVcu2rQXnhUzsdWEzhtqAiARTr3Tj7J+DQ7Kq7FKrnDq1sXA1le4qnZo8yLGdFpDXa7dF6M4UYggMWF/ymE1PWWMdxnvC+O0XQrY9+LpcOp3gY0A16dpXg0DfRE3pA==',
        'dtPC': '-2874$333272599_856h-vREFSWLUUWRVPWHRKFJBKMIINLWRHAKHW-0e0',
        'rxvt': '1764335074845|1764333272602',
        'dtCookie': 'v_4_srv_5_sn_T3PFC44SQ5LEFO1FKUU65D5TV2UCOII0_app-3A3f16de555ca9d69d_0_ol_0_perc_100000_mul_1',
        'shippingCountry': 'US',
        'currency': 'USD',
        'dtSa': 'true%7CC%7C-1%7CSAVE%20%26%20CONTINUE%7C-%7C1764333279795%7C333272599_856%7Chttps%3A%2F%2Fwww.bloomingdales.com%2Fshop%2Fproduct%2Fbeach-riot-eva-colorblock-rib-bikini-top-emmy-bikini-bottom%3FID%3D4332555%7C%7C%7C%7C',
        'SEED': '-7738721860143462048%7C2153-21%2C2157-21%2C2512-20%7C2139-21%2C2354-21%2C2483-22%2C2503-21%2C2505-21%2C2532-21%2C2546-22%2C2547-21%2C2568-21%2C2570-21%2C2595-21%2C2635-21%2C2641-21%2C2644-21',
        'akavpau_www_www1_bcom': '1764333584~id=f5051b98d5ad1d06b8b98c2c02b1c4df',
        'bm_sz': '9B6C6F309409B37B7340F703C267FEB5~YAAQB+scuAFipaSaAQAAF2t1yh1wvLG4lwdXp9QA9XrPgunOjuEIiTiS5uCG1YFfvqXdt6dQd6dxclVwLYMO1w3EL48A6M/ZhYJ9pGkeQTvpmUinXlb3b1hfDf8jP1BA3f/BLgQ9XbWBhtxi37I9ztM627Z26qDXhXAB89RXsXh3Kk4fEO8Cglvg1EOm8JO65MWV+R+1VMM9vuiXgXgQELRYQ7ojJ2CWh4EK+duwWcos5BsLQyPqOsx1VTV8V7pBOKizOxoG1ZbJklegIc3mnIuL9HTGW9A1kbZqCe+eCenstqA9WPNjn7GPf0Bpfh1sa4fDYjV4QE2p/rCoeB1ikAbQHeUPxl2TF0yEXMwbA28DHb30LMYW5LlZ0Pmf+VChLzX8uCXWrv8gWMjILF0q5WMlnH/famkr7KICcUfBkNULMqH8TSYTKviy/Rf4zFCEpyBYEOXC7gIV7H56+fYUsfSSXukKQSqOJ6P7Lstui/2QHGl8M+6a0mwqEyM4DwbQwvLo3g==~4535604~3355974',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Nov+28+2025+18%3A04%3A47+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A0%2CSPD_BG%3A0%2CC0005%3A0%2CC0004%3A0&AwaitingReconsent=false&geolocation=IN%3BGJ',
        '_abck': 'B951D109C0B16DA4529D1914FDDC82FA~-1~YAAQB+scuFpkpaSaAQAAsnp1yg6yYz1tLqjuFflJMxR8rOZZCB507kWvtTggbZgmYJV1tazfF9fnyRFG2AwEGOTLmKpniT7aqPwiEXWZOwt9SFUBgniVrtIOd1WiTrYKmugA6hH16J3HEnlIVazWXNP9FywlqYIvhKOKck0W37ph91EpupT28gxmFD9daidwHh/ySivvHmu+eVLBidcqnKD0kuw4f1HnDGm1YOhdOzmj6kDeMVrLFRtv71ZLx9Oy3S/2++suCblFoGj4ziRspHXLSBt+TU0GL5p6b4lrYBl6kY7n1fw85t1TwvRq3yjXxEmfKiQwAF8RRUVZhz2BOtvHsDMmgss9Seu8hf+Tcz4zcnJATbEsEoJqoHbyCmrcuO/GgGUm14MSkSXPUqBICnoGhQNjLOV9CDsPde20JQ4YshoRK2vZRnhJMO51A+l4/RmzQUtf5TdfOgAE/toW79QbbrelRjrz8NAHLa5s1ZLrF9Hy92gVBAKWmTf6NeEohxZSmPcLh0YsUEFoopN9BalOgau/luiQ9gYtyvQ8zuJ9WVBb1h0bTwLbhw6HGm8amEsid8ON5jVM383SvPJS2soB5xvQVqps0KiSzxU6X0zKUnx536rCoZsMhZo1eKedCDjdEPvBj106rlIIGMMOyjWdLNF4coacmi2ZfX8SLxYvM7OiR5LT3ZNhRmavoh82wZYIGg==~-1~-1~1764336703~AAQAAAAE%2f%2f%2f%2f%2fwPKtf2Y7r6uYc7sZB2venYZ648O8n1YpHwkoz6xQI4dOcezU1vsFkYZlDXNx2Lih1Aw6V+wlCp1T+hOFsAyMcpm+opa90SYz8vU~1764333348',
        'bm_sv': '611D619D15A72C3DC62530EB01C5F5C7~YAAQB+scuH5kpaSaAQAAU3t1yh1Tk9y0eN/Qyh0AYvgX6LA2sLnlMpmi9vtDNyEkGjR0woANgNz42x7kBCFk+NQ+Tw4tlrBVBi758Ki2wnIbTNVN72HQf0qFLNZzuZcRxOesDF3zSzcLc0AQzAZRB6zuNoBfmfM2CHotZpi+pmAkxV1jgOehlK6YlMfbP0E7NulV5h2du3+4xP7B91dfAw2TRvDXQaq93POlNqDJsQMlf3DwW7DMroZwgUvNROPP9+yshn4fKps=~1',
        'utag_main': 'v_id:019aca72a9490016342fa0eeb8900506f0071067007e8$_sn:1$_se:24$_ss:0$_st:1764335088350$ses_id:1764333103434%3Bexp-session$_pn:10%3Bexp-session$dc_visit:1$dc_event:8%3Bexp-session$dc_region:me-central-1%3Bexp-session',
        'RT': '"z=1&dm=bloomingdales.com&si=bdd95454-1488-4240-99de-fa24d8f05a62&ss=miiudgs6&sl=f&tt=s69&bcn=%2F%2F684d0d48.akstat.io%2F&obo=1&ld=42kd"',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }

    # Todo: New Headers & Cookies
    cookies = {
        'SignedIn': '0',
        'GCs': 'CartItem1_92_03_87_UserName1_92_4_02_',
        'mercury': 'true',
        'rxVisitor': '17644185526810PDTDFNV0KO1O46R2J6D7A5G5GP8UIQB',
        'BVBRANDID': '866cdc7f-dd46-45e2-acc0-346b2d195077',
        'BVBRANDSID': '04981ad7-7b6d-44bd-b7b4-f2beea986e9d',
        'OptanonAlertBoxClosed': '2025-11-29T12:15:52.853Z',
        'RTD': '7b26ad007b26c0a07b26aa307b2602707b26b0807b2616507b2652f07b26bf30',
        'MISCGCs': '',
        'dtPC': '-8003$418552680_251h-vKMCBDPPQQTAFMHILMPJVHRMQGSGQTPMR-0e0',
        'ak_bmsc': 'AAA38087BA3FBB095CA46C1357AD1252~000000000000000000000000000000~YAAQTHxBF7PU08SaAQAAOouKzx3cAuHGRvz4BC246kEbEo/S1O0owPViYhPOyRsM47fXT9hZuC6ndbmE9smAyFz07aZAu0kT56Nl8oVxg7QAyOrPzlrRI1VgiZSfMp35NgtxmCp1IbPOzJRAJiGHM0L9oqIq2mIUQZiBPyPSTLr8m5QZtv51hlYgfJ3COPw2lW3V2zdM6vaLy3LqW/GVPemveUCFg/h0W+6aMBW9BcY7DDPmdXSAq8pNBaxo0zSOrgADP6rHFnY8UheZYlfjkRRasyRnmkvGmGBTn8qcg7UAd/U+IbUiDYx9FzwiSU9cJ/pTIAJtQLW2CpTXEmwKpyLuuk6Grv+HJxJYMZ8pTy1EGU6NLxe/1aqQDtXxuOdIyFFFhEb8WZxnfLqfZNM144W61SWIyk1WOJV7cLtEgFTEgaDhhLSxJl4zl2RwiFIYWYg0n/ASxbf6BoLHV5H9vD6xHDfG',
        'rxvt': '1764420354386|1764418552682',
        'dtCookie': 'v_4_srv_5_sn_V1787OI934ED011ERC08V4H9MNUQ969M_app-3A3f16de555ca9d69d_0_ol_0_perc_100000_mul_1',
        'GCLB': 'CIvR9Kjb7em6ugEQAw',
        'shippingCountry': 'US',
        'currency': 'USD',
        'dtSa': 'true%7CC%7C-1%7CSAVE%20%26%20CONTINUE%7C-%7C1764418566929%7C418552680_251%7Chttps%3A%2F%2Fwww.bloomingdales.com%2Fshop%2Fproduct%2Fdea-luxury-linens-trattegio-embroidered-standard-pillow-sham%3FID%3D5479468%7C%7C%7C%7C',
        'visitor_fpid_id': '454fc757-a514-42be-a062-fd8995dea452',
        'SEED': '-8790739527826125217%7C2153-21%2C2157-21%2C2512-20%7C2139-21%2C2354-21%2C2483-22%2C2503-21%2C2505-21%2C2532-21%2C2546-22%2C2547-21%2C2568-21%2C2570-21%2C2595-21%2C2635-21%2C2641-21%2C2644-21',
        'akavpau_www_www1_bcom': '1764418873~id=2d693b2f029e70b3740e80a8e6ac0c36',
        'bm_sz': 'F9199FFDF9C2904C8B31D2E18AB37407~YAAQTHxBF0nX08SaAQAAFNSKzx1NaYvw+0sEBRi2WrA8WwEsBku0YJro8IVncv/SgazauPaHlap1OtZP/nD+wgRcTFEnQWSfWbt1Smzcm5mP7BiAfDwAspdPx0vntWVgmUjkQAfkespdMQqmxCt3Vhc15Gh1X7pdrhs/LEP0infuGuE+XM5nUt40EVewk5TAyxsC2n9lrHL9jQN06HHMfvW02E1kIRaUHmHYW6dAsRcP2QW6PjKJWnIhxtS8GihgYAhunm5wUZ/rx/oNH2BQ2Ug4jaDQFDyLyUu9V/uXiwFD8lRcNti0Jz5sI4S/AZQepHGFzMt8qCf6IKBrnz9z5rSStL7G9/jIhjjhBRIoLvuf98L0+5CIhCsxfFTPsNmtyHPCsavRMG9aQeQxrMkG5zjPe57AMW5BTuX6JN8y07HV8OdWjinGs+uARiPiefW/rdUhk58Jv24SrVKVoftLme200oS1D0dH/xLyfouXxKoPqg==~3421762~4339509',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Sat+Nov+29+2025+17%3A46%3A12+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A0%2CSPD_BG%3A0%2CC0005%3A0%2CC0004%3A0&AwaitingReconsent=false&geolocation=IN%3BMH',
        'RT': '"z=1&dm=bloomingdales.com&si=9ab00d50-0dcd-4301-9cef-c2be1acdc4bc&ss=mik97zgb&sl=7&tt=dm3&bcn=%2F%2F684d0d49.akstat.io%2F&ld=1gqf"',
        'bm_sv': 'D133F2B74ECC91AD77294D66B5CC0997~YAAQTHxBF+fX08SaAQAA092Kzx1dvFccSPRJ7pCgcAc+c+5xJqn94OgpiM8VSIEOXGYrTKOdgdRPu0GxCO01wE1UzFX1h4tQUVoiomVJzK/vi3dFd+RDjmTUOOXtEEHe9eLgmN7HrqoVFsEoS1sKnKfIbZp2GahReiHm+Prw/lq8ifI6n7NauigzGNmWKUJ4UQa/lmXpi9mphZ9eotufvJga5KG2Yvw8JfnjkWr4tbYVKDzeUBqELs9ob9SkiBSksY+NrBryWVA=~1',
        'utag_main': 'v_id:019acf89d14d001408ada5c6f01e0506f005c06700bd0$_sn:1$_se:23$_ss:0$_st:1764420374703$ses_id:1764418507086%3Bexp-session$_pn:7%3Bexp-session$dc_visit:1$dc_event:6%3Bexp-session$dc_region:me-central-1%3Bexp-session',
        '_abck': '73230118372FAE2003A8B7524579C05F~-1~YAAQTHxBF0jY08SaAQAA2uqKzw5v/7m5Bg6i8wB9gvv7BP+r+MD13Xqe60EOOGSLmMnzhlub5vAh/e4W5WsWBhbVxm6aJsLVVUclFES9i9yV+8WEqL4GKkvE2Hlrau7LbzajO0bX0kfMjuh3HbWAg4ME/hKPgFOI9nFmcSrylU52vEO6k2RQF9TXrPiuW1H1GsLxjCgYNENfnXMQ06UikzVTvpF9bdMQmKWvpwN2n1ChjK/6mK0X7p/aL1gXLs3EyJ/eOPLfzZ3TvHDQLVtx8C+EhqZVF0Ek1Pt0lAg3AdWDEcwzetSOn/fwg0I20DxUMG3ID6csoetLU+B7tBszzZCRxWHAIQJsBNPIj5cU9IqfDoRx3rC9kWVC3aXj9r2ZPGuk+h9jYiHPeibDyJwqYGXSqfoQkb5WYRkixS1ur9EZTv9Y6M5mUz9Vkgp+LnlJl79GxlyqnJUiYF/kviUNC9gu2Meub7wXMvQPpzpsFCdfKBxGTaYH0/ThVknnMdNrkMRIvHg/63stYnj6jt7yZmTbnp/IHlWbAZ+CHAkih7Vbh2I8IHUczwjyN62FyL3npIw/+2zyeNcSM6uXK8LYFxRwYuKQ3XXpVNQT35hGHlIxrsdJ1F64aZbXrzLYlhXLBeDXc/UEUwVEs6L4Gy21ZB5mKyz0Ry3ObuWQP/0KqlstdFDsHL2rrYZZsl+Y0Tn5DAiuKlqnLjsf7BhxyQ==~-1~-1~1764422108~AAQAAAAE%2f%2f%2f%2f%2fwkoJciQxXKJsNu+x9Fjun0zf8eu27myaoWRNIUl7E48YytUtyIpa6Xf4qGz6JbLNiuDR8PaY8DVgTSt16uvApDLjV%2fnrO9ZHc%2fr~1764418639',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(product_url, cookies=cookies, headers=headers, timeout=10)
            # response = requests.get(product_url,  headers=headers, timeout=10)

            if response.status_code == 200:
                return response

            print(f"[{attempt}/{max_retries}] Status {response.status_code}, retrying in {delay}s...")

        except requests.RequestException as e:
            print(f"[{attempt}/{max_retries}] Request failed: {e}. Retrying in {delay}s...")

        time.sleep(delay)

    print("❌ Failed after max retries.")
    return None


def parseResponse(response):
    selector = Selector(text=response.text)
    return selector


def make_pagesave(response, hash_id):
    current_date = datetime.now().strftime("%d_%m_%Y")
    # pagesave_path = fr"E:\Nirav\Project_page_save\{db.database_name}\{current_date}"
    pagesave_path = fr"D:\Nirav Chauhan\Pagesave\{db.database_name}\{current_date}"
    full_path = f"{pagesave_path}\{hash_id}.html.gz"
    if response.status_code == 200:
        if not os.path.exists(pagesave_path):
            os.makedirs(pagesave_path, exist_ok=True)
            with gzip.open(full_path, mode="wb") as file:
                file.write(response.content)
        else:
            with gzip.open(full_path, mode="wb") as file:
                file.write(response.content)


def getWebName():
    return "Bloomingdale"


def getPid(json_data, product_url):
    product_id = json_data.get('productID')
    if product_id:
        return product_id
    else:
        product_id = product_url.split("ID=")
        product_id = product_id[-1]
        return product_id.strip()


def cleanText(text):
    text = re.sub("\s+", " ", text)
    text = re.sub("[\n\t]", "", text)
    text = text.strip("-")
    return text.strip()


def getPname(json_data, response):
    product_name = json_data.get("name")
    if product_name:
        product_name = cleanText(product_name)
        return product_name
    else:
        product_name = response.xpath('//h1[@class="product-title"]/span/text()').get()
        product_name = cleanText(product_name)
        return product_name


def getShorDescription(response):
    short_description = response.xpath('//div[@class="free-shipping"]//text()').get()
    if short_description:
        short_description = cleanText(short_description)
        return short_description
    else:
        return None


def getDescription(response):
    description_list = response.xpath('//section[@id="product-details"]//text()').getall()
    if description_list:
        description = "".join(description_list[1:])
        description = cleanText(description)
        return description.replace("  ", " ")
    else:
        return None


def getCategory(response):
    breadcrumb_list = response.xpath("//script[contains(text(),'BreadcrumbList')]/text()").get()
    try:
        breadcrumb_list = breadcrumb_list.replace("window.__INITIAL_STATE__=", "").strip()
        breadcrumb_list = json.loads(breadcrumb_list)
        breadcrumb_list = breadcrumb_list.get('itemListElement')
        breadcrumb_lst = []
        for breadcrumb in breadcrumb_list:
            breadcrumb = breadcrumb.get('name')
            breadcrumb = breadcrumb.replace("Home", "")
            if breadcrumb:
                breadcrumb_lst.append(breadcrumb)
        if len(breadcrumb_lst) > 0:
            return "/".join(breadcrumb_lst)
        else:
            return breadcrumb_lst if breadcrumb_lst else None
    except:
        breadcrumb_list = repair_json(breadcrumb_list)
        breadcrumb_list = json.loads(breadcrumb_list)
        breadcrumb_list = breadcrumb_list.get('itemListElement')
        breadcrumb_lst = []
        if breadcrumb_list:
            for breadcrumb in breadcrumb_list:
                breadcrumb = breadcrumb.get('name')
                breadcrumb = breadcrumb.replace("Home", "")
                if breadcrumb:
                    breadcrumb_lst.append(breadcrumb)
            if len(breadcrumb_lst) > 0:
                return "/".join(breadcrumb_lst)
            else:
                return breadcrumb_lst if breadcrumb_lst else None
        else:
            return None


def getImageurl(json_data, response):
    image_url = json_data.get('image')
    if image_url:
        return image_url[0]
    else:
        image_url = response.xpath('//img[@class="picture-image loaded stylitics-shop-similar"]/@src').get()
        if image_url:
            return image_url
        else:
            return None


def getPrice(json_data, response):
    return None


def getVPrice(response, variant,variant1):
    try:
        price_list = variant.get('pricing').get('price').get('tieredPrice')
        for price_data in price_list:
            if "Reg. [PRICE]" in price_data.get('label'):
                mrp_price = price_data.get('values')[0]
                price = mrp_price.get('value')
                if price:
                    return float(price)
                else:
                    return None
    except:
        price = response.xpath('//div[@class="price-strike-lg large"]/text()').get()
        if price:
            price = price.replace("$", "")
            price = price.strip()
            price = price.replace(",","")
            return float(price)
        else:
            price = variant1.get('price')
            return float(price) if price else None


def getVPriceCurrency():
    price_currency = "USD"
    return price_currency


def saleVPrice(response, variant,variant1):
    sale_price = ''
    try:
        price_list = variant.get('pricing').get('price').get('tieredPrice')
        for price_data in price_list:
            if "Sale [PRICE]" in price_data.get('label'):
                sale_price = price_data.get('values')[0]
                sale_price = sale_price.get('value')
                return float(sale_price)
            elif price_data.get('label') == "[PRICE]":
                sale_price = price_data.get('values')[0]
                sale_price = sale_price.get('value')
                if sale_price:
                    return float(sale_price)
                else:
                    return None
    except:
        if sale_price:
            return float(sale_price)
        else:
            sale_price = variant1.get('price')
            if sale_price:
                return float(sale_price)
            else:
                return None


def getVDiscount(mrp, sale_price):
    if mrp and sale_price:
        try:
            mrp = mrp.replace(",", "")
            sale_price = sale_price.replace(",", "")
            discount = float(mrp) - float(sale_price)
            return discount
        except:
            discount = float(mrp) - float(sale_price)
            return discount
    else:
        return None


def getVIsinStock(variant):
    in_stock = variant.get('availability')
    if 'InStock' in in_stock:
        return "True"
    else:
        return "False"


def getVSKU(variant, product_id):
    sku = variant.get('SKU')
    if sku:
        return sku
    else:
        return product_id


def getVColour(variant):
    color = variant.get('itemOffered')
    if color:
        return color.get('color')
    else:
        return None


def getVSize(variant):
    size = variant.get('itemOffered')
    if size:
        size = size.get('size')
        return size
    else:
        return None


def getPriceCurrency(json_data, response):
    return None


def salePrice(json_data, response):
    return None


def getDiscount(mrp, price):
    if mrp and price:
        discount = float(mrp) - float(price)
        return discount
    else:
        return None


def getIsinStock(response):
    try:
        if "Sorry, this item is currently unavailable" in response._text:
            return "False"
        else:
            return "True"
    except:
        if "Sorry, this item is currently unavailable" in response.text:
            return "False"
        else:
            return "True"


def getBrand(json_data, response):
    brand = json_data.get("brand")
    if brand:
        brand = brand.get('name')
        return brand.strip()
    else:
        brand = response.xpath('//label[@itemprop="brand"]//text()').get()
        brand = cleanText(brand)
        return brand


def getSKU(json_data, product_id):
    return product_id


def getColour(json_data):
    return None


def getVariationLIst(json_data):
    variation_list = json_data.get('offers')
    if variation_list:
        return variation_list
    else:
        return None


def getGender(json_data):
    gender = json_data.get('product_gender_group')
    if gender:
        color = "".join(gender)
        return color.strip()
    else:
        gender = json_data.get('product_gender_class')
        if gender:
            color = "".join(gender)
            return color.strip()
        else:
            return None


def getAlternateImage(json_data, response, image_url, variant):
    image_url_list = json_data.get('image')
    if image_url_list:
        # Todo: Remove Main ImageUrl
        image_url_list = image_url_list[1:]
        if image_url_list:
            return " | ".join(image_url_list)
        else:
            image_url_list = response.xpath("//li[@class='image-wrapper']//picture/img/@src").getall()
            if image_url_list:
                return " | ".join(image_url_list)
            else:
                image_url_list = response.xpath(
                    "//li[@class='image-wrapper']/div[@class='picture-container']/source/@srcset").getall()
                if image_url_list:
                    return " | ".join(image_url_list)
                else:
                    image_url_list = variant.get('traits').get('colors').get('colorMap')
                    image_list = []
                    for key, value in image_url_list.items():
                        imagery = value.get('imagery')
                        if imagery:
                            for image in imagery.get("images"):
                                image = image.get('filePath')
                                if image not in image_url:
                                    image_url = f"https://images.bloomingdalesassets.com/is/image/BLM/products/{image}"
                                    image_list.append(image_url)
                            return " | ".join(image_list)
                        else:
                            return None

    else:
        image_url_list = response.xpath("//li[@class='image-wrapper']//picture/img/@src").getall()
        if image_url_list:
            return " | ".join(image_url_list)
        else:
            image_url_list = variant.get('traits').get('colors').get('colorMap')
            image_list = []
            for key, value in image_url_list.items():
                imagery = value.get('imagery')
                if imagery:
                    for image in imagery.get("images"):
                        image = image.get('filePath')
                        if image not in image_url:
                            image_url = f"https://images.bloomingdalesassets.com/is/image/BLM/products/{image}"
                            image_list.append(image_url)
                    return " | ".join(image_list)
                else:
                    return None


def getNumRatings(json_data):
    try:
        number_of_rating = json_data.get('aggregateRating').get("reviewCount")
    except:
        number_of_rating = None

    if number_of_rating:
        return number_of_rating
    else:
        return None


def getAvgRatings(json_data):
    try:
        avg_rating = json_data.get('aggregateRating').get("ratingValue")
    except:
        avg_rating = None

    if avg_rating:
        return avg_rating
    else:
        return None


def get_HashId(product_url, sku):
    hash_id = int(hashlib.md5(bytes(str(product_url) + str(sku), "utf8")).hexdigest(), 16) % (
            10 ** 18)
    return hash_id


def getVHashId(product_url, sku, colour, size):
    hash_id = int(hashlib.md5(bytes(str(product_url) + str(sku) + str(colour) + str(size), "utf8")).hexdigest(), 16) % (
            10 ** 18)
    return hash_id


def getHashId(product_url, sku, colour):
    hash_id = int(hashlib.md5(bytes(str(product_url) + str(sku) + str(colour), "utf8")).hexdigest(), 16) % (
            10 ** 18)
    return hash_id


def insertItemToSql(item, product_url, connection, cursor):
    try:
        # Convert dict or list to JSON so SQL won't break
        value_list = [
            json.dumps(v) if isinstance(v, (dict, list)) else v
            for v in item.values()
        ]

        # Build INSERT query dynamically
        field_list = [f"`{field}`" for field in item.keys()]
        placeholders = ["%s"] * len(item)

        fields = ",".join(field_list)
        placeholders_str = ",".join(placeholders)

        # insert_db = f"INSERT INTO {db.pdp_data} ({fields}) VALUES ({placeholders_str})"
        insert_db = f"INSERT IGNORE INTO {db.pdp_data} ({fields}) VALUES ({placeholders_str})"

        cursor.execute(insert_db, value_list)
        connection.commit()
        logger.info("Item Successfully Inserted...")
    except Exception as e:
        print("Error:", str(e))
