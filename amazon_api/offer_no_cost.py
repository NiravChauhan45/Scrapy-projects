import re
from itertools import product

import requests
from parsel import Selector



def get_cashback(product_id):
    cookies = {
        'session-id': '525-1433283-0746461',
        'i18n-prefs': 'INR',
        'lc-acbin': 'en_IN',
        'ubid-acbin': '262-6324041-1804233',
        'session-id-time': '2082787201l',
        'session-token': 'hIZofOg+Sw9i18mPbq+aGxOD7wGGHC9h8KSoVbR+IVnqiNGeakUrHpNLLAOeFMMYCSLHREXxDengEoQhF+MJZMmxlpSDorW7Dqh5QMsforjnMrCkll7X7XDeMWSgh80agrG2lG+je229jNxPQYASeCA/GeFp0MqO4M22NamK3XJE//99nfp1CjDZ+zJ9nva07uPabVeC2TFDfBiNmA4PcpUZvLTlx5tuKWgBecLXhMs8iZ2CGdo88UBWyVFfgwlNVUxnFS/nxYj23V/52gmhEe8uiDPUNxQ8340TMgR2bg27AUIDPz9orj7XHmh410jw/w3xYkoRpv0QqQjcvlBjdUym31uJHFXR',
        'csm-hit': 'tb:VDH0J4A68W9XHG165Q0X+s-7HSWS1T9R5QR5V5285VX|1756561441269&t:1756561441269&adb:adblk_no',
        'rxc': 'AOVIvZ7CH0yhrUfx4tw',
    }

    headers = {
        'accept': 'text/html,*/*',
        'accept-language': 'en-US,en;q=0.9',
        'device-memory': '8',
        'downlink': '1.35',
        'dpr': '0.75',
        'ect': '3g',
        'priority': 'u=1, i',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'viewport-width': '2560',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'session-id=525-1433283-0746461; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=262-6324041-1804233; session-id-time=2082787201l; session-token=hIZofOg+Sw9i18mPbq+aGxOD7wGGHC9h8KSoVbR+IVnqiNGeakUrHpNLLAOeFMMYCSLHREXxDengEoQhF+MJZMmxlpSDorW7Dqh5QMsforjnMrCkll7X7XDeMWSgh80agrG2lG+je229jNxPQYASeCA/GeFp0MqO4M22NamK3XJE//99nfp1CjDZ+zJ9nva07uPabVeC2TFDfBiNmA4PcpUZvLTlx5tuKWgBecLXhMs8iZ2CGdo88UBWyVFfgwlNVUxnFS/nxYj23V/52gmhEe8uiDPUNxQ8340TMgR2bg27AUIDPz9orj7XHmh410jw/w3xYkoRpv0QqQjcvlBjdUym31uJHFXR; csm-hit=tb:VDH0J4A68W9XHG165Q0X+s-7HSWS1T9R5QR5V5285VX|1756561441269&t:1756561441269&adb:adblk_no; rxc=AOVIvZ7CH0yhrUfx4tw',
    }

    response = requests.get(
        f'https://www.amazon.in/gp/product/ajax/a2iSMXSecondaryView?deviceType=web&requestId=7HSWS1T9R5QR5V5285VX&asin={product_id}&isVariationalMember=1&isVariationalParent=0&productTypeName=DRINK_FLAVORED&productGroupID=grocery_display_on_website&variationalParentASIN=B0B63MTV6Q&isB2BCustomer=false&buyingOptionIndex=0&encryptedMerchantId=A3HBGZ226XBAP1&showFeatures=sopp,inemi,promotions,vendorPoweredCoupon,sns&language=en_IN&isPrime=false&featureParams=viewName:cashbackSecondaryView',
        cookies=cookies,
        headers=headers,
    )
    selector = Selector(text=response.text)
    cashback = selector.xpath("//div[@class='a-row a-spacing-medium']/text()").get()
    cashback = re.sub("\\s+", " ", cashback).strip()
    item = {"cashback": cashback}
    return item


if __name__ == '__main__':
    product_id = "B00TTX2700"
    cashback = get_cashback(product_id)
    print(cashback)