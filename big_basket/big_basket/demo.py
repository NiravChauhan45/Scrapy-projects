import requests

cookies = {
    '_bb_pin_code': '110026',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': 'x-entry-context-id=100; x-entry-context=bb-b2c; _bb_locSrc=default; x-channel=web; _bb_bhid=; _bb_nhid=1723; _bb_vid=NjAxODYwNzE3NzczMTYxNzEw; _bb_dsevid=; _bb_dsid=; _bb_cid=1; _bb_aid=MzA4NTgxODk5Nw==; csrftoken=72c3iw7hIMyjNDicaFYRlzlfUX5yaqY3kio16EsIavpTFc4OJYhnRQjdlHYsjYAz; _bb_home_cache=25c6ea2a.1.visitor; _bb_bb2.0=1; is_global=1; _bb_addressinfo=; _bb_pin_code=; _bb_sa_ids=10654; _is_tobacco_enabled=0; _is_bb1.0_supported=0; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xMDY1NA==; is_integrated_sa=0; bb2_enabled=true; csurftoken=6K1dcg.NjAxODYwNzE3NzczMTYxNzEw.1739940895768.hprXzRh2drtoyZwg6JbRykIj891p47tTbYYhdhpXy2k=; bigbasket.com=2c1e1a3b-d098-40ab-bcac-cd102a6d1d3c; _gcl_au=1.1.1542882375.1739940768; jarvis-id=b76abe01-2491-455b-bd04-53c1d89c0c9e; _gid=GA1.2.52505219.1739940768; _fbp=fb.1.1739940767924.809745978442071696; adb=0; ufi=1; ts=2025-02-19%2010:25:22.545; _ga=GA1.2.271261501.1739940768; _ga_FRRYG5VKHX=GS1.1.1739940767.1.1.1739940862.60.0.0',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    # 'referer': 'https://www.bigbasket.com/ps/?q=namkeen&nc=as&page=3',
    # 'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'x-channel': 'BB-WEB',
    'x-tracker': 'a7d5a183-47f5-4d9e-afc5-cf609efc37bb',
}

params = {
    'type': 'pc',
    'slug': 'tea',
    'page': '1',
}

response = requests.request('GET','https://www.bigbasket.com/listing-svc/v2/products', params=params, cookies=cookies, headers=headers)


print(response.status_code)