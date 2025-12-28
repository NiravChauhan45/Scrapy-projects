import json
import os
import time
from html import unescape
from dateutil import tz
import requests
# from curl_cffi import requests
import datetime
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger
from parsel import Selector
from curl_cffi import requests as rs
import concurrent.futures

from requests import Session

from myntra.db_config import current_date

MAX_RETRIES = 5  # Set max retry count
RETRY_DELAY = 2  # Delay (in seconds) between retries

scrape_do_token = 'f42a5b59aec3467e97a8794c611c436b91589634343'
scrape_proxy = {
    'http': f'http://{scrape_do_token}:@proxy.scrape.do:8080',
    'https': f'http://{scrape_do_token}:@proxy.scrape.do:8080'
}
proxies = {
    "https": f"http://{scrape_do_token}&geoCode=in@proxy.scrape.do:8080"
}

cookies = {
    'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pT1RZd09URmhORGN0TXpkaFl5MHhNV1l3TFdKaE1qVXRaVEk1T0ROa05EWXpZMkk0SWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpNMU16azBPRE1zSW1semN5STZJa2xFUlVFaWZRLmlvUXM2VTFSU1MzcXZXaHdnN3YwRTJyRzJ1SGRGWWl4S2NMblR6Rnd1ZEU=',
}
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

india_tz = tz.gettz('Asia/Kolkata')


def fetch_product(product_url):
    for attempt in range(MAX_RETRIES):
        try:
            # api_url = f"https://api.scrape.do/?token={scrape_do_token}&geoCode=IN&url={product_url}"
            api_url = product_url
            print(f"Fetching URL (attempt {attempt + 1}): {product_url}")
            response = requests.get(api_url, headers=headers, verify=True)
            # Parsing the response text using parsel Selector
            selector = Selector(text=response.text)

            # Extracting the product data embedded in a script tag
            data = selector.xpath(
                "//script[contains(text(), 'window.__myx') and contains(text(), 'pdpData') and contains(text(), 'discountedPrice')]/text()"
            ).get()

            if not data:
                continue

            print(f"Response Status Code: {response.status_code}")
            if response.status_code == 200:
                return {
                    "HTTP Status Code": response.status_code,
                    "Description": "success",
                    "Data": response
                }
            elif response.status_code == 400:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "INVALID_REQUEST",
                    "Description": "Bad request, malformed syntax, missing parameters, or invalid values",
                    "Error Message": "The request could not be understood or is missing required parameters."
                }
            elif response.status_code == 401:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "UNAUTHORIZED",
                    "Description": "API key missing or invalid",
                    "Error Message": "Unauthorized request. Please check your API key."
                }
            elif response.status_code == 403:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "FORBIDDEN",
                    "Description": "The user does not have permission to access the resource",
                    "Error Message": "Access forbidden. You do not have the necessary permissions."
                }
            elif response.status_code == 404:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "NOT_FOUND",
                    "Description": "The requested product or resource could not be found",
                    "Error Message": "The requested resource was not found."
                }
            elif response.status_code == 408:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "REQUEST_TIMEOUT",
                    "Description": "The request took too long to complete",
                    "Error Message": "The request timed out. Please try again later."
                }
            elif response.status_code == 429:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "TOO_MANY_REQUESTS",
                    "Description": "Rate limit exceeded",
                    "Error Message": "Too many requests. Please slow down and try again later."
                }
            elif response.status_code == 500:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "INTERNAL_SERVER_ERROR",
                    "Description": "General server error",
                    "Error Message": "Internal server error. Please try again later."
                }
            elif response.status_code == 502:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "BAD_GATEWAY",
                    "Description": "Upstream server error",
                    "Error Message": "Received an invalid response from the upstream server."
                }
            elif response.status_code == 503:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "SERVICE_UNAVAILABLE",
                    "Description": "Server is temporarily overloaded or under maintenance",
                    "Error Message": "Service temporarily unavailable. Please try again shortly."
                }
            elif response.status_code == 504:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "GATEWAY_TIMEOUT",
                    "Description": "Timeout while waiting for upstream response",
                    "Error Message": "Gateway timeout. Please retry the request."
                }


        except requests.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}): {e}")

        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)


def is_valid_url(url: str) -> bool:
    """
    Validates if the provided string is a properly formatted URL.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    if not url:
        return False

    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)


def get_reviews(product_id):
    product_url = f"https://www.myntra.com/reviews/{product_id}"

    # api_url = f"https://api.scrape.do/?token={scrape_do_token}&geoCode=IN&url={product_url}"
    api_url = product_url
    for attempt in range(MAX_RETRIES):
        try:
            response = rs.get(api_url, headers=headers, timeout=10, verify=True, impersonate='chrome110')

            if response.status_code == 200:
                if 'Site Maintenance' in response.text:
                    continue
                return {
                    "HTTP Status Code": response.status_code,
                    "Description": "success",
                    "Data": response
                }
            elif response.status_code == 400:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "INVALID_REQUEST",
                    "Description": "Bad request, malformed syntax, missing parameters, or invalid values",
                    "Error Message": "The request could not be understood or is missing required parameters."
                }
            elif response.status_code == 401:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "UNAUTHORIZED",
                    "Description": "API key missing or invalid",
                    "Error Message": "Unauthorized request. Please check your API key."
                }
            elif response.status_code == 403:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "FORBIDDEN",
                    "Description": "The user does not have permission to access the resource",
                    "Error Message": "Access forbidden. You do not have the necessary permissions."
                }
            elif response.status_code == 404:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "NOT_FOUND",
                    "Description": "The requested product or resource could not be found",
                    "Error Message": "The requested resource was not found."
                }
            elif response.status_code == 408:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "REQUEST_TIMEOUT",
                    "Description": "The request took too long to complete",
                    "Error Message": "The request timed out. Please try again later."
                }
            elif response.status_code == 429:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "TOO_MANY_REQUESTS",
                    "Description": "Rate limit exceeded",
                    "Error Message": "Too many requests. Please slow down and try again later."
                }
            elif response.status_code == 500:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "INTERNAL_SERVER_ERROR",
                    "Description": "General server error",
                    "Error Message": "Internal server error. Please try again later."
                }
            elif response.status_code == 502:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "BAD_GATEWAY",
                    "Description": "Upstream server error",
                    "Error Message": "Received an invalid response from the upstream server."
                }
            elif response.status_code == 503:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "SERVICE_UNAVAILABLE",
                    "Description": "Server is temporarily overloaded or under maintenance",
                    "Error Message": "Service temporarily unavailable. Please try again shortly."
                }
            elif response.status_code == 504:
                return {
                    "HTTP Status Code": response.status_code,
                    "Error Code": "GATEWAY_TIMEOUT",
                    "Description": "Timeout while waiting for upstream response",
                    "Error Message": "Gateway timeout. Please retry the request."
                }

            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)

        except requests.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}): {e}")


def get_similer_products(product_id):
    for attempt in range(MAX_RETRIES):
        try:
            product_id = product_id.split('/')[-1]
            product_url = f'https://www.myntra.com/gateway/v2/product/{product_id}/related'
            # https://www.myntra.com/gateway/v2/product/32085910/related

            # api_url = f"https://api.scrape.do/?token={scrape_do_token}&customHeaders=true&url={product_url}"
            #
            # cookies = {
            #     'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pT1RZd09URmhORGN0TXpkaFl5MHhNV1l3TFdKaE1qVXRaVEk1T0ROa05EWXpZMkk0SWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpNMU16azBPRE1zSW1semN5STZJa2xFUlVFaWZRLmlvUXM2VTFSU1MzcXZXaHdnN3YwRTJyRzJ1SGRGWWl4S2NMblR6Rnd1ZEU=',
            # }
            # headers = {
            #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
            # }

            response = ''
            try:
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9',
                    'priority': 'u=0, i',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                }
                # Todo: Make Session
                _session = Session()
                _session.headers = headers
                _session.get("https://www.myntra.com")
                response = _session.get(product_url)

                # response = requests.get(api_url,
                #                         headers=headers,
                #                         # cookies=cookies,
                #                         verify=True)

            except Exception as e:
                print(e)

            if response.status_code == 200:
                return {
                    "HTTP Status Code": response.status_code,
                    "Description": "success",
                    "Data": response
                }
            else:
                continue

        except requests.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}): {e}")


def get_links(cookies_, headers_, keyword, url):
    list_of_links = []
    response = requests.get(url=url, cookies=cookies_, headers=headers_)
    selector = Selector(text=response.text)
    json_data = selector.xpath("//script[contains(text(),'searchData')]/text()").get()
    if json_data:
        json_data = json_data.replace("window.__myx =", "").strip()
        json_data = json.loads(json_data)
    else:
        json_data = json.loads(response.text)
    results = json_data.get('searchData').get('results').get('products')
    if not results:
        results = results.get('products')

    if results:
        for index, result in enumerate(results):
            # Todo: Break Loop If Index Count: 25
            if index >= 25:
                break
            index += 1

            item = dict()
            product_id = result.get('productId')
            product_url = result.get('landingPageUrl')
            if product_url:
                product_url = f"https://www.myntra.com/{product_url}"

            # Todo: make item fileds
            # item['keyword'] = keyword
            # item['product_id'] = product_id
            # item['product_url'] = product_url
            list_of_links.append(product_url)

        print(list_of_links)

        # Todo: make requests if results(Product Counts) length < 25
        if len(results) < 25:
            cookies = {
                'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pWVRnek1EYzNNemd0TlRGaVl5MHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZME1EVXhNVFlzSW1semN5STZJa2xFUlVFaWZRLnN5aFcwTHJtdy1LQlRwR2hoU2Z2b1JMUmZmTDRDSDdNaU1remF0MTFUQlE=',
                'lt_timeout': '1',
                'lt_session': '1',
                '_d_id': '110e2c85-58a4-4dbe-9301-20ae21870966',
                'bm_ss': 'ab8e18ef4e',
                'bm_s': 'YAAQSs4tF6A6K3yXAQAASGT6pgNTyQ5scnNRaWzsBdQkPbjmGXU3wbZOz5Sp+uu/iMQKf+8bAE5zfLcEz0kCRtDKWekUoOZwTVIdPpbZfTbkkY6XRi0mLwBDpOLctF7H9P+d0uQGhoe+TvYZs2gISHy/KBtdeGHgcVpB8Ejh01BqXoqoJi7Jp9KUH0SRlcjVQcbSXQeGP9S7Mnx96kcE6mDC4bpFTVNNWVVKDx+k6pCeXb9j23Uu81soVZie2EZs5ay5/rJBqiBScvkI3gtwQW3KAbjxFn5Vra66GvBpGa/06C3RQulx1GTBPC2mckUPWSu/ZgKsQhDLzFOM+1lyrAi3tjq71lzn6eXeJfwi9mkv7+J54tREluLMQHTMl4FyTwdRpDFkmeJLTYnXSDDahX5jiFQFuQX/6NbyF+z2f50Y8U3X96eY5BWESTxEFCj5bsqKlNM4ye0ALgnHnAa1hIvn8ivA9zaMhv0ENX8kCcDoH9TgMAju/G75bft0eMXjqZAPTqraA2uRaCX3arwr4T4ZSnUy94jDxILQZg9zLFYymuJZ4KJw',
                'bm_so': '8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=',
                'mynt-eupv': '1',
                '_mxab_': 'config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled',
                'microsessid': '665',
                '_xsrf': '0JJscjS4YERWw58YPlwqOLLEb4843MNH',
                'bm_lso': '8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=^1750853121030',
                'mynt-ulc-api': 'pincode%3A380001',
                'mynt-loc-src': 'expiry%3A1750854561369%7Csource%3AIP',
                'ak_bmsc': '9B17AA5F63EF7FEBE0CDFE4E8A62E889~000000000000000000000000000000~YAAQSs4tF4Q7K3yXAQAAdnX6phy4aGlyovUWccQG+8uS0qNWkYps/GCOUCQ8vRESKHB/57LE2MgIMYGtzAlot3eTFOkIVUXDe40NOGivT5d1bLABy3E5dzIAZl7e38Yt9JR4ypvfzDut7WaYOVlwNSWB1N518TfPz0FwJg1bRiGlEUz5vXr/KLmUhP/0Pu1PR57Np0xkyg06i3Ph566Up2w+r5NIvpqo2LrTrpTfUsDtuy5CDfSbKrDWzd2ekd72Y81eBEcA9ZqKYq8bjQy65HJHf78NMw5eYirX7Lyn9v4ld+v76FUYba0z5JwW1cgKGclk8ujRwyF0EZHTfzRUakn1zNgFub7R3W17BlxMpLO8pqeMWOhxGIsor9I25bxvOHR8yAc172uVEv+X50AYBUkH1ZGWPu7SHrtoLAj/bLJZ6znZul4ewQyCB7CMSFPRVFRaALQOvLeZQJA/',
                '_gcl_au': '1.1.650218370.1750853122',
                'x-mynt-pca': 'f1ndLPB9m7Kj9HabABct0F8en18USiopZzWWd40h0ee-1Uw2ErbNYm1cg7_f5wBJssSndWpI2q59UqKLIweE6-l5KQqG7cbdimztU-XF9fbYPzfAMhd6de19qf3J28DCuHTS_PsGVtbM7wm6eWDLQJzkqyLQ-GMu71IjvPO8hEKeefT_3e717w%3D%3D',
                'tvc_VID': '1',
                '_scid': 'x2cwiqJo0xSTmZVV3KAe5dF8_AlVkJGx',
                '_cs_ex': '1',
                '_cs_c': '1',
                '_fbp': 'fb.1.1750853123203.929586668242512692',
                '_ScCbts': '%5B%5D',
                '_sctr': '1%7C1750789800000',
                '_abck': '20DCFFB6096F390F279FD729F4F28671~0~YAAQRc4tF4nFroOXAQAAFJD6pg7TdLACUWQrCai8+TlBUEXiyc+0KiNzMHIYHXAzSk4ywIeGjU7Mk9Q9pA1VRNmegQlXmxvCvhbp4ks7OW39gHB1yFNvQp2DrMTptzuGpjBVKSXt/yDh63huE6aPdi3NflYNOgOvgHBA/A+OT5nAAJQGpLh2m02lvl3aMLKyxX2Dg3v8hVNUxapQHEKc7KWJSY0dWSHDuHXb3LfYPrZKS/rTcCqzTlb13vWh6Lbtib8FWcKFyFM/uDDJ1VCuEwJnkXnb9ZtkaseFHdTRBom39L23HQwJkknm74KkDtiCCgkYr166oDD0QaDHQIiTWQory4KE1VU3Y4ivwk+0xDBscyn0D7/J4ljvARhIMgSCG4HxBGkGpSGmVUbKEJT1rvEQJzmDUAqyTFcHUcWlFT5tQnzhbiEiZuq6Lv970JgUUBhWpg7Kv0BbmTyWEP0N1gRH4zEbKSLFO3qjYLo0JZxwDcJtbawlIqEayJ4qePu2V793SkftcNDfs/IXoZASYxr7fVBgK5wh8rlPS4TcqvzVotek1t17JxDQWXpN9A7vMRV6fkKfIzYwSRFWrt8iZGXgKTohjeeQMCUFckXIa2me7z3SyVp+f/XdZp55~-1~-1~-1',
                '_ma_session': '%7B%22id%22%3A%22fb2116b0-47b6-4a24-8f09-dbe92dde4266-110e2c85-58a4-4dbe-9301-20ae21870966%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D',
                'bm_sz': 'B6E993881B0953753EDE09764AFC253C~YAAQSM4tF+CW4IOXAQAAchz7phxzu2RDvrV2WGUW+suiGyV96SZIYTZ5uZwiKUf3kGK7yopU7s2FpC0U/dAW571RdQsE7GKa0pvVjqGAJquqihQ91ls+Zvy3ZGZgXePTJTr+mMw6byj45ZrvTugrzjs3Gxf45Y85Y7hJNhi3hjGQ84U1N/jHf8VYw257WquZ4Ab7EDTQmgk5TIooLDFF+3uoVhGn3S1w6hxjlUm7DuOnIvEyrxgSkZtV4HDFqiPsJQzw9jK8EPuH+n6AjNQBVsRsvnpZdz6vie3lbNLbiW7u82cDhRA0XT9ID+RtosFNMEj9MHpdspwwhyfTxwteqygrzap4fxLuU2s8a4Hs5imrnbiI2Nx4vXY3AkYzf36eGeO+cUp8j8juPMyfNVKjr72oOSrq9/9nHpsz~3158082~4408901',
                'ak_RT': '"z=1&dm=myntra.com&si=0f4d4fff-b049-41a8-9a0f-3782fd5b439e&ss=mcbwqlt1&sl=2&tt=7ur&obo=1&rl=1"',
                '_scid_r': '0ecwiqJo0xSTmZVV3KAe5dF8_AlVkJGxl5grJQ',
                '_pv': 'default',
                'dp': 'd',
                'utrid': 'R2B%2BRQ5TG1YYBUZDC0tAMCMzMjU3NTI5MDk1JDI%3D.40f16deaaf87366d4d478ec7bcc6c0fb',
                'bm_sv': '64071DE2050E96B4F20E5A3B026F3B2A~YAAQbw7EF6/nCXuXAQAAI+cOpxzt3MtPZSer4AMWrOuJDdptJq5j9JEsFa92jRlm5kd76NgDqw84aig/sigxwVRG9oQmgQ/Mh3/V4YVMMFTTc/dLITuDhzQWiQYu+HXBjh7fhzryf2rcDWSVqCtXMUxXV+484aqgytdGeAi00G2Y5o6rjWdn7VHwVlQuTSMLvzRWwoFRbfKyrAGjzJ7sTTUYaRcnF1sKGugHpqaVbIwFoYxGbkxvIApG3tXuofhspg==~1',
            }
            headers = {
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9',
                'app': 'web',
                'content-type': 'application/json',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwNjIwNzEiLCJhcCI6IjcxODQwNzY0MyIsImlkIjoiNjA4OGM5MzExNWIwMjJjYSIsInRyIjoiZGZlNjVmNzkyN2U5NjI0MDk5MGY5NTRjYjc1OGU5M2EiLCJ0aSI6MTc1MDg1NDU3ODA4NCwidGsiOiI2Mjk1Mjg2In19',
                'pagination-context': '{"scImgVideoOffset":"0_0","v":1.0,"productsRowsShown":0,"paginationCacheKey":"1fdfa418-9b8f-4fa6-8a60-93972510090d","inorganicRowsShown":0,"plaContext":"eyJwbGFPZmZzZXQiOjAsIm9yZ2FuaWNPZmZzZXQiOjMyLCJleHBsb3JlT2Zmc2V0IjowLCJmY2NQbGFPZmZzZXQiOjUwLCJzZWFyY2hQaWFub1BsYU9mZnNldCI6NDcsImluZmluaXRlU2Nyb2xsUGlhbm9QbGFPZmZzZXQiOjAsInRvc1BpYW5vUGxhT2Zmc2V0IjozLCJvcmdhbmljQ29uc3VtZWRDb3VudCI6MTQyLCJhZHNDb25zdW1lZENvdW50Ijo1MCwiZXhwbG9yZUNvbnN1bWVkQ291bnQiOjAsImN1cnNvciI6eyJUT1BfT0ZfU0VBUkNIIjoiZmVhOmt3dHxpZHg6M3xzcmM6RkNDfmZlYTpua3d0fGlkeDowfHNyYzpGQ0N+ZmVhOmt3dHxpZHg6MHxzcmM6TVlOVFJBX1BMQX5mZWE6bmt3dHxpZHg6MHxzcmM6TVlOVFJBX1BMQSIsIlNFQVJDSCI6ImZlYTprd3R8aWR4OjQ3fHNyYzpGQ0N+ZmVhOm5rd3R8aWR4OjB8c3JjOkZDQ35mZWE6a3d0fGlkeDowfHNyYzpNWU5UUkFfUExBfmZlYTpua3d0fGlkeDowfHNyYzpNWU5UUkFfUExBIn0sInBsYXNDb25zdW1lZCI6W10sImFkc0NvbnN1bWVkIjpbXSwib3JnYW5pY0NvbnN1bWVkIjpbXSwiZXhwbG9yZUNvbnN1bWVkIjpbXX0\\u003d","refresh":false,"scOffset":0,"reqId":"1fdfa418-9b8f-4fa6-8a60-93972510090d"}',
                'priority': 'u=1, i',
                'referer': f'https://www.myntra.com/{keyword}',
                'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'traceparent': '00-dfe65f7927e96240990f954cb758e93a-6088c93115b022ca-01',
                'tracestate': '6295286@nr=0-1-3062071-718407643-6088c93115b022ca----1750854578084',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-location-context': 'pincode=380001;source=IP',
                'x-meta-app': 'channel=web',
                'x-myntra-app': 'deviceID=110e2c85-58a4-4dbe-9301-20ae21870966;customerID=;reqChannel=web;appFamily=MyntraRetailWeb;',
                'x-myntraweb': 'Yes',
                'x-requested-with': 'browser',
                # 'cookie': 'at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pWVRnek1EYzNNemd0TlRGaVl5MHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZME1EVXhNVFlzSW1semN5STZJa2xFUlVFaWZRLnN5aFcwTHJtdy1LQlRwR2hoU2Z2b1JMUmZmTDRDSDdNaU1remF0MTFUQlE=; lt_timeout=1; lt_session=1; _d_id=110e2c85-58a4-4dbe-9301-20ae21870966; bm_ss=ab8e18ef4e; bm_s=YAAQSs4tF6A6K3yXAQAASGT6pgNTyQ5scnNRaWzsBdQkPbjmGXU3wbZOz5Sp+uu/iMQKf+8bAE5zfLcEz0kCRtDKWekUoOZwTVIdPpbZfTbkkY6XRi0mLwBDpOLctF7H9P+d0uQGhoe+TvYZs2gISHy/KBtdeGHgcVpB8Ejh01BqXoqoJi7Jp9KUH0SRlcjVQcbSXQeGP9S7Mnx96kcE6mDC4bpFTVNNWVVKDx+k6pCeXb9j23Uu81soVZie2EZs5ay5/rJBqiBScvkI3gtwQW3KAbjxFn5Vra66GvBpGa/06C3RQulx1GTBPC2mckUPWSu/ZgKsQhDLzFOM+1lyrAi3tjq71lzn6eXeJfwi9mkv7+J54tREluLMQHTMl4FyTwdRpDFkmeJLTYnXSDDahX5jiFQFuQX/6NbyF+z2f50Y8U3X96eY5BWESTxEFCj5bsqKlNM4ye0ALgnHnAa1hIvn8ivA9zaMhv0ENX8kCcDoH9TgMAju/G75bft0eMXjqZAPTqraA2uRaCX3arwr4T4ZSnUy94jDxILQZg9zLFYymuJZ4KJw; bm_so=8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=; mynt-eupv=1; _mxab_=config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled; microsessid=665; _xsrf=0JJscjS4YERWw58YPlwqOLLEb4843MNH; bm_lso=8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=^1750853121030; mynt-ulc-api=pincode%3A380001; mynt-loc-src=expiry%3A1750854561369%7Csource%3AIP; ak_bmsc=9B17AA5F63EF7FEBE0CDFE4E8A62E889~000000000000000000000000000000~YAAQSs4tF4Q7K3yXAQAAdnX6phy4aGlyovUWccQG+8uS0qNWkYps/GCOUCQ8vRESKHB/57LE2MgIMYGtzAlot3eTFOkIVUXDe40NOGivT5d1bLABy3E5dzIAZl7e38Yt9JR4ypvfzDut7WaYOVlwNSWB1N518TfPz0FwJg1bRiGlEUz5vXr/KLmUhP/0Pu1PR57Np0xkyg06i3Ph566Up2w+r5NIvpqo2LrTrpTfUsDtuy5CDfSbKrDWzd2ekd72Y81eBEcA9ZqKYq8bjQy65HJHf78NMw5eYirX7Lyn9v4ld+v76FUYba0z5JwW1cgKGclk8ujRwyF0EZHTfzRUakn1zNgFub7R3W17BlxMpLO8pqeMWOhxGIsor9I25bxvOHR8yAc172uVEv+X50AYBUkH1ZGWPu7SHrtoLAj/bLJZ6znZul4ewQyCB7CMSFPRVFRaALQOvLeZQJA/; _gcl_au=1.1.650218370.1750853122; x-mynt-pca=f1ndLPB9m7Kj9HabABct0F8en18USiopZzWWd40h0ee-1Uw2ErbNYm1cg7_f5wBJssSndWpI2q59UqKLIweE6-l5KQqG7cbdimztU-XF9fbYPzfAMhd6de19qf3J28DCuHTS_PsGVtbM7wm6eWDLQJzkqyLQ-GMu71IjvPO8hEKeefT_3e717w%3D%3D; tvc_VID=1; _scid=x2cwiqJo0xSTmZVV3KAe5dF8_AlVkJGx; _cs_ex=1; _cs_c=1; _fbp=fb.1.1750853123203.929586668242512692; _ScCbts=%5B%5D; _sctr=1%7C1750789800000; _abck=20DCFFB6096F390F279FD729F4F28671~0~YAAQRc4tF4nFroOXAQAAFJD6pg7TdLACUWQrCai8+TlBUEXiyc+0KiNzMHIYHXAzSk4ywIeGjU7Mk9Q9pA1VRNmegQlXmxvCvhbp4ks7OW39gHB1yFNvQp2DrMTptzuGpjBVKSXt/yDh63huE6aPdi3NflYNOgOvgHBA/A+OT5nAAJQGpLh2m02lvl3aMLKyxX2Dg3v8hVNUxapQHEKc7KWJSY0dWSHDuHXb3LfYPrZKS/rTcCqzTlb13vWh6Lbtib8FWcKFyFM/uDDJ1VCuEwJnkXnb9ZtkaseFHdTRBom39L23HQwJkknm74KkDtiCCgkYr166oDD0QaDHQIiTWQory4KE1VU3Y4ivwk+0xDBscyn0D7/J4ljvARhIMgSCG4HxBGkGpSGmVUbKEJT1rvEQJzmDUAqyTFcHUcWlFT5tQnzhbiEiZuq6Lv970JgUUBhWpg7Kv0BbmTyWEP0N1gRH4zEbKSLFO3qjYLo0JZxwDcJtbawlIqEayJ4qePu2V793SkftcNDfs/IXoZASYxr7fVBgK5wh8rlPS4TcqvzVotek1t17JxDQWXpN9A7vMRV6fkKfIzYwSRFWrt8iZGXgKTohjeeQMCUFckXIa2me7z3SyVp+f/XdZp55~-1~-1~-1; _ma_session=%7B%22id%22%3A%22fb2116b0-47b6-4a24-8f09-dbe92dde4266-110e2c85-58a4-4dbe-9301-20ae21870966%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D; bm_sz=B6E993881B0953753EDE09764AFC253C~YAAQSM4tF+CW4IOXAQAAchz7phxzu2RDvrV2WGUW+suiGyV96SZIYTZ5uZwiKUf3kGK7yopU7s2FpC0U/dAW571RdQsE7GKa0pvVjqGAJquqihQ91ls+Zvy3ZGZgXePTJTr+mMw6byj45ZrvTugrzjs3Gxf45Y85Y7hJNhi3hjGQ84U1N/jHf8VYw257WquZ4Ab7EDTQmgk5TIooLDFF+3uoVhGn3S1w6hxjlUm7DuOnIvEyrxgSkZtV4HDFqiPsJQzw9jK8EPuH+n6AjNQBVsRsvnpZdz6vie3lbNLbiW7u82cDhRA0XT9ID+RtosFNMEj9MHpdspwwhyfTxwteqygrzap4fxLuU2s8a4Hs5imrnbiI2Nx4vXY3AkYzf36eGeO+cUp8j8juPMyfNVKjr72oOSrq9/9nHpsz~3158082~4408901; ak_RT="z=1&dm=myntra.com&si=0f4d4fff-b049-41a8-9a0f-3782fd5b439e&ss=mcbwqlt1&sl=2&tt=7ur&obo=1&rl=1"; _scid_r=0ecwiqJo0xSTmZVV3KAe5dF8_AlVkJGxl5grJQ; _pv=default; dp=d; utrid=R2B%2BRQ5TG1YYBUZDC0tAMCMzMjU3NTI5MDk1JDI%3D.40f16deaaf87366d4d478ec7bcc6c0fb; bm_sv=64071DE2050E96B4F20E5A3B026F3B2A~YAAQbw7EF6/nCXuXAQAAI+cOpxzt3MtPZSer4AMWrOuJDdptJq5j9JEsFa92jRlm5kd76NgDqw84aig/sigxwVRG9oQmgQ/Mh3/V4YVMMFTTc/dLITuDhzQWiQYu+HXBjh7fhzryf2rcDWSVqCtXMUxXV+484aqgytdGeAi00G2Y5o6rjWdn7VHwVlQuTSMLvzRWwoFRbfKyrAGjzJ7sTTUYaRcnF1sKGugHpqaVbIwFoYxGbkxvIApG3tXuofhspg==~1',
            }
            next_page_url = f'https://www.myntra.com/gateway/v2/search/{keyword}?rows=50&o=49'
            get_links(cookies, headers, keyword, next_page_url)

        return list_of_links
    else:
        logger.error("Product Details Can Not Found")


def get_myntra_data(product_url: str, reviews: bool = False, similar_products: bool = False,
                    variant_level: bool = False):
    total_number_of_requests = 1

    if not product_url:
        return {
            "HTTP Status Code:": "400 BAD_REQUEST",
            "Error Code": "INVALID_URL_DOMAIN",
            "Message": "The provided URL is not a valid Myntra product URL. Please ensure you're using a correct Flipkart product link."
        }

    if 'http' not in product_url:
        match = re.search(r'(\d+)', product_url)
        product_id = match.group(0) if match else None

    elif 'buy' not in product_url:
        match = re.search(r'/(\d+)', product_url)
        product_id = match.group(1) if match else None

    else:
        match = re.search(r'/(\d+)/buy', product_url)
        product_id = match.group(1) if match else None

    api_url = f"https://www.myntra.com/{product_id}"
    if not "www.myntra.com" in product_url:
        product_url = api_url

    raw_json = None
    response_result = None
    reviews_result = None
    similar_products_result = None

    # Use ThreadPoolExecutor for cleaner and safer threading
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_get_response = executor.submit(fetch_product, api_url)
        # if reviews:
        #     future_get_reviews = executor.submit(get_reviews, api_url)
        if similar_products:
            future_get_similar = executor.submit(get_similer_products, api_url)

        # Optionally fetch the results if needed
        response_result = future_get_response.result()
        # if reviews:
        #     reviews_result = future_get_reviews.result()
        if similar_products:
            similar_products_result = future_get_similar.result()

    ## PDP DATA :-
    # Parsing the response text using parsel Selector
    selector = Selector(text=response_result['Data'].text)

    # Extracting the product data embedded in a script tag
    data = selector.xpath(
        "//script[contains(text(), 'window.__myx') and contains(text(), 'pdpData') and contains(text(), 'discountedPrice')]/text()"
    ).get()

    if not data:
        return {
            "HTTP Status Code": 404,
            "Error Code": "NOT_FOUND",
            "Description": "The requested product or resource could not be found",
            "Error Message": "The requested resource was not found."
        }

    # Clean and parse the extracted data
    try:
        data = data.split('window.__myx = ')[1].strip()
        if data.endswith(';'):
            data = data[:-1]
    except:
        data = data.split('window.__myx = ')[0].strip()
        if data.endswith(';'):
            data = data[:-1]

    try:
        parsed_data = json.loads(data)  # Convert string to Python dict
    except json.JSONDecodeError as e:
        return {"statusCode": 500, "status": "error", "message": f"Failed to parse JSON data: {e}"}

    pdp_data = parsed_data.get('pdpData', {})
    product_id = pdp_data.get('id', "N/A")

    # Initializing the result dictionary
    result = {
        # 'date_given': datetime.now().strftime("%Y-%m-%d"),
        'product_name': pdp_data.get('name', "N/A").strip(),
        'product_id': product_id,  # Placeholder, adjust as needed
        # 'scrap_date_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'scrap_date_and_time': str(datetime.datetime.now()).replace(" ", "T")[:-3] + "Z",
        'image_urls': [],
        'brand': pdp_data.get('brand', "NA").get('name'),
        'product_details': {},
        'product_specifications': "N/A",
        'seller_info': "N/A",
        'product_url': product_url,
        'mrp': "",
        "available_sizes": "",
        'selling_price': pdp_data.get('price', {}).get('discounted', "N/A"),
        'discount': "N/A",
        'color_list': [],
        'in_stock_out_of_stock_status': "",
        'colour': "N/A",
        'size_list': "N/A",
        'size_chart': "N/A",
        'product_rating': round(pdp_data.get('ratings', {}).get('averageRating', 0), 1),
        'total_rating_count': pdp_data.get('ratings', {}).get('totalCount', 0),
        'individual_ratings_count': "N/A",
        'category': "N/A",
    }

    try:
        result['variant'] = [variant['displayText'] for variant in pdp_data.get('relatedStyles')]
    except:
        pass

    # TODO : discount: need to set when no price
    try:
        result['discount'] = pdp_data.get('discounts', [{}])[0].get('discountPercent', "N/A")
    except:
        result['discount'] = "N/A"
    try:
        # Initialize the 'image_links': [], list in the result dictionary
        result['image_urls'] = []

        # Loop through the albums in the 'media' key
        for album in pdp_data.get('media', {}).get('albums', []):
            for image in album.get('images', []):
                result['image_urls'].append(image.get('imageURL', "NA").strip())

    except Exception as e:
        result['image_urls'] = "N/A"
        print(f"Error: {e}")

    desc_text = {}

    for item in pdp_data.get('productDetails', []):
        title = item.get('title', 'Unknown Title')
        description = item.get('description', '')

        if "<b>" in description:
            html_text = unescape(description)

            # ✅ Handle free text before first <b>
            first_b_match = re.search(r"<b>", html_text)
            if first_b_match:
                initial_text = html_text[:first_b_match.start()].strip()
                initial_text = re.sub(r'<br\s*/?>', '\n', initial_text, flags=re.IGNORECASE)
                initial_text = re.sub(r'<[^>]+>', '', initial_text).strip()
                if initial_text:
                    if title == 'Product Details':
                        desc_text['text'] = initial_text
                    else:
                        desc_text[title.lower().replace(" ", "_")] = initial_text

            # ✅ Now handle all <b>...</b> blocks
            matches = list(re.finditer(r"<b>(.*?)</b>(.*?)(?=<b>|$)", html_text, re.DOTALL))
            for match in matches:
                key = match.group(1).strip().lower().replace(" ", "_")
                content = match.group(2).strip()

                if '<ul>' in content:
                    items = re.findall(r"<li>(.*?)</li>", content)
                    desc_text[key] = [item.strip() for item in items]
                else:
                    text = re.sub(r'<[^>]+>', '', content).strip()
                    desc_text[key] = text

        else:
            clean_description = re.sub(r'<br\s*/?>', '\n', description, flags=re.IGNORECASE)
            # Clean the description (remove unwanted escape characters and format text)
            clean_description = re.sub(r'\\\"', '', clean_description)  # Remove escaped quotes

            # Ensure there is a space before "Machine Wash"

            # If the title is 'product_details', change it to 'text'
            if title == 'Product Details':
                title = 'text'

            # For the 'SIZE & FIT', format it more clearly
            if title == 'SIZE & FIT':
                clean_description = re.sub(r'(\d+)"', r'\1 inches', clean_description)  # Convert height in inches
                clean_description = clean_description.replace('MChest', 'Chest').replace('Height',
                                                                                         'Height:')  # Readable formatting
            clean_description = re.sub("<.*?>", "", clean_description).replace('&nbsp;', ' ')
            title = title.lower().replace(" ", "_")
            desc_text[title] = [part.strip() for part in clean_description.split('\n') if part.strip()]

    try:
        result['product_details'] = desc_text
    except Exception as e:
        print(f"Error in Description json dumps :: {e}")
        result['product_details'] = "N/A"

    # Extracting product specifications
    try:
        def strip_html(text):
            return re.sub(r'<[^>]+>', '', text).strip()

        specification = pdp_data.get('articleAttributes', {})
        result['product_specifications'] = {
            key.lower().replace("-", "_").replace(" ", "_"): strip_html(value)
            for key, value in specification.items()
            if value.strip() not in ['N/A', '']
        }
    except:
        pass

    try:
        def lower_keys(obj):
            if isinstance(obj, dict):
                return {k.lower(): lower_keys(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [lower_keys(item) for item in obj]
            else:
                return obj

        sellers = pdp_data.get('sellers', [])

        if isinstance(sellers, list):
            if len(sellers) >= 1:
                sellers = sellers[0]

        result['seller_info'] = lower_keys(sellers)
    except KeyError as e:
        print(f"KeyError: Missing expected key seller info - {e}")
        result['seller_info'] = "N/A"
    except Exception as e:
        print(f"An unexpected error occurred seller info: {e}")
        result['seller_info'] = "N/A"

    try:
        # Extract only the 'label' (size) for each entry
        size_labels = [size.get("label") for size in pdp_data.get('sizes', [])]
        result['size_list'] = size_labels
    except KeyError as e:
        print(f"KeyError: Missing expected key - {e}")
        result['size_list'] = "N/A"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result['size_list'] = "N/A"

    try:
        Tag = []
        for available_sizes in pdp_data.get('sizes'):
            size_seller_data = available_sizes.get('sizeSellerData', [])

            if size_seller_data:
                left_item_count = size_seller_data[0].get('availableCount', 0)

                left_size = available_sizes.get('label', 'Unknown Size')

                if left_item_count:  # "tagText": "Only Few Left!","skuThreshold": 5,
                    Tag.append(f"{left_size}")
        if Tag:
            result['available_sizes'] = Tag
        else:
            result['available_sizes'] = "N/A"
    except:
        result['available_sizes'] = "N/A"

    try:
        # Extract only the 'label' (size) for each entry
        colors = pdp_data.get('baseColour', "N/A")

        result['colour'] = colors
    except KeyError as e:
        print(f"KeyError: Missing expected key - {e}")
        result['colour'] = "N/A"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result['colour'] = "N/A"

    result['mrp'] = pdp_data.get('mrp', "N/A")

    try:
        out_of_stock = pdp_data.get('flags', {}).get('outOfStock', None)

        if out_of_stock is False:
            instock_status = True  # Item is in stock
        else:
            instock_status = False  # Out of stock or unknown status

    except Exception as e:
        instock_status = False  # Default to False in case of an error
        print(f"Error: {str(e)}")  # Log the error for debugging

    result['in_stock_out_of_stock_status'] = instock_status

    # tODO  : size_chart
    all_sizes = pdp_data.get('sizes', [])
    size_chart = []

    for allsize in all_sizes:
        size_data = {}
        size_data["size_list"] = allsize.get("label", "N/A").strip()

        for m in allsize.get("measurements", []):
            name = m.get("name", "").strip()
            name = name.lower().replace(" ", "_")
            value = m.get("value", "").strip()
            size_data[name] = value
            size_data['unit'] = m.get("unit", "").strip()

        size_chart.append(size_data)

    try:
        result['size_chart'] = size_chart
    except Exception as e:
        print(f"Errorn in size_chart json dumps :{str(e)}")

        # TODO : Reviews
    try:
        if reviews:
            total_number_of_requests += 1
            response_review = reviews_result

            if response_review['HTTP Status Code'] != 200:
                result['reviews'] = response_review

            # TODO - format reviews
            selector = Selector(text=response_review['Data'].text)
            review_data_text = selector.xpath("//script[contains(text(),'reviewsData')]/text()").get()

            review_json_data = review_data_text.replace('window.__myx =', '').strip()

            try:
                review_json_data = json.loads(review_json_data)
                review_json_data = review_json_data['reviewsData']
            except:
                print("error in review_json_data")
                pass

            reviews_data = []

            for review in review_json_data.get('reviews', []):
                user_name = review.get('userName', 'N/A')
                review_text = review.get('review', 'N/A').replace('\n\n', '')

                timestamp_ms = review.get('updatedAt', 'N/A')
                if timestamp_ms:
                    timestamp_ms = int(timestamp_ms)
                    review_date = str(datetime.datetime.fromtimestamp(int(timestamp_ms) / 1000))

                else:
                    review_date = "N/A"

                reviewer_rating = review.get('userRating', 'N/A')
                review_images = [image.get("url") for image in review.get('images', [])]

                reviews_data.append({
                    'review_descriptions': review_text,
                    'reviewer_ratings': reviewer_rating,
                    'images_posted_by_reviewers': review_images,
                    'relative_review_dates': review_date,
                    'reviewer_name': user_name,
                })
            result['reviews'] = reviews_data

    except Exception as e:
        result['reviews'] = "N/A"

    try:
        # Extract only the 'label' (size) for each entry
        rating_info = pdp_data.get('ratings', {}).get('ratingInfo', [])
        # Filter and sort the ratings by rating value (as integers)
        sorted_rating_info = sorted(
            [item for item in rating_info if item['count'] > 0],
            key=lambda x: int(x['rating'])
        )

        result['individual_ratings_count'] = {
            str(item['rating']): item['count'] for item in sorted_rating_info
        }
    except KeyError as e:
        result['individual_ratings_count'] = "N/A"

    try:
        cat = selector.xpath('//script[contains(text(), "BreadcrumbList")]/text()').get()
        clean_data = re.sub(r'\s+', ' ', cat).strip()
        clean_data = json.loads(clean_data)
        categories = clean_data['itemListElement']

        # Create the desired category mapping
        category_map = {}

        # Iterate over the list and assign each category to the L1, L2, L3, etc.
        for i, category1 in enumerate(categories):
            category_name = category1['item']['name']
            category_map[f'l{i + 1}'] = category_name

        result['category'] = category_map
    except Exception as e:
        print(f"Exception in category: {e}")
        result['category'] = "N/A"

    try:
        color_list = []
        if variant_level:
            veriation_ids = [veria_id for veria_id in pdp_data.get('colours', [])]
            for varia in veriation_ids:
                if 'label' in varia:
                    varia['url'] = "https://www.myntra.com/" + varia.get('url')
                    varia['colour'] = varia.pop('label')
                    color_list.append(varia['colour'])
            result['color_list'] = color_list
            result['variant_level'] = veriation_ids
    except Exception as e:
        result['variant_level'] = "N/A"

    try:
        # TODO: similar products
        if similar_products:
            data1 = None
            total_number_of_requests += 1

            for attempt in range(3):
                response_similar_products = similar_products_result
                if response_similar_products['HTTP Status Code'] != 200:
                    result['similar_product'] = response_similar_products
                try:
                    data1 = json.loads(response_similar_products['Data'].text)
                    break
                except json.JSONDecodeError as e:
                    print(f"Retrying ....:{attempt}")
                    attempt += 1
                    # print(f"[Attempt {attempt + 1}] JSON error: {e}")

            product_list = []
            for products in data1.get('related'):
                if products.get('type') == 'Similar':
                    for item in products.get('products'):
                        name = item.get('name', "N/A")
                        MRP = item.get('price').get('mrp', "N/A")
                        product_price = item.get('price').get('discounted', "N/A")
                        image_url = item.get('defaultImage').get('src')
                        product_url = "https://www.myntra.com/" + item.get('landingPageUrl')
                        discount = item.get('price').get('discount').get('label').strip('(').strip(')')
                        try:
                            rating = round(item.get('rating'))
                        except:
                            rating = "N/A"

                        if discount:
                            discount_list = re.findall(r"\d+", discount)
                            discount = "".join([discount.strip() for discount in discount_list if discount])
                            discount = int(discount)
                        else:
                            discount = "N/A"

                        product_list.append({
                            "name": name,
                            "mrp": MRP,
                            "product_rice": product_price,
                            "product_url": product_url,
                            "image_url": image_url,
                            "discount": discount,
                            "rating": rating
                        })
            result['similar_product'] = product_list

    except:
        result['similar_product'] = []

    result['total_number_of_requests'] = total_number_of_requests

    try:
        result['discount'] = str(round((1 - float(result['selling_price']) / float(result['mrp'])) * 100))
    except:
        result['discount'] = "N/A"

    result['individual_ratings_count'] = result['individual_ratings_count'] if result[
        'individual_ratings_count'] else "N/A"

    if result['discount'] != 'N/A':
        result['discount'] = int(result['discount'])

    if result['discount'] == 0 or result['discount'] == str(0):
        result['discount'] = 'N/A'

    del result['reviews']
    return result


def fetch_product_data(product_link):
    return get_myntra_data(
        product_url=product_link,
        reviews=True,
        similar_products=True,
        variant_level=True
    )


def replace_ampersand(obj):
    if isinstance(obj, dict):
        return {k: replace_ampersand(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_ampersand(i) for i in obj]
    elif isinstance(obj, str):
        return obj.replace("&amp;", "&")
    else:
        return obj


if __name__ == '__main__':
    cookies = {
        '_pv': 'default',
        'dp': 'd',
        'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pWldabFlUQTROVFl0TlRVM1lpMHhNV1l3TFdKbFltVXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZNE1UY3hNalFzSW1semN5STZJa2xFUlVFaWZRLlhURFJURlgyX29zWlVBYnRaQ2VhbmdxR2xtRU1JWkVkR3BjR0NrSnAzelE=',
        'utm_track_v1': '%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1751265124%2C%22trackend%22%3A1751265184%7D',
        'lt_timeout': '1',
        'lt_session': '1',
        '_d_id': 'fa19abf8-c5e6-4722-8e7a-7f8c6795f9aa',
        'bm_ss': 'ab8e18ef4e',
        'bm_so': '8CAB1A1D6DF03E79480B5B2DC22D7BE6D9DF117C6E894D9C8983D438373EFAC6~YAAQNA7EF37g3HqXAQAAZyGJvwRfnvFr3onHBrcEBBWX+XhVqcUlPHsEluLS6RG4kT+4fIwQzgNM0ExFPGTP1eRcXbdsEUelDRjH/GlKfmjm0EJuGEKyptrBZQv4uJsZhFcfHDaBMfwgmVW/c1QvmmqMGJ5j7ejkvLarsrug2TFhQmv1EV0sMxAvwLzjXHasi85vuwCy2+BHYUzZwFygjnSz7qhK9uDH5C1PtK05eRPNII6D3PUCae1bkHmdQTDY3MfXb7ZmK8YF9SRw84d6LTogvpdk15885nY1dIL776Jz3g1TWFeioc8YiG8Gh6FIvaJcmr8HHN8An8wi6c2PfloGLxO8SmXD5fwqZIi3j59yrY+kr3cEwl5xNKKSJPnjwR9yjjlfBC06pCvD3EPn9bp4j7yIo4VOxcCjoAt+aUHL7gkhVlSqlzqg5LxTIPS32T5CDWPB8BuyxTIr08k=',
        'bm_sz': 'A92959DE8C86B81C44C50AB76CA62F00~YAAQNA7EF3/g3HqXAQAAZyGJvxyDzD5b1IESBBaLNrwhaFkdGcMwAjwW8c1qZoGleRvhQe9utFA+dGw0M3/Q/9G76xV3HYXtKhsJwpE5SHeBQsBYZxwQWEK9UkRSqji+uHbAQ7+jMiM8eUbFeaRyNNt++CW1duyE06NVeGtVBa5bwbtAYLubQCIlZtqtFYI2qFRad7TOujFztg3n8SadIuoHbe2EqXZZmWuUFzrojIUw5bD7J7jPKtS+qtwI7Lq6RXMKNLOgP6jc6s9CkKEHmakwtsX0YB3CAXr7zcRMIHhtrc41NKJ57i11aFk659ZbEW4JcW3e5CbWhGY9iV49X59XfISbHb7d5EuFycBFdQ9XUSg31jW/vxHpFI+shvWaeJrFElRHiMP5wx1piQw=~3159856~3224884',
        '_mxab_': 'config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled',
        'microsessid': '959',
        '_xsrf': 'PlcY5S5Fq0qNIqbinvXlmXsKgj7TLmCj',
        'user_session': 'z0EosNJkn2Z5aZXm3sgh4Q.BD1X4DARNC17_SdBgV6Ew7CNuclrbeZHvF212X9y5NRmhLKZYV3I5GXllViVWWrWE9nHBCfKs1os33ZH_zCD6Q_kzP4KaJjYRqRzc25dO13m4jqvf2q4fTySb7Z6_7CYGaOuTxlA8IgxKtZTt5Qmiw.1751265126152.86400000.H5X_DbV6wtjfYPi1n6EZQBFwl19gwBXMwRi_GfeKq_I',
        'mynt-eupv': '1',
        'bm_lso': '8CAB1A1D6DF03E79480B5B2DC22D7BE6D9DF117C6E894D9C8983D438373EFAC6~YAAQNA7EF37g3HqXAQAAZyGJvwRfnvFr3onHBrcEBBWX+XhVqcUlPHsEluLS6RG4kT+4fIwQzgNM0ExFPGTP1eRcXbdsEUelDRjH/GlKfmjm0EJuGEKyptrBZQv4uJsZhFcfHDaBMfwgmVW/c1QvmmqMGJ5j7ejkvLarsrug2TFhQmv1EV0sMxAvwLzjXHasi85vuwCy2+BHYUzZwFygjnSz7qhK9uDH5C1PtK05eRPNII6D3PUCae1bkHmdQTDY3MfXb7ZmK8YF9SRw84d6LTogvpdk15885nY1dIL776Jz3g1TWFeioc8YiG8Gh6FIvaJcmr8HHN8An8wi6c2PfloGLxO8SmXD5fwqZIi3j59yrY+kr3cEwl5xNKKSJPnjwR9yjjlfBC06pCvD3EPn9bp4j7yIo4VOxcCjoAt+aUHL7gkhVlSqlzqg5LxTIPS32T5CDWPB8BuyxTIr08k=^1751265126407',
        '_ma_session': '%7B%22id%22%3A%228292f5ad-df4c-450e-8d28-85e19fc43e3e-fa19abf8-c5e6-4722-8e7a-7f8c6795f9aa%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D',
        'mynt-ulc-api': 'pincode%3A380001',
        'mynt-loc-src': 'expiry%3A1751266566810%7Csource%3AIP',
        'ak_bmsc': '9ACDEAA8AA06F6B21E1DB7F4136D18A7~000000000000000000000000000000~YAAQNA7EF7vg3HqXAQAAsimJvxwawSbDg6c8pyw0bwUl8JIH97GQAZs6g2f3skzjW1PlUf/DHzz6+Wy6vJSJj5Tk77pfcm2HJL3fCXqvapYMm2hBDAYoPJiEpK4ohloxLF90YLcZpyXkhwusR9JeFxqTDHIrpXDJBekyqGpScB2GSKkAE7Oop1IwEnvOBMwvgxroxU5CZkjWatQbsw8Xjq0uQcG8In5tPiquiwvua3yK+rK1LTai6iApS1pmc2MYDbJ982j+ymRGdOYu9+uMcqpQyDjCXZQ1GNYDkGiLHH0mq7FZW07O8gQAGgxnkkA3dV3S4RNnAG3cxeVTWz0xKUpqMgOyAOkjMH9/awzSLTIRHZMR1Xfx+GsHOiYA0zWRH356a7T7PZTqRtS8IgVFKu/EPFknjlMJng2DnKnfD1sQ63WaObF8DaVPDm+BvRBEP+BCJ7/1fRAd0Tok',
        'x-mynt-pca': 'VMOrMsNvI4QZA03w0CkbEE2i6iO691xGap8CY4hgLMQcNf4xwhORUdeVcfTkX7O7BRPvlj0fwnuJD4E0YuGIIk9KZelKErAS8bZuUXDvs49m-PiJT_neXXxR5hptbSnD-l7yP8MlypXXr7skLj3BusGEj7HbIVmpZMb4XEHS8Rf6V2p5mfpvpA%3D%3D',
        '_gcl_au': '1.1.1347321738.1751265127',
        '_abck': 'F2E8BD3E646E130A2A0296548497B4AD~-1~YAAQNA7EF8fg3HqXAQAAKiyJvw6qXo1E6H1FQbXAiIY63J3drewp7+v/GZ8A35MaA6MHAkvofFTzp4+hb/SaBFSQ7wFedzKq9667CFRHQFUz5y2au5GkQNWCOtORh3RLafpRdCSmgKIil32r2xhGF1lAZnHa5LQHJybsvbkP/6tGqQqQK9Umm9aMaFtVnjHf0PzkUY2znGHA2YeH6oGkV+XmsT6lkmhBwuSlzgIebQWqVwdGWA8eYmlO4acqvyphJTilRgXBai+gk7DtQdyi/Tkos8zkDlb5AqsfcK2+7wPams7kuXkpWSWTPh4KIIQcFGBTUyIZ8E6iYC9pSsPqfOmJNKNmGwr3LdDLxg8mQf1ayY/GkMLMZ+aS8jV8wB1M97AO4bLuyudG61dwJbBqYcqR+kOpxABmY7q7XpdMf4aQWn+htC0y4aCDCI1YkSnRL+Plqvuq2bKtve4JQhzz7DL+sOIIW0W0KG3ifojDF/AYiato4/l7Pgeg9oBIp5FHXf84lfIm1au3CmwVUzIP9wqxHnPb05mEfBNDvpbIiHfUArd9i6ey9588In1cM9y1ASSwWx5dlnWRu0Ot0MVfomnlfniSge8SVbLeoFPX~-1~||0||~-1',
        '_cs_ex': '1',
        '_cs_c': '1',
        'tvc_VID': '1',
        '_fbp': 'fb.1.1751265127758.531104310362316049',
        '_scid': 'J89R5P9ceButr7V1bIEnvBfUHWO7E-gy',
        '_scid_r': 'J89R5P9ceButr7V1bIEnvBfUHWO7E-gy',
        '_ScCbts': '%5B%5D',
        '_sctr': '1%7C1751221800000',
        'utrid': 'dH8PeFd0bWFZeHdaAR1AMCM3NjIxMjgyMzYkMg%3D%3D.26acd740d6546e634caf56cd16382db0',
        'bm_sv': '34A899F97CD8E9D2D5BDB2E7E27BC7A2~YAAQNA7EFzvh3HqXAQAAgTuJvxweYmPUtU8WpVCj2S+E6H3/h1GXjrVrnfNqBfIQtmv/aHmy2sQ5WPiKQgZBy01stZmaBEpa1bAQlpVTNsxwo9ewpb8TPzDN9+OJPJy7/Ot+rE6yszDXVuBs4UzzSioct4OMIU3vFP9h3qk6sCLQGHMJp+p/FVtL/QJTscihkugE12W34mKRQlVtZHCsdAZgNFaBXi4T7iEFA+RUpfPRs562ynjfpjD0S/6hGVrU~1',
        'bm_s': 'YAAQNA7EF1Ph3HqXAQAApj6JvwOpE+2o9CQqEO053B8/dNph0Voj8Gf71lmxW2qF8Dgybr1usYlzh/QtEAlz9a7eKvNJmr2L8KTlxT3b9HNJ/8lYEjbB0SF7ECAXafJQF+bfC+c5fW8f9+UJxLDvuvgi1Q2+9zDI1FcfrIsOE20p3c2PKjkAqtbw4llXw9fQy+BQ91oxSRf1P+UZvQeuEUfc34Vrt7udA/6bU2zOwFN9367C7pAfKrY3I0VVwxwhEV3N3vqeeIkv8LMDnqrBLRUcQXrOPoGH2nI6CzWUDL1vCCjd6dwYnVGL80qI+hMO5JbbqPDM84ATAmBVU7qE/uKHFUBItvdhieY71oJqNciIX2z1Dg5tGliT0qx/Dn+bdLd1IOVrbEXmsR9I3j5Qllnp6ETH1wshmD+PXzcROznay/w719x9S2Flr6xwITfBNsq+djtU3UDmUrUQ/fNUybz4T6+a4/t0wu97FnSvxPMGFHZEnZix2CJEuSRrT1viuC8/U7mIrrFxV3kUlCAtwSBXhJtEqKi5XVzkQzZAAj8u6Jq7WHFpaSo6KyNc6MdnbTIpPUA=',
        'ak_RT': '"z=1&dm=myntra.com&si=1b1aaeda-d856-45e1-b821-569dddf8fcf7&ss=mciq1dza&sl=1&tt=3wg&rl=1&ld=3wj&ul=a4w"',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"e652d-9bXGyxdwTiU5+6MFDFuhNX+0wU0"',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # 'cookie': '_pv=default; dp=d; at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pWldabFlUQTROVFl0TlRVM1lpMHhNV1l3TFdKbFltVXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZNE1UY3hNalFzSW1semN5STZJa2xFUlVFaWZRLlhURFJURlgyX29zWlVBYnRaQ2VhbmdxR2xtRU1JWkVkR3BjR0NrSnAzelE=; utm_track_v1=%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1751265124%2C%22trackend%22%3A1751265184%7D; lt_timeout=1; lt_session=1; _d_id=fa19abf8-c5e6-4722-8e7a-7f8c6795f9aa; bm_ss=ab8e18ef4e; bm_so=8CAB1A1D6DF03E79480B5B2DC22D7BE6D9DF117C6E894D9C8983D438373EFAC6~YAAQNA7EF37g3HqXAQAAZyGJvwRfnvFr3onHBrcEBBWX+XhVqcUlPHsEluLS6RG4kT+4fIwQzgNM0ExFPGTP1eRcXbdsEUelDRjH/GlKfmjm0EJuGEKyptrBZQv4uJsZhFcfHDaBMfwgmVW/c1QvmmqMGJ5j7ejkvLarsrug2TFhQmv1EV0sMxAvwLzjXHasi85vuwCy2+BHYUzZwFygjnSz7qhK9uDH5C1PtK05eRPNII6D3PUCae1bkHmdQTDY3MfXb7ZmK8YF9SRw84d6LTogvpdk15885nY1dIL776Jz3g1TWFeioc8YiG8Gh6FIvaJcmr8HHN8An8wi6c2PfloGLxO8SmXD5fwqZIi3j59yrY+kr3cEwl5xNKKSJPnjwR9yjjlfBC06pCvD3EPn9bp4j7yIo4VOxcCjoAt+aUHL7gkhVlSqlzqg5LxTIPS32T5CDWPB8BuyxTIr08k=; bm_sz=A92959DE8C86B81C44C50AB76CA62F00~YAAQNA7EF3/g3HqXAQAAZyGJvxyDzD5b1IESBBaLNrwhaFkdGcMwAjwW8c1qZoGleRvhQe9utFA+dGw0M3/Q/9G76xV3HYXtKhsJwpE5SHeBQsBYZxwQWEK9UkRSqji+uHbAQ7+jMiM8eUbFeaRyNNt++CW1duyE06NVeGtVBa5bwbtAYLubQCIlZtqtFYI2qFRad7TOujFztg3n8SadIuoHbe2EqXZZmWuUFzrojIUw5bD7J7jPKtS+qtwI7Lq6RXMKNLOgP6jc6s9CkKEHmakwtsX0YB3CAXr7zcRMIHhtrc41NKJ57i11aFk659ZbEW4JcW3e5CbWhGY9iV49X59XfISbHb7d5EuFycBFdQ9XUSg31jW/vxHpFI+shvWaeJrFElRHiMP5wx1piQw=~3159856~3224884; _mxab_=config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled; microsessid=959; _xsrf=PlcY5S5Fq0qNIqbinvXlmXsKgj7TLmCj; user_session=z0EosNJkn2Z5aZXm3sgh4Q.BD1X4DARNC17_SdBgV6Ew7CNuclrbeZHvF212X9y5NRmhLKZYV3I5GXllViVWWrWE9nHBCfKs1os33ZH_zCD6Q_kzP4KaJjYRqRzc25dO13m4jqvf2q4fTySb7Z6_7CYGaOuTxlA8IgxKtZTt5Qmiw.1751265126152.86400000.H5X_DbV6wtjfYPi1n6EZQBFwl19gwBXMwRi_GfeKq_I; mynt-eupv=1; bm_lso=8CAB1A1D6DF03E79480B5B2DC22D7BE6D9DF117C6E894D9C8983D438373EFAC6~YAAQNA7EF37g3HqXAQAAZyGJvwRfnvFr3onHBrcEBBWX+XhVqcUlPHsEluLS6RG4kT+4fIwQzgNM0ExFPGTP1eRcXbdsEUelDRjH/GlKfmjm0EJuGEKyptrBZQv4uJsZhFcfHDaBMfwgmVW/c1QvmmqMGJ5j7ejkvLarsrug2TFhQmv1EV0sMxAvwLzjXHasi85vuwCy2+BHYUzZwFygjnSz7qhK9uDH5C1PtK05eRPNII6D3PUCae1bkHmdQTDY3MfXb7ZmK8YF9SRw84d6LTogvpdk15885nY1dIL776Jz3g1TWFeioc8YiG8Gh6FIvaJcmr8HHN8An8wi6c2PfloGLxO8SmXD5fwqZIi3j59yrY+kr3cEwl5xNKKSJPnjwR9yjjlfBC06pCvD3EPn9bp4j7yIo4VOxcCjoAt+aUHL7gkhVlSqlzqg5LxTIPS32T5CDWPB8BuyxTIr08k=^1751265126407; _ma_session=%7B%22id%22%3A%228292f5ad-df4c-450e-8d28-85e19fc43e3e-fa19abf8-c5e6-4722-8e7a-7f8c6795f9aa%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D; mynt-ulc-api=pincode%3A380001; mynt-loc-src=expiry%3A1751266566810%7Csource%3AIP; ak_bmsc=9ACDEAA8AA06F6B21E1DB7F4136D18A7~000000000000000000000000000000~YAAQNA7EF7vg3HqXAQAAsimJvxwawSbDg6c8pyw0bwUl8JIH97GQAZs6g2f3skzjW1PlUf/DHzz6+Wy6vJSJj5Tk77pfcm2HJL3fCXqvapYMm2hBDAYoPJiEpK4ohloxLF90YLcZpyXkhwusR9JeFxqTDHIrpXDJBekyqGpScB2GSKkAE7Oop1IwEnvOBMwvgxroxU5CZkjWatQbsw8Xjq0uQcG8In5tPiquiwvua3yK+rK1LTai6iApS1pmc2MYDbJ982j+ymRGdOYu9+uMcqpQyDjCXZQ1GNYDkGiLHH0mq7FZW07O8gQAGgxnkkA3dV3S4RNnAG3cxeVTWz0xKUpqMgOyAOkjMH9/awzSLTIRHZMR1Xfx+GsHOiYA0zWRH356a7T7PZTqRtS8IgVFKu/EPFknjlMJng2DnKnfD1sQ63WaObF8DaVPDm+BvRBEP+BCJ7/1fRAd0Tok; x-mynt-pca=VMOrMsNvI4QZA03w0CkbEE2i6iO691xGap8CY4hgLMQcNf4xwhORUdeVcfTkX7O7BRPvlj0fwnuJD4E0YuGIIk9KZelKErAS8bZuUXDvs49m-PiJT_neXXxR5hptbSnD-l7yP8MlypXXr7skLj3BusGEj7HbIVmpZMb4XEHS8Rf6V2p5mfpvpA%3D%3D; _gcl_au=1.1.1347321738.1751265127; _abck=F2E8BD3E646E130A2A0296548497B4AD~-1~YAAQNA7EF8fg3HqXAQAAKiyJvw6qXo1E6H1FQbXAiIY63J3drewp7+v/GZ8A35MaA6MHAkvofFTzp4+hb/SaBFSQ7wFedzKq9667CFRHQFUz5y2au5GkQNWCOtORh3RLafpRdCSmgKIil32r2xhGF1lAZnHa5LQHJybsvbkP/6tGqQqQK9Umm9aMaFtVnjHf0PzkUY2znGHA2YeH6oGkV+XmsT6lkmhBwuSlzgIebQWqVwdGWA8eYmlO4acqvyphJTilRgXBai+gk7DtQdyi/Tkos8zkDlb5AqsfcK2+7wPams7kuXkpWSWTPh4KIIQcFGBTUyIZ8E6iYC9pSsPqfOmJNKNmGwr3LdDLxg8mQf1ayY/GkMLMZ+aS8jV8wB1M97AO4bLuyudG61dwJbBqYcqR+kOpxABmY7q7XpdMf4aQWn+htC0y4aCDCI1YkSnRL+Plqvuq2bKtve4JQhzz7DL+sOIIW0W0KG3ifojDF/AYiato4/l7Pgeg9oBIp5FHXf84lfIm1au3CmwVUzIP9wqxHnPb05mEfBNDvpbIiHfUArd9i6ey9588In1cM9y1ASSwWx5dlnWRu0Ot0MVfomnlfniSge8SVbLeoFPX~-1~||0||~-1; _cs_ex=1; _cs_c=1; tvc_VID=1; _fbp=fb.1.1751265127758.531104310362316049; _scid=J89R5P9ceButr7V1bIEnvBfUHWO7E-gy; _scid_r=J89R5P9ceButr7V1bIEnvBfUHWO7E-gy; _ScCbts=%5B%5D; _sctr=1%7C1751221800000; utrid=dH8PeFd0bWFZeHdaAR1AMCM3NjIxMjgyMzYkMg%3D%3D.26acd740d6546e634caf56cd16382db0; bm_sv=34A899F97CD8E9D2D5BDB2E7E27BC7A2~YAAQNA7EFzvh3HqXAQAAgTuJvxweYmPUtU8WpVCj2S+E6H3/h1GXjrVrnfNqBfIQtmv/aHmy2sQ5WPiKQgZBy01stZmaBEpa1bAQlpVTNsxwo9ewpb8TPzDN9+OJPJy7/Ot+rE6yszDXVuBs4UzzSioct4OMIU3vFP9h3qk6sCLQGHMJp+p/FVtL/QJTscihkugE12W34mKRQlVtZHCsdAZgNFaBXi4T7iEFA+RUpfPRs562ynjfpjD0S/6hGVrU~1; bm_s=YAAQNA7EF1Ph3HqXAQAApj6JvwOpE+2o9CQqEO053B8/dNph0Voj8Gf71lmxW2qF8Dgybr1usYlzh/QtEAlz9a7eKvNJmr2L8KTlxT3b9HNJ/8lYEjbB0SF7ECAXafJQF+bfC+c5fW8f9+UJxLDvuvgi1Q2+9zDI1FcfrIsOE20p3c2PKjkAqtbw4llXw9fQy+BQ91oxSRf1P+UZvQeuEUfc34Vrt7udA/6bU2zOwFN9367C7pAfKrY3I0VVwxwhEV3N3vqeeIkv8LMDnqrBLRUcQXrOPoGH2nI6CzWUDL1vCCjd6dwYnVGL80qI+hMO5JbbqPDM84ATAmBVU7qE/uKHFUBItvdhieY71oJqNciIX2z1Dg5tGliT0qx/Dn+bdLd1IOVrbEXmsR9I3j5Qllnp6ETH1wshmD+PXzcROznay/w719x9S2Flr6xwITfBNsq+djtU3UDmUrUQ/fNUybz4T6+a4/t0wu97FnSvxPMGFHZEnZix2CJEuSRrT1viuC8/U7mIrrFxV3kUlCAtwSBXhJtEqKi5XVzkQzZAAj8u6Jq7WHFpaSo6KyNc6MdnbTIpPUA=; ak_RT="z=1&dm=myntra.com&si=1b1aaeda-d856-45e1-b821-569dddf8fcf7&ss=mciq1dza&sl=1&tt=3wg&rl=1&ld=3wj&ul=a4w"',
    }

    # Todo: Working keyword list : ["tshirts","fabindia","funky","lakme","bajaj","adidas","puma"]
    keyword_name = "tshirts"

    keyword_url = f'https://www.myntra.com/{keyword_name}'
    list_of_product_links = get_links(cookies, headers, keyword_name, keyword_url)

    final_data = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(fetch_product_data, link): link for link in list_of_product_links}
        for future in as_completed(futures):
            try:
                result = future.result()
                result['Keyword'] = keyword_name
                final_data.append(result)
            except Exception as e:
                print(f"Error fetching data for {futures[future]}: {e}")

    filepath = f"E:\\Nirav\\Project_code\\myntra\\myntra\\output_data\\{current_date}"
    os.makedirs(filepath, exist_ok=True)
    filepath = f"{filepath}\\{keyword_name}.json"

    cleaned_data = replace_ampersand(final_data)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=4, ensure_ascii=False, sort_keys=True)
