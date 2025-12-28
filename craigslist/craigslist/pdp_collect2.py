import hashlib
import json
import os

from parsel import Selector
import pymysql


# from ruamel.yaml.comments import line_col_attrib


def create_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8', errors='ignore'))
    return md5_hash.hexdigest()


def insert_data(table, item):
    field_list = []
    value_list = []
    for field in item:
        field_list.append(str(field))
        value_list.append('%s')
    fields = ','.join(field_list)
    values = ", ".join(value_list)
    insert_db = f"insert ignore into {table}( " + fields + " ) values ( " + values + " )"
    try:
        cur.execute(insert_db, tuple(item.values()))
        con.commit()
        print('Inserted')
    except Exception as e:
        if 'duplicate' not in str(e).lower():
            print(e)
        else:
            print(e)


def read_pl_old():
    # cur.execute("select * from cat_country_links where status='pending'")
    # cur.execute("select * from cat_country_links where status='done'")
    # cur.execute("SELECT * FROM `cat_country_links` WHERE link LIKE '%newyork%';")
    # rows = cur.fetchall()
    rows = [{'link': ""}]
    for row in rows:
        url = row['link']
        # cat = row['cat']

        # hashid = create_md5_hash(url)
        file_name = url.replace("://", '_').replace('.', '_').replace('/', '_')
        file_name = "newyork"
        f = open(fr'D:\Smitesh\pagesave\craigslist\pl\{hashid}.html', 'r', encoding='utf8')
        data = f.read()
        selector = Selector(data)
        main_div = selector.xpath("//*[@class='cl-static-search-result']")
        for i in main_div:
            name = i.xpath(".//*[@class='title']/text()").get()
            price = i.xpath(".//*[@class='price']/text()").get()
            location = i.xpath(".//*[@class='location']/text()").get()
            if location:
                location = location.strip()
            pdp_url = i.xpath(".//a/@href").get()
            hashid = create_md5_hash(f'{pdp_url}')
            item = {}
            item['name'] = name
            item['price'] = price
            item['location'] = location
            item['pdp_url'] = pdp_url
            item['hashid'] = hashid
            item['category'] = ''
            item['listing_url'] = url

            item['city'] = pdp_url.split('.')[0].replace('https://', '')
            insert_data('pdp_links', item)
        # cur.execute(f"update cat_country_links set status='done' where link='{url}'")
        # con.commit()

        # jsn_raw = selector.xpath("//script[contains(@id,'ld_searchpage_results')]//text()").get()
        # jsn = json.loads(jsn_raw.strip())
        # for element in jsn['itemListElement']:
        #     name = element['item']['name']
        #     description = element['item']['description']
        #     image_list = element['item']['image'][0]
        #     price = element['item']['offers']['price']
        #     currency = element['item']['offers']['priceCurrency']
        #     address_locality = element['item']['offers']['availableAtOrFrom']['address']['addressLocality']
        #     postalcode = element['item']['offers']['availableAtOrFrom']['address']['postalCode']
        #     streetaddress = element['item']['offers']['availableAtOrFrom']['address']['streetAddress']
        #     addressregion = element['item']['offers']['availableAtOrFrom']['address']['addressRegion']
        #     addresscountry = element['item']['offers']['availableAtOrFrom']['address']['addressCountry']
        #     lat = element['item']['offers']['availableAtOrFrom']['geo']['latitude']
        #     lng = element['item']['offers']['availableAtOrFrom']['geo']['longitude']
        #
        #     item = {}
        #
        #     item['name'] = name
        #     item['description'] = description
        #     item['image'] = image_list
        #     item['price'] = price
        #     item['currency'] = currency
        #     item['address_locality'] = address_locality
        #     item['postal_code'] = postal_code
        #     item['street_address'] = street_address
        #     item['address_region'] = address_region
        #     item['address_country'] = address_country
        #     item['lat'] = lat
        #     item['lng'] = lng
        #     item['category'] = category
        #     # hashid = create_md5_hash(f'{}')


def read_pl():
    while True:
        cur.execute("select * from newyork_links_30052025 where status='done'")

        # cur.execute("select * from cat_country_links where status='done'")
        # cur.execute("select * from cat_country_links where link='https://fargo.craigslist.org/search/vga'")
        # cur.execute("SELECT * FROM `cat_country_links` WHERE link LIKE '%newyork%';")
        rows = cur.fetchall()
        if rows:
            # rows = [{'link':'https://newyork.craigslist.org/search/sss?excats=7-13-22-2-24-1-4-19-1-1-1-1-1-1-3-6-10-1-1-1-2-2-8-1-1-1-1-1-4-1-3-1-3-1-1-1-1-7-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-1&isTrusted=true#search=2~gallery~0'}]
            for row in rows:
                url = row['link']
                # cat = row['cat']

                # hashid = create_md5_hash(url)
                file_name = url.replace("://", '_').replace('.', '_').replace('/', '_')
                # file_name = 'newyork'
                for i in range(1000):
                    # file_path = fr'D:\Smitesh\pagesave\craigslist\pl\{file_name}\page_{i}.html'
                    file_path = fr'E:\Nirav\Project_page_save\craigslist\pl\{file_name}\page_{i}.html'
                    if os.path.exists(file_path):
                        f = open(file_path, 'r', encoding='utf8')
                        data = f.read()
                        selector = Selector(data)
                        # main_div = selector.xpath("//*[@class='cl-static-search-result']")
                        # main_div = selector.xpath("//*[contains(@class,'cl-search-result')]")
                        main_div = selector.xpath("//@data-pid/..")
                        for i in main_div:
                            name = i.xpath("./@title").get()
                            # price = i.xpath(".//*[@class='price']/text()").get()
                            # location = i.xpath(".//*[@class='location']/text()").get()
                            # if location:
                            #     location = location.strip()
                            pdp_url = i.xpath(".//a/@href").get()
                            hashid = create_md5_hash(f'{pdp_url}{url}')
                            item = {}
                            item['name'] = name
                            # item['price'] = price
                            # item['location'] = location
                            item['pdp_url'] = pdp_url
                            item['hashid'] = hashid
                            item['category'] = ''
                            item['listing_url'] = url

                            item['city'] = pdp_url.split('.')[0].replace('https://', '')
                            insert_data('pdp_links_30052025', item)
                    else:
                        break
                cur.execute(f"update newyork_links_30052025 set status='done2' where link='{url}'")
                con.commit()
        else:
            break

        # jsn_raw = selector.xpath("//script[contains(@id,'ld_searchpage_results')]//text()").get()
        # jsn = json.loads(jsn_raw.strip())
        # for element in jsn['itemListElement']:
        #     name = element['item']['name']
        #     description = element['item']['description']
        #     image_list = element['item']['image'][0]
        #     price = element['item']['offers']['price']
        #     currency = element['item']['offers']['priceCurrency']
        #     address_locality = element['item']['offers']['availableAtOrFrom']['address']['addressLocality']
        #     postalcode = element['item']['offers']['availableAtOrFrom']['address']['postalCode']
        #     streetaddress = element['item']['offers']['availableAtOrFrom']['address']['streetAddress']
        #     addressregion = element['item']['offers']['availableAtOrFrom']['address']['addressRegion']
        #     addresscountry = element['item']['offers']['availableAtOrFrom']['address']['addressCountry']
        #     lat = element['item']['offers']['availableAtOrFrom']['geo']['latitude']
        #     lng = element['item']['offers']['availableAtOrFrom']['geo']['longitude']
        #
        #     item = {}
        #
        #     item['name'] = name
        #     item['description'] = description
        #     item['image'] = image_list
        #     item['price'] = price
        #     item['currency'] = currency
        #     item['address_locality'] = address_locality
        #     item['postal_code'] = postal_code
        #     item['street_address'] = street_address
        #     item['address_region'] = address_region
        #     item['address_country'] = address_country
        #     item['lat'] = lat
        #     item['lng'] = lng
        #     item['category'] = category
        #     # hashid = create_md5_hash(f'{}')


if __name__ == '__main__':
    con = pymysql.connect(host='localhost', user='root', password='actowiz', database='craigslist')
    cur = con.cursor(pymysql.cursors.DictCursor)
    read_pl()
