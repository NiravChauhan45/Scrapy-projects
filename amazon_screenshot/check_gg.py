import os
import re
import time
from DrissionPage import Chromium, ChromiumOptions
import sys
import pymysql
from concurrent.futures import ThreadPoolExecutor
import datetime
from parsel import Selector

import db_config as db

co = ChromiumOptions()
co.set_argument('--no-sandbox')
co.no_imgs(True)
co.no_js(True)
co.add_extension(
    # r'C:\Users\admin\AppData\Local\Google\Chrome\User Data\Default\Default\Extensions\ghbmnnjooekpmoecnnnilnnbdlolhkhi')
    r'C:\Users\nirav.chauhan\AppData\Local\Google\Chrome\User Data\Default\Extensions\eifflpmocdbdmepbjaopkkhbfmdgijcc')


def page_save(conn, page_id, html):
    os.makedirs(db.pagesave_filepath, exist_ok=True)
    file_name = fr'{db.pagesave_filepath}\{page_id}.html'
    # Save the HTML content to a file
    with open(file_name, 'wb') as file:
        file.write(html.encode())
    print(f"Saved page to: {file_name}")

    # Update the status in the database (set 'status' to 'done' for the given page_id)
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='actowiz',
            database='amazon_fresh_screenshot'
        )
        cur = conn.cursor()
        cur.execute(f"UPDATE {db.pdp_link_table} SET status = 'Pending' WHERE id = %s", (page_id,))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Updated status for page id: {page_id}")
    except Exception as e:
        print(f"Error updating database: {e}")


def fetch_page(tab, urls, conn):
    tab.get('https://www.amazon.in/')
    res = Selector(text=tab.html)

    if "Enter the characters you see below" in res._text or "Click the button below to continue shopping" in res._text:  # or "Click the button below to continue shopping" in res._text
        tab.refresh()

    check_pincode_list = res.xpath("//div[@id='glow-ingress-block']//span//text()").getall()
    check_pincode = " ".join([re.sub("\\s+", " ", i).strip() for i in check_pincode_list if i])
    if sys.argv[5] not in check_pincode:
        try:
            location_button = tab.ele('xpath://a[@id="nav-global-location-popover-link"]')
            if location_button:
                location_button.click()
            else:
                print("Location button not found.")
                return False
        except Exception as e:
            print(f"Error clicking location button: {e}")
            return False

        try:
            from_input = tab.ele("xpath://input[@class='GLUX_Full_Width a-declarative']")
            if from_input:
                from_input.click()
                from_input.clear()
                from_input.input(sys.argv[5])
                time.sleep(2)
                tab.actions.key_down('DOWN').key_down('ENTER')
            else:
                print("Pincode input field not found.")
                return False

            time.sleep(1)
            update_button = tab.ele("xpath://span[@id='GLUXZipUpdate-announce']")
            if update_button:
                update_button.click()
                time.sleep(1)

            else:
                print("Update button not found.")
                return False
        except Exception as e:
            print(f"Error entering pincode or clicking update: {e}")
            return False

    res = Selector(text=tab.html)
    check_pincode_list = res.xpath("//div[@id='glow-ingress-block']//span//text()").getall()
    check_pincode = " ".join([re.sub("\\s+", " ", i).strip() for i in check_pincode_list if i])

    if sys.argv[5] in check_pincode:
        time.sleep(5)
        for pdp_name, page_id, pdp_url, pincode in urls:
            if 'https://www.amazon.in' in pdp_url or 'https://www.amazon.iN' in pdp_url or 'https://wwwamazon.in' in pdp_url:
                tab.get(pdp_url)
                if pdp_url:
                    try:
                        pid = pdp_url.split('/dp/')[-1].split('/')[0].split('?')[0].strip() or 'N/A'
                    except:
                        pid = 'N/A'

                time.sleep(2)
                os.makedirs(db.screenshot_filepath, exist_ok=True)
                res = Selector(text=tab.html)
                check_pincode_list = res.xpath("//div[@id='glow-ingress-block']//span//text()").getall()
                check_pincode = " ".join([re.sub("\\s+", " ", i).strip() for i in check_pincode_list if i])
                if sys.argv[5] in check_pincode:
                    tab.get_screenshot(path=db.screenshot_filepath, name=f"{pid}_{pincode}_{db.current_date}.png",
                                       full_page=True)
                    print("Screenshot successfully taken.")
                    html = tab.html
                    page_save(conn, page_id, html)
            else:
                sku_input = tab.ele("xpath://input[@id='twotabsearchtextbox']")
                if sku_input:
                    sku_input.clear()
                    sku_input.input(pdp_name)
                    tab.actions.key_down('DOWN').key_down('ENTER')
                    try:
                        time.sleep(2)
                        tab.get_screenshot(path=db.screenshot_filepath,
                                           name=f"{page_id}_{pincode}_{db.current_date}.png",
                                           full_page=True)
                    except Exception as e:
                        print(e)
                    html = tab.html
                    page_save(conn, page_id, html)
                    print("Screenshot successfully taken.")
                print()
                pass
        tab.close()


def fetch_all(browser, urls, conn, num_tabs):
    # Split the URLs into batches with their corresponding IDs
    url_batches = [urls[i::num_tabs] for i in range(num_tabs)]

    tabs = [browser.new_tab() for _ in range(num_tabs)]

    with ThreadPoolExecutor(max_workers=num_tabs) as executor:
        for i in range(num_tabs):
            executor.submit(fetch_page, tabs[i], url_batches[i], conn)


if __name__ == '__main__':

    # create_table()  # Todo: Create table if does not exists
    # pending_links()  # Todo: Pending all links if all links are Done / Finally_Done
    current_date = datetime.datetime.now().strftime("%d_%m_%Y")
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
        print("num_tabs must be an integer.")
        sys.exit(1)
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database='amazon_fresh_screenshot'
    )

    cur = conn.cursor()

    # Fetch the site_map_link_table_feb and their IDs from the database
    cur.execute(
        f'SELECT Id, `Name of the Product`,`Amazon Fresh`,`zipcode`  FROM {db.pdp_link_table} WHERE id BETWEEN {start_id} AND {end_id} and zipcode="{pincode}" and status="Pending"')
    results = cur.fetchall()
    # Prepare a list of tuples (product_urls, id)
    urls = [(row[1], row[0], row[2], row[3]) for row in results]  # Extracting URL and ID from query results
    browser = Chromium(f'127.0.0.1:{port}', co)
    # Fetch all pages and save them
    fetch_all(browser, urls, conn, num_tabs)
    browser.quit()
