import json
import os
from datetime import datetime
import urllib.parse
import mysql.connector
import requests
import scrapy
from scrapy.cmdline import execute
from scrapy.http import HtmlResponse
import deliveroo.df_config as db


class LinksSpider(scrapy.Spider):
    name = "links"
    start_urls = ["https://example.com"]

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def parse(self, response):
        mydb = mysql.connector.connect(
            host=db.host,
            user=db.username,
            password=db.password,
            database=db.database_name
        )
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        mycursor = mydb.cursor()
        mycursor.execute(f"select * from {db.geohash_data} where status = 'pending' limit {self.a},{self.b};")
        # mycursor.execute(f"select * from geohash_data where id = '2301' limit {self.a},{self.b};")
        myresult = mycursor.fetchall()
        for d in myresult:
            geo_hash1 = d[2]
            # list = ["a", "b", "e", "c", "d", "e", "f", "g", "h", "i", 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z']
            list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", 'j']
            # list = ["a"]
            for al in list:
                u = urllib.parse.quote(f"https://deliveroo.hk/en/restaurants/hong-kong/{al}?fulfillment_method=DELIVERY&geohash={geo_hash1}&collection=all-restaurants")
                # url = f"http://api.scraperapi.com?api_key=de51e4aafe704395654a32ba0a14494d&url={u}" # Todo: using scraper api
                url = f"http://api.scrape.do?token=aa48e53ef4934d95a56acecacaec8fe454ebf634a98&url={u}&device=desktop"
                payload = {}
                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
                    'Cookie': '_fbp=fb.1.1730883540340.914872122351880258; locale=eyJsb2NhbGUiOiJlbiJ9; browse_data=eyJsb2NhdGlvbiI6eyJjb29yZGluYXRlcyI6WzExNC4xNDg2OTYyLDIyLjI4MDk0NzldLCJpZCI6bnVsbCwiZm9ybWF0dGVkX2FkZHJlc3MiOiI1MiBDb25kdWl0IFJkLCBNaWQtTGV2ZWxzLCBIb25nIEtvbmciLCJwbGFjZV9pZCI6IkNoSUpXWl9kbVhrQUJEUVJRN3MtU2FUSkJyRSIsInBpbl9yZWZpbmVkIjpmYWxzZSwiY2l0eSI6bnVsbH19; location_data=eyJsb2NhdGlvbiI6eyJjb29yZGluYXRlcyI6WzExNC4xNDg2OTYyLDIyLjI4MDk0NzldLCJpZCI6bnVsbCwiZm9ybWF0dGVkX2FkZHJlc3MiOiI1MiBDb25kdWl0IFJkLCBNaWQtTGV2ZWxzLCBIb25nIEtvbmciLCJwbGFjZV9pZCI6IkNoSUpXWl9kbVhrQUJEUVJRN3MtU2FUSkJyRSIsInBpbl9yZWZpbmVkIjpmYWxzZSwiY2l0eSI6bnVsbH19; roo_super_properties=eyJjb250ZXh0Ijp7InVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzAuMC4wLjAgU2FmYXJpLzUzNy4zNiIsImlwIjoiMTkzLjE3Ni4yMTEuNTEiLCJsb2NhdGlvbiI6eyJjb3VudHJ5IjoiSG9uZyBLb25nIn0sImxvY2FsZSI6ImVuIn0sIlJlcXVlc3RlZCBMb2NhbGUiOiJlbiIsIlJvb0Jyb3dzZXIiOiJDaHJvbWUiLCJSb29Ccm93c2VyVmVyc2lvbiI6IjEzMCIsIkRldmljZSBUeXBlIjoiZGVza3RvcCIsIlBsYXRmb3JtIjoid2ViIiwiVExEIjoiaGsiLCJMb2NhbGUiOiJlbiIsIndoaXRlX2xhYmVsX2JyYW5kIjoiY29yZSJ9; __cf_bm=1SkPHMOJCjqu6FiYQQeuerxLvEc8SOjGyB5wTm1Kg1I-1730883557-1.0.1.1-pSM9JsVzBP4uOkYpaaW94P1OwfNJfNnbF1joCoE0v4UM7Sk4Awy_8yWwIHyvWsdF4.4oRYfgP_gZpeHaEjScOBV7576e7srvSpCSPk00Nj8; roo_guid=60a920fa-e0db-4a7f-96dd-e67dcb27d141; roo_session_guid=820a1a41-a2ef-4cce-bba6-6e7dd70a837b; external_device_id=1aea7625-bf6c-4497-957f-15c6e163e071; _gcl_au=1.1.1256658927.1730883562; OptanonAlertBoxClosed=2024-11-06T08:59:22.027Z; _ga=GA1.1.243585388.1730883562; pxcts=6a2136ae-9c1d-11ef-81c4-ba02674e95f2; _pxvid=6a212c75-9c1d-11ef-81c4-277e869dfed9; roo_guid=60a920fa-e0db-4a7f-96dd-e67dcb27d141; dtm_token_sc=AQAG468AZ79H1QFyjH1iAQA6yQABAQCSAbItPAEBAJIBsi08; __pxvid=6a989a9f-9c1d-11ef-afee-0242ac120002; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+06+2024+14%3A29%3A25+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=dd291773-4cd7-41da-8bfb-acfb3ffe8a34&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=H95%3A1%2CH5%3A1%2CH111%3A1%2CH79%3A1%2CH80%3A1%2CH86%3A1%2CH85%3A1%2CH4%3A1%2CH155%3A1%2CH74%3A1%2CH38%3A1%2CH89%3A1%2CH99%3A1%2CH108%3A1%2CH167%3A1%2CH20%3A1%2CH77%3A1%2CH164%3A1%2CH156%3A1%2CH101%3A1%2CH104%3A1%2CH25%3A1%2CH162%3A1%2CH83%3A1%2CH39%3A1%2CH159%3A1&genVendors=&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false; _scid=AUU6v90arvCOiWse609ZW9Ta9jivKhOipjdmPQ; _scid_r=AUU6v90arvCOiWse609ZW9Ta9jivKhOipjdmPQ; dtm_token=AQAG468AZ79H1QFyjH1iAQA6yQABAQCSAbItPAEBAJIBsi08; _tt_enable_cookie=1; _ttp=nhD_UN2PBkGCU9ROFCbw5WoaNK8; _uetsid=6cd0a2a09c1d11ef8b7b578abe105c31; _uetvid=6cd0edb09c1d11ef956daf1d1fe84c32; _pin_unauth=dWlkPU5HUTNNalpqWXpRdE9UQmpaUzAwWmpWaExXRXlOall0TlRjeVpUSmtOakF3WkRjeQ; _ScCbts=%5B%5D; _clck=1i9k0m%7C2%7Cfqn%7C0%7C1771; cwa_user_preferences={%22deviceStats%22:{%22innerWidth%22:1422}%2C%22seen_modals%22:{%22nc_promos_nux_180d2673-0ae2-43e0-a991-92c998cd4bf2%22:{%22id%22:%22nc_promos_nux_180d2673-0ae2-43e0-a991-92c998cd4bf2%22%2C%22timestamp%22:1730883568}}}; _sctr=1%7C1730831400000; _ga_ZW8Q7SZ57X=GS1.1.1730883562.1.1.1730883578.44.0.0; _clsk=1x5ahca%7C1730883579167%7C5%7C0%7Cv.clarity.ms%2Fcollect',
                    'referer': 'https://deliveroo.hk/en/',
                    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                    'sec-ch-ua-full-version-list': '"Google Chrome";v="129.0.6668.60", "Not=A?Brand";v="8.0.0.0", "Chromium";v="129.0.6668.60"',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                if response.status_code == 429:  # Todo: if response is 429 then make requests 3 time
                    for lo in range(3):
                        response = requests.request("GET", url, headers=headers, data=payload)
                        if response.status_code == 200:
                            break

                # path = f"C:\\Actowiz\\pagesave\\Deliveroo\\Geohash_new\\{al}_keyword\\"
                path = db.geohash_path + f"{al}_keyword\\"
                if not os.path.exists(path):
                    os.makedirs(path)
                file_name = path + geo_hash1 + ".html"
                file_name = file_name.replace("\\", '\\\\')
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(url)
                # if response.status_code ==404:
                #     sql = f"update geohash_data set `status`='404'  where geo='{geo_hash1}';"
                #     mycursor.execute(sql)
                #     mydb.commit()
                # else:
                try:
                    response = HtmlResponse(body=response.text, url=url, encoding='utf-8')
                    data_json = response.xpath('//script[@type="application/json"]//text()').get()
                    json_data = json.loads(data_json)
                    item_loop_data = json_data['props']['initialState']['home']['feed']['results']['data']
                    # props.initialState.checkoutPayment.blocks
                    for items in item_loop_data:
                        items_more = items['blocks']
                        try:
                            for ii in items_more:
                                vendor_id = ii['target']['restaurant']['id']
                                lead_source = "Deliveroo"
                                name = ii['target']['restaurant']['name']
                                url_rest = "https://deliveroo.hk/en" + ii['target']['restaurant']['links']['self'][
                                    'href']

                                item = {}
                                item['vendor_id'] = vendor_id
                                item['name'] = name
                                item['geohash'] = geo_hash1
                                item['url'] = url_rest
                                item['pagesave'] = file_name
                                try:
                                    field_list = []
                                    value_list = []
                                    for field in item:
                                        field_list.append(str(field))
                                        value_list.append(str(item[field]).replace("'", "’"))
                                    fields = ','.join(field_list)
                                    values = "','".join(value_list)
                                    insert_db = f"insert into {db.restaurant_links} ( " + fields + " ) values ( '" + values + "' )"
                                    mycursor.execute(insert_db)
                                    mydb.commit()
                                    print(insert_db)
                                except Exception as e:
                                    print(str(e))
                            sql = f"update {db.geohash_data} set `status`='done'  where geo='{geo_hash1}';"
                            mycursor.execute(sql)
                            mydb.commit()

                        except:
                            sql = f"update {db.geohash_data} set `status`='no_data'  where geo='{geo_hash1}';"
                            mycursor.execute(sql)
                            mydb.commit()
                except:
                    print("no response")


if __name__ == '__main__':
    execute(f"scrapy crawl links -a a=0 -a b=2300".split())
