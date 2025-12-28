import gzip
import re
import os
import json
import random
from datetime import datetime, timedelta
from idlelib.iomenu import encoding

import requests
from parsel import Selector
from scrapy.http import TextResponse
from nykaa_fashion_weekly.config.database_config import ConfigDatabase
import scrapy
from scrapy import cmdline, Request
import nykaa_fashion_weekly.db_config as db
import pymysql
from nykaa_fashion_weekly.items import PdpDataItem


def get_future_date(days_after_today):
    today = datetime.today()
    # Start counting from tomorrow
    future_date = today + timedelta(days=days_after_today)
    return future_date.strftime("%Y-%m-%d")


def clean_html_description(html_text):
    # Replace bold label tags with formatted label:
    html_text = re.sub(r'<b>([^<]+?)\s*:\s*</b>', r'\1: ', html_text)

    # Replace paragraph tags with newlines
    html_text = re.sub(r'</?p>', '\n', html_text)

    # Remove any other HTML tags if present
    html_text = re.sub(r'<[^>]+>', '', html_text)

    # Collapse multiple newlines and strip whitespace
    html_text = re.sub(r'\n+', '\n', html_text).strip()

    cleaned_text = re.sub(r'\s{2,}', ' ', html_text.strip())

    return cleaned_text


def get_product_details(product_data):
    sections = product_data.get('pdp_sections', [])

    # Find the section titled "Know your product" with widget type 'plain_collapsable_widget'
    know_your_product = [
        section.get('value', 'N/A')
        for section in sections
        if section.get('widget_type') == 'plain_collapsable_widget'
           and section.get('title') == 'Know your product'
    ]

    # Join and clean up
    product_details = clean_html_description(" | ".join(know_your_product) or "N/A")
    return product_details


def get_specifications(product_data):
    sections = product_data.get('pdp_sections', [])
    specs = []

    for section in sections:
        if section.get('title') != 'Product details':
            continue

        for widget in section.get('child_widgets', []):
            if widget.get('widget_type') == 'attribute_columnize_widget':
                for attr in widget.get('attributes', []):
                    specs.append(f"{attr.get('label', 'N/A')}: {attr.get('value', 'N/A')}")

            elif widget.get('widget_type') == 'plain_widget':
                specs.append(f"{widget.get('title', 'N/A')}: {widget.get('value', 'N/A')}")

    specifications = " | ".join(specs) or "N/A"

    return specifications


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"
    allowed_domains = ["www.nykaafashion.com"]

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_impersonate.ImpersonateDownloadHandler",
            "https": "scrapy_impersonate.ImpersonateDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
    browser = random.choice(["chrome110", "edge99", "safari15_5"])

    handle_httpstatus_list = [404]

    def __init__(self, start_id, end, **kwargs):
        super().__init__(**kwargs)
        self.PAGE_SAVE_PATH = f"E:\\Nirav\\Project_page_save\\nykaa_fashion_weekly\\{db.current_date}"
        os.makedirs(self.PAGE_SAVE_PATH, exist_ok=True)
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="actowiz",
            database=db.database_name
        )

        self.cur = self.conn.cursor()
        self.start_id = start_id
        self.end = end
        self.db = ConfigDatabase(database=f"nykaa_fashion", table=f'{db.current_date}_{db.input_name}')
        self.cookies = {
            '_ga': 'GA1.1.1013695182.1761275781',
            '_ga_DZ4MXZBLKH': 'GS2.1.s1761275781$o1$g1$t1761275781$j60$l0$h0',
            'EXP_prod': 'prod-a',
            'EXP_search_dn_widgets': 'search_dn_widgets-a',
        }
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        }

    def start_requests(self):
        results = self.db.fetchResultsfromSql(
            conditions={'status': 'Pending'},
            start=self.start_id,
            end=self.end
        )

        for result in results:
            product_id = result.get('product_id')
            product_url = result.get('product_url')
            pagesave_path = os.path.join(self.PAGE_SAVE_PATH, f"{product_id}.html.gz")
            status = False
            if not os.path.exists(pagesave_path):
                yield scrapy.Request(
                    url=product_url,
                    headers=self.headers,
                    # cookies=self.cookies,
                    cb_kwargs={
                        "product_id": product_id,
                        "product_url": product_url,
                        "status": status
                    },
                    meta={
                        "impersonate": self.browser
                    },
                    dont_filter=True
                )
            else:
                status = True
                with gzip.open(pagesave_path, 'rb') as f:
                    html_content = f.read().decode('utf-8', errors='ignore')

                yield scrapy.Request(
                    url=f'file:///{pagesave_path}',
                    body=html_content,
                    cb_kwargs={
                        "product_id": product_id,
                        "product_url": product_url,
                        "status": status
                    },
                    dont_filter=True
                )

    def parse(self, response, **kwargs):
        response = gzip.decompress(response.body)
        response = response.decode('utf-8')
        response = Selector(text=response)

        product_id = kwargs.get('product_id')
        status = kwargs.get('status')
        product_url = kwargs.get('product_url')
        pagesave_path = os.path.join(self.PAGE_SAVE_PATH, f"{product_id}.html.gz")

        if status == False:
            if response.status == 404:
                sql = f"UPDATE {db.current_date}_{db.input_name} SET status = %s WHERE product_id = %s"
                values = (response.status, product_id)
                self.cur.execute(sql, values)
                self.conn.commit()
                self.logger.warning(f"Page not found: {response.url}")

            if response.status == 200:
                # Todo: pagesave
                if not os.path.exists(pagesave_path):
                    with gzip.open(pagesave_path, 'wb') as f:
                        f.write(response.body)

        try:
            match = re.search(r'<script id="__PRELOADED_STATE__" type="application/json">({.*?})</script>',
                              response.text,
                              re.DOTALL)
        except:
            match = re.search(r'<script id="__PRELOADED_STATE__" type="application/json">({.*?})</script>',
                              response._text,
                              re.DOTALL)
        if not match:
            print("Match not found in data")

        json_data = json.loads(match.group(1))
        product_data = json_data.get("details", {}).get("skuData", {}).get("product", {})

        # Todo: category hierarchy
        category_data = product_data.get("primary_categories_json_all", {})

        sorted_category_keys = sorted(
            (k for k in category_data.keys() if re.match(r"l\d+_Category", k)),
            key=lambda x: int(re.search(r"\d+", x).group())
        )

        category_hierarchy = " > ".join(
            category_data.get(key, {}).get("name", "N/A") for key in sorted_category_keys
        )

        if product_data.get("id") == str(product_id):
            print("fetched PID:", product_data.get("id"))

            # Todo: product id
            product_id = product_data.get('id', 'N/A')

            # Todo: catalog name
            catalog_name = f"{product_data.get('title', '')} {product_data.get('subTitle', '')}"

            # Todo: catalog id
            catalog_id = product_data.get('id', 'N/A')

            # Todo: source
            source = "Nykaa"

            # Todo: scraped_date
            scraped_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Todo: product_name
            product_name = f"{product_data.get('title', '')} {product_data.get('subTitle', '')}"

            # Todo: image_url
            image_url = product_data.get("meta_data", {}).get("imgUrl", "N/A")

            # Todo: product_price
            product_price = product_data.get("discountedPrice", "N/A")

            # Todo: arrival_date
            arrival_date = get_future_date(int(product_data.get("shipsIn", "N/A")))

            # Todo: shipping_charges
            shipping_charges = "N/A"

            # Todo: is_sold_out
            is_sold_out = product_data.get("isOutOfStock", 0) != 0

            # Todo: discount
            discount = product_data.get("discount", "N/A") if product_data.get("discount", "N/A") != 0 else "N/A"

            # Todo: mrp
            mrp = product_data.get("price", "N/A")

            # Todo: product_url
            product_url = product_data.get("meta_data", {}).get("productUrl", "N/A")

            # Todo: number_of_ratings
            number_of_ratings = product_data.get("review_rating_json", {}).get("star_rating_count", "N/A")

            # Todo: avg_rating
            avg_rating = product_data.get("review_rating_json", {}).get("star_rating", "N/A")

            # Todo: country_code
            country_code = "IN"

            # Todo: images
            images = " | ".join([media['url'] for media in product_data.get('productMedia', [])]) or "N/A"

            # Todo: Offers
            offer_cookies = {
                'bcookie': 'ae7a4160-41cd-494a-9d1e-6ef40e30e43c',
                'EXP_plp-virtualizer-exp': 'plp-virtualizer-exp-b',
                'EXP_rating-review-v2': 'rating-review-v2-a',
                'EXP_fe-api-migration-ab': 'fe-api-migration-a',
                'EXP_UPDATED_AT': '1758862083781',
                'EXP_SSR_CACHE': '51a68182adcfb34378dc7558b4c91d09',
                'bm_ss': 'ab8e18ef4e',
                'tm_stmp': '1760088054061',
                'rum_abMwebSort': '6',
                'PHPSESSID': '73892715ca8b4f6381bc898f59fa0447',
                'EXP_prod': 'prod-a',
                'EXP_search_dn_widgets': 'search_dn_widgets-a',
                '_gcl_au': '1.1.1068756885.1760088055',
                'NYK_VISIT': 'ae7a4160-41cd-494a-9d1e-6ef40e30e43c~1760088054832',
                'EXP_checkout-ssr-mweb': 'variant-pci',
                'EXP_checkout-ssr-dweb': 'variant-pci',
                'EXP_login-nudge-plp': 'Variant1',
                'EXP_speculation-rule-cart-ab': 'speculation-rule-cart-a',
                'EXP_postorder_variant_ab': 'postorder_default_A',
                '_ga': 'GA1.1.721437364.1760088055',
                'EXP_gamification-nudge': 'gamification-nudge-b',
                'WZRK_G': '569419521c9348359cc2a0320c98e31a',
                'EXP_account_order_carousel': 'account_order_carousel-a',
                '_clck': 'x3suaw%5E2%5Eg01%5E0%5E2109',
                'EXP_image-search': 'image-search-a',
                '_fbp': 'fb.1.1760088058451.487675722400817723',
                'WZRK_S_WRK-4W9-R55Z': '%7B%22p%22%3A5%2C%22s%22%3A1760088056%2C%22t%22%3A1760088271%7D',
                '_clsk': '1zliyz%5E1760088272327%5E5%5E0%5Ey.clarity.ms%2Fcollect',
                'bm_lso': 'C8020CAD63CAF3D6D49163FEBEB37C3846459EEEAFDE65217CB6FC869787FA70~YAAQMBzFF2txC6SZAQAAqK5vzQWuJAJ6fqp6NIjM5Rg3v20bi7S2V5GqXum3q/msiGVzBpQj54SX5GZvqSgr/1M8nSPC+7ASmL6hcwm92M7HUE098ut10KKrs8uxgSIeASzHU/uSdBuXnRcP07Jt7QQqvZPxfLwihZEL739fcE8mfRcJGIj2EPKaEnbw9PnavQoiNKOs1ZJvZ4w2B7i4oK3UKvpRdODZs5R3n9fzoELTuxoackmWxqzDNobbzRijmDFsXTK5+o2J8y/y99kR0bTK6HgCffl8gUbOfO+RIVbKlcKgcJTy4klirkdNuPYiLhrq8vI8NwjfKcgcAq5nMrG22mjVruxMgXXZSnZPGmk2VAsP8219p/uinzARyMTObYfDW11+4ix3jijUiUGKZj0IWocVIiaw9d+9Obe8Qb9RamD/NAnp7HWH20SvvuRkOJmjPoDmHxaZ+JI8yzh7CxHDdzVBSMYI^1760088272849',
                'bm_so': '4BF4330C30B2475882D152A78DE8E99118E4F6B964E6B0E3BFA796DE3F15F44D~YAAQMBzFF4WHDKSZAQAAH2p7zQXThkntZWoDpDglqP/3scETqWGXzs5G92uBfE99XE9yN3ZrWe5kuRHvC79QhkRuwVUJm72sl9AbQsb8AKyCRbzhRNovNJsnXlv6g0SGm2SnnH2Uc7jXS1/M859Hfjzc/60lHRj2VUwzpiU1UYY56JzoaoMdNL68WWBxXHnOMXxkSDgvZbV/5/uBucEeWSu+YkHJ7uIHV5AiTtpANDWPmzYQ1HESNcIsxMCnbkXcdG++1Nw8VSdR2D2jGlMOBAU9+M7oQhpnTCiGmTG0riUD1lvkO89vdhEFyOiPZ9Z25hrxBkYPOLXVB55TBwU6yvb/pnuNSxuKCxGnrrom1XbvFU0dFHSgT9P1pEbeGPB4iL/MgpGu9FSbl1gMre6IPYvpPpnb2ZIcXNGlw0Z1zZ6QNMUMaTbLjtkWFErmKMwK50RYza9b7lGb8mMPye1Gqo+WwaILHUc=',
                'bm_sz': 'E747E80CEEA5D1ACEB4098AE3200D127~YAAQMBzFF4aHDKSZAQAAH2p7zR3+//qIdwjTEPGCuf5caBYixhxx6r5q42m4kOpfFBbusimGoiwGxQvVNBe4VYb2oVcdGjEDB3eolCTjvLGxlOCX4Sdg16v1taCjKDq3t1QC+qLINs+CQdv3HI24P8jDPGHVwDvGNXH+44PTbD55QHT8LLspdyhX4hUIxQf19iJkbsnBQ36BB5MEt1FSsEn0MgiJ1UMVyNzrnprDXb3/Qr38OpzNtoePuDew7YAf6isrFnXDhHlAk0Gpr8yavdIuvU+8XhjRbOaMQbV6bLe4QgTrpHgRo1fjGr4fC9VJG5s05ZhA7+o3YOS8v+vkiKp5uqw8/JDp8+KHvYfLKadt6y+1Y3aq4o3I2AY1jt1F7a8KqtOoN1hnCkWwhokKl5DmPGDp3LqUg1yHxISp8nYiKuHj72kizmAP5n2d02raFBGn347XjYsMYFIzdgRdl/PFQOXNPGk6zVIc~4601394~3752515',
                '_ga_DZ4MXZBLKH': 'GS2.1.s1760088055$o1$g1$t1760089039$j60$l0$h0',
                '_abck': '2BC6A1A06D2FC5D679308EB2FD3792A3~0~YAAQMBzFF46HDKSZAQAAo2p7zQ43YTlXEx75ufzPZZsRTeX10FcswRLSJiQIeyuB7npyEdsRpS3S69vCF80+su2Fdu9iL1G8CTZEUtD3MNyeBUUL+DlY3gR8fZWlAVqmGFDia7IpoytYQtWxZJJss/Vk/sXbAPVsOrHKhpM5+1KMncq9arb82JHN+08Y51unzhP53px9OEK7nexamF+j9WNUQ96t2Pa8srSC/tQB/lSmKsynPNBhzw11vnL4SGK7hidTRQSGvLAg+moAIGksO232437xh+wPmpg7NkJZt0edHOB46kWrATTe1AH8+QTyLM7ZYU3+aWqhm9BE5TvQRf7V7iMzJHyfoI3HAkCe01bgloZQ8yr7w0qywE7rQ4/gvX83kSW6tfjo8w4YSq6hrALHcEOXSOP8FHSy2iML8qOB4gtxC+5xjPRNrMaRuTbgbwj017PEfnsZ6Yr4DwTlCopPTKc9pDtyEt9bm+LFIC3VhylO+jrltEcFQRlu5LTJZyoyywBwgpSIy1Mg0It8b3CzFFPpwhWyzqbmnn5NIFiLI2mTQWq6ivmMcZOpRy5gcWYrcLGGx6YNGF8zO1VEHdUSIZ8Y+gn5SPjouf0B5NT2dAAcWB4YIAvOgiiId/xZ2C75CzRnNJmIBBZWqF94vSRFGbUSb0zkbsNXX7lpVLLhSi9zlf5jTpkZdLfUSYJyI08KYOy8FBJTxUUpsig=~-1~-1~1760091655~AAQAAAAE%2f%2f%2f%2f%2fyYcNK9LIRFsumTcZghpvLjTCtDR0FjUILq62sjguh5VNBtZQUNFcMQcLiYUy9riLzmjeJGs+3mjc+VFsXImqCfdLttZd7SIvW9eEryu4wfMbfuOOPM5scODOoXb5DtagOpAm1M%3d~-1',
                'bm_s': 'YAAQMBzFF8KHDKSZAQAA2Wx7zQS5fBooRTFT1ZqjsIstNkHK6/psc6UMcACFJGhvdnTbjfYtQHosgC/HscQq8l0q2PEXFBVMLJuDPEUZlhIPyRyv+OpYTWdMqwUSJhcGR8xhuoFESk7KovV/1nqW/Y5DWdRv65BAOY1EqMB1Oak8cwdWCyE7xVtM8tCC9pZzSCi4mzGJVET3eiB6yIY1+YC5Ghm2J2EOrBUifNaez+LUHetZqK+4GpyTzwyVSDE04ilEl3rZLODTU+NMk4nxmtGfDCQ6NrLCGOqRU8604M4H2rtGJjC/YCqBw9hXifFOMBlO9EWClD10jzw8/xE0LDhcrdDJjJ2Twy7+tNJYNRZdT0g4N4ofLn2OqKTboOqe2lewUG7rL1ZwgQek5bXa5R3HlAcmzt0+INhAmZRx8o2+ho0HE5hmL8oWSz9o6wM/phGHWC7Ecnsbx+d4A8qZ5Gog4pTZcsdr+hWHMmSPTHUE1HEfYxy25cZjwYLpy3fyRSvtkgx3knDC2qmrYWeScqOJzR0RPJ/Nnh0DpjAncMV/tTrQQok9IAiagMvkuzRgSb4KdXoiSSxUEBc49103',
                'NYK_PCOUNTER': '6',
                'NYK_ECOUNTER': '24',
            }
            offer_headers = {
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'priority': 'u=1, i',
                'referer': 'https://www.nykaafashion.com/fabindia-cotton-printed-pathani-kurta-with-cuff/p/5157135',
                'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                # 'cookie': 'bcookie=ae7a4160-41cd-494a-9d1e-6ef40e30e43c; EXP_plp-virtualizer-exp=plp-virtualizer-exp-b; EXP_rating-review-v2=rating-review-v2-a; EXP_fe-api-migration-ab=fe-api-migration-a; EXP_UPDATED_AT=1758862083781; EXP_SSR_CACHE=51a68182adcfb34378dc7558b4c91d09; bm_ss=ab8e18ef4e; tm_stmp=1760088054061; rum_abMwebSort=6; PHPSESSID=73892715ca8b4f6381bc898f59fa0447; EXP_prod=prod-a; EXP_search_dn_widgets=search_dn_widgets-a; _gcl_au=1.1.1068756885.1760088055; NYK_VISIT=ae7a4160-41cd-494a-9d1e-6ef40e30e43c~1760088054832; EXP_checkout-ssr-mweb=variant-pci; EXP_checkout-ssr-dweb=variant-pci; EXP_login-nudge-plp=Variant1; EXP_speculation-rule-cart-ab=speculation-rule-cart-a; EXP_postorder_variant_ab=postorder_default_A; _ga=GA1.1.721437364.1760088055; EXP_gamification-nudge=gamification-nudge-b; WZRK_G=569419521c9348359cc2a0320c98e31a; EXP_account_order_carousel=account_order_carousel-a; _clck=x3suaw%5E2%5Eg01%5E0%5E2109; EXP_image-search=image-search-a; _fbp=fb.1.1760088058451.487675722400817723; WZRK_S_WRK-4W9-R55Z=%7B%22p%22%3A5%2C%22s%22%3A1760088056%2C%22t%22%3A1760088271%7D; _clsk=1zliyz%5E1760088272327%5E5%5E0%5Ey.clarity.ms%2Fcollect; bm_lso=C8020CAD63CAF3D6D49163FEBEB37C3846459EEEAFDE65217CB6FC869787FA70~YAAQMBzFF2txC6SZAQAAqK5vzQWuJAJ6fqp6NIjM5Rg3v20bi7S2V5GqXum3q/msiGVzBpQj54SX5GZvqSgr/1M8nSPC+7ASmL6hcwm92M7HUE098ut10KKrs8uxgSIeASzHU/uSdBuXnRcP07Jt7QQqvZPxfLwihZEL739fcE8mfRcJGIj2EPKaEnbw9PnavQoiNKOs1ZJvZ4w2B7i4oK3UKvpRdODZs5R3n9fzoELTuxoackmWxqzDNobbzRijmDFsXTK5+o2J8y/y99kR0bTK6HgCffl8gUbOfO+RIVbKlcKgcJTy4klirkdNuPYiLhrq8vI8NwjfKcgcAq5nMrG22mjVruxMgXXZSnZPGmk2VAsP8219p/uinzARyMTObYfDW11+4ix3jijUiUGKZj0IWocVIiaw9d+9Obe8Qb9RamD/NAnp7HWH20SvvuRkOJmjPoDmHxaZ+JI8yzh7CxHDdzVBSMYI^1760088272849; bm_so=4BF4330C30B2475882D152A78DE8E99118E4F6B964E6B0E3BFA796DE3F15F44D~YAAQMBzFF4WHDKSZAQAAH2p7zQXThkntZWoDpDglqP/3scETqWGXzs5G92uBfE99XE9yN3ZrWe5kuRHvC79QhkRuwVUJm72sl9AbQsb8AKyCRbzhRNovNJsnXlv6g0SGm2SnnH2Uc7jXS1/M859Hfjzc/60lHRj2VUwzpiU1UYY56JzoaoMdNL68WWBxXHnOMXxkSDgvZbV/5/uBucEeWSu+YkHJ7uIHV5AiTtpANDWPmzYQ1HESNcIsxMCnbkXcdG++1Nw8VSdR2D2jGlMOBAU9+M7oQhpnTCiGmTG0riUD1lvkO89vdhEFyOiPZ9Z25hrxBkYPOLXVB55TBwU6yvb/pnuNSxuKCxGnrrom1XbvFU0dFHSgT9P1pEbeGPB4iL/MgpGu9FSbl1gMre6IPYvpPpnb2ZIcXNGlw0Z1zZ6QNMUMaTbLjtkWFErmKMwK50RYza9b7lGb8mMPye1Gqo+WwaILHUc=; bm_sz=E747E80CEEA5D1ACEB4098AE3200D127~YAAQMBzFF4aHDKSZAQAAH2p7zR3+//qIdwjTEPGCuf5caBYixhxx6r5q42m4kOpfFBbusimGoiwGxQvVNBe4VYb2oVcdGjEDB3eolCTjvLGxlOCX4Sdg16v1taCjKDq3t1QC+qLINs+CQdv3HI24P8jDPGHVwDvGNXH+44PTbD55QHT8LLspdyhX4hUIxQf19iJkbsnBQ36BB5MEt1FSsEn0MgiJ1UMVyNzrnprDXb3/Qr38OpzNtoePuDew7YAf6isrFnXDhHlAk0Gpr8yavdIuvU+8XhjRbOaMQbV6bLe4QgTrpHgRo1fjGr4fC9VJG5s05ZhA7+o3YOS8v+vkiKp5uqw8/JDp8+KHvYfLKadt6y+1Y3aq4o3I2AY1jt1F7a8KqtOoN1hnCkWwhokKl5DmPGDp3LqUg1yHxISp8nYiKuHj72kizmAP5n2d02raFBGn347XjYsMYFIzdgRdl/PFQOXNPGk6zVIc~4601394~3752515; _ga_DZ4MXZBLKH=GS2.1.s1760088055$o1$g1$t1760089039$j60$l0$h0; _abck=2BC6A1A06D2FC5D679308EB2FD3792A3~0~YAAQMBzFF46HDKSZAQAAo2p7zQ43YTlXEx75ufzPZZsRTeX10FcswRLSJiQIeyuB7npyEdsRpS3S69vCF80+su2Fdu9iL1G8CTZEUtD3MNyeBUUL+DlY3gR8fZWlAVqmGFDia7IpoytYQtWxZJJss/Vk/sXbAPVsOrHKhpM5+1KMncq9arb82JHN+08Y51unzhP53px9OEK7nexamF+j9WNUQ96t2Pa8srSC/tQB/lSmKsynPNBhzw11vnL4SGK7hidTRQSGvLAg+moAIGksO232437xh+wPmpg7NkJZt0edHOB46kWrATTe1AH8+QTyLM7ZYU3+aWqhm9BE5TvQRf7V7iMzJHyfoI3HAkCe01bgloZQ8yr7w0qywE7rQ4/gvX83kSW6tfjo8w4YSq6hrALHcEOXSOP8FHSy2iML8qOB4gtxC+5xjPRNrMaRuTbgbwj017PEfnsZ6Yr4DwTlCopPTKc9pDtyEt9bm+LFIC3VhylO+jrltEcFQRlu5LTJZyoyywBwgpSIy1Mg0It8b3CzFFPpwhWyzqbmnn5NIFiLI2mTQWq6ivmMcZOpRy5gcWYrcLGGx6YNGF8zO1VEHdUSIZ8Y+gn5SPjouf0B5NT2dAAcWB4YIAvOgiiId/xZ2C75CzRnNJmIBBZWqF94vSRFGbUSb0zkbsNXX7lpVLLhSi9zlf5jTpkZdLfUSYJyI08KYOy8FBJTxUUpsig=~-1~-1~1760091655~AAQAAAAE%2f%2f%2f%2f%2fyYcNK9LIRFsumTcZghpvLjTCtDR0FjUILq62sjguh5VNBtZQUNFcMQcLiYUy9riLzmjeJGs+3mjc+VFsXImqCfdLttZd7SIvW9eEryu4wfMbfuOOPM5scODOoXb5DtagOpAm1M%3d~-1; bm_s=YAAQMBzFF8KHDKSZAQAA2Wx7zQS5fBooRTFT1ZqjsIstNkHK6/psc6UMcACFJGhvdnTbjfYtQHosgC/HscQq8l0q2PEXFBVMLJuDPEUZlhIPyRyv+OpYTWdMqwUSJhcGR8xhuoFESk7KovV/1nqW/Y5DWdRv65BAOY1EqMB1Oak8cwdWCyE7xVtM8tCC9pZzSCi4mzGJVET3eiB6yIY1+YC5Ghm2J2EOrBUifNaez+LUHetZqK+4GpyTzwyVSDE04ilEl3rZLODTU+NMk4nxmtGfDCQ6NrLCGOqRU8604M4H2rtGJjC/YCqBw9hXifFOMBlO9EWClD10jzw8/xE0LDhcrdDJjJ2Twy7+tNJYNRZdT0g4N4ofLn2OqKTboOqe2lewUG7rL1ZwgQek5bXa5R3HlAcmzt0+INhAmZRx8o2+ho0HE5hmL8oWSz9o6wM/phGHWC7Ecnsbx+d4A8qZ5Gog4pTZcsdr+hWHMmSPTHUE1HEfYxy25cZjwYLpy3fyRSvtkgx3knDC2qmrYWeScqOJzR0RPJ/Nnh0DpjAncMV/tTrQQok9IAiagMvkuzRgSb4KdXoiSSxUEBc49103; NYK_PCOUNTER=6; NYK_ECOUNTER=24',
            }
            offer_params = {
                'customerGroupId': '0',
                'domain': 'fashion',
                'deviceType': 'WEBSITE',
                'isLoyal': '1',
                'productId': str(product_id),
                'mrp': product_data.get("price"),
                'sp': product_data.get("price"),
                'fetchUniversalOffers': 'true',
                'fetchCouponOffers': 'true',
                'fetchPaymentMethodOffers': 'true',
                'fetchTradeOffers': 'true',
                'fetchBestOffers': 'true',
            }
            offer_response = requests.get(
                'https://www.nykaafashion.com/gateway-api/offer/api/v1/product/customer/offer',
                params=offer_params,
                cookies=offer_cookies,
                headers=offer_headers,
            )
            response_data = ''
            try:
                response_data = offer_response.json().get('data')
            except Exception as error:
                print(error)

            # Todo: offer_pagesave
            offer_pagesave = f"E:\\Nirav\\Project_page_save\\nykaa_fashion_weekly\\{db.current_date}\\offer"
            os.makedirs(offer_pagesave, exist_ok=True)
            try:
                with open(f"{offer_pagesave}/{product_id}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(response_data))
            except Exception as e:
                print(e)

            # Todo: best_offer
            best_offers = None
            if response_data.get('coupons'):
                best_offer_list = response_data['coupons']  # Take the first best offer
                best_offers = " | ".join(
                    [f"{best_offers.get('title')} {best_offers.get('description')}" for best_offers in
                     best_offer_list])
            else:
                best_offers = None

            # Todo: best price
            best_price = response_data.get('offerBestPrice')

            # Todo: Bank Offer (from `paymentOffers`)
            bank_offers_lst = response_data.get('paymentOffers', [])
            bank_offers = [offer.get('title') for offer in bank_offers_lst if offer.get('title')]

            # Todo: product_details
            product_details = get_product_details(product_data)

            # Todo: specifications
            specifications = get_specifications(product_data)

            # Todo: rating
            rating = product_data.get("review_rating_json", {}).get("star_rating", "N/A")

            # Todo: MOQ
            moq = 1

            # Todo: brand
            brand = product_data.get("title", "N/A")

            # Todo: product_code
            product_code = product_data.get("sku", "N/A")

            # Todo: Available_sizes
            available_sizes = " | ".join(
                [s.get('sizeName') for s in product_data.get("sizeOptions", {}).get('options', [])]) or "N/A"

            # Todo: sellerPartnerId
            seller_partner_id = product_data.get("sku", "N/A")

            # Todo: seller_return_policy
            seller_return_policy = next(
                (section.get('value', 'N/A') for section in product_data.get('pdp_sections', []) if
                 section.get('title') == 'Return and exchange policy'), "N/A")

            # Todo: manufacturing_info_packerInfo
            manufacturing_info_packerinfo = next(
                (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', []) if
                 section.get('widget_type') == 'attribute_widget' for attr in section.get('attributes', []) if
                 'Address of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A")

            # Todo: manufacturing_info_seller_name
            manufacturing_info_seller_name = next(
                (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', []) if
                 section.get('widget_type') == 'attribute_widget' for attr in section.get('attributes', []) if
                 'Name of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A")

            # Todo: manufacturing_info_importerinfo
            manufacturing_info_importerinfo = next(
                (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', []) if
                 section.get('widget_type') == 'attribute_widget' for attr in section.get('attributes', []) if
                 'Address of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A")

            # Todo: manufacturing_info_countryOfOrigin
            manufacturing_info_country_of_origin = next(
                (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                 if section.get('widget_type') == 'attribute_widget'
                 for attr in section.get('attributes', [])
                 if 'Country of Origin' in attr.get('label', '')), "N/A")

            # Todo: manufacturing_info_manufacturerInfo
            manufacturing_info_manufacturerinfo = next(
                (attr.get('value', 'N/A') for section in product_data.get('pdp_sections', [])
                 if section.get('widget_type') == 'attribute_widget'
                 for attr in section.get('attributes', [])
                 if 'Address of Manufacturer/ Packer/ Importer' in attr.get('label', '')), "N/A")

            # Todo: More_colours
            color_list = []
            more_color_lst = [color.get('name').lower() for color in product_data.get('colorOptions', []) if
                              color.get('name')]
            color = [product_data.get('color').get('name')] if product_data.get('color').get('name') else ''
            if more_color_lst:
                color_list.extend(more_color_lst)
            if color:
                color_list.extend(color)

            more_colors = ''
            if more_color_lst:
                m_color_list = [color.strip() for color in color_list if color.strip()]
                more_colors = " | ".join(set(m_color_list)) if m_color_list else "N/A"
            else:
                more_colors = 'N/A'

            # Todo: variation_id
            variation_id = " | ".join(
                [f"{color.get('name', '').lower()} : {color.get('sku')}" for color in
                 product_data.get('colorOptions', [])]
            ) or "N/A"

            item = PdpDataItem()
            item['product_id'] = product_id
            item['catalog_name'] = catalog_name
            item['catalog_id'] = catalog_id
            item['source'] = source
            item['scraped_date'] = scraped_date
            item['product_name'] = product_name
            item['image_url'] = image_url
            item['category_hierarchy'] = category_hierarchy.replace('Nykaa >', '').strip()
            item['category_hierarchy'] = item['category_hierarchy'].replace('Home >', '').strip()
            item['product_price'] = product_price
            item['arrival_date'] = "N/A" if is_sold_out else arrival_date
            item['shipping_charges'] = shipping_charges
            item['is_sold_out'] = is_sold_out
            item['discount'] = discount
            item['mrp'] = mrp
            item['page_url'] = "N/A"
            item['product_url'] = product_url
            item['number_of_ratings'] = number_of_ratings
            item['avg_rating'] = avg_rating
            item['position'] = "N/A"
            item['country_code'] = country_code
            item['images'] = images
            item['Best_price'] = best_price
            item['Best_offers'] = best_offers
            item['bank_offers'] = bank_offers if bank_offers else "N/A"
            item['product_details'] = product_details
            item['specifications'] = specifications
            item['rating'] = rating
            item['MOQ'] = moq
            item['brand'] = brand
            item['product_code'] = product_code
            item['Available_sizes'] = available_sizes
            item['sellerPartnerId'] = "N/A"
            item['seller_return_policy'] = seller_return_policy
            item['manufacturing_info_packerInfo'] = manufacturing_info_packerinfo
            item['manufacturing_info_seller_name'] = manufacturing_info_seller_name
            item['manufacturing_info_importerInfo'] = manufacturing_info_importerinfo
            item['manufacturing_info_countryOfOrigin'] = manufacturing_info_country_of_origin
            item['manufacturing_info_manufacturerInfo'] = manufacturing_info_manufacturerinfo
            item['More_colours'] = more_colors
            item['variation_id'] = variation_id
            yield item


if __name__ == '__main__':
    cmdline.execute(f"scrapy crawl {PdpDataSpider.name} -a start_id=1 -a end=1".split())
