# from curl_cffi import requests
# from parsel import Selector
#
# variant_product_url_list = [
#     "https://www.amazon.in/LG-Inverter-Fully-Automatic-Washing-FHM1207SDM/dp/B0BMGD9Y2X",
#     "https://www.amazon.in/Whirlpool-6-5-Fully-Automatic-WHITEMAGIC-ROYAL/dp/B08QNZTQ96",
#     "https://www.amazon.in/Hisense-Fully-Automatic-Loading-Washing-WFVB7012MS/dp/B09DT1TM9Q",
#     "https://www.amazon.in/IFB-Washing-Machine-Silver-Protection/dp/B09R6ZL9RP"]
#
# for url in variant_product_url_list:
#     cookies = {
#         'session-id': '260-4198031-7496017',
#         'i18n-prefs': 'INR',
#         'ubid-acbin': '259-4958529-9696045',
#         'session-token': 'X+3M9V2Efgcurv8fOxsUSIll57kayxTx5sKhlD7V+bSxltjYbK76YnkDP77GBEJYy1VM/7iJ9WTM91JCr/sZyv5+hHSF+octkyv4ucfqguz6UdLRmAA9LdjetC74vk8ZXImrUQIqI9ITZ2q7CyEVuZr97DO34NUnOFjsTUj+/BKuvMuy1b2UIC44zpKyHa+wDJF9n9eYydviPxGRwdnlRyBDS+Ta4BnSS9XWehPtDSRLPGcYOuUDRrMig7+SBjvCSIl1qSOZTD34Z44883i9u0OiAPe7ZYoZOlN9kboX4iOdiprUaKVxrMSoqCYUpMHH1NnErg94lIpgrMOxKTLWvskgmaUsxl1O',
#         'session-id-time': '2082758401l',
#         'csm-hit': 'tb:AAN4D908E588JRW7A8F2+s-AAN4D908E588JRW7A8F2|1741765653985&t:1741765653985&adb:adblk_no',
#     }
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'accept-language': 'en-US,en;q=0.9',
#         'cache-control': 'no-cache',
#         'device-memory': '8',
#         'downlink': '10',
#         'dpr': '1.2000000000000002',
#         'ect': '4g',
#         'pragma': 'no-cache',
#         'priority': 'u=0, i',
#         'rtt': '50',
#         'sec-ch-device-memory': '8',
#         'sec-ch-dpr': '1.2000000000000002',
#         'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-ch-ua-platform-version': '"10.0.0"',
#         'sec-ch-viewport-width': '1600',
#         'sec-fetch-dest': 'document',
#         'sec-fetch-mode': 'navigate',
#         'sec-fetch-site': 'none',
#         'sec-fetch-user': '?1',
#         'upgrade-insecure-requests': '1',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
#         'viewport-width': '1600',
#         # 'cookie': 'session-id=260-4198031-7496017; i18n-prefs=INR; ubid-acbin=259-4958529-9696045; session-token=X+3M9V2Efgcurv8fOxsUSIll57kayxTx5sKhlD7V+bSxltjYbK76YnkDP77GBEJYy1VM/7iJ9WTM91JCr/sZyv5+hHSF+octkyv4ucfqguz6UdLRmAA9LdjetC74vk8ZXImrUQIqI9ITZ2q7CyEVuZr97DO34NUnOFjsTUj+/BKuvMuy1b2UIC44zpKyHa+wDJF9n9eYydviPxGRwdnlRyBDS+Ta4BnSS9XWehPtDSRLPGcYOuUDRrMig7+SBjvCSIl1qSOZTD34Z44883i9u0OiAPe7ZYoZOlN9kboX4iOdiprUaKVxrMSoqCYUpMHH1NnErg94lIpgrMOxKTLWvskgmaUsxl1O; session-id-time=2082758401l; csm-hit=tb:AAN4D908E588JRW7A8F2+s-AAN4D908E588JRW7A8F2|1741765653985&t:1741765653985&adb:adblk_no',
#     }
#     token = "2d76727898034978a3091185c24a5df27a030fdc3f8"
#     proxy_host = "proxy.scrape.do:8080"
#     proxyModeUrl = f"http://{token}@{proxy_host}?extraHeaders=true&render=true"
#     proxies = {
#         "http": proxyModeUrl,
#         "https": proxyModeUrl,
#     }
#     response = requests.get(
#         url,
#         cookies=cookies,
#         headers=headers, proxies=proxies, verify=False
#     )
#     page_save_id = url.split('/dp/')[-1]
#     main_path = fr'F:\Nirav\Project_code\amazon\amazon\pagesave\{page_save_id}.html'
#     with open(main_path, "w",encoding="utf-8") as f:
#         f.write(response.text)
#     print(f"page save for this {page_save_id}")
#     selector = Selector(text=response.text)
#
#     for data in selector.xpath("//div[contains(@data-totalvariationcount, '')]//div[@id='apex_price']/../../../.."):
#         name = data.xpath(".//span[contains(@class,'swatch-title-text-display')]/text()").getall()
#         print(name)

import asyncio
from pyppeteer import launch


async def fetch_data():
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Load page and wait for network to be idle
    await page.goto("https://www.amazon.in/LG-Inverter-Fully-Automatic-Washing-FHM1207SDM/dp/B0BMGD9Y2X", {"waitUntil": "networkidle2"})

    # Extract data using XPath
    elements = await page.xpath('//ul[@data-action="a-button-group"]//li//span[@class="a-offscreen"]')

    for element in elements:
        text = await page.evaluate('(el) => el.textContent', element)
        print(text)

    await browser.close()


asyncio.run(fetch_data())
