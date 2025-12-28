import os
import time
import pymysql
from numpy.f2py.crackfortran import previous_context
from playwright.sync_api import sync_playwright


def get_rendered_html(url):
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to the URL and wait for network to be idle (i.e., all JS is done)
        page.goto(url, wait_until='networkidle')

        # Optional: Wait for a specific element if needed
        # page.wait_for_selector('div.content')

        # Get the full rendered page HTML
        html = page.content()

        # Close browser
        browser.close()
        return html

# def scroll_and_save_html(url, scroll_pause=1, step_size=10000, max_scrolls=1000):
def scroll_and_save_html(url, scroll_pause=1, step_size=20000, max_scrolls=1000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until='domcontentloaded')
        time.sleep(20)
        previous_content = None


        for i in range(max_scrolls):
            # if i < 5:
            #     step_size += 1000
            file_name = url.replace("://", '_').replace('.', '_').replace('/', '_')
            # file_name = 'newyork'
            # path = fr"D:\Smitesh\pagesave\craigslist\pl\{file_name}"
            path = fr"E:\Nirav\Project_page_save\craigslist\pl\{file_name}"
            if not(os.path.exists(path)):
                os.makedirs(path)
            # output_file = fr"D:\Smitesh\Projects\craigslist\pages\page_{i}.html"
            output_file = fr"{path}\page_{i}.html"
            html = page.content()
            if html == previous_content:
                break
            previous_content = html

            # Save HTML to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(html)
                f.close()

            # todo
            # Scroll down by a fixed step
            page.evaluate(f"window.scrollBy(0, {step_size})")
            time.sleep(scroll_pause)

            # Optionally, print progress
            print(f"Scrolled step {i + 1}")
            time.sleep(1)

            # Optional: break if reached bottom
            at_bottom = page.evaluate("""
                () => {
                    return (window.innerHeight + window.scrollY) >= document.body.scrollHeight
                }
            """)

            if at_bottom:
                print("Reached bottom of the page.")
                break
            # todo
            # print(scroll_to_bottom(page))

            print(f"HTML content saved to: {output_file}")
        browser.close()


# Example usage
# url = "https://newyork.craigslist.org/search/ela"
# html = get_rendered_html(url)
# scroll_and_save_html('https://newyork.craigslist.org/search/ela')
# print(html)

if __name__ == '__main__':
    con = pymysql.connect(host='localhost', user='root', password='actowiz', database='craigslist')
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute("select * from newyork_links_30052025 where status='pending'")
    rows = cur.fetchall()
    for row in rows:
        scroll_and_save_html(row['link'])
        cur.execute(f"update newyork_links_30052025 set status='done' where link='{row['link']}'")
        con.commit()

    # scroll_and_save_html("https://newyork.craigslist.org/search/sss?excats=20-22-2-25-4-46-3-2-21-1-14-1-2-1-4-22-1-1-1-1-11-1&isTrusted=true#search=2~gallery~0")



