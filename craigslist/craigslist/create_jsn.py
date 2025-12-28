import datetime
import json
import html
import pandas as pd
import pymysql
from numpy.ma.core import masked_invalid
YYYYmmdd = datetime.date.today().strftime('%Y%m%d')
data_table = 'pdp_data_30052025'
def create_json():
    cur.execute(f"select * from {data_table} group by listing_id")
    rows = cur.fetchall()
    # df = pd.read_sql(f"select * from {data_table}", con)
    list_of_jsn = list()
    for row in rows:
        main_jsn = {}
        main_jsn['listing_id'] = row['product_id']
        main_jsn['source'] = 'craigslist'
        main_jsn['scrape_timestamp'] = row['scrape_timestamp']
        main_jsn['title'] = row['product_title']
        main_jsn['description'] = html.unescape(row['description'])
        main_jsn['category'] = row['category']
        main_jsn['price'] = row['price']
        main_jsn['currency'] = row['currency']
        main_jsn['condition'] = row['condition']
        if row['images']:
            image_list = row['images'].split('|')
            image_list2 = []
            img_count = 0
            for i in image_list:
                img_count += 1
                image_list2.append(
                    {'original_url': i, 'path': f'{YYYYmmdd}_craigslist_{main_jsn['category']}/assets/{main_jsn["listing_id"]}_{img_count}.jpg'})

        else:
            image_list2 = []

        main_jsn['assets'] = image_list2
        main_jsn['attributes'] = []
        attributes = row['attributes']
        if attributes:
            attributes_jsn = json.loads(attributes)
            for i, v in attributes_jsn.items():
                main_jsn['attributes'].append({'name':i, 'value':v})


        main_jsn['seller'] = None
        main_jsn['listing_url'] = row['product_url']
        main_jsn['category_url'] = row['listing_url']
        main_jsn['quantity_available'] = None
        main_jsn['location'] = row['address']
        main_jsn['created_date'] = row['created_date']
        main_jsn['updated_date'] = row['updated_date']
        list_of_jsn.append(main_jsn)

    for dict_ in list_of_jsn:
        f = open(f'{datetime.datetime.today().strftime("%Y%m%d")}_craigslist.jsonl', 'a')
        f.write(json.dumps(dict_)+'\n')

def json_to_excel():
    cur.execute(f"select * from {data_table}  group by listing_id")
    rows = cur.fetchall()
    list_of_jsn = list()
    for row in rows:
        main_jsn = {}
        main_jsn['listing_id'] = row['product_id']
        main_jsn['source'] = 'craigslist'
        main_jsn['scrape_timestamp'] = row['scrape_timestamp']
        main_jsn['title'] = row['product_title']
        main_jsn['description'] = html.unescape(row['description'])
        main_jsn['category'] = row['category']
        main_jsn['price'] = row['price']
        main_jsn['currency'] = row['currency']
        main_jsn['condition'] = row['condition']
        if row['images']:
            image_list = row['images'].split('|')
            image_list2 = []
            img_count = 0
            for i in image_list:
                img_count +=1
                image_list2.append({'original_url': i, 'path':f'{YYYYmmdd}_craigslist_{main_jsn['category']}/assets/{main_jsn["listing_id"]}_{img_count}.jpg'})

        else:image_list2 = []

        main_jsn['assets'] = image_list2
        main_jsn['attributes'] = []
        attributes = row['attributes']
        if attributes:
            attributes_jsn = json.loads(attributes)
            for i, v in attributes_jsn.items():
                main_jsn['attributes'].append({'name': i, 'value': v})
        main_jsn['seller'] = None
        main_jsn['listing_url'] = row['product_url']
        main_jsn['category_url'] = row['listing_url']
        main_jsn['quantity_available'] = None
        main_jsn['location'] = row['address']
        main_jsn['created_date'] = row['created_date']
        main_jsn['updated_date'] = row['updated_date']
        # main_jsn['sold_date'] = None
        # main_jsn['gtin'] = None
        # main_jsn['mpn'] = None
        # main_jsn['pricing'] = {
        #     'original_price': row['price'],
        #     'discount_amount': None,
        #     'discount_percentage': None,
        #     'discount_ends': None
        # }
        #
        #
        #
        # main_jsn['shipping'] = None
        # main_jsn['product'] = {
        #     'product_id': row['product_id'],
        #     'product_url': row['product_url'],
        #     'product_title': row['product_title']
        # }
        #
        # main_jsn['raw_data'] = None
        # main_jsn['seller'] = None


        list_of_jsn.append(main_jsn)

    df = pd.DataFrame(list_of_jsn)
    df.fillna('NA', inplace=True)
    writer = pd.ExcelWriter(
        f'{datetime.datetime.today().strftime("%Y%m%d")}_craigslist.xlsx',
        engine='xlsxwriter',
        engine_kwargs={'options': {'strings_to_urls': False}}
    )

    # writer.book.use_zip64()
    # df.replace("", "NA", inplace=True)
    # df.fillna("NA", inplace=True)
    df.to_excel(writer, index=False)
    writer.close()



if __name__ == '__main__':
    con = pymysql.connect(host='172.27.131.195', user='root', password='actowiz', database='craigslist')
    cur = con.cursor(pymysql.cursors.DictCursor)
    create_json()
    json_to_excel()