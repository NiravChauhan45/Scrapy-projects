import requests

cookies = {
    '_ga': 'GA1.1.1013695182.1761275781',
    '_ga_DZ4MXZBLKH': 'GS2.1.s1761275781$o1$g1$t1761275781$j60$l0$h0',
    'EXP_prod': 'prod-a',
    'EXP_search_dn_widgets': 'search_dn_widgets-a',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
}

response = requests.get(
    'https://www.nykaafashion.com/%20/p/5157135',
    cookies=cookies,
    headers=headers,
)
print(response.text)
