import hashlib
import json
from datetime import datetime
from typing import Any

import mysql.connector
import scrapy
from scrapy.cmdline import execute
from scrapy.http import Response
import deliveroo.df_config as db


class MenuDetailsDeliverySpider(scrapy.Spider):
    name = "menu_details_delivery"
    start_urls = ["https://example.com"]

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.mydb = mysql.connector.connect(
            host=db.host,
            user=db.username,
            password=db.password,
            database=db.database_name
        )
        self.mycursor = self.mydb.cursor()

    def start_requests(self):
        current_date = datetime.now()
        pagesave_date = current_date.strftime("%Y-%m-%d")
        formatted_date = current_date.strftime("%Y_%m_%d")

        self.mycursor.execute(f"select * from {db.deliveroo_restaurant} where status = 'pending' limit {self.a},{self.b}")
        # self.mycursor.execute(f"select * from deliveroo_restaurant_{formatted_date} where vendor_id = '351088' ")
        myresult = self.mycursor.fetchall()
        for d in myresult:
            vendor_id = d[1]
            # path=f"C:\\Actowiz\\pagesave\\Deliveroo\\{pagesave_date}\\Data\\{vendor_id}.html"
            path = db.pagesave_data_path + f"{vendor_id}.html"
            yield scrapy.Request(url=f"file:///{path}".replace("\\", "/"), callback=self.parse,
                                 meta={'vendor_id': vendor_id})

    def parse(self, response):
        now = datetime.now()
        formatted_date = now.strftime('%Y_%m_%d')
        lead_source = "Deliveroo"
        vendor_id = response.meta['vendor_id']
        try:
            data_json = response.xpath('//script[@type="application/json"]//text()').get()
            json_data = json.loads(data_json)
            categorys = json_data['props']['initialState']['menuPage']['menu']['meta']['categories']
            cat_json = {}
            for c in categorys:
                cat_id = c['id']
                cat_name = c['name']
                cat_json[cat_id] = cat_name
            menu_details = json_data['props']['initialState']['menuPage']['menu']['meta']['items']
            if menu_details != []:
                for m in menu_details:
                    menu_id = m['id']
                    # print(menu_id)
                    cat_id_response_item = m['categoryId']
                    try:
                        menu_Category = cat_json[cat_id_response_item]
                    except:
                        menu_Category = ""

                    menu_items = m['name']
                    try:
                        image_url = m['image']['url']
                    except:
                        image_url = ""
                    original_price_Delivery = m['price']['formatted'].replace("$", "").replace(",", "")
                    try:
                        discounted_price_Delivery = m['priceDiscounted']['formatted'].replace("$", "").replace(",", "")
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
                    if "For Two" in menu_items:
                        is_MFO = "False"
                    date_of_scrape = now.strftime('%Y-%m-%d')
                    date_of_data_inserted = now.strftime('%Y-%m-%d')
                    if menu_Category != "":
                        item = dict()
                        item['vendor_id'] = vendor_id
                        item['menu_id'] = menu_id
                        item['menu_Category'] = menu_Category
                        item['menu_items'] = menu_items
                        item['image_url'] = image_url
                        item['original_price_Delivery'] = original_price_Delivery
                        item['discounted_price_Delivery'] = discounted_price_Delivery
                        item['discount_price_Delivery'] = discount_price_Delivery
                        item['discount_MOV_Delivery'] = discount_MOV_Delivery
                        # item['is_MFO']=is_MFO
                        item['date_of_scrape'] = date_of_scrape
                        item['date_of_data_inserted'] = date_of_data_inserted
                        hash_str = str(vendor_id) + str(menu_Category) + str(menu_items) + str(
                            menu_id) + str(image_url)
                        item['hashid'] = int(hashlib.md5(bytes(f"{hash_str}", "utf8")).hexdigest(), 16) % (10 ** 10)
                        try:
                            field_list = []
                            value_list = []
                            for field in item:
                                field_list.append(str(field))
                                value_list.append(str(item[field]).replace("'", "’"))
                            fields = ','.join(field_list)
                            values = "','".join(value_list)
                            insert_db = f"insert into {db.data_menu_delivery} ( " + fields + " ) values ( '" + values + "' )"
                            self.mycursor.execute(insert_db)
                            self.mydb.commit()
                            # print(insert_db)
                        except Exception as e:
                            print(str(e))
                sql = f"update {db.deliveroo_restaurant} set `status`='Done'  where vendor_id={vendor_id};"
                self.mycursor.execute(sql)
                self.mydb.commit()
            else:
                sql = f"update {db.deliveroo_restaurant} set `status`='No_Menu'  where vendor_id={vendor_id};"
                self.mycursor.execute(sql)
                self.mydb.commit()
        except Exception as e:
            print(e)
            sql = f"update {db.deliveroo_restaurant} set `status`='Issue'  where vendor_id={vendor_id};"
            self.mycursor.execute(sql)
            self.mydb.commit()


if __name__ == '__main__':
    execute("scrapy crawl menu_details_delivery -a a=0 -a b=15000".split())
