# # import requests
# #
# # cookies = {
# #     'bigbasket.com': '902c92da-fac1-4e90-8949-f215b5488e69',
# #     '_bb_locSrc': 'default',
# #     'x-channel': 'web',
# #     '_bb_vid': 'Nzc1OTA1MjY4MjEwMTk3OTk4',
# #     '_bb_nhid': '7427',
# #     '_bb_dsid': '7427',
# #     '_bb_dsevid': '7427',
# #     '_bb_bhid': '',
# #     '_bb_loid': '',
# #     'csrftoken': 'eQBOuwKPa8XAMZxiaSa6FyzEnIuMHB6eSUdxznxfBkexORSBgx96tyMilIj95WBm',
# #     'isintegratedsa': 'true',
# #     'jentrycontextid': '10',
# #     'xentrycontextid': '10',
# #     'xentrycontext': 'bbnow',
# #     '_bb_bb2.0': '1',
# #     '_is_bb1.0_supported': '0',
# #     'is_integrated_sa': '1',
# #     'bb2_enabled': 'true',
# #     'csurftoken': 'b_9wpw.Nzc1OTA1MjY4MjEwMTk3OTk4.1750314759844.eMF9BGTGS20l2uML5pbgk3rlET8NbIqSrB0mlBTPIJI=',
# #     'ufi': '1',
# #     '_gcl_au': '1.1.364527014.1750314761',
# #     'jarvis-id': '752df0e4-bb6f-42bc-bd44-a69fd4679915',
# #     '_gid': 'GA1.2.682520415.1750314762',
# #     '_gat_UA-27455376-1': '1',
# #     'adb': '0',
# #     '_fbp': 'fb.1.1750314762671.865880692666383177',
# #     '_bb_lat_long': 'MjguNjU1Njc5M3w3Ny4xODc0NjAx',
# #     '_bb_cid': '18',
# #     '_bb_aid': '"MzAxNzU0OTAyMw=="',
# #     'is_global': '0',
# #     '_bb_addressinfo': 'MjguNjU1Njc5M3w3Ny4xODc0NjAxfEJsb2NrIDE4QnwxMTAwMDV8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==',
# #     '_bb_pin_code': '110005',
# #     '_bb_sa_ids': '17507',
# #     '_is_tobacco_enabled': '1',
# #     '_bb_cda_sa_info': 'djIuY2RhX3NhLjEwLjE3NTA3',
# #     '_ga_FRRYG5VKHX': 'GS2.1.s1750314762$o1$g1$t1750314807$j15$l0$h0',
# #     '_ga': 'GA1.2.521104999.1750314762',
# #     'ts': '2025-06-19%2012:03:28.012',
# # }
# #
# # headers = {
# #     'accept': '*/*',
# #     'accept-language': 'en-US,en;q=0.9',
# #     'common-client-static-version': '101',
# #     'content-type': 'application/json',
# #     'origin': 'https://www.bigbasket.com',
# #     'priority': 'u=1, i',
# #     'referer': 'https://www.bigbasket.com/pd/40125873/maggi-2-minute-noodles-masala-840-g/',
# #     'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
# #     'sec-ch-ua-mobile': '?0',
# #     'sec-ch-ua-platform': '"Windows"',
# #     'sec-fetch-dest': 'empty',
# #     'sec-fetch-mode': 'cors',
# #     'sec-fetch-site': 'same-origin',
# #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
# #     'x-channel': 'BB-WEB',
# #     'x-csurftoken': 'b_9wpw.Nzc1OTA1MjY4MjEwMTk3OTk4.1750314759844.eMF9BGTGS20l2uML5pbgk3rlET8NbIqSrB0mlBTPIJI=',
# #     'x-entry-context': 'bbnow',
# #     'x-entry-context-id': '10',
# #     'x-tracker': 'ea62e1d2-7c80-44bf-9f7a-73e07c06af73',
# #     # 'cookie': 'bigbasket.com=902c92da-fac1-4e90-8949-f215b5488e69; _bb_locSrc=default; x-channel=web; _bb_vid=Nzc1OTA1MjY4MjEwMTk3OTk4; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=eQBOuwKPa8XAMZxiaSa6FyzEnIuMHB6eSUdxznxfBkexORSBgx96tyMilIj95WBm; isintegratedsa=true; jentrycontextid=10; xentrycontextid=10; xentrycontext=bbnow; _bb_bb2.0=1; _is_bb1.0_supported=0; is_integrated_sa=1; bb2_enabled=true; csurftoken=b_9wpw.Nzc1OTA1MjY4MjEwMTk3OTk4.1750314759844.eMF9BGTGS20l2uML5pbgk3rlET8NbIqSrB0mlBTPIJI=; ufi=1; _gcl_au=1.1.364527014.1750314761; jarvis-id=752df0e4-bb6f-42bc-bd44-a69fd4679915; _gid=GA1.2.682520415.1750314762; _gat_UA-27455376-1=1; adb=0; _fbp=fb.1.1750314762671.865880692666383177; _bb_lat_long=MjguNjU1Njc5M3w3Ny4xODc0NjAx; _bb_cid=18; _bb_aid="MzAxNzU0OTAyMw=="; is_global=0; _bb_addressinfo=MjguNjU1Njc5M3w3Ny4xODc0NjAxfEJsb2NrIDE4QnwxMTAwMDV8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=110005; _bb_sa_ids=17507; _is_tobacco_enabled=1; _bb_cda_sa_info=djIuY2RhX3NhLjEwLjE3NTA3; _ga_FRRYG5VKHX=GS2.1.s1750314762$o1$g1$t1750314807$j15$l0$h0; _ga=GA1.2.521104999.1750314762; ts=2025-06-19%2012:03:28.012',
# # }
# #
# # json_data = {
# #     'prod_id': 40125873,
# #     'qty': 1,
# #     '_bb_client_type': 'web',
# #     'first_atb': 1,
# # }
# #
# # # response = requests.post('https://www.bigbasket.com/mapi/v3.5.2/c-incr-i/', cookies=cookies, headers=headers, json=json_data)
# #
# #
# # for i in range(30):
# #     with requests.Session() as session:
# #         session.cookies.update(cookies)
# #         response = session.post('https://www.bigbasket.com/mapi/v3.5.2/c-incr-i/',
# #                                 headers=headers,
# #                                 json=json_data)
# #         data_json = response.json()
# #
# #         if response.json()['status'] != 'OK':
# #             print(response.json()['allowed'])
# #             break
# #
#
# from curl_cffi import requests
#
# import requests
# from parsel import Selector
#
# cookies = {
#     '_bb_locSrc': 'default',
#     'x-channel': 'web',
#     '_bb_vid': 'Nzc1OTM1NTM4ODA5NjY5MTAy',
#     '_bb_nhid': '7427',
#     '_bb_dsid': '7427',
#     '_bb_dsevid': '7427',
#     '_bb_bhid': '',
#     '_bb_loid': '',
#     'csrftoken': 'rM8oOQEarfLYZj5UQAqkvfbrVjlLpwAgmvzIGhC3bym79NHzgi7e57P0QEdXYDlj',
#     '_bb_bb2.0': '1',
#     '_is_tobacco_enabled': '0',
#     '_is_bb1.0_supported': '0',
#     'bb2_enabled': 'true',
#     'ufi': '1',
#     'jarvis-id': '6199ce4d-215e-46c5-b792-18d58d9c6eeb',
#     '_gcl_au': '1.1.2102135277.1750316564',
#     '_gid': 'GA1.2.2108815024.1750316565',
#     'adb': '0',
#     '_fbp': 'fb.1.1750316565036.311000028265183553',
#     'bigbasket.com': 'e3886c44-f726-4956-970c-3f266c29231c',
#     'xentrycontext': 'bb-b2c',
#     'xentrycontextid': '100',
#     'jentrycontextid': '100',
#     '_bb_lat_long': 'MjguNjMyNzQyNnw3Ny4yMTk1OTY5',
#     '_bb_cid': '18',
#     '_bb_aid': '"Mjk4MDU5Mjk0Ng=="',
#     'isintegratedsa': 'false',
#     'is_global': '0',
#     '_bb_addressinfo': 'MjguNjMyNzQyNnw3Ny4yMTk1OTY5fE0uQ3wxMTAwMDF8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==',
#     '_bb_pin_code': '110001',
#     '_bb_sa_ids': '15108',
#     '_bb_cda_sa_info': 'djIuY2RhX3NhLjEwMC4xNTEwOA==',
#     'is_integrated_sa': '0',
#     'ts': '2025-06-19%2012:51:45.308',
#     '_ga': 'GA1.1.664876844.1750315228',
#     '_ga_FRRYG5VKHX': 'GS2.1.s1750315228$o1$g1$t1750317706$j58$l0$h0',
#     'csurftoken': 'FWkjTg.Nzc1OTM1NTM4ODA5NjY5MTAy.1750317779579.HvPOhZeaYzODe1FF7kt35EM27UwEVldiY7vZIjRh/eo=',
# }
#
# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'max-age=0',
#     'priority': 'u=0, i',
#     'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
#     # 'cookie': '_bb_locSrc=default; x-channel=web; _bb_vid=Nzc1OTM1NTM4ODA5NjY5MTAy; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=rM8oOQEarfLYZj5UQAqkvfbrVjlLpwAgmvzIGhC3bym79NHzgi7e57P0QEdXYDlj; _bb_bb2.0=1; _is_tobacco_enabled=0; _is_bb1.0_supported=0; bb2_enabled=true; ufi=1; jarvis-id=6199ce4d-215e-46c5-b792-18d58d9c6eeb; _gcl_au=1.1.2102135277.1750316564; _gid=GA1.2.2108815024.1750316565; adb=0; _fbp=fb.1.1750316565036.311000028265183553; bigbasket.com=e3886c44-f726-4956-970c-3f266c29231c; xentrycontext=bb-b2c; xentrycontextid=100; jentrycontextid=100; _bb_lat_long=MjguNjMyNzQyNnw3Ny4yMTk1OTY5; _bb_cid=18; _bb_aid="Mjk4MDU5Mjk0Ng=="; isintegratedsa=false; is_global=0; _bb_addressinfo=MjguNjMyNzQyNnw3Ny4yMTk1OTY5fE0uQ3wxMTAwMDF8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=110001; _bb_sa_ids=15108; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xNTEwOA==; is_integrated_sa=0; ts=2025-06-19%2012:51:45.308; _ga=GA1.1.664876844.1750315228; _ga_FRRYG5VKHX=GS2.1.s1750315228$o1$g1$t1750317706$j58$l0$h0; csurftoken=FWkjTg.Nzc1OTM1NTM4ODA5NjY5MTAy.1750317779579.HvPOhZeaYzODe1FF7kt35EM27UwEVldiY7vZIjRh/eo=',
# }
#
# response = requests.get(
#     'https://www.bigbasket.com/pd/30003294/id-fresho-malabar-parotaparatha-350-g-pouch/',
#     cookies=cookies,
#     headers=headers,
# )
#
# se = Selector(response.text)
#
# json_data = se.xpath("//script[@id='__NEXT_DATA__']/text()").get()
#
# print(json_data)


import requests
cookies = {
    '_bb_locSrc': 'default',
    'x-channel': 'web',
    '_bb_vid': 'Nzc3NTg4MjQ1NzE0NjA5MTM0',
    '_bb_nhid': '7427',
    '_bb_dsid': '7427',
    '_bb_dsevid': '7427',
    '_bb_bhid': '',
    '_bb_loid': '',
    'csrftoken': 'XguOWfwVkMoWfihTL1CuSapBmKihi6BRTGKeXwgntGTMirrDCTgxJcr6OuvkBwKq',
    '_bb_bb2.0': '1',
    '_is_tobacco_enabled': '0',
    '_is_bb1.0_supported': '0',
    'bb2_enabled': 'true',
    'csurftoken': 'UiNjWg.Nzc3NTg4MjQ1NzE0NjA5MTM0.1750415072519.ILXSZJFVdr+xNw2SlC7Z7Kv4YvVEovEsLMDZaLw73os=',
    'ufi': '1',
    '_gcl_au': '1.1.702203103.1750415074',
    'jarvis-id': 'ecea4f13-a801-46c0-a9db-4a46f34c0eb3',
    'adb': '0',
    '_gid': 'GA1.2.1837000771.1750415074',
    '_fbp': 'fb.1.1750415074332.487811911939344287',
    'bigbasket.com': '67813f03-0694-4f89-bc92-c2cd5d8e3e2a',
    'xentrycontext': 'bb-b2c',
    'xentrycontextid': '100',
    'jentrycontextid': '100',
    '_bb_lat_long': 'MjguNjMyNzQyNnw3Ny4yMTk1OTY5',
    '_bb_cid': '18',
    '_bb_aid': '"Mjk4MDU5Mjk0Ng=="',
    'isintegratedsa': 'false',
    'is_global': '0',
    '_bb_addressinfo': 'MjguNjMyNzQyNnw3Ny4yMTk1OTY5fE0uQ3wxMTAwMDF8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==',
    '_bb_pin_code': '110001',
    '_bb_sa_ids': '15108',
    '_bb_cda_sa_info': 'djIuY2RhX3NhLjEwMC4xNTEwOA==',
    'is_integrated_sa': '0',
    '_ga_FRRYG5VKHX': 'GS2.1.s1750415074$o1$g1$t1750415113$j21$l0$h0',
    '_ga': 'GA1.2.761639096.1750415074',
    'ts': '2025-06-20%2015:55:14.301',
}
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'common-client-static-version': '101',
    'content-type': 'application/json',
    'origin': 'https://www.bigbasket.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bigbasket.com/pd/40224575/nissin-nissin-geki-hot-spicy-korean-veg-flavour-80-g/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-channel': 'BB-WEB',
    'x-csurftoken': 'UiNjWg.Nzc3NTg4MjQ1NzE0NjA5MTM0.1750415072519.ILXSZJFVdr+xNw2SlC7Z7Kv4YvVEovEsLMDZaLw73os=',
    'x-entry-context': 'bb-b2c',
    'x-entry-context-id': '100',
    'x-tracker': '69db056e-b471-4d5e-9a25-f4069902b80e',
    # 'cookie': '_bb_locSrc=default; x-channel=web; _bb_vid=Nzc3NTg4MjQ1NzE0NjA5MTM0; _bb_nhid=7427; _bb_dsid=7427; _bb_dsevid=7427; _bb_bhid=; _bb_loid=; csrftoken=XguOWfwVkMoWfihTL1CuSapBmKihi6BRTGKeXwgntGTMirrDCTgxJcr6OuvkBwKq; _bb_bb2.0=1; _is_tobacco_enabled=0; _is_bb1.0_supported=0; bb2_enabled=true; csurftoken=UiNjWg.Nzc3NTg4MjQ1NzE0NjA5MTM0.1750415072519.ILXSZJFVdr+xNw2SlC7Z7Kv4YvVEovEsLMDZaLw73os=; ufi=1; _gcl_au=1.1.702203103.1750415074; jarvis-id=ecea4f13-a801-46c0-a9db-4a46f34c0eb3; adb=0; _gid=GA1.2.1837000771.1750415074; _fbp=fb.1.1750415074332.487811911939344287; bigbasket.com=67813f03-0694-4f89-bc92-c2cd5d8e3e2a; xentrycontext=bb-b2c; xentrycontextid=100; jentrycontextid=100; _bb_lat_long=MjguNjMyNzQyNnw3Ny4yMTk1OTY5; _bb_cid=18; _bb_aid="Mjk4MDU5Mjk0Ng=="; isintegratedsa=false; is_global=0; _bb_addressinfo=MjguNjMyNzQyNnw3Ny4yMTk1OTY5fE0uQ3wxMTAwMDF8TmV3IERlbGhpfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg==; _bb_pin_code=110001; _bb_sa_ids=15108; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xNTEwOA==; is_integrated_sa=0; _ga_FRRYG5VKHX=GS2.1.s1750415074$o1$g1$t1750415113$j21$l0$h0; _ga=GA1.2.761639096.1750415074; ts=2025-06-20%2015:55:14.301',
}
json_data = {
    'prod_id': 40224575,
    '_bb_client_type': 'web',

}

response = requests.post('https://www.bigbasket.com/mapi/v3.5.2/c-incr-i/', cookies=cookies,headers=headers, json=json_data)
print(response.text)
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"prod_id":40224575,"qty":1,"_bb_client_type":"web","first_atb":1}'
#response = requests.post('https://www.bigbasket.com/mapi/v3.5.2/c-incr-i/', headers=headers, data=data)