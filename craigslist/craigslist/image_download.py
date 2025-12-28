# import os
# import sys
#
# import pymysql
# import requests
# from dropbox.files import download
# import concurrent.futures
# from create_jsn import YYYYmmdd
# from fake_useragent import UserAgent
#
#
#
# ua = UserAgent()
#
#
#
#
# def craigslist_img(img_dict):
#     img = img_dict['img']
#     download_img_path = img_dict['download_img_path']
#     src = img
#     dir_raw = download_img_path.split('/')
#     dir = '/'.join(dir_raw[:-1])
#     if not(os.path.exists(fr'D:\Smitesh\pagesave\craigslist\images\{dir}')):
#         os.makedirs(fr'D:\Smitesh\pagesave\craigslist\images\{dir}')
#     token = "3b51c7dae74a4f8cbb7d5d45930eea8797ac5cf6bde"
#     proxyModeUrl = "http://{}:customHeaders=true@proxy.scrape.do:8080".format(token)
#     proxies = {
#         "http": proxyModeUrl,
#         "https": proxyModeUrl,
#     }
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         # 'accept-language': 'en-US,en;q=0.9,gu;q=0.8',
#         # 'cache-control': 'no-cache',
#         # 'pragma': 'no-cache',
#         # 'priority': 'u=0, i',
#         # 'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
#         # 'sec-ch-ua-mobile': '?0',
#         # 'sec-ch-ua-platform': '"Windows"',
#         # 'sec-fetch-dest': 'document',
#         # 'sec-fetch-mode': 'navigate',
#         # 'sec-fetch-site': 'same-origin',
#         # 'sec-fetch-user': '?1',
#         # 'upgrade-insecure-requests': '1',
#         'user-agent': ua.random,
#     }
#
#     if not(os.path.exists(fr'D:\Smitesh\pagesave\craigslist\images\{download_img_path}')):
#
#         try:
#             response = requests.get(src, proxies=proxies, verify=False)
#             # response = requests.get(src,headers=headers, verify=False)
#             if response.status_code == 200:
#                 response.raise_for_status()
#                 # os.makedirs(os.path.dirname(asset_file), exist_ok=True)
#                 with open(fr'D:\Smitesh\pagesave\craigslist\images\{download_img_path}', 'wb') as f:
#                     f.write(response.content)
#                 print(f'Done: {download_img_path}')
#             else:print(response.status_code)
#         except Exception as e:
#             print(f"Download failed: {src} -> {e}")
#
#
# if __name__ == '__main__':
#     # try:
#     #     start = sys.argv[1]
#     #     end = sys.argv[2]
#     # except:
#     #     start = 0
#     #     end = 1
#
#     with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
#         futures = []
#         YYYYmmdd = '03062025'
#         con = pymysql.connect(host='172.27.131.195', user='root', password='actowiz', database='craigslist')
#         cur = con.cursor(pymysql.cursors.DictCursor)
#         cur.execute(f"select * from pdp_data_30052025 where status='pending' group by listing_id")
#         # cur.execute("select * from pdp_data_30052025 where listing_id='7853165202'")
#         rows = cur.fetchall()
#         for row in rows:
#             images = row['images']
#             if images:
#                 img_list = images.split('|')
#                 c = 1
#                 for img in img_list:
#                     download_img_url = img
#                     download_img_path = f'{YYYYmmdd}_craigslist_{row['category']}/assets/{row['listing_id']}_{c}.jpg'
#                     c+=1
#                     img_dict = {}
#                     img_dict['img'] = download_img_url
#                     img_dict['download_img_path'] = download_img_path
#                     # craigslist_img(download_img_url, download_img_path)
#                     futures.append(executor.submit(craigslist_img, img_dict))
#
#             # cur.execute(f"update pdp_data_30052025_img set status='done' where listing_id='{row['listing_id']}'")
#             # con.commit()
#             # print('listing_id:', row['listing_id'], 'done')
#
#
#     # YYYYmmdd = '03062025'
#     # con = pymysql.connect(autocommit=True,host='172.27.131.195', user='root', password='actowiz', database='craigslist')
#     # cur = con.cursor(pymysql.cursors.DictCursor)
#     # cur.execute(f"select * from pdp_data_30052025_img where status='pending' group by listing_id limit {start},{end}")
#     # # cur.execute("select * from pdp_data_30052025 where listing_id='7853165202'")
#     # rows = cur.fetchall()
#     # for row in rows:
#     #     images = row['images']
#     #     if images:
#     #         img_list = images.split('|')
#     #         c = 1
#     #         for img in img_list:
#     #             download_img_url = img
#     #             download_img_path = f'{YYYYmmdd}_craigslist_{row['category']}/assets/{row['listing_id']}_{c}.jpg'
#     #             c+=1
#     #             img_dict = {}
#     #             img_dict['img'] = download_img_url
#     #             img_dict['download_img_path'] = download_img_path
#     #             # craigslist_img(download_img_url, download_img_path)
#     #             craigslist_img(img_dict)
#     #
#     #     cur.execute(f"update pdp_data_30052025_img set status='done' where listing_id='{row['listing_id']}'")
#     #     # con.commit()
#     #     print('listing_id:', row['listing_id'], 'done')
#
#
#
#
#
#
#
