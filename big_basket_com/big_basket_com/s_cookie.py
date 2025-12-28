import json
import os
import time
from logger import logger
from DrissionPage import Chromium, ChromiumOptions
import hashlib
import sys
import zipfile
import pymysql
from concurrent.futures import ThreadPoolExecutor
import datetime
import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from scrapy import Selector

import db_config as db

final_dict = dict()

zipcode_saved = list()

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='actowiz',
    database='big_basket_com'
)

table = "pincodes"

cur = conn.cursor()

cur.execute(
    f'SELECT id, `city`,`pincode` FROM {table} WHERE status = "pending";')
results = cur.fetchall()

pincode = '380054'  # Ahmedabad
for result in results:
    final_dict = dict()
    zipcode_saved = list()
    driver = webdriver.Chrome()
    i = 1
    pincode_set = True
    driver.get('https://www.bigbasket.com/')  # You may want to replace this sleep with an explicit wait
    driver.implicitly_wait(10)

    pincode = result[2]
    while pincode_set:
        try:
            # Todo: Match ZipCode
            try:
                match_zipcode = driver.find_element(By.XPATH,
                                                    "//button[@class='AddressDropdown___StyledMenuButton2-sc-i4k67t-3 ZpLbn']/span |(//button[@class='AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW']/span)[2]")

                if pincode in match_zipcode.text:
                    print('PinCode Already Successfully Seted..!')
                    break
                else:
                    pass
            except Exception as e:
                print(e)

            # Todo: Check System Block or Not
            page_not_found = driver.find_element(By.XPATH, "//title")
            if "Access Denied" in page_not_found.text:
                driver.refresh()
            else:
                pass

            # Todo: Click Location Button
            try:
                location_button = driver.find_element(By.XPATH,
                                                      '(//button[contains(@class,"AddressDropdown")]//span[contains(text(),"Select Location")])[2]|(//button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"])[2]')
                location_button.click()
            except:
                location_button = driver.find_element(By.XPATH,
                                                      '//button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"]')
                location_button.click()
                if not location_button:
                    print("Location button not found.")

            from_input = driver.find_element(By.XPATH,
                                             "(//input[@class='Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn'])[2] | (//input[@placeholder='Search for area or street name'])[2]")

            from_input.click()
            from_input.send_keys(pincode)
            time.sleep(2)
            update_button = driver.find_element(
                By.XPATH,
                f"(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 cTJSLV'])[{i}]|(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX'])[{i}]|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 ggMOKv']|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN']")
            if update_button:
                update_button.click()
                service_not_available = ''
                try:
                    service_not_available = driver.find_element(By.XPATH,
                                                                "//span[contains(text(),'The selected city is not serviceable at the moment')]")
                except Exception as e:
                    print(e)
                try:
                    if service_not_available.text:
                        driver.refresh()
                except Exception as e:
                    print(e)
                i += 1
            else:
                print("Update button not found.")
        except Exception as e:
            logger.error(f"Error entering pincode or clicking update: {e}")

    # Todo: count
    try:
        try:
            driver.get('https://www.bigbasket.com/pd/40090894')
            add_to_basket = driver.find_element(By.XPATH, '(//button[contains(text(),"Add to basket")])[1]')
            add_to_basket.click()
            driver.refresh()
            updated_cookies = driver.get_cookies()
        except:
            driver.get('https://www.bigbasket.com/pd/100647221')
            add_to_basket = driver.find_element(By.XPATH, '(//button[contains(text(),"Add to basket")])[1]')
            add_to_basket.click()
            driver.refresh()
            updated_cookies = driver.get_cookies()

        cookies_dict = dict()
        for key in updated_cookies:
            cookies_dict[key['name']] = key['value']

        final_dict[pincode] = cookies_dict
        new_cookie = json.dumps(final_dict)
        open('Newzip.json', 'w').write(new_cookie)
        print("Cookie Successfully geted")

        # Todo: Update Cookie in Table
        try:
            table_cookie = json.dumps(cookies_dict)
            update_query = f"UPDATE {table} SET cookies = %s WHERE pincode = %s"
            cur.execute(update_query, (table_cookie, pincode))
            conn.commit()
        except Exception as e:
            print(e)

        # Todo: Done-Pending
        try:
            update_query = f"UPDATE {table} SET status = %s WHERE pincode = %s"
            cur.execute(update_query, ("Done", pincode))
            conn.commit()
        except Exception as e:
            print(e)

        driver.delete_all_cookies()
        time.sleep(1)

    except Exception as e:
        print(e)
    driver.quit()
