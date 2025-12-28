import json
import re

import pymysql
import requests
from parsel import Selector
from urllib3 import request

# Use DictCursor to get dictionary results
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="amazon_s",
    cursorclass=pymysql.cursors.DictCursor  # ✅ This is the key change
)

cur = connection.cursor()

sql_query = "SELECT * FROM product_links WHERE status = 'pending'"
cur.execute(sql_query)
results = cur.fetchall()

# Print each row as a dict
for parent_index, result in enumerate(results, start=1):
    item_type = result['item_type']
    product_id = result['product_id']
    product_url = result['product_url']
    parent_pid = product_id

    cookies = {
        'session-id': '257-8197099-3389816',
        'i18n-prefs': 'INR',
        'lc-acbin': 'en_IN',
        'ubid-acbin': '261-8449377-2614061',
        'csm-hit': 'tb:7RNBWDMEA9NB7F7B2GHH+s-VFAM7R1JB3JFHKCRZAEF|1752314666477&t:1752314666477&adb:adblk_no',
        'session-id-time': '2082758401l',
        'session-token': 'SxModWPDCgNNau3pe28wBffk0hHyAWPlHw033+wfIMNx1LgOxuFwnOJCNUfynLkfxBuuybx11FGMYsTgE6qW+RwmzIMCSDSVXerq8rfGZiN3tfh5KjsaeQ/6FJ4IkSqXvB7rEaaJ32iJ0KJCxvJ2ZoYJXW3lJetI3WnJG2vVLIK38ZcEv/yLwBjiyY9Am9GW6car6jxxDbBNKfD0HZE5beX1qnennsGnl8arghJpbSHArs+2veivggqL/wthy0f3qrKk4H88Nkd/7G5tS4BvMMMUswOw343yWNBC3cdxJnia8nYnVhLWlaWjpCnt064E4NXCfB65GFpnkGrmvkboERSguRvCkz/I',
        'rxc': 'AKsPUdgEhyrXiy9gp7M',
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
        'rtt': '150',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'viewport-width': '1920',
    }
    response = requests.get(url=product_url, cookies=cookies, headers=headers)
    selector = Selector(text=response.text)

    other_data = {}

    variation_id = list()
    variation_id.append(parent_pid)

    all_asin = re.findall(r'dimensionToAsinMap\" :(.*?)\n', response.text)
    if all_asin:
        all_asin = re.findall(r'dimensionToAsinMap\" :(.*?)\n', response.text)[0]
        all_asin_json = json.loads(all_asin.strip(",").strip())
        for asin in all_asin_json:
            asin = all_asin_json[asin]
            if asin not in variation_id:
                variation_id.append(asin)
    else:
        variation_id = []

    sr_nos_1 = parent_index
    for child_index, variation in enumerate(variation_id, start=1):
        child_pid = variation
        sr_nos_2 = f"{parent_index}.{child_index}"
        unique_key = f"{parent_pid}_{child_pid}"
        sql = "INSERT IGNORE INTO variation_id_table (item_type, product_url, parent_pid, child_pid, sr_nos_1, sr_nos_2, unique_key) VALUES (%s, %s, %s,%s, %s,%s, %s)"
        cur.execute(sql, (item_type, product_url, parent_pid, child_pid, sr_nos_1, sr_nos_2, unique_key))
        connection.commit()
        print({"item_type": item_type, "parent_id": parent_pid, "child_id": child_pid, "product_url": product_url})
    sql = f"UPDATE product_links SET status='Done' WHERE product_id='{parent_pid}'"
    cur.execute(sql)
    connection.commit()
cur.close()
connection.close()
