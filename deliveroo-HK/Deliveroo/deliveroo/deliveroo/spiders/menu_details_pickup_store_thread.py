import hashlib
import json
import os
from datetime import datetime
from threading import Thread
import deliveroo.df_config as db
import mysql.connector
import requests
from scrapy.http import HtmlResponse


def thread_delivery(a, v):
    now = datetime.now()
    current_date = datetime.now()

    formatted_date_pagesave = current_date.strftime("%Y-%m-%d")
    formatted_date = current_date.strftime("%Y_%m_%d")
    formatted_date = "2025_01_21"
    formatted_date_pagesave = "2025-01-21"
    mydb = mysql.connector.connect(
        host=db.host,
        user=db.username,
        password=db.password,
        database=db.database_name
    )
    mycursor = mydb.cursor()
    mycursor.execute(
        f"select * from {db.deliveroo_restaurant} where status = 'store_delivery_Done'  limit {a},{v}") # deliveroo_restaurant_{formatted_date}
    myresult = mycursor.fetchall()
    for d in myresult:
        url = d[9]
        vendor_id = d[1]
        lead_source = "Deliveroo"
        category = d[8].decode("utf8")
        cat = category.split("|=|")[1]
        cat_id_list = cat.split(",")
        for c in cat_id_list:
            print(c)
            cat_url = url + "&fulfillment_method=collection&category_id=" + c

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
                'cache-control': 'max-age=0',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"130.0.6723.92"',
                'sec-ch-ua-full-version-list': '"Chromium";v="130.0.6723.92", "Google Chrome";v="130.0.6723.92", "Not?A_Brand";v="99.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            }
            response = requests.request("GET", cat_url, headers=headers)
            if response.status_code != 200:
                for loopi in range(5):
                    response = requests.request("GET", cat_url, headers=headers)
                    if response.status_code == 200:
                        break

            response = HtmlResponse(url="", body=response.text, encoding="utf8")
            data = response.xpath('//script[@id="__NEXT_DATA__"]//text()').get()
            json_data = json.loads(data)
            try:
                menu_category = json_data['props']['initialState']['menuPage']['menu']['meta']['categories'][0][
                    'name'].replace("\n", "").replace("\t", "")
            except:
                print("respo  error")

                menu_category = ""
            if menu_category != "":
                # path = f"C:\\Actowiz\\pagesave\\Deliveroo\\{formatted_date_pagesave}\\Menu_Store_Pickup\\"
                path = db.menu_store_pickup_path
                if not os.path.exists(path):
                    os.makedirs(path)
                file_name = path + vendor_id + "_" + c + ".html"
                file_name = file_name.replace("\\", '\\\\')
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                items = json_data['props']['initialState']['menuPage']['menu']['meta']['items']
                for i in items:
                    menu_id = i['id']
                    menu_items = i['name']
                    try:
                        image_url = i['image']['url']
                    except:
                        image_url = ""
                    original_price_Delivery = i['price']['formatted'].replace("$", "").replace(",", "")
                    try:
                        discounted_price_Delivery = i['priceDiscounted']['formatted'].replace("$", "").replace(",", "")
                    except:
                        discounted_price_Delivery = original_price_Delivery
                    if discounted_price_Delivery == "0.00" or discounted_price_Delivery == "Free":
                        discounted_price_Delivery = original_price_Delivery
                    if original_price_Delivery != discounted_price_Delivery:
                        try:
                            discount_price_Delivery = ((float(original_price_Delivery) - float(
                                discounted_price_Delivery)) / float(original_price_Delivery)) * 100
                            discount_price_Delivery = round(discount_price_Delivery, 2)
                        except:
                            discount_price_Delivery = ""
                            print("")
                    else:
                        discount_price_Delivery = "0"
                    discount_MOV_Delivery = "0"
                    is_MFO = "True"
                    date_of_scrape = now.strftime('%Y-%m-%d')
                    date_of_data_inserted = now.strftime('%Y-%m-%d')
                    if menu_category != "":
                        item = dict()
                        item['vendor_id'] = vendor_id
                        item['menu_id'] = menu_id
                        item['menu_Category'] = menu_category
                        item['menu_items'] = menu_items
                        item['image_url'] = image_url
                        item['original_price_pickup'] = original_price_Delivery
                        item['discounted_price_pickup'] = discounted_price_Delivery
                        item['discount_price_pickup'] = discount_price_Delivery
                        item['discount_MOV_pickup'] = discount_MOV_Delivery
                        # item['is_MFO']=is_MFO
                        item['date_of_scrape'] = date_of_scrape
                        item['date_of_data_inserted'] = date_of_data_inserted
                        hash_str = str(vendor_id) + str(menu_category) + str(menu_id)
                        item['hashid'] = int(hashlib.md5(bytes(f"{hash_str}", "utf8")).hexdigest(), 16) % (10 ** 10)
                        try:
                            field_list = []
                            value_list = []
                            for field in item:
                                field_list.append(str(field))
                                value_list.append(str(item[field]).replace("'", "’"))
                            fields = ','.join(field_list)
                            values = "','".join(value_list)
                            insert_db = f"insert into {db.data_menu_pickup} ( " + fields + " ) values ( '" + values + "' )"#data_menu_pickup_{formatted_date}
                            mycursor.execute(insert_db)
                            mydb.commit()
                            print(insert_db)
                        except Exception as e:
                            print(str(e))
        sql = f"update {db.deliveroo_restaurant} set `status`='store_pickup_Done'  where vendor_id={vendor_id};"#deliveroo_restaurant_{formatted_date}
        mycursor.execute(sql)
        mydb.commit()


if __name__ == '__main__':
    data_c = 6
    run_count = 0
    while data_c != 0 and run_count < 100:
        total_count = data_c
        variable_count = total_count // 2
        if variable_count == 0:
            variable_count = total_count ** 2
        count = 1
        threads = [Thread(target=thread_delivery, args=(i, variable_count + i)) for i in
                   range(0, total_count, variable_count)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        run_count += 1



# SET GLOBAL max_connections=99999
# PURGE BINARY LOGS BEFORE NOW()
