import json
import os
import re
import time
from logger import logger
from DrissionPage import Chromium, ChromiumOptions
import hashlib
import sys
import pymysql as sql
import zipfile
import pymysql
from concurrent.futures import ThreadPoolExecutor
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from big_basket_screenshot.config.database_config import ConfigDatabase
from scrapy import Selector

import db_config as db

co = ChromiumOptions()
co.set_argument('--no-sandbox')
co.no_imgs(True)
co.no_js(True)

co.add_extension(
    r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Default\Extensions\eifflpmocdbdmepbjaopkkhbfmdgijcc')
# co.set.set_cookies(None)
current_date = datetime.datetime.now().strftime("%d_%m_%Y")

SERVICE_ACCOUNT_FILE = r'D:\Nirav Chauhan\code\big_basket_screenshot\big_basket_screenshot\nirav-458910-cab1bea12b92.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = '1QqoFxUnJ8IVtMpfghdvQ3GWqYBGVd1TX'  # Screenshot destination folder


connSql = pymysql.connect(
    host="localhost",
    user="root",
    passwd="actowiz",
    database=db.database_name, autocommit=True
)

# Todo: Pending all done links
try:
    mycursor = connSql.cursor()
    sql = f"SELECT COUNT(*) FROM {db.pdp_link_table} WHERE STATUS='Pending' HAVING COUNT(id)>0;"
    mycursor.execute(sql)
    count_of_data = mycursor.fetchall()
    if len(count_of_data)==0:
        try:
            mycursor = connSql.cursor()
            sql = f"UPDATE {db.pdp_link_table} SET status = 'Pending'"
            mycursor.execute(sql)
            connSql.commit()
        except Exception as e:
            logger.error(e)
    connSql.commit()
except Exception as e:
    logger.error(e)




# ======================= Create Date Folder on Drive =======================
def create_date_folder():
    today_drive = datetime.datetime.now().strftime('%Y_%m_%d')  # for drive folder name (e.g. 2025_04_16)
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': today_drive,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [PARENT_FOLDER_ID]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')

    permission = {'type': 'anyone', 'role': 'reader'}
    service.permissions().create(fileId=folder_id, body=permission).execute()

    return today_drive, folder_id


# ======================= Check if File Exists in Drive =======================
def file_exists_in_drive(filename, drive_folder_id, creds_path):
    creds = service_account.Credentials.from_service_account_file(creds_path,
                                                                  scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)

    query = f"'{drive_folder_id}' in parents and name = '{filename}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return len(files) > 0


# ======================= Upload Single Screenshot (Thread Safe) =======================
def upload_single_image_thread_safe(filename, folder_id, screenshot_path, creds_path):
    try:
        # New service object for thread safety
        creds = service_account.Credentials.from_service_account_file(creds_path,
                                                                      scopes=['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=creds)

        # Check if file exists
        if file_exists_in_drive(filename, folder_id, creds_path):
            return filename, None, "Already exists"

        file_path = os.path.join(screenshot_path, filename)
        file_metadata = {'name': filename, 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='image/jpeg')
        uploaded = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploaded.get('id')
        file_link = f"https://drive.google.com/file/d/{file_id}/view"
        return file_link

    except Exception as e:
        return filename, None, str(e)


def insert_data(*args):
    new_id = args[0]
    new_category = args[2]
    name_of_the_brand = args[1]
    name_of_the_product = args[3]
    single_pack = args[5]
    bundle_pack = args[6]
    quantity_of_the_product = args[4]
    product_url = args[9]
    quantity = args[7]
    packaging_of_the_product = args[8]
    new_zipcode = args[12]
    city_name = args[11]
    quantity_caping = args[13]
    big_basket_approve_not_approve = args[10]
    pack_shot_name =args[15]
    response = Selector(text=args[14])

    today_drive, folder_id = create_date_folder()
    base_path = db.screenshot_filepath
    screenshot_path = os.path.join(base_path)
    if os.path.exists(screenshot_path):
        updated_packshot_link = upload_single_image_thread_safe(pack_shot_name, folder_id, screenshot_path, SERVICE_ACCOUNT_FILE)
    else:
        logger.error("Screenshot path not created")


    per_gm = ''
    mrp = ''
    stock_avaibility = ''
    selling_price = ''
    discount = ''
    save_rs = ''
    # count = 0
    pack_shot_name = ''
    on_site_sku_name = ''
    if not product_url:
        try:
            pack_shot_name = f"{new_id}_{new_zipcode}_{db.current_date}"
            pack_shot_name = f"{pack_shot_name}.png"
        except:
            pack_shot_name = 'N/A'
    else:
        try:
            pid = product_url.split('/pd/')[-1].split('/')[0].strip()
            if pid:
                if '?' in pid:
                    pid = pid.split('?')[0].strip()
            else:
                pid = 'N/A'
        except Exception as error:
            logger.error(error)

        try:
            if pid != 'N/A':
                pack_shot_name = f"{pid}_{new_zipcode}_{db.current_date}.png"
                os.makedirs(db.screenshot_filepath, exist_ok=True)
            else:
                pack_shot_name = 'N/A'
        except Exception as error:
            logger.error(error)

        try:
            mrp = "".join(
                response.xpath('//td[contains(text(),"MRP:")]/following-sibling::td/text()').getall())
            if mrp:
                mrp = "".join(mrp).replace('₹', '').strip()
            else:
                mrp = "N/A"
        except:
            mrp = "N/A"

            # Todo: price
        try:
            price = "".join(
                response.xpath(
                    "//td[@class='Description___StyledTd-sc-82a36a-4 fLZywG']//text()").getall()).strip()
            price = price.replace('₹', '').strip()
        except:
            price = "N/A"

            # Todo: selling_price
        try:
            if price:
                selling_price = price.split(':')[-1].strip()
            else:
                selling_price = mrp
        except:
            selling_price = mrp

        # Todo: assign selling_price if mrp is not an available
        if selling_price != "N/A" and mrp == "N/A":
            mrp = selling_price

            # Todo: discount and save_rs

        try:
            discount_text = response.xpath(
                "//td[contains(text(),'You Save:')]/following-sibling::td[contains(text(),'OFF')]/text()").get()
            if discount_text:
                if "%" in discount_text:
                    digits = re.findall(r'\d+', discount_text)
                    discount = "".join(digits)
            else:
                discount = 'N/A'
        except:
            discount = "N/A"

            # Todo: save_rs
        try:
            if not save_rs:
                # save_rs = int(float(mrp) - float(selling_price))
                save_rs = round(float(mrp) - float(selling_price))
                if int(save_rs) == 0:
                    save_rs = '0'
        except:
            save_rs = "N/A"

            # Todo: add_to_cart
        try:
            if response.xpath('(//button[contains(text(),"Add to basket")])[1]'):
                add_to_cart = "In Stock"
            else:
                add_to_cart = "Out of Stock"
        except:
            add_to_cart = 'Not listed'

        # Todo: Update quantity_caping value if add_to_cart "Out of stock" or "Not listed"
        if add_to_cart == "Out of Stock" or add_to_cart == "Not listed":
            quantity_caping = "N/A"

            # Todo: per_gm
        try:
            per_gm = "".join(
                response.xpath('//td[contains(text(),"Price")]/following-sibling::td/text()').getall())
            per_gm = per_gm.replace('(', '').replace(')', '').replace('₹', '').replace(' / ', '/')
        except:
            per_gm = "N/A"

        try:
            on_site_sku_name = response.xpath(
                '//h1[@class="Description___StyledH-sc-82a36a-2 bofYPK"]/text()').get('').strip()
        except:
            on_site_sku_name = 'N/A'

    hash_id = str(int(hashlib.md5(bytes(str(str(
        new_id) + city_name + product_url + name_of_the_brand + new_category + new_zipcode + name_of_the_product + quantity_of_the_product),
                                        "utf8")).hexdigest(), 16) % (10 ** 10))
    item = dict()
    item["Sr.No"] = new_id
    item["Portal Name"] = "BigBasket"
    item["Product Url"] = product_url if product_url else 'N/A'
    item["Date (Crawler Date)"] = datetime.datetime.now().strftime("%d-%m-%Y")
    item["Time (Crawler Time)"] = datetime.datetime.now().strftime("%H:%M")
    item["City Name"] = city_name
    item["Pincode"] = new_zipcode
    item["Brand"] = name_of_the_brand if name_of_the_brand else 'N/A'
    item["Category"] = new_category if new_category else 'N/A'
    item["SKU Packshot"] = updated_packshot_link
    item["SKU Name"] = name_of_the_product if name_of_the_product else 'N/A'
    item["Pack Size"] = quantity_of_the_product if quantity_of_the_product else 'N/A'
    item["Single Pack"] = single_pack if single_pack else 'N/A'
    item["Bundle Pack"] = bundle_pack if bundle_pack else 'N/A'
    item["Per Gm Price (Unit Price)"] = per_gm if per_gm else 'N/A'
    item["MRP"] = mrp if mrp else 'N/A'
    item["Selling price"] = selling_price if selling_price else 'N/A'
    item["Discount (%)"] = discount if discount else 'N/A'
    item["Save Rs."] = save_rs if save_rs else "N/A"
    item["On-site SKU Name"] = on_site_sku_name
    item["Availability Status"] = add_to_cart if product_url else 'Not listed'
    item["Quantity Caping"] = quantity_caping if quantity_caping else 'N/A'
    item["Remarks"] = "N/A"
    item["Quantity"] = quantity if quantity else 'N/A'
    item["Packaging of the product"] = packaging_of_the_product if packaging_of_the_product else 'N/A'
    item["big_basket_approve_not_approve"] = big_basket_approve_not_approve
    item["hash_id"] = hash_id

    try:
        pdp_data_table = ConfigDatabase(table=db.pdp_data_table, database=db.database_name)
    except Exception as e:
        logger.error(e)


    # Todo: Pending all links
    connSql = pymysql.connect(
        host="localhost",
        user="root",
        passwd="actowiz",
        database=db.database_name, autocommit=True
    )

    # try:
    #     mycursor = connSql.cursor()
    #     sql = f"SELECT COUNT(*) FROM pdp_link_table_11_06_2025 WHERE STATUS='Pending' HAVING COUNT(id)=0;"
    #     mycursor.execute(sql)
    #     conn.commit()
    # except Exception as e:
    #     logger.error(e)

    # Todo: Create table if not exists
    try:
        create_table = f"""
            CREATE TABLE IF NOT EXISTS `{db.pdp_data_table}` (
                  `Sr.No` int NOT NULL AUTO_INCREMENT,
                  `Portal Name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
                  `Product Url` longtext,
                  `Date (Crawler Date)` varchar(100) DEFAULT NULL,
                  `Time (Crawler Time)` varchar(100) DEFAULT NULL,
                  `City Name` varchar(255) DEFAULT NULL,
                  `Pincode` varchar(100) DEFAULT NULL,
                  `Brand` varchar(150) DEFAULT NULL,
                  `Category` varchar(200) DEFAULT NULL,
                  `SKU Packshot` varchar(200) DEFAULT NULL,
                  `SKU Name` varchar(200) DEFAULT NULL,
                  `On-site SKU Name` varchar(255) DEFAULT NULL,
                  `Pack Size` varchar(200) DEFAULT NULL,
                  `Single Pack` varchar(200) DEFAULT NULL,
                  `Bundle Pack` varchar(200) DEFAULT NULL,
                  `Per Gm Price (Unit Price)` varchar(20) DEFAULT NULL,
                  `MRP` varchar(10) DEFAULT NULL,
                  `Selling price` varchar(10) DEFAULT NULL,
                  `Discount (%)` varchar(10) DEFAULT NULL,
                  `Save Rs.` varchar(10) DEFAULT NULL,
                  `Availability Status` varchar(30) DEFAULT NULL,
                  `Quantity Caping` varchar(10) DEFAULT NULL,
                  `Remarks` varchar(10) DEFAULT NULL,
                  `Quantity` varchar(10) DEFAULT NULL,
                  `Packaging of the product` varchar(40) DEFAULT NULL,
                  `big_basket_approve_not_approve` varchar(255) DEFAULT NULL,
                  `hash_id` varchar(50) DEFAULT NULL,
                  PRIMARY KEY (`Sr.No`),
                  UNIQUE KEY `hash_id` (`hash_id`)
                ) ENGINE=InnoDB AUTO_INCREMENT=801 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
        """
        pdp_data_table.crsrSql.execute(create_table)
    except Exception as error:
        logger.error(error)

    # Todo: Create table if not exists
    try:
        # mycursor = connSql.cursor()
        # sql = f"UPDATE {db.pdp_link_table} SET status = 'Finaly_Done' WHERE id = {item['Sr.No']}"
        # mycursor.execute(sql)
        # conn.commit()

        try:
            pdp_data_table.insertItemToSql(item)
        except Exception as e:
            logger.error(e)

        try:
            mycursor = connSql.cursor()
            sql = f"UPDATE {db.pdp_link_table} SET status = 'Finaly_Done' WHERE id = {item['Sr.No']}"
            mycursor.execute(sql)
            conn.commit()
        except Exception as e:
            logger.error(e)
    except Exception as e:
        print(e)


def page_save(conn, count, page_id, html):
    os.makedirs(db.pagesave_filepath, exist_ok=True)
    file_name = fr'{db.pagesave_filepath}\{page_id}.html'
    # Save the HTML content to a file
    with open(file_name, 'wb') as file:
        file.write(html.encode())
    print(f"Saved page to: {file_name}")

    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='actowiz',
            database=db.database_name
        )

        cur = conn.cursor()
        cur.execute(f"UPDATE {db.pdp_link_table} SET status = 'Done' WHERE id = %s", (page_id,))
        conn.commit()

        if count == '':
            count = 'N/A'

        try:
            sql = f"""UPDATE {db.pdp_link_table} SET quantity_caping = '{count}' WHERE id = {page_id}"""
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)

        cur.close()
        conn.close()

        logger.info(f"Updated status for page id: {page_id}")
    except Exception as e:
        logger.error(f"Error updating database: {e}")


def fetch_page(tab, urls, conn):
    print()
    i = 1
    pincode_set = True
    while pincode_set:
        try:
            while True:
                tab.get('https://www.bigbasket.com/')
                res = Selector(text=tab.html)
                page_not_found = res.xpath("//title/text()").get()
                if "Access Denied" in page_not_found:
                    tab.refresh()
                else:
                    break
            time.sleep(0.5)
            res = Selector(text=tab.html)
            match_zipcode = res.xpath(
                "//button[@class='AddressDropdown___StyledMenuButton2-sc-i4k67t-3 ZpLbn']/span/text()|//button[@class='AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW']/span/text()").get()

            if match_zipcode:
                if sys.argv[5] in match_zipcode:
                    print('Pincode successfully set')
                    break
                else:
                    pass

            location_button = tab.ele(
                'xpath:(//button[contains(@class,"AddressDropdown")]//span[contains(text(),"Select Location")])[2]|(//button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"])[2]')
            if location_button:
                location_button.click()
            else:
                location_button = tab.ele(
                    'xpath://button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"]')
                location_button.click()
                if not location_button:
                    print("Location button not found.")
                    return False
        except Exception as e:
            logger.error(f"Error clicking location button: {e}")
            return False

        try:
            from_input = tab.ele(
                "xpath:(//input[@class='Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn'])[2] | (//input[@placeholder='Search for area or street name'])[2]")
            if from_input:
                from_input.click()
                from_input.input(sys.argv[5])
                time.sleep(2)
                tab.actions.key_down('DOWN').key_down('ENTER')
            else:
                if not from_input:
                    from_input = tab.ele(
                        "xpath://input[contains(@placeholder,'Search for area or street name')]")
                    if from_input:
                        from_input.click()
                        from_input.input(sys.argv[5])
                        time.sleep(2)
                        tab.actions.key_down('DOWN').key_down('ENTER')
                    else:
                        print("Pincode input field not found.")
                        return False

            update_button = tab.ele(
                f"xpath:(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 cTJSLV'])[{i}]|(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX'])[{i}]|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 ggMOKv']|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN']")
            if update_button:
                update_button.click()
                response = Selector(text=tab.html)
                service_not_available = response.xpath(
                    "//span[contains(text(),'The selected city is not serviceable at the moment')]")
                if service_not_available:
                    tab.refresh()
                i += 1
            else:
                print("Update button not found.")
                return False
        except Exception as e:
            logger.error(f"Error entering pincode or clicking update: {e}")
            return False

    time.sleep(1)
    for page_id, brand, category, pdp_name, quantity_of_the_product, single_pack, bundle_pack, quantity, packaging_of_the_product, pdp_url, big_basket_approve_not_approve, City_Name, zipcode in urls:
        if pdp_url:
            try:
                tab.get(pdp_url)
            except Exception as e:
                logger.error('Somethig wrong in chrome tab', e)
            pid = ''
            if pdp_url:
                try:
                    pid = pdp_url.split('/pd/')[-1]
                    if '/' in pid:
                        pid = pid.split('/')[0]
                except:
                    pid = 'N/A'

            time.sleep(2)

            orginal_html = tab.html

            os.makedirs(db.screenshot_filepath, exist_ok=True)
            tab.get_screenshot(path=db.screenshot_filepath, name=f"{pid}_{pincode}_{db.current_date}.png",
                               full_page=True)  # full_page=True
            pack_shot_name = f"{pid}_{pincode}_{db.current_date}.png"
            print("Screenshot successfully taken.")

            # Todo: count
            try:
                add_to_basket = tab.ele('xpath:(//button[contains(text(),"Add to basket")])[1]')
                add_to_basket.click()
                count = 0
                while True:
                    element = tab.ele(
                        'xpath:(//button[contains(@class,"PdCartCTA___StyledButton2-sc-mq73zq-3")])[1]')
                    if element:
                        html = tab.html
                        response = Selector(text=html)
                        original_count = response.xpath(
                            "//div[@class='PdCartCTA___StyledDiv2-sc-mq73zq-2 cdHBKF']/text()").get(
                            '').strip()
                        count += 1
                        if original_count:
                            if count == int(original_count):
                                element.click()
                            else:
                                count = count - 1
                                break
                        else:
                            break
                        time.sleep(1)
                    else:
                        print("Element not found, exiting loop.")
                        break  # Exit loop if element is not available
            except:
                try:
                    count = response.xpath("//div[@class='PdCartCTA___StyledDiv2-sc-mq73zq-2 cdHBKF']/text()").get()
                    if not count:
                        count = 0
                except Exception as e:
                    print(e)

            # os.makedirs(db.screenshot_filepath, exist_ok=True)
            # tab.get_screenshot(path=db.screenshot_filepath, name=f"{pid}_{pincode}_{db.current_date}.png",
            #                    full_page=True)  # full_page=True
            # pack_shot_name = f"{pid}_{pincode}_{db.current_date}.png"
            # print("Screenshot successfully taken.")
            page_save(conn, count, page_id, orginal_html)
            insert_data(page_id, brand, category, pdp_name, quantity_of_the_product, single_pack, bundle_pack, quantity,
                        packaging_of_the_product, pdp_url, big_basket_approve_not_approve, City_Name, zipcode, count,
                        orginal_html, pack_shot_name)
        else:
            sku_input = tab.ele("xpath:(//input[@placeholder='Search for Products...'])[2]")
            if sku_input:
                sku_input.clear()
                sku_input.input(pdp_name)
                tab.actions.key_down('DOWN').key_down('ENTER')
                try:
                    time.sleep(2)
                    os.makedirs(db.screenshot_filepath, exist_ok=True)
                    tab.get_screenshot(path=db.screenshot_filepath,
                                       name=f"{page_id}_{pincode}_{db.current_date}.png",
                                       full_page=True)  # full_page=True
                    pack_shot_name = f"{page_id}_{pincode}_{db.current_date}.png"
                except Exception as e:
                    logger.error("Screenshot can't taken: ", e)
                html = tab.html
                count = ''
                page_save(conn, count, page_id, html)
                logger.info("Screenshot successfully taken.")
                insert_data(page_id, brand, category, pdp_name, quantity_of_the_product, single_pack, bundle_pack,
                            quantity,
                            packaging_of_the_product, pdp_url, big_basket_approve_not_approve, City_Name, zipcode,
                            count,
                            orginal_html, pack_shot_name)
    tab.close()


def fetch_all(browser, urls, conn, num_tabs):
    # Split the URLs into batches with their corresponding IDs
    url_batches = [urls[i::num_tabs] for i in range(num_tabs)]

    tabs = [browser.new_tab() for _ in range(num_tabs)]

    with ThreadPoolExecutor(max_workers=num_tabs) as executor:
        for i in range(num_tabs):
            executor.submit(fetch_page, tabs[i], url_batches[i], conn)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Usage: python script.py <port> <start_id> <end_id> <num_tabs>")
        sys.exit(1)
    port = sys.argv[1]
    start_id = sys.argv[2]
    end_id = sys.argv[3]
    pincode = sys.argv[5]
    try:
        num_tabs = int(sys.argv[4])
    except ValueError:
        logger.error("num_tabs must be an integer.")
        sys.exit(1)
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database=db.database_name
    )

    cur = conn.cursor()
    cur.execute(
        f'SELECT * FROM {db.pdp_link_table} WHERE status = "pending" and zipcode="{pincode}";')
    results = cur.fetchall()
    # Prepare a list of tuples (product_urls, id)
    urls = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            for row in results]  # Extracting URL and ID from query results
    browser = Chromium(f'127.0.0.1:{port}', co)
    # Fetch all pages and save them
    fetch_all(browser=browser, urls=urls, conn=conn, num_tabs=num_tabs)
    browser.quit()
