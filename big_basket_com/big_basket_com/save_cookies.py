import json
import os.path
import re
import time

import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

zipcodes = [600083, 560034, 560001, 500081, 380054, 440010, 110001, 110016, 110026, 110092, 400001, 400013, 400050,
            400101, 700017, 700019, 700026, 700034, 226001, 226004, 226010, 226021, 800001, 800002, 800008, 800013]

final_dict = dict()

zipcode_saved = list()

driver = webdriver.Chrome()


for zipcode in zipcodes:
    if zipcode in zipcode_saved:
        continue
    driver.get('https://www.bigbasket.com/')  # You may want to replace this sleep with an explicit wait
    driver.implicitly_wait(10)  # Wait for up to 10 seconds for elements to load

    element = driver.find_element(By.XPATH,
                                  '(//button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"])[2]')
    element.click()

    input_element = driver.find_element(By.XPATH,
                                        "(//input[@class='Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn'])[2] | (//input[@placeholder='Search for area or street name'])[2]")
    input_element.send_keys(zipcode)

    i = 1
    while True:
        submit_button = driver.find_element(By.XPATH,
                                            f"(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 cTJSLV'])[{i}]|(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX'])[{i}]|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 ggMOKv']|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN']")

        submit_button.click()

        match_zipcode = driver.find_element(By.XPATH,
                                            "(//button[@class='AddressDropdown___StyledMenuButton2-sc-i4k67t-3 ZpLbn']/span | //button[@class='AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW']/span)[2]")
        if str(zipcode) in match_zipcode.text:
            driver.get('https://www.bigbasket.com/pd/10000298/')
            add_to_cart = driver.find_element(By.XPATH, "(//button[contains(text(),'Add to basket')])[1]")
            if "Add to basket" in add_to_cart.text:
                add_to_cart.click()
                time.sleep(4)
            else:
                pass
            break
        else:
            i += 1


    cookies_dict = dict()
    for key in driver.get_cookies():
        cookies_dict[key['name']] = key['value']

    final_dict[zipcode] = cookies_dict
    open('Newzip.json', 'w').write(json.dumps(final_dict))

    driver.delete_all_cookies()
    time.sleep(1)
driver.quit()
