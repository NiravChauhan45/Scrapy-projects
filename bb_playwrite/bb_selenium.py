from selenium.webdriver.chrome.options import Options
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pymysql

# Sample data (uncomment DB part if needed)
results = [['New Delhi', '110016']]

for i in results:
    zipcode = i[1]
    city_name = i[0]

    options = Options()
    # options.add_argument('--headless')  # Optional: run headless
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.bigbasket.com/')

        wait = WebDriverWait(driver, 15)

        # Click 'Select Location' button
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//button[contains(@class,'AddressDropdown')]//span[contains(text(),'Select Location')])[2]")
        )).click()

        # Enter zip code
        input_element = wait.until(EC.presence_of_element_located(
            (By.XPATH,
             "//div[@class='AddressDropdown___StyledDiv-sc-i4k67t-7 eXGbTp']//input[@placeholder='Search for area or street name']")
        ))
        input_element.click()
        input_element.send_keys(zipcode)

        # Select first option from dropdown
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@id,'option-0')]")
        )).click()

        # Click continue button
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@name='continue']")
        )).click()

        # Collect cookies
        ck = {}
        for cook in driver.get_cookies():
            if cook['name'] in ['_bb_visaddr', '_bb_lat_long']:
                ck[cook['name']] = cook['value']

        with open('cookies_yummiez_21_8.txt', 'a', encoding='utf-8') as f:
            f.write(f"{city_name}@{zipcode}@{json.dumps(ck)}\n")

        driver.close()

        if ck:
            print("Cookies captured:", ck)
            # You can add your database update code here

        else:
            print("No cookies found!")

    except Exception as e:
        print("Error occurred:", e)

        try:
            # Check if specific text exists in page source
            if "Sorry! We couldn't find any choices" in driver.page_source:
                with open('cookies_yummiez_21_8.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{city_name}@{zipcode}@not_found\n")
            else:
                with open('cookies_yummiez_21_8.txt', 'a', encoding='utf-8') as f:
                    f.write(f"{city_name}@{zipcode}@\n")
        except:
            pass
        driver.close()


# await page.fill(
#             '(//input[@class="Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn"])[2]',
#             zipcode)