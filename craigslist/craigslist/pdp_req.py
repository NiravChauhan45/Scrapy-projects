import hashlib
import os

import pymysql
import requests
import concurrent.futures



# cookies = {
#             'cl_b': '4|ab325c3d766e61fb0c51937143872d51dc8fe297|1745381879V6TyE',
#             'cl_def_hp': 'abilene',
#         }
#
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Connection': 'keep-alive',
#     'Referer': 'https://abilene.craigslist.org/',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     # 'Cookie': 'cl_b=4|ab325c3d766e61fb0c51937143872d51dc8fe297|1745381879V6TyE; cl_def_hp=abilene',
# }
# token = "2d76727898034978a3091185c24a5df27a030fdc3f8"
# proxyModeUrl = "http://{}&geoCode=us:@proxy.scrape.do:8080".format(token)
# proxies = {
#     "http": proxyModeUrl,
#     "https": proxyModeUrl,
# }
#
# url = 'https://albany.craigslist.org/ele/d/schenectady-ink/7844213755.html'
#
# response = requests.get(url, cookies=cookies,
#                                     headers=headers, proxies=proxies, verify=False)
#
# print()
def create_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8', errors='ignore'))
    return md5_hash.hexdigest()
def pdp_pagesave(row):
    url = row['pdp_url']
    cookies = {
        'cl_b': '4|ab325c3d766e61fb0c51937143872d51dc8fe297|1745381879V6TyE',
        'cl_def_hp': 'abilene',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://abilene.craigslist.org/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        # 'Cookie': 'cl_b=4|ab325c3d766e61fb0c51937143872d51dc8fe297|1745381879V6TyE; cl_def_hp=abilene',
    }
    token = "2d76727898034978a3091185c24a5df27a030fdc3f8"
    proxyModeUrl = "http://{}&geoCode=us:@proxy.scrape.do:8080".format(token)
    proxies = {
        "http": proxyModeUrl,
        "https": proxyModeUrl,
    }

    pagesave_path = r'D:\Smitesh\pagesave\craigslist\pdp'
    if not(os.path.exists(pagesave_path)):
        os.makedirs(pagesave_path)
    hashid = create_md5_hash(url)
    if not (os.path.exists(fr'{pagesave_path}/{hashid}.html')):

        response = requests.get(url, cookies=cookies,
                                headers=headers, proxies=proxies, verify=False)
        if response.status_code == 200:
            f = open(fr'{pagesave_path}/{hashid}.html', 'w', encoding='utf8')
            f.write(response.text)
            f.close()
        print(response.status_code, url)
        if response.status_code == 200:
            return row['hashid']
    else:
        return row['hashid']

def update_status(hashid):
        cur.execute(f"update {pdp_links_table} set status ='done' where hashid='{hashid}'")
        con.commit()


if __name__ == '__main__':
    con = pymysql.connect(host='localhost', user='root', password='actowiz', database='craigslist')
    cur = con.cursor(pymysql.cursors.DictCursor)

    pdp_links_table = 'pdp_links_30052025'

    # collect()
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        futures = []
        cur.execute(f"select * from {pdp_links_table} where status='pending'")
        rows = cur.fetchall()
        for row in rows:
            futures.append(executor.submit(pdp_pagesave, row=row))
        for future in concurrent.futures.as_completed(futures):
            item_list = future.result()
            cur.execute(f"update {pdp_links_table} set status ='done' where hashid='{item_list}'")
            con.commit()