import requests

cookies = {
    '_bb_vid': 'Nzc0OTU2NjQ1MDYwMjQwNjIy',
    '_bb_lat_long': 'MjYuODM5MTgwNXw4MC45MDQxODE3',
    '_bb_pin_code': '226004',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'common-client-static-version': '101',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://www.bigbasket.com/pd/40135128/dabur-toothpaste-red-gel-combo-pack-150-g/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

json_data = {
    'prod_id': 274035,
    '_bb_client_type': 'web',
}

# response = requests.post('https://www.bigbasket.com/mapi/v3.5.2/c-decr-i/', cookies=cookies, headers=headers, json=json_data)


for i in range(30):
    new_cookies = {
        '_bb_vid': 'Nzc0OTU2NjQ1MDYwMjQwNjIy',
        '_bb_lat_long': 'MjYuODM5MTgwNXw4MC45MDQxODE3',
        '_bb_pin_code': '226004',
        # consider rotating _bb_vid if server tracks it
    }
    with requests.Session() as session:
        session.cookies.update(new_cookies)
        response = session.post('https://www.bigbasket.com/mapi/v3.5.2/c-incr-i/',
                                headers=headers,
                                json=json_data)
        data_json = response.json()

        if response.json()['status'] != 'OK':
            print(response.json()['allowed'])
            break

