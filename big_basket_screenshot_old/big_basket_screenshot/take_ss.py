# import os
# import time
# from logger import logger
# from DrissionPage import Chromium, ChromiumOptions
# import hashlib
# import sys
# import zipfile
# import pymysql
# from concurrent.futures import ThreadPoolExecutor
# import datetime
# from big_basket_screenshot.create_table import create_table, pending_links
# from scrapy import Selector
#
# import db_config as db
#
# co = ChromiumOptions()
# co.set_argument('--no-sandbox')
# co.no_imgs(True)
# co.no_js(True)
#
# co.add_extension(
#     r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data\Default\Extensions\eifflpmocdbdmepbjaopkkhbfmdgijcc')
# # co.set.set_cookies(None)
# current_date = datetime.datetime.now().strftime("%d_%m_%Y")
#
#
# def page_save(conn,count, page_id, html):
#     os.makedirs(db.pagesave_filepath, exist_ok=True)
#     file_name = fr'{db.pagesave_filepath}\{page_id}.html'
#     # Save the HTML content to a file
#     with open(file_name, 'wb') as file:
#         file.write(html.encode())
#     print(f"Saved page to: {file_name}")
#
#     try:
#         conn = pymysql.connect(
#             host='localhost',
#             user='root',
#             password='actowiz',
#             database=db.database_name
#         )
#
#         cur = conn.cursor()
#         cur.execute(f"UPDATE {db.pdp_link_table} SET status = 'Done' WHERE id = %s", (page_id,))
#         conn.commit()
#
#         if count=='':
#             count='N/A'
#
#         try:
#             sql = f"""UPDATE {db.pdp_link_table} SET quantity_caping = '{count}' WHERE id = {page_id}"""
#             cur.execute(sql)
#             conn.commit()
#         except Exception as e:
#             print(e)
#
#         cur.close()
#         conn.close()
#
#         logger.info(f"Updated status for page id: {page_id}")
#     except Exception as e:
#         logger.error(f"Error updating database: {e}")
#
#
# def fetch_page(tab, urls, conn):
#     print()
#     i=1
#     pincode_set = True
#     while pincode_set:
#         try:
#             tab.get('https://www.bigbasket.com/')
#             # res = Selector(text=tab.html)
#             # #
#             # page_not_found = res.xpath("//title/text()").get()
#             # if "Access Denied" in page_not_found:
#             #     tab.refresh()
#             time.sleep(0.5)
#             res = Selector(text=tab.html)
#             match_zipcode = res.xpath("//button[@class='AddressDropdown___StyledMenuButton2-sc-i4k67t-3 ZpLbn']/span/text()|//button[@class='AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW']/span/text()").get()
#
#             if match_zipcode:
#                 if sys.argv[5] in match_zipcode:
#                     print('nirvo')
#                     # pincode_set = False
#                     break
#                 else:
#                     pass
#
#             location_button = tab.ele(
#                     'xpath:(//button[contains(@class,"AddressDropdown")]//span[contains(text(),"Select Location")])[2]|(//button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"])[2]')
#             if location_button:
#                 location_button.click()
#             else:
#                 location_button = tab.ele(
#                         'xpath://button[@class="AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW"]')
#                 location_button.click()
#                 if not location_button:
#                     print("Location button not found.")
#                     return False
#         except Exception as e:
#             logger.error(f"Error clicking location button: {e}")
#             return False
#
#         try:
#             from_input = tab.ele(
#                 "xpath:(//input[@class='Input-sc-tvw4mq-0 AddressDropdown___StyledInput-sc-i4k67t-8 hpyysx eQvECn'])[2] | (//input[@placeholder='Search for area or street name'])[2]")
#             if from_input:
#                 from_input.click()
#                 from_input.input(sys.argv[5])
#                 time.sleep(2)
#                 tab.actions.key_down('DOWN').key_down('ENTER')
#             else:
#                 if not from_input:
#                     from_input = tab.ele(
#                         "xpath://input[contains(@placeholder,'Search for area or street name')]")
#                     if from_input:
#                         from_input.click()
#                         from_input.input(sys.argv[5])
#                         time.sleep(2)
#                         tab.actions.key_down('DOWN').key_down('ENTER')
#                     else:
#                         print("Pincode input field not found.")
#                         return False
#
#             update_button = tab.ele(
#                 f"xpath:(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 cTJSLV'])[{i}]|(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX'])[{i}]|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 ggMOKv']|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN']")
#             if update_button:
#                 update_button.click()
#                 response = Selector(text=tab.html)
#                 service_not_available = response.xpath(
#                     "//span[contains(text(),'The selected city is not serviceable at the moment')]")
#                 if service_not_available:
#                     tab.refresh()
#                 i += 1
#             else:
#                 print("Update button not found.")
#                 return False
#         except Exception as e:
#             logger.error(f"Error entering pincode or clicking update: {e}")
#             return False
#
#     time.sleep(1)
#     for pdp_name, page_id, pdp_url, pincode in urls:
#         if pdp_url:
#             try:
#                 tab.get(pdp_url)
#             except Exception as e:
#                 logger.error('Somethig wrong in chrome tab',e)
#             pid = ''
#             if pdp_url:
#                 try:
#                     pid = pdp_url.split('/pd/')[-1]
#                     if '/' in pid:
#                         pid = pid.split('/')[0]
#                 except:
#                     pid = 'N/A'
#
#             time.sleep(2)
#
#             orginal_html = tab.html
#
#             # Todo: count
#             try:
#                 add_to_basket=tab.ele('xpath:(//button[contains(text(),"Add to basket")])[1]')
#                 add_to_basket.click()
#                 count = 0
#                 while True:
#                     element = tab.ele(
#                         'xpath:(//button[contains(@class,"PdCartCTA___StyledButton2-sc-mq73zq-3")])[1]')
#                     if element:
#                         html = tab.html
#                         response = Selector(text=html)
#                         original_count = response.xpath("//div[@class='PdCartCTA___StyledDiv2-sc-mq73zq-2 cdHBKF']/text()").get(
#                             '').strip()
#                         count += 1
#                         if original_count:
#                             if count == int(original_count):
#                                 element.click()
#                             else:
#                                 count = count - 1
#                                 break
#                         else:
#                             break
#                         time.sleep(1)
#                     else:
#                         print("Element not found, exiting loop.")
#                         break  # Exit loop if element is not available
#             except:
#                 count = 0
#
#             os.makedirs(db.screenshot_filepath, exist_ok=True)
#             tab.get_screenshot(path=db.screenshot_filepath, name=f"{pid}_{pincode}_{db.current_date}.png",
#                                full_page=True)  # full_page=True
#             print("Screenshot successfully taken.")
#             page_save(conn,count, page_id, orginal_html)
#         else:
#             sku_input = tab.ele("xpath:(//input[@placeholder='Search for Products...'])[2]")
#             if sku_input:
#                 sku_input.clear()
#                 sku_input.input(pdp_name)
#                 tab.actions.key_down('DOWN').key_down('ENTER')
#                 try:
#                     time.sleep(2)
#                     os.makedirs(db.screenshot_filepath, exist_ok=True)
#                     tab.get_screenshot(path=db.screenshot_filepath,
#                                        name=f"{page_id}_{pincode}_{db.current_date}.png",full_page=True)  # full_page=True
#                 except Exception as e:
#                     logger.error("Screenshot can't taken: ",e)
#                 html = tab.html
#                 count = ''
#                 page_save(conn,count,page_id, html)
#                 logger.info("Screenshot successfully taken.")
#             print()
#             pass
#     tab.close()
#
#
# def fetch_all(browser, urls, conn, num_tabs):
#     # Split the URLs into batches with their corresponding IDs
#     url_batches = [urls[i::num_tabs] for i in range(num_tabs)]
#
#     tabs = [browser.new_tab() for _ in range(num_tabs)]
#
#     with ThreadPoolExecutor(max_workers=num_tabs) as executor:
#         for i in range(num_tabs):
#             executor.submit(fetch_page, tabs[i], url_batches[i], conn)
#
#
# if __name__ == '__main__':
#     pending_links()
#     create_table()
#     if len(sys.argv) != 6:
#         print("Usage: python script.py <port> <start_id> <end_id> <num_tabs>")
#         sys.exit(1)
#     port = sys.argv[1]
#     start_id = sys.argv[2]
#     end_id = sys.argv[3]
#     pincode = sys.argv[5]
#     try:
#         num_tabs = int(sys.argv[4])
#     except ValueError:
#         logger.error("num_tabs must be an integer.")
#         sys.exit(1)
#     conn = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='actowiz',
#         database=db.database_name
#     )
#
#     cur = conn.cursor()
#
#     # Fetch the site_map_link_table_feb and their IDs from the database
#     # cur.execute(
#         # f'SELECT Id, `Name_of_the_Product`,`big_basket`,`zipcode`  FROM {db.pdp_link_table} WHERE status = "pending" and zipcode="{pincode}" limit {start_id},{end_id}')
#     cur.execute(
#         f'SELECT Id, `Name_of_the_Product`,`big_basket`,`zipcode`  FROM {db.pdp_link_table} WHERE status = "pending" and zipcode="{pincode}";')
#     results = cur.fetchall()
#     # Prepare a list of tuples (product_urls, id)
#     urls = [(row[1], row[0], row[2], row[3]) for row in results]  # Extracting URL and ID from query results
#     browser = Chromium(f'127.0.0.1:{port}', co)
#     # Fetch all pages and save them
#     fetch_all(browser=browser, urls=urls, conn=conn, num_tabs=num_tabs)
#     browser.quit()
