import base64
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import pymysql
from loguru import logger
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--incognito")
options.add_argument("--start-maximized")
options.add_argument("window-size=1920,1080")

def page_save(conn, count, page_id, html):
    conn = pymysql.connect(
        # host='172.27.131.57',
        host='localhost',
        user='root',
        password='actowiz',
        database="big_basket_screenshot"
    )

    cur = conn.cursor()

    pagesave_filepath = "E:\\Nirav\\Learning\\selenium\\pagesave"
    os.makedirs(pagesave_filepath, exist_ok=True)

    file_name = fr'{pagesave_filepath}\{page_id}.html'
    # Save the HTML content to a file
    with open(file_name, 'wb') as file:
        file.write(html.encode())
    print(f"Saved page to: {file_name}")

    try:
        cur.execute(f"UPDATE pdp_link_table_21_06_2025 SET status = 'Done' WHERE id = %s", (page_id,))
        conn.commit()

        if count == '':
            count = 'N/A'

        try:
            sql = f"""UPDATE pdp_link_table_21_06_2025 SET quantity_caping = '{count}' WHERE id = {page_id}"""
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)

        cur.close()
        conn.close()

        logger.info(f"Updated status for page id: {page_id}")
    except Exception as e:
        logger.error(f"Error updating database: {e}")


def fetch_page(driver, results, conn):
    main_screeshot_path = "E:\\Nirav\\Learning\\selenium\\Screenshots"
    os.makedirs(main_screeshot_path, exist_ok=True)

    for pincode, district, StateName in results:
        i = 1
        pincode_set = True
        while pincode_set:
            try:
                time.sleep(1)
                driver.get("https://www.bigbasket.com/")
                # Todo: Reload page if condition is True
                if "access denite" in driver.page_source.lower():
                    pass

                # Todo: Match Zipcode
                try:
                    time.sleep(2)
                    match_zipcode = driver.find_element(
                        By.XPATH,
                        "//button[@class='AddressDropdown___StyledMenuButton2-sc-i4k67t-3 ZpLbn']/span | //button[@class='AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW']/span"
                    ).text
                    if match_zipcode:
                        if pincode in match_zipcode or pincode in driver.page_source:
                            print("Zipcode are matched successfully !!")
                            break
                        else:
                            pass
                except Exception as e:
                    print(e)

                # Todo: Location Button
                try:
                    location_button = driver.find_element(By.XPATH,
                                                          '(//button[contains(@class,"AddressDropdown")]//span[contains(text(),"Select Location")])[2]|(//button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"])[2]')
                    if location_button:
                        location_button.click()
                    else:
                        location_button = driver.find_element(By.XPATH,
                                                              '//button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"]')
                        if not location_button:
                            print("Location button not found.")
                        else:
                            location_button.click()
                except Exception as e:
                    print(e)

                # Todo: Input Pincode
                try:
                    time.sleep(2)
                    from_input = driver.find_element(By.XPATH,
                                                     "(//input[@class='Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn'])[2] | (//input[@placeholder='Search for area or street name'])[2]")
                    if from_input:
                        from_input.click()
                        from_input.send_keys(pincode)
                        time.sleep(2)
                        ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
                    else:
                        time.sleep(1)
                        from_input = driver.find_element(By.XPATH,
                                                         "//input[contains(@placeholder,'Search for area or street name')]")
                        if from_input:
                            from_input.click()
                            from_input.send_keys(pincode)
                            time.sleep(2)
                            ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
                        else:
                            print("Pincode input field not found.")
                except Exception as e:
                    print(e)

                # Todo: Update Button
                try:
                    time.sleep(2)
                    update_button = driver.find_element(By.XPATH,
                                                        f"(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 cTJSLV'])[{i}]|(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX'])[{i}]|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 ggMOKv']|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN']")
                    if update_button:
                        time.sleep(0.5)
                        update_button.click()
                        # driver.refresh()
                        time.sleep(1)
                        response = Selector(text=driver.page_source)
                        service_not_available = response.xpath(
                            "//span[contains(text(),'The selected city is not serviceable at the moment')]/text()").get()
                        if service_not_available:
                            driver.refresh()
                        i += 1
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

        #save cookies
        driver.get_cookie()



if __name__ == '__main__':
    # if len(sys.argv) != 4:
    #     print("Usage: python script.py <port> <start_id> <end_id> <num_tabs>")

    # try:
    #     port = sys.argv[1]
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     start_id = sys.argv[2]
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     end_id = sys.argv[3]
    # except Exception as e:
    #     print(e)
    #
    # try:
    #     pincode = sys.argv[4]
    # except Exception as e:
    #     print(e)
    #


    conn = pymysql.connect(
        # host='172.27.131.57',
        host='localhost',
        user='root',
        password='actowiz',
        database="big_basket_api"
    )

    cur = conn.cursor()
    cur.execute(
        f'SELECT Pincode,District,StateName FROM `all_india_pincode` WHERE status = "pending";')
    results = cur.fetchall()
    urls = [(row[0], row[1], row[2]) for row in results]  # Extracting URL and ID from query results

    # options.add_argument(f"--remote-debugging-port={sys.argv[0]}")
    driver = webdriver.Chrome(options=options)
    fetch_page(driver=driver, results=results, conn=conn)
