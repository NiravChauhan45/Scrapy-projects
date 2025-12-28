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

    for page_id, pdp_name, pdp_url, pincode in results:
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
                        if sys.argv[4] in match_zipcode or sys.argv[4] in driver.page_source:
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
                        from_input.send_keys(sys.argv[4])
                        time.sleep(2)
                        ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
                    else:
                        time.sleep(1)
                        from_input = driver.find_element(By.XPATH,
                                                         "//input[contains(@placeholder,'Search for area or street name')]")
                        if from_input:
                            from_input.click()
                            from_input.send_keys(sys.argv[4])
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
                        response = Selector(text=driver.page_source)
                        service_not_available = response.xpath(
                            "//span[contains(text(),'The selected city is not serviceable at the moment')]")
                        if service_not_available:
                            driver.refresh()
                        i += 1
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

        # Todo: count
        add_to_basket_count = 0
        pid = ''

        if pdp_url:
            try:
                try:
                    pid = pdp_url.split('/pd/')[-1]
                    if '/' in pid:
                        pid = pid.split('/')[0]
                except:
                    pid = 'N/A'
                try:
                    time.sleep(1)
                    driver.get(pdp_url)
                except Exception as e:
                    logger.error('Somethig wrong in chrome tab', e)

                # driver.execute_script("window.scrollBy(0, 100)")
                add_to_basket = driver.find_element(By.XPATH, '(//button[contains(text(),"Add to basket")])[1]')
                add_to_basket.click()
                time.sleep(5)
                while True:
                    element = driver.find_element(By.XPATH,
                                                  '(//button[contains(@class,"PdCartCTA___StyledButton2-sc-mq73zq-3")])[1]')
                    if element:
                        html = driver.page_source
                        response = Selector(text=html)
                        original_count = response.xpath(
                            "//div[@class='PdCartCTA___StyledDiv2-sc-mq73zq-2 cdHBKF']/text()").get(
                            '').strip()
                        add_to_basket_count += 1
                        if original_count:
                            if add_to_basket_count == int(original_count):
                                element.click()
                            else:
                                add_to_basket_count = add_to_basket_count - 1
                                break
                        else:
                            break
                        time.sleep(1)
                    else:
                        print("Element not found, exiting loop.")
                        break  # Exit loop if element is not available
            except:
                add_to_basket_count = 0
            try:
                current_date = datetime.now().strftime("%d_%m_%Y")
                time.sleep(2)

                screeshot_path = f"\\{pid}_{pincode}_{current_date}.png"
            except Exception as e:
                logger.error("Screenshot can't taken: ", e)
            print(f"Count Of This Product id: {pdp_url.split('/pd/')[-1]} Count: {add_to_basket_count}")
        else:
            sku_input = driver.find_element(By.XPATH, "(//input[@placeholder='Search for Products...'])[2]")
            if sku_input:
                sku_input.clear()
                sku_input.send_keys(pdp_name)
                # driver.actions.key_down('DOWN').key_down('ENTER')
                ActionChains(driver).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
                try:
                    current_date = datetime.now().strftime("%d_%m_%Y")
                    time.sleep(2)

                    screeshot_path = f"\\{page_id}_{pincode}_{current_date}.png"
                except Exception as e:
                    logger.error("Screenshot can't taken: ", e)
            print("No Url Found !!")

        html = driver.page_source
        page_save(conn, add_to_basket_count, page_id, html)
        logger.info("Pagesave successfully Saved.")

        # Capture full-page screenshot using CDP
        result = driver.execute_cdp_cmd("Page.captureScreenshot", {
            "captureBeyondViewport": True,
            "fromSurface": True
        })

        ss_path = main_screeshot_path + screeshot_path
        # Save the screenshot
        with open(ss_path, "wb") as f:
            f.write(base64.b64decode(result['data']))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python script.py <port> <start_id> <end_id> <num_tabs>")

    try:                                
        port = sys.argv[1]
    except Exception as e:
        print(e)

    try:
        start_id = sys.argv[2]
    except Exception as e:
        print(e)

    try:
        end_id = sys.argv[3]
    except Exception as e:
        print(e)

    try:
        pincode = sys.argv[4]
    except Exception as e:
        print(e)

    try:
        num_tabs = int(sys.argv[5])
    except ValueError:
        logger.error("num_tabs must be an integer.")
        sys.exit(1)

    conn = pymysql.connect(
        # host='172.27.131.57',
        host='localhost',
        user='root',
        password='actowiz',
        database="big_basket_screenshot"
    )

    cur = conn.cursor()
    cur.execute(
        f'SELECT Id, `Name_of_the_Product`,`big_basket`,`zipcode` FROM pdp_link_table_21_06_2025 WHERE status = "pending" and zipcode="{pincode}";')
    results = cur.fetchall()
    urls = [(row[0], row[1], row[2], row[3]) for row in results]  # Extracting URL and ID from query results

    options.add_argument(f"--remote-debugging-port={sys.argv[1]}")
    driver = webdriver.Chrome(options=options)
    fetch_page(driver=driver, results=results, conn=conn)
