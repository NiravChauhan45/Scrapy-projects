import json
import os
from bs4 import BeautifulSoup
from curl_cffi import requests
import re
from re import sub
import dateparser
from datetime import datetime, timedelta
from urllib.parse import urljoin
import pytz
from parsel import Selector
from itemloaders.processors import TakeFirst, Join, MapCompose
from scrapy.loader import ItemLoader
import calendar

today_date = datetime.now(pytz.timezone('Asia/Calcutta'))


def identify_date_or_time(text):
    try:
        text = text.strip().lower()
    except:
        text = ''

    if text:
        # Regex for time (like "5 AM", "07:30 PM", "5 am – 7 am")
        time_pattern = re.compile(r'(\d{1,2}(:\d{2})?\s?(am|pm))')

        # Regex for date (like "11 September", "11 - 12 September")
        # date_pattern = re.compile(r'(\d{1,2})(\s*-\s*\d{1,2})?\s*[a-z]+')
        date_pattern = re.compile(r'\b\d{1,2}\s*-\s*\d{1,2}\s+[A-Za-z]+\b')

        found_time = bool(time_pattern.search(text))
        found_date = bool(date_pattern.search(text)) or "tomorrow" in text or "today" in text
        if found_date and found_time:
            return "Contains both DATE and TIME"
        elif found_date:
            return "Contains DATE only"
        elif found_time:
            return "Contains TIME only"
        else:
            return "No valid DATE or TIME found"
    else:
        return text


def clear_price(value: str):
    if value.strip():
        sub_value = sub(r'[^0-9.]', '', value).strip()
        if sub_value and sub_value.strip(".") and sub_value != ".":
            return sub_value


def two_process_arrival_date(text):
    text = text.strip().lower()
    year = datetime.now().year  # assume current year

    parts = text.replace("-", " ").split()

    if len(parts) == 3:
        # Case 1: "11 - 15 september"
        start_day, end_day, month = parts
        start_date = datetime.strptime(f"{start_day} {month} {year}", "%d %B %Y")
        end_date = datetime.strptime(f"{end_day} {month} {year}", "%d %B %Y")
        min_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        max_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        return min_date, max_date

    elif len(parts) == 2:
        # Case 2: "11 september"
        day, month = parts
        date = datetime.strptime(f"{day} {month} {year}", "%d %B %Y")
        return (date.strftime("%Y-%m-%d %H:%M:%S"), None)

    else:
        raise ValueError("Unexpected date format")


def parse_amazon_emi_html(html):
    soup = BeautifulSoup(html, "html.parser")

    headings = []
    for tag in soup.find_all(['h1', 'h4']):
        headings.extend(tag.stripped_strings)
    try:
        keys = headings[0]
    except:
        return {}

    result = {
        keys: []
    }

    # Step 1: Find processing fee if mentioned in the content
    fee_text = soup.find(text=lambda t: t and "Processing Fee" in t)
    if fee_text:
        result["Processing Fee"] = fee_text.strip()

    # Step 2: Find the table with EMI plans

    table = soup.find("table", class_="inemi-plans-table")
    if table:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 3:
                # EMI Plan
                emi_amount = cols[0].find_all("span")
                emi_plan = " ".join([s.get_text(strip=True) for s in emi_amount])

                # Interest
                interest = " ".join([s.get_text(strip=True) for s in cols[1].find_all("span")])

                # Total cost
                total_cost = cols[2].get_text(strip=True)

                result[keys].append({
                    "EMI Plan": emi_plan,
                    "Interest(pa)": interest,
                    "Total cost": total_cost
                })

    return result


def offer_strucute(response, product_id, offer_type, merchnt_id):
    selector = Selector(text=response.text)
    item_list = list()
    try:
        if offer_type == 'GCCashback':
            item = dict()
            details = selector.xpath(
                '//div[@id="GCCashback-single-offer"]//h1/text()|//div[@class="a-row a-spacing-medium"]/text()').get().strip()
            item['title'] = 'Cashback'
            item['details'] = details
            return {'Cashback': [item]}
        elif offer_type == 'NoCostEmi':
            for data in selector.xpath(
                    '//div[@id="NoCostEmi-sideSheet"]//div[@class="a-section vsx-offers-desktop-lv__item"] | //div[@class="a-section vsx-offers-desktop-lv__item"]'):
                item = dict()
                title = re.sub("\\s+", " ", data.xpath("./h1/text()").get()).strip()
                details = data.xpath("./p[@class='a-spacing-mini a-size-base-plus']/text()").get()
                if title and details:
                    title = title.strip()
                    item['title'] = title
                    item['details'] = details
                    item_list.append(item)
            if not item_list:
                proxyModeUrl = "http://{}:extraHeaders=true@proxy.scrape.do:8080".format(
                    'f42a5b59aec3467e97a8794c611c436b91589634343')
                proxies = {
                    "http": proxyModeUrl,
                    "https": proxyModeUrl,
                }
                cookies = {
                    'session-id': '259-2318549-0183642',
                    'i18n-prefs': 'INR',
                    'lc-acbin': 'en_IN',
                    'ubid-acbin': '262-8705498-9430766',
                    'rxc': 'AODB517mSgTDxb0Fx+A',
                    'session-token': '0vHuy9Bq/O4rS7kb3p4ebuTjMIjsos0wzHFEMoEf7/uBnib8ntF92GFXDvEKIrfHlYUmFVaziBESNizOZJ8IJBj17/7ee4NkTj3O+TGmaAJszp2R3A3+Bd2BOrHv91iD6rgdni60GfVact1AUsR0rJZXlBqh3qWXZdHZfGpwBtFpVf0b75zeVTnNF8Pkbuz2/Od5uqB4jjsOXxdyzAl9swnVydsDRfVxgrLlO1Vj4gLdBslA70TQ/aVVQmW5ORH+oocREYT0bNC1zPUP3sgN/X4PRFXInN+8fKE6csqeZmHtFU7tcVOkIrNmtuHvGd5oC2z/EKd5DK0iUzBz3GQ4QtgrnX3CFAEx',
                    'csm-hit': 'adb:adblk_no&t:1756705700154&tb:s-S0C6R6T2DD2WKYAXANYM|1756705700153',
                    'session-id-time': '2082758401l',
                }
                headers = {
                    'accept': 'text/html; charset=utf-8',
                    'accept-language': 'en-US,en;q=0.9',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                    'viewport-width': '1600',
                    'x-requested-with': 'XMLHttpRequest',
                }
                params = {
                    'asin': product_id,
                    'showFeatures': 'inEmiPopOver-fetch,inemi',
                    'deviceType': 'desktop',
                    'experienceId': 'emiMenueSVAjaxExperience',
                    'merchantId': merchnt_id,
                }

                response = requests.get('https://www.amazon.in/gp/product/ajax', params=params, cookies=cookies,
                                        headers=headers, proxies=proxies, verify=False)
                response = Selector(response.text)
                main_dict = dict()
                for key in response.xpath('//ul//li[contains(@class, "a-tab-heading")]'):
                    keys = key.xpath('.//@data-a-tab-name').get()
                    name = key.xpath('.//span//text()').get().strip()
                    main_dict[keys] = name

                main_data = dict()
                for div_name in main_dict:
                    name_ = main_dict[div_name]
                    html_text = response.xpath(f'//div[@data-a-name="{div_name}"]').get()
                    if div_name == 'AmazonPay':
                        amazon_pay = parse_amazon_emi_html(html_text)
                        if amazon_pay:
                            main_data[name_] = amazon_pay
                    elif div_name == 'Credit':
                        credit_dict = dict()
                        html_response = Selector(html_text)
                        credit_card_list = html_response.xpath('//p[@id="inemi-bank-name"]//text()').getall()

                        for credit_data in html_response.xpath('//div[contains(@id, "dp-emi")]'):
                            plans_chk = credit_data.xpath(
                                './/div[@class="a-expander-content inemi-expander-content a-expander-section-content a-section-expander-inner"]//h4//text()').get(
                                '').strip()
                            if plans_chk == 'No Cost EMI Plans':
                                credit_name = credit_data.xpath('.//p[@id="inemi-bank-name"]//text()').get().strip()
                                processing_fees = credit_data.xpath('.//p[@id="inemi-bank-name"]//span//text()').get(
                                    'N/A')
                                credit_dict[credit_name] = dict()
                                if processing_fees != 'N/A':
                                    credit_dict[credit_name]['Processing Fee'] = processing_fees.strip()

                                for details in credit_data.xpath(
                                        './/div[@class="a-expander-content inemi-expander-content a-expander-section-content a-section-expander-inner"]'):
                                    category_list = details.xpath('.//h4//text() | .//h1//text()').getall()
                                    tables = details.xpath('.//table').getall()
                                    for category in range(len(tables)):
                                        cat = category_list[category].strip()
                                        if cat == 'No Cost EMI Plans':
                                            credit_dict[credit_name][cat] = dict()
                                            html_content = tables[category]
                                            # Parse the HTML content with BeautifulSoup
                                            soup = BeautifulSoup(html_content, 'html.parser')

                                            # Extract data from the table rows
                                            data = []
                                            rows = soup.find_all('tr', class_='inemi-installment-plan-row')
                                            for row in rows:
                                                cols = row.find_all('td')
                                                emi_plan = cols[0].get_text(strip=True)
                                                interest = cols[1].get_text(strip=True)
                                                total_cost = cols[2].get_text(strip=True)
                                                # Check if there's a 4th column (cols[3]), and combine cols[2] with cols[1] if it exists
                                                if len(cols) > 3:
                                                    discount = total_cost
                                                    total_cost = cols[3].get_text(strip=True)
                                                    data.append({'EMI Plan': emi_plan,
                                                                 'Interest(pa)': interest,
                                                                 'Discount': discount,
                                                                 'Total cost': total_cost})
                                                else:
                                                    data.append({'EMI Plan': emi_plan,
                                                                 'Interest(pa)': interest,
                                                                 'Total cost': total_cost})
                                            credit_dict[credit_name][cat] = data

                        if credit_dict:
                            main_data[name_] = credit_dict

                    elif div_name == 'Debit':
                        debit_dict = dict()
                        html_response = Selector(html_text)
                        debit_card_list = html_response.xpath('//p[@id="inemi-bank-name"]//text()').getall()

                        for debit_data in html_response.xpath('//div[contains(@id, "dp-emi")]'):
                            plans_chk = debit_data.xpath(
                                './/div[@class="a-expander-content inemi-expander-content a-expander-section-content a-section-expander-inner"]//h4//text()').get().strip()
                            if plans_chk == 'No Cost EMI Plans':
                                debit_name = debit_data.xpath('.//p[@id="inemi-bank-name"]//text()').get().strip()
                                processing_fees = debit_data.xpath('.//p[@id="inemi-bank-name"]//span//text()').get(
                                    'N/A')
                                debit_dict[debit_name] = dict()
                                if processing_fees != 'N/A':
                                    debit_dict[debit_name]['Processing Fee'] = processing_fees.strip()
                                for debit_details in debit_data.xpath(
                                        './/div[@class="a-expander-content inemi-expander-content a-expander-section-content a-section-expander-inner"]'):
                                    category_list = debit_details.xpath('.//h4//text() | .//h1//text()').getall()
                                    tables = debit_details.xpath('.//table').getall()
                                    for category in range(len(tables)):
                                        cat = category_list[category].strip()
                                        if cat == 'No Cost EMI Plans':
                                            debit_dict[debit_name][cat] = dict()
                                            html_content = tables[category]
                                            # Parse the HTML content with BeautifulSoup
                                            soup = BeautifulSoup(html_content, 'html.parser')

                                            # Extract data from the table rows
                                            data = []
                                            rows = soup.find_all('tr', class_='inemi-installment-plan-row')
                                            for row in rows:
                                                cols = row.find_all('td')
                                                emi_plan = cols[0].get_text(strip=True)
                                                interest = cols[1].get_text(strip=True)
                                                total_cost = cols[2].get_text(strip=True)
                                                # Check if there's a 4th column (cols[3]), and combine cols[2] with cols[1] if it exists
                                                if len(cols) > 3:
                                                    discount = total_cost
                                                    total_cost = cols[3].get_text(strip=True)
                                                    data.append({'EMI Plan': emi_plan,
                                                                 'Interest(pa)': interest,
                                                                 'Discount': discount,
                                                                 'Total cost': total_cost})
                                                else:
                                                    data.append({'EMI Plan': emi_plan,
                                                                 'Interest(pa)': interest,
                                                                 'Total cost': total_cost})
                                            debit_dict[debit_name][cat] = data

                        if debit_dict:
                            main_data[name_] = debit_dict

                item_list.append(main_data)
            return {'No Cost EMI': item_list}
        elif offer_type == 'InstantBankDiscount':
            for data in selector.xpath("//div[@class='a-section vsx-offers-desktop-lv__item']"):
                item = dict()
                title = re.sub("\\s+", " ", data.xpath("./h1/text()").get()).strip()
                details = data.xpath("./p[@class='a-spacing-mini a-size-base-plus']/text()").get()
                if title and details:
                    title = title.strip()
                    item['title'] = title
                    item['details'] = details
                    item_list.append(item)
            if not item_list:
                item = dict()
                details = re.sub("\\s+", " ", selector.xpath(
                    '//div[contains(@class,"a-section vsx-offers-desktop-")]//h1/text()').get('')).strip()
                item['title'] = 'Bank Offer'
                item['details'] = details
                item_list.append(item)
            return {'Bank Offer': item_list}
        elif offer_type == 'Partner':
            title = "Partner Offers"
            details = selector.xpath(
                "//div[@class='a-section vsx-offers-desktop-dv__content aok-block']//h1//text() | //div[@id='Partner-single-offer']//h1/text()").get()
            details = re.sub("\\s+", " ", details).strip()
            item = dict()
            item['title'] = title
            item['details'] = details
            return {'Partner Offers': [item]}

        return item_list
    except Exception as e:
        print(e)


def process_arrival_date(value: str):
    if 'Need a gift sooner?' == value.strip(): return None
    if value.strip():
        value = value.replace('\n', '').strip()

        if value == 'FREE Delivery':
            return None

        if value == "Today":
            return str(today_date.date()) + " 00:00:00"
        check_today = re.findall('Today\s*\d*\s*[ampmAMPM]*\s*[–|-]+\s*\d*\s*[ampmAMPM]*', value, flags=re.IGNORECASE)
        if check_today:
            return str(today_date.date()) + " 00:00:00"

        if "as soon as" in value.lower():
            value = value.replace("as soon as", "")

        if "Tomorrow" in value:
            check_val = re.findall('Tomorrow\s*\d*\s*[ampmAMPM]*\s*[–|-]+\s*\d*\s*[ampmAMPM]*', value)
            if value == 'Tomorrow' or check_val:
                return str(today_date.date() + timedelta(days=1)) + " 00:00:00"
            value = value.replace("Tomorrow", "")

        if str(datetime.now().year + 1) in value:
            value = value.split("-", 1)[-1].strip()

        if "-" in value:
            if re.findall("(\d{1,2} \w+, \d{4}) - (\d{1,2} \w+, \d{4})", value):
                pass
            elif re.findall("\d+ - \d+", value):
                value = re.sub("-\s*\d+", "", value)
        elif '–' in value:
            if re.findall("(\d{1,2} \w+, \d{4}) – (\d{1,2} \w+, \d{4})", value):
                pass
            elif re.findall("\d+ – \d+", value):
                value = re.sub("–\s*\d+", "", value)

        try:
            if '–' in value:
                arrival = (dateparser.parse(value.split("–")[0], settings={'DATE_ORDER': 'DMY'})).replace(
                    tzinfo=pytz.timezone('Asia/Calcutta'))
            else:
                arrival = (dateparser.parse(value.split("-")[0], settings={'DATE_ORDER': 'DMY'})).replace(
                    tzinfo=pytz.timezone('Asia/Calcutta'))
        except:
            arrival = (dateparser.parse(value.split("–")[0], settings={'DATE_ORDER': 'DMY'})).replace(
                tzinfo=pytz.timezone('Asia/Calcutta'))
        if arrival:
            arrival = arrival.replace(tzinfo=pytz.timezone('Asia/Calcutta'))
            diff = arrival - today_date
            if diff.days < -100:
                # Get the current year
                current_year = datetime.now().year
                # Check if the current year is a leap year
                is_leap = calendar.isleap(current_year)
                # Number of days in the current year
                days_in_year = 366 if is_leap else 365
                arrival = arrival + timedelta(days=days_in_year)
                # arrival = arrival + timedelta(days=365)

            return str(arrival.date()) + " 00:00:00"


def modifies_image_urls(images: str):
    image_list = []
    for image in images:
        if image:
            image_split = image.split('.')
            if len(image_split) > 4:
                image_url = '.'.join(image_split[:-2])
                image_data = image_url + '.' + image_split[-1]
                image_list.append(image_data)
            else:
                image_list.append(image)
    return image_list


def clean_name(value: str):
    if value.strip():
        value = (
            value.strip()
            .replace('\\', '')
            .replace('"', '\"')
            .replace("\u200c", "")
            .replace("\u200f", "")
            .replace("\u200e", "")
        )
        if "\n" in value:
            value = " ".join(value.split())
        return value


def get_cashback(response, offer_type):
    selector = Selector(text=response.text)
    cashback = selector.xpath('//div[contains(@class,"sopp-secondary-view")]//div[@class="a-row a-spacing-medium"]')
    main_offer = dict()
    offer_list = list()
    cashback_len = len(cashback)
    for index, ofer in enumerate(cashback, start=1):
        offer_dict = dict()
        offer_details = " ".join(ofer.xpath('./text()').getall())
        cashback = re.sub("\\s+", " ", offer_details).strip()
        if cashback_len != 1:
            offer_dict["title"] = f"Offer {index}"
        offer_dict["title"] = offer_type
        offer_dict["details"] = cashback
        offer_list.append(offer_dict)
    main_offer[offer_type] = offer_list
    if main_offer:
        return main_offer


def get_response(product_id):
    headers = {
        'sd-Cookie': 'session-id=259-2318549-0183642; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=262-8705498-9430766; session-token=C4/saGsP+bVjnVTFKFBOopVLIROjQE8lbvpcKo0HTlJTwfCeZooG8Qem7/wwXloeFek6aGHW1XYHQkGEOKKSaHxoiKw+XfFXAUfLRNe8qSlFWOrVv/6OtjRrQh3KYpLHgPTQ8CZf9izus9cEmayNChi1mmjdJ4o67D+ppxqN2clp3Jy8L3LyR+7siafQWJL800iD5ahcwOyViZEBusL/s2AvdMHBveBCvRK7NvdHRK8SMGwsUx68HB3kVPmc4cuJRlzdCD+EMwv/iSGRl95m4BfWCv3ntdE0K2XRZo851k+C3hOkjis4gtIjNSFYkgJpQturUpFJQw+s4OZPg7wlBtptwo8k9Sla; csm-hit=adb:adblk_no&t:1756704919451&tb:977E9NCQR8Y74DY78X4J+s-977E9NCQR8Y74DY78X4J|1756704919451; session-id-time=2082787201l; rxc=AODB517hSQTDxb0F1eA',
    }
    proxyModeUrl = "http://{}:extraHeaders=true@proxy.scrape.do:8080".format(
        'f42a5b59aec3467e97a8794c611c436b91589634343')
    proxies = {
        "http": proxyModeUrl,
        "https": proxyModeUrl,
    }

    if "http" not in product_id:
        response = requests.get(f'https://www.amazon.in/dp/{product_id}?th=1', headers=headers, proxies=proxies,
                                verify=False)
    else:
        url = f'https://www.amazon.in/dp/{product_id}?th=1'
        response = requests.request("GET", url, proxies=proxies, headers=headers, verify=False)

    return response.text


def get_offer(response, product_id):
    offeradd_list = list()
    selector = Selector(text=response)
    try:
        sr_id = selector.xpath('//div[@id="ppd"]//input[@id="hctpAttachPreATCStateData"]/@data-request-id').get('')
        merchnt_id = selector.xpath("//input[@id='merchantID']/@value").get()
        offer_list = selector.xpath("//div[contains(@id,'itembox')]/@id").getall()
        offer_lst = [i.strip() for i in offer_list if i.strip()]
        if not offer_lst:
            json_offer = selector.xpath(
                '//div[contains(@class,"sopp-offer-container")]//span[@class="a-declarative"]/@data-a-modal').getall()
            for jsn_offer in json_offer:
                jsn_offer = json.loads(jsn_offer)
                if jsn_offer:
                    url = 'https://www.amazon.in' + jsn_offer['url']
                    cookies = {
                        'session-id': '260-6343795-8869440',
                        'i18n-prefs': 'INR',
                        'lc-acbin': 'en_IN',
                        'ubid-acbin': '261-6762347-7100065',
                        'session-token': 'txHmdGi16f2PIV7rytWpmt+KFlHtqKFXy+0Nup2tAeLMiPhJkjkYea4iR9GiEeuh3kUpFXqyWfqrKo/j8suJhY1f9l+TnGQxUkXuOUzXzd7AQnF//ewxTEUcadg6BfWW5SkS1MYQr0qyikXY4bakoRKzPp4AJi2+EY01A7+3ZuihnTAEPqEbGmQRV27RVhpYPip9USh/Auah9lEmbL9mLlyZuVE1eRLl749MAYzs7SJ+TWdk3LO9gpKsORy5bbQP5UzRN9TmgIsSes72i8sZoRA/HTaT7hfW4PMhLMdhklXYvYw9GL0+XmYafL5l+eGdCOeMtGQslRqTIKo+miFWFZwDfxyeaaUl',
                        'csm-hit': 'tb:CK2A3DH0G8ZWSXQMF7T7+s-E9PVHZNSA158K9H1D1RR|1756712857825&t:1756712857826&adb:adblk_no',
                        'session-id-time': '2082787201l',
                        'rxc': 'ACjnuKxYqMb6bqxs4hQ',
                    }
                    headers = {
                        'accept': 'text/html,*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                        'viewport-width': '1600',
                        'x-requested-with': 'XMLHttpRequest',
                    }
                    offer_type = jsn_offer['header']
                    response = requests.get(url, headers=headers, cookies=cookies)
                    if response.status_code == 200:
                        other_formate = get_cashback(response, offer_type)
                        offeradd_list.append(other_formate)
            return offeradd_list
    except:
        offer_lst = ''

    if offer_lst:
        for offer_text in offer_lst:
            offer_type = offer_text.split('-')[-1]
            cookies = {
                'session-id': '525-1433283-0746461',
                'session-id-time': '2082787201l',
                'i18n-prefs': 'INR',
                'lc-acbin': 'en_IN',
                'ubid-acbin': '262-6324041-1804233',
                'session-token': 'uxKUjQq192+k3lyiiApWdKmhBtHlsTP0MIJDxlR4nRA1ipLFfgF1YPY0QfhPquA0Ddo/kKBY4GBXZ9CPHvOhOkLv148I58YOaDRZ8YseLaI8/yXyVr/SHmu8wWaQCQAciYPtFO/qdwxOcUpv+CRxtTIPYJbEeEp6NZIfC2GppiosbEssKUrMjXqsO16U5swbWcmyr/woogZWl4pqfd66Y/loOQ/29XMwMDpgYXFSXX3p5THnOnH8c7AeCKfV/rUG64r0mQV75gp5CdHzzbeem4192mUgJopLwBww3RgcTUQGrtepZZ5xOoonlwl+o1+bmiw63oC2My1MBtSA1Cxft+hlHvT7fxu3',
                'csm-hit': 'tb:VVQ3PYGGRCMY0FR1GC09+s-VVQ3PYGGRCMY0FR1GC09|1756469732490&t:1756469732490&adb:adblk_no',
                'rxc': 'AOVIvZ4Xhk6hrUfxJt8',
            }
            headers = {
                'accept': 'text/html, charset:utf-8',
                'accept-language': 'en-US,en;q=0.9',
                'device-memory': '8',
                'downlink': '3.25',
                'dpr': '0.75',
                'ect': '4g',
                'priority': 'u=1, i',
                'rtt': '100',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
                'viewport-width': '2560',
                'x-requested-with': 'XMLHttpRequest',

            }
            params = {
                'asin': product_id,
                'deviceType': 'web',
                'offerType': offer_type,
                'buyingOptionIndex': '0',
                'additionalParams': f'merchantId:{merchnt_id}',
                'smid': '',
                'encryptedMerchantId': merchnt_id,
                'sr': sr_id,
                'experienceId': 'vsxOffersSecondaryView',
                'showFeatures': 'vsxoffers',
                'featureParams': f'OfferType:{offer_type},DeviceType:web',
            }

            response = requests.get('https://www.amazon.in/gp/product/ajax', params=params, cookies=cookies,
                                    headers=headers)
            try:
                stru_offer = offer_strucute(response, product_id, offer_type, merchnt_id)
                offeradd_list.append(stru_offer)
            except:
                pass

        return offeradd_list


def otherseller_details(response, product_id):
    selector = Selector(text=response)
    qid = selector.xpath('//input[@name="qid"]/@value').get('')

    params = {
        'asin': f'{product_id}',
        'm': '',
        'qid': f'{qid}',
        'smid': '',
        'sourcecustomerorglistid': '',
        'sourcecustomerorglistitemid': '',
        'sr': '',
        'pc': 'dp',
        'experienceId': 'aodAjaxMain',
    }
    cookies = {
        'session-id': '259-5143329-0027666',
        'ubid-acbin': '260-9731439-6427404',
        'x-amz-captcha-1': '1756128546115358',
        'x-amz-captcha-2': 'csXm7MabPbyedlz773hNTg==',
        'i18n-prefs': 'INR',
        'lc-acbin': 'en_IN',
        'at-acbin': 'Atza|IwEBILDy5QLoASLqQQ4lrWVfWrNEvh0kS1IoHDNv4h1VXIcNwoZvmqp4mPwxx7cstbjdGXMZ9Xp2GVXL6HLCWuHzjNuslYy9W1xiCKojTaIufMOfiUu9_Y5rHf0yj3LMiALx2F72YcK5eiHXt6jRrDBQLxPiA4uvY5n7JA8Ce6dLmlFRMtnx17CUu-3POJuatsC16j5y_LRE6ln3dSeu4iEUxC9P1-a0tbtF5qhZYYDK_CMzhg',
        'sess-at-acbin': '"rNME1gXdFw9fWn/blAoeh07l/x4UBm7t8hqZ/IosBas="',
        'sst-acbin': 'Sst1|PQFP3-jFAjeUFffisr9NVSWwCZk8Ef2hqb7x9pRAAR37KBbR9Eynbyn4oMcrDsnKSE9YtYdFJs6oB_608-AQqjNfO8Y-iDsWLz7tR3QMoMACPRRkXUB5KXjM3esdgDDVkvaXpfTVVyRl5L9Oc1SQi4hnahMYZCuyzkxyLbH1NjN8L6IkE1AOsIc782rrqG64-DD5sgShcTHyWkC6pCLJxwAdDtqypXnHckp1xWhOzPOA4u-xkGnrm32UP7LT2TT0ObQSftwfFZSieV7GiwjL8i6e0mW78lNAH6zKZQyZBNGARd4',
        'session-id-time': '2082787201l',
        'session-token': '4v7ECqHcfGvr81tvxB+EmWmTgAkUsYIl6vdPFhTTIMgwpkXfHY1LnjfqAjnYTlZdBeOemWjpVEAhtRaxkTri0GUrRgvcJSMoZ5HrPhtn+OzuPC9d4LqZp9ytqQd3DhgChwEBC5nSDTWA8YUpSec2H+vc0QDjBXx0DvECcOcg6v5lcp2DRrwVevnfzXtOsBevHwD4vYLtEkE/En/uQl8oxdfdy/NdYJvR2/UrMF4XxJOHas1+IKDF3HH0gf78NRud9W3IacM5uzE45R7HfflSg+n6/0aSkvDouNBWTNiDiHgFJllMbQLqKwxajIUKAF/Y135QXjt0nB7xaqmZJBoqYV4K5f7oW/0RXy70q+BxtrvW9iFpMYCgUQMWBvHcsSAT',
        'x-acbin': '"6eRjHyD@GXkEjvdoDudmSULg0kITtUc5dvNkiD5IUBCuxLQB7c0JE0jcVOVmifks"',
        'csm-hit': 'tb:895B57J27XAWTCF3WQV0+s-0ZKY07HZFYFCS87R05WQ|1756466361488&t:1756466361488&adb:adblk_no',
        'rxc': 'AM843Yqw7OoUjW1jggE',
    }
    headers = {
        'accept': 'text/html,*/*',
        'accept-language': 'en-US,en;q=0.9',
        'device-memory': '8',
        'downlink': '10',
        'dpr': '1.2',
        'ect': '4g',
        'priority': 'u=1, i',
        'referer': 'https://www.amazon.in/Lenovo-IdeaPad-i5-12450H-Windows-83ER00KPIN/dp/B0DR96PF63/ref=sr_1_1_sspa?crid=GTJSK0UW0AMG&dib=eyJ2IjoiMSJ9._ll_wpnGfQfeex2LR5GADxzjPO30I3m5EbYB8Q_oNNX8j8QWWCITpcDuvIJ6asHFYHdmEIPZcRaRkHjMcgADSPvvXmBZOdFR32V2PT8Y94QgQE2e9BiV34qAi8BpKtMVdrYxI_wjm-3_iKi1HYzgg7c_inxR0kEw1gvFOJoxbfGTuK0gtz9psnbRL5bMGJPGVsUUPmvDPEI_TCA5KgY_TrgK3gXka-xS9oGyTXC9vrc.omzzqFcWBfqS0ZiP4blwNywY1Bz_NZS7QzFJDY1uNK0&dib_tag=se&keywords=laptop&qid=1756466331&sprefix=laptop%2Caps%2C234&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1',
        'rtt': '50',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.2',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-viewport-width': '1600',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'viewport-width': '1600',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'session-id=259-5143329-0027666; ubid-acbin=260-9731439-6427404; x-amz-captcha-1=1756128546115358; x-amz-captcha-2=csXm7MabPbyedlz773hNTg==; i18n-prefs=INR; lc-acbin=en_IN; at-acbin=Atza|IwEBILDy5QLoASLqQQ4lrWVfWrNEvh0kS1IoHDNv4h1VXIcNwoZvmqp4mPwxx7cstbjdGXMZ9Xp2GVXL6HLCWuHzjNuslYy9W1xiCKojTaIufMOfiUu9_Y5rHf0yj3LMiALx2F72YcK5eiHXt6jRrDBQLxPiA4uvY5n7JA8Ce6dLmlFRMtnx17CUu-3POJuatsC16j5y_LRE6ln3dSeu4iEUxC9P1-a0tbtF5qhZYYDK_CMzhg; sess-at-acbin="rNME1gXdFw9fWn/blAoeh07l/x4UBm7t8hqZ/IosBas="; sst-acbin=Sst1|PQFP3-jFAjeUFffisr9NVSWwCZk8Ef2hqb7x9pRAAR37KBbR9Eynbyn4oMcrDsnKSE9YtYdFJs6oB_608-AQqjNfO8Y-iDsWLz7tR3QMoMACPRRkXUB5KXjM3esdgDDVkvaXpfTVVyRl5L9Oc1SQi4hnahMYZCuyzkxyLbH1NjN8L6IkE1AOsIc782rrqG64-DD5sgShcTHyWkC6pCLJxwAdDtqypXnHckp1xWhOzPOA4u-xkGnrm32UP7LT2TT0ObQSftwfFZSieV7GiwjL8i6e0mW78lNAH6zKZQyZBNGARd4; session-id-time=2082787201l; session-token=4v7ECqHcfGvr81tvxB+EmWmTgAkUsYIl6vdPFhTTIMgwpkXfHY1LnjfqAjnYTlZdBeOemWjpVEAhtRaxkTri0GUrRgvcJSMoZ5HrPhtn+OzuPC9d4LqZp9ytqQd3DhgChwEBC5nSDTWA8YUpSec2H+vc0QDjBXx0DvECcOcg6v5lcp2DRrwVevnfzXtOsBevHwD4vYLtEkE/En/uQl8oxdfdy/NdYJvR2/UrMF4XxJOHas1+IKDF3HH0gf78NRud9W3IacM5uzE45R7HfflSg+n6/0aSkvDouNBWTNiDiHgFJllMbQLqKwxajIUKAF/Y135QXjt0nB7xaqmZJBoqYV4K5f7oW/0RXy70q+BxtrvW9iFpMYCgUQMWBvHcsSAT; x-acbin="6eRjHyD@GXkEjvdoDudmSULg0kITtUc5dvNkiD5IUBCuxLQB7c0JE0jcVOVmifks"; csm-hit=tb:895B57J27XAWTCF3WQV0+s-0ZKY07HZFYFCS87R05WQ|1756466361488&t:1756466361488&adb:adblk_no; rxc=AM843Yqw7OoUjW1jggE',
    }

    seller_response = requests.get(
        'https://www.amazon.in/gp/product/ajax/aodAjaxMain/ref=dp_aod_NEW_mbc',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    other_seller = list()
    response = Selector(seller_response.text)
    ranking = 0
    try:
        for sd in response.xpath('//div[@id="aod-offer"] | //div[@id="aod-pinned-offer"]'):
            seller_detail = dict()
            rating = sd.xpath('.//span[@id="seller-rating-count-{iter}"]//text()').getall()
            try:
                count_rating = re.findall('\((\d+)\s*rating', " ".join(rating).strip())[0]
                count_rating = int(count_rating)
            except:
                count_rating = 'N/A'

            try:
                mrp = clear_price(
                    sd.xpath('.//*[contains(text(),"M.R.P.")]//span[@class="a-offscreen"]/text()').get('').strip())
            except:
                mrp = "N/A"

            try:
                price = clear_price("".join(sd.xpath(
                    './/span[contains(@id,"aod-price")]//span[contains(@class,"a-price aok-align-center")]/span[@class="a-offscreen"]/following-sibling::span//text()').getall()).strip())
            except:
                price = 'N/A'

            try:
                if isinstance(price, str):
                    price = float(price)
            except:
                pass

            discount = ''
            try:
                if isinstance(mrp, str):
                    mrp = float(mrp)
                if not mrp:
                    mrp = price
                if price and mrp > price:
                    discount = round((1 - (price / mrp)) * 100)
                else:
                    discount = 'N/A'
            except Exception as e:
                print(e)

            details = sd.xpath('.//span[@id="seller-rating-count-{iter}"]/span/br/following-sibling::text()').get(
                '').strip()
            delivery_date = process_arrival_date(
                sd.xpath('.//div[contains(@class,"aod-delivery-promise")]//span/@data-csa-c-delivery-time').get(
                    '').strip())

            try:
                avg_rating = sd.xpath('.//div[@id="aod-offer-seller-rating"]/i/span/text()').get('').strip()
                match = re.search(r"(?<=Seller rating is )\d+(?:\.\d+)?(?= out of 5 stars)", avg_rating)
                if match:
                    avg_rating = match.group()
                    if isinstance(avg_rating, str):
                        seller_detail['avg_rating'] = float(avg_rating)
                else:
                    seller_detail['avg_rating'] = 'N/A'
            except:
                seller_detail['avg_rating'] = 'N/A'

            try:
                if details:
                    seller_detail['details'] = details
                else:
                    seller_detail['details'] = 'N/A'
            except:
                seller_detail['details'] = "N/A"

            seller_detail['mrp'] = mrp

            if delivery_date:
                seller_detail['arrival_date'] = delivery_date
            else:
                seller_detail['arrival_date'] = 'N/A'
            seller_detail['price'] = price
            seller_detail['discount'] = discount
            seller_detail['rating'] = count_rating

            try:
                key = sd.xpath(
                    './/div[contains(@id,"aod-offer-shipsFrom")]//span[contains(@class,"a-color-tertiary")]/text()').get()
                value = sd.xpath(
                    './/div[contains(@id,"aod-offer-shipsFrom")]//span[contains(@class,"a-color-base")]/text()').get()
                seller_detail[key.strip()] = value.strip()
            except:
                pass

            attri_key = sd.xpath(
                './/div[@id="aod-offer-soldBy"]//span[contains(@class,"a-color-tertiary")]/text()').get()
            attri_value = sd.xpath('.//div[@id="aod-offer-soldBy"]//span[contains(@class,"a-color-base")]/text()').get(
                '').strip()
            if not attri_value:
                attri_value = sd.xpath('.//div[contains(@id,"aod-offer-s")]//a/text()').get('').strip()
            if attri_key and attri_value:
                if attri_key == 'Sold by':
                    seller_link = sd.xpath('.//div[contains(@id,"aod-offer-s")]//a/@href').get()
                    if seller_link:
                        if 'http' not in seller_link:
                            seller_link = f'https://www.amazon.in{seller_link}'
                        seller_detail['Seller_link'] = seller_link
                seller_detail[attri_key] = attri_value
                ranking = ranking + 1
                seller_detail['ranking'] = ranking
                other_seller.append(seller_detail)
        return other_seller
    except Exception as e:
        print(e)


def set_item(item):
    new_item = dict()
    other_data = json.loads(item['others'])
    try:
        new_item['Product ID'] = item['catalog_id']
    except:
        new_item['Product ID'] = "N/A"

    # try:
    #     new_item['Keyword'] = 'N/A'
    # except:
    #     new_item['Keyword'] = "N/A"

    # try:
    #     new_item['Category Name'] = json.loads(item['category_hierarchy'])['l2']
    # except:
    #     new_item['Category Name'] = "N/A"

    # try:
    #     new_item['Sub Category Name'] = json.loads(item['category_hierarchy'])['l3']
    # except:
    #     new_item['Sub Category Name'] = "N/A"

    try:
        new_item['Seller Name'] = other_data['seller_detail']['Sold by']
    except:
        new_item['Seller Name'] = "N/A"

    try:
        new_item['Platform'] = "Amazon"
    except:
        new_item['Platform'] = "N/A"

    try:
        new_item['SKU'] = item['catalog_id']
    except:
        new_item['SKU'] = "N/A"

    try:
        new_item['Brand Name'] = other_data['brand']
    except:
        new_item['Brand Name'] = 'N/A'

    try:
        new_item['Link'] = item['product_url']
    except:
        new_item['Link'] = 'N/A'

    try:
        new_item['Pincode'] = item['zip_code']
    except:
        new_item['Pincode'] = "N/A"

    try:
        category_data = json.loads(item['category_hierarchy'])
        category_path = ''
        category_list = []
        try:
            for category in category_data.values():
                category_list.append(category.strip())
            category_path = " > ".join(category_list)
        except:
            pass
        new_item['Category Path'] = category_path
    except:
        new_item['Category Path'] = "N/A"

    try:
        # date_time = item['arrival_date']
        new_item['Date & Time of Crawling'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    except:
        new_item['Date & Time of Crawling'] = "N/A"

    try:
        for key_name in ['product_detail', 'product_attributes', 'product_specification']:
            model_name = 'N/A'
            if key_name in other_data:
                if 'Item model number' in other_data[key_name] or 'Model' in other_data[key_name]:
                    try:
                        model_name = other_data[key_name]['Item model number']
                    except:
                        model_name = other_data[key_name]['Model']
                    break

        new_item['Model Name/Number'] = model_name
    except:
        new_item['Model Name/Number'] = "N/A"

    try:
        new_item['Image URL'] = other_data['images'][0]
    except:
        new_item['Image URL'] = "N/A"

    try:
        new_item['Product Name'] = item['product_name']
    except:
        new_item['product_name'] = "N/A"

    try:
        new_item['Rating'] = float(item['avg_rating'])
    except:
        new_item['Rating'] = "N/A"

    try:
        new_item['No of Ratings'] = int(item['number_of_ratings'])
    except:
        new_item['No of Ratings'] = "N/A"

    try:
        new_item['5 Star'] = other_data['individualRatingsCount']['5']
    except:
        new_item['5 Star'] = "N/A"
    try:
        new_item['4 Star'] = other_data['individualRatingsCount']['4']
    except:
        new_item['4 Star'] = "N/A"
    try:
        new_item['3 Star'] = other_data['individualRatingsCount']['3']
    except:
        new_item['3 Star'] = "N/A"
    try:
        new_item['2 Star'] = other_data['individualRatingsCount']['2']
    except:
        new_item['2 Star'] = "N/A"
    try:
        new_item['1 Star'] = other_data['individualRatingsCount']['1']
    except:
        new_item['1 Star'] = "N/A"

    number_of_ratings = item['number_of_ratings']
    if number_of_ratings and number_of_ratings != 'N/A':
        review_rating_count_dict = other_data['individualRatingsCount']
        rating_counts = {key: round((int(value) / 100) * int(number_of_ratings)) for key, value in
                         review_rating_count_dict.items()}
        try:
            new_item['5 Star'] = int(rating_counts['5'])
            new_item['4 Star'] = int(rating_counts['4'])
            new_item['3 Star'] = int(rating_counts['3'])
            new_item['2 Star'] = int(rating_counts['2'])
            new_item['1 Star'] = int(rating_counts['1'])
        except:
            new_item['5 Star'] = "N/A"
            new_item['4 Star'] = "N/A"
            new_item['3 Star'] = "N/A"
            new_item['2 Star'] = "N/A"
            new_item['1 Star'] = "N/A"
    else:
        new_item['5 Star'] = "N/A"
        new_item['4 Star'] = "N/A"
        new_item['3 Star'] = "N/A"
        new_item['2 Star'] = "N/A"
        new_item['1 Star'] = "N/A"

    try:
        new_item['Coupon'] = other_data['coupon']
    except:
        new_item['Coupon'] = "N/A"

    try:
        new_item['Promotions'] = "N/A"
    except:
        new_item['Promotions'] = "N/A"

    try:
        new_item['Bestseller'] = other_data['best_seller_badge']
        if other_data['best_seller_badge']['is_badge_available'] == True:
            new_item['Bestseller'] = True
        else:
            new_item['Bestseller'] = False
    except:
        new_item['Bestseller'] = False

    try:
        if item['is_sold_out'] == 'false':
            new_item['Stock'] = "Available"
        else:
            new_item['Stock'] = "Not Available"
    except:
        new_item['Stock'] = "Not Available"

    try:
        new_item['Delivery Date'] = item['arrival_date'] if item['arrival_date'] else item['arrival_date']
    except:
        new_item['Delivery Date'] = "N/A"

    if item['check_date']:
        # new_item['Min delivery days'] = item['arrival_date']
        new_item['Min delivery days'] = item['min_arraival'] if item['min_arraival'] else "N/A"
        date_obj = datetime.strptime(item['arrival_date'], "%Y-%m-%d %H:%M:%S")
        next_day = date_obj + timedelta(days=1)
        next_day_str = next_day.strftime("%Y-%m-%d %H:%M:%S")
        new_item['Max delivery days'] = item['max_arraival'] if item['max_arraival'] else "N/A"
    else:
        try:
            new_item['Min delivery days'] = item['arrival_date']
        except:
            new_item['Min delivery days'] = "N/A"

        try:
            new_item['Max delivery days'] = item['arrival_date']
        except:
            new_item['Max delivery days'] = "N/A"

    try:
        new_item['MRP'] = item['mrp'] if item['mrp'] else "N/A"
    except:
        new_item['MRP'] = "N/A"
    try:
        new_item['Offer Price'] = item['product_price'] if item['product_price'] else "N/A"
    except:
        new_item['Offer Price'] = "N/A"
    try:
        new_item['Max Operating Price'] = new_item['MRP']
    except:
        new_item['Max Operating Price'] = "N/A"
    try:
        new_item['Discount%'] = item['discount'] if item['discount'] else "N/A"
    except:
        new_item['Discount%'] = "N/A"

    new_item['Others'] = json.loads(item['others'])
    return new_item


def parse(product_id, response_content, login_status=0):
    # PAGE_SAVE_PATH = 'D:/amazon/'
    PAGE_SAVE_PATH = 'E:/Nirav/Project_page_save/amazon_api'
    response = Selector(response_content)
    item = dict()

    post_code_value_list = response.xpath(
        '//*[@id="nav-global-location-slot"]//span[@id="glow-ingress-line2" and not(contains(text(), "Select your address"))]//text()'
    ).getall()
    post_code_value = [post_code.strip() for post_code in post_code_value_list if post_code.strip()]
    post_code_value = "".join(post_code_value).replace("\u200c", "")
    digits = re.findall(r'\d+', post_code_value)
    post_code_value = ''.join(digits)
    item['zip_code'] = post_code_value

    final_page_path = f"{PAGE_SAVE_PATH}/{post_code_value}"

    if 'http' in product_id:
        product_id = product_id.split("/dp/")[-1]

    if not os.path.exists(final_page_path):
        os.makedirs(final_page_path)
    open(f"{final_page_path}/{product_id}.html", "w", encoding='utf-8').write(response_content)

    # loader.add_value('is_zip', 1)
    item['is_zip'] = 1
    item['zip_code'] = post_code_value

    item['product_url'] = f'https://www.amazon.in/dp/{product_id}'
    # PRODUCT NAME

    # Todo : catalog_name
    try:
        item['catalog_name'] = "".join(
            [i.strip() for i in response.xpath('//h1[@id="title"]//text()').getall()]).strip()
        if not item['catalog_name']:
            response.xpath('//span[@id="productTitle"]//text()').get('').strip()
    except:
        item['catalog_name'] = "N/A"

    item['catalog_id'] = product_id

    # PRODUCT PRICE
    try:
        decimal_price = response.xpath(
            '//div[@data-feature-name="corePriceDisplay_desktop" and @data-csa-c-slot-id="newAccordionRow_0"]//span[contains(@class, "apexPriceToPay") or contains(@class, "PriceToPay") or @id="priceblock_ourprice"]//text()').getall()
        if decimal_price:
            decimal_price = ''.join(decimal_price).replace('\n', '').replace('\r', '').replace('\t', '').strip()
        if not decimal_price:
            decimal_price = response.xpath(
                '//div[@id="desktop_qualifiedBuyBox"]//div[@data-feature-name="corePriceDisplay_desktop"]//span[contains(@class, "apexPriceToPay") or contains(@class, "PriceToPay") or @id="priceblock_ourprice"]//text()').getall()
        if decimal_price:
            decimal_price = ''.join(decimal_price).replace('\n', '').replace('\r', '').replace('\t', '').strip()
            if decimal_price:
                item['product_price'] = clear_price(decimal_price)

        decimal_price = response.xpath(
            '//div[@class="a-box a-last"]//div[@class="a-box-inner"]//*[contains(text(), "Add to Cart")]/ancestor::div[@class="a-box-inner"]//div[@class="a-section"]/span/span[@class="a-offscreen"]/text()').getall()
        decimal_price = "".join(decimal_price)
        if not decimal_price:
            decimal_price = response.xpath(
                '//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//span[@class="a-price-whole"]/text()').get()
            if decimal_price:
                decimal_price = decimal_price.replace(',', '')
        item['product_price'] = clear_price(decimal_price)

        # ---------

        if not decimal_price:
            decimal_price = response.xpath(
                '//div[@data-feature-name="corePrice"]//span[@class="a-offscreen"]/text()').get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath(
                "//*[@data-a-color='price' and @id='tp-tool-tip-subtotal-price-value']//*[@class='a-offscreen']/text()").get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath(
                '//div[@data-feature-name="corePrice_desktop" or @data-feature-name="corePriceDisplay_desktop"]//span[contains(@class, "apexPriceToPay") or contains(@class, "PriceToPay") or @id="priceblock_ourprice"]//text()').get()

            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath('//*[@data-a-color="price"]//*[@class="a-offscreen"]/text()').get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath(
                '//div[@id="corePrice_desktop"]//td[contains(text(), "Price")]/following-sibling::td/span[@id="priceblock_ourprice"]/span'
            )
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath(
                '//*[@class="a-size-base a-color-price" and not (preceding-sibling::span[contains(text(), "New") and contains(text(), "from")])]/text()').get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath('//*[@id="price"]/text()').get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath('//*[@id="kindle-price"]/text()').get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath('//*[@id="kindle-price"]/text()').get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath(
                '//*[@class="a-color-base" and contains(text(), "from") and not(@role="article") and not (ancestor::div[@id="productFactsDesktop_feature_div"])]/following-sibling::span[@class="a-price"]/span[@class="a-offscreen"]/text()'
            )
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath('//input[@name="priceValue"]/@value').get()
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            decimal_price = response.xpath(
                '//div[@id="Northstar-Buybox"]//div[@id="tmmSwatches"]//div[contains(@class,"swatchElement selected")]//span[@class="slot-price"]//text()')
            item['product_price'] = clear_price(decimal_price)

        if not decimal_price:
            item['product_price'] = '0.0'
    except:
        item['product_price'] = "N/A"

    # MRP
    try:
        mrp = response.xpath(
            '//div[@data-feature-name="corePrice_desktop" or @data-feature-name="corePriceDisplay_desktop"]//span[contains(@class, "priceBlockStrikePriceString") or @data-a-strike="true"]//text()'
        ).get()

        if mrp:
            item['mrp'] = clear_price(mrp)

        if not mrp:
            mrp = response.xpath(
                '//div[@id="ppd"]//*[contains(text(), "M.R.P.:")]/..//span[@aria-hidden="true" or @id="listPrice"]/text()'
            ).get()
            item['mrp'] = clear_price(mrp)

        if not mrp:
            mrp = response.xpath(
                '//div[@id="ppd"]//*[@data-a-color="secondary"]//*[@class="a-offscreen"]/text()').get()
            item['mrp'] = clear_price(mrp)

        if not mrp:
            mrp = response.xpath(
                '//div[@id="corePrice_desktop"]//span[contains(@class, "priceBlockStrikePriceString")]//text()'
            ).get()
            item['mrp'] = clear_price(mrp)

        # 29052024
        if not mrp:
            mrp = response.xpath('//div[@id="buybox"]//td[@id="basis-price"]/text()').get()
            item['mrp'] = clear_price(mrp)

        if not mrp:
            mrp = response.xpath('//div[@id="desktop_qualifiedBuyBox"]//span[@id="listPrice"]/text()').get()
            item['mrp'] = clear_price(mrp)

        if not mrp:
            item['mrp'] = "0.0"
    except:
        item['mrp'] = "0.0"

    # CATEGORY HIERARCHY
    try:
        hierarchy_text = " ".join(
            response.xpath('//div[@class="a-subheader a-breadcrumb feature"]//li//text()').getall())
        category_hierarchy = {
            f'l{index}': cat
            for index, cat in enumerate([cat.strip() for cat in hierarchy_text.split('›') if cat.strip()], start=1)
        }
        category_hierarchy = json.dumps(category_hierarchy)

        item['category_hierarchy'] = category_hierarchy
    except:
        item['category_hierarchy'] = "N/A"

    # SHIPPING CHARGES
    try:
        shipping_charges = response.xpath(
            '//*[@id="mir-layout-DELIVERY_BLOCK-slot-DELIVERY_MESSAGE"]//a[contains(text(), "delivery")]/text()').get()

        if not shipping_charges:
            shipping_charges = response.xpath("//*[@data-csa-c-delivery-price]/@data-csa-c-delivery-price").get()
            item['shipping_charges'] = shipping_charges

        if not shipping_charges:
            shipping_charges = response.xpath('//*[@data-csa-c-delivery-price]/@data-csa-c-delivery-price').get()
            item['shipping_charges'] = shipping_charges

        if not shipping_charges:
            response.xpath('//div[@id="deliveryBlockMessage"]//div[contains(text(), "delivery")]/text()').get()
            item['shipping_charges'] = shipping_charges
    except:
        item['shipping_charges'] = "N/A"

    # IMAGE_URLS
    try:
        image_list = list()
        videos_list = list()
        image_json = re.findall("jQuery.parseJSON\(\'(.*?)\'\);", response_content)
        image_json2 = response.xpath('//script[contains(text(),"ImageBlockATF")]//text()').get()

        if image_json:
            image_dict = list()
            try:
                image_json = json.loads(image_json[0])
            except:
                image_json = json.loads(image_json[0].replace(b'\\\'', b''))
            if 'colorToAsin' in image_json:
                asin = re.findall(r',&quot;url&quot;:&quot;https://www.amazon.in/dp/(.*?)&quot;,&quot;',
                                  response_content)
                asin = asin[0].split('?')[0]
                for key in image_json['colorToAsin']:
                    if asin in image_json['colorToAsin'][key]['asin'] and key in image_json[
                        'colorImages']:
                        image_dict = image_json['colorImages'][key]
                        break

            for img in image_dict:

                hiRes = img.get('hiRes')
                large = img.get('large')
                thumb = img.get('thumb')

                if hiRes:
                    image_list.append(hiRes)
                elif large:
                    image_list.append(large)
                elif thumb:
                    image_list.append(thumb)
            try:
                vid_ls = image_json['videos']
            except:
                vid_ls = []

            if vid_ls:
                for vurl in vid_ls:
                    vid_link = vurl.get('url')
                    if vid_link:
                        videos_list.append(vid_link)
        if image_json2 and not image_list:
            try:
                # image_json2=image_json2.split('var data =')[1].split("'colorToAsin")[0].replace('\\n','').replace('\\t','').replace('\\r','').strip().replace("'colorImages'",'"colorImages"').replace("'initial'",'"initial"')
                image_json2 = image_json2.split("{ 'initial':")[1].split("'colorToAsin")[0].replace('\\n',
                                                                                                    '').replace(
                    '\\t', '').replace('\\r', '').strip()
                if image_json2.endswith('},'):
                    image_json2 = image_json2[:-2]
                # forimg=json.loads(image_json2)

                image_list_d = json.loads(image_json2)

                for img in image_list_d:
                    hiRes = img.get('hiRes')
                    large = img.get('large')
                    thumb = img.get('thumb')

                    if hiRes:
                        image_list.append(hiRes)
                    elif large:
                        image_list.append(large)
                    elif thumb:
                        image_list.append(thumb)
            except:
                ...

        if image_list:
            # loader.add_value('image_url', image_list[0])
            item['image_url'] = image_list[0]
        else:
            item['image_url'] = response.xpath(
                '//*[@class="imgTagWrapper"]/img/@src|//*[@class="image-wrapper"]/img/@src').get()

            if not item['image_url']:
                item['image_url'] = response.xpath(
                    '//*[@id="ebooks-img-canvas"]//img[@id="ebooksImgBlkFront"]/@src|//*[@id="img-wrapper"]//img/@src').get()
    except:
        item['image_url'] = "N/A"

    # AVERAGE RATINGS
    try:
        item['avg_rating'] = response.xpath('normalize-space(//*[@id="acrPopover"]/@title)').re_first(
            r'(.*)out of 5 stars').strip()
        number_of_ratings = response.xpath('//*[@id="acrCustomerReviewText"]/text()').get('')
        if 'K' in number_of_ratings:
            number_of_ratings = str(
                int(float(number_of_ratings.replace('K', '').replace('(', '').replace(')', '')) * 1000))
    except:
        item['avg_rating'] = "N/A"

    try:
        item['number_of_ratings'] = clear_price(number_of_ratings)
    except:
        item['number_of_ratings'] = "N/A"

    # ARRIVAL DATE
    try:
        item['arrival_date'] = response.xpath(
            '//div[contains(@id,"DeliveryMessage_feature_div")]//span[@class="a-size-base a-color-secondary a-text-normal"]/span/text()').get()
        if not item['arrival_date']:
            item['arrival_date'] = response.xpath('//*[@id="mir-layout-DELIVERY_BLOCK"]//b/text()').get()
        if not item['arrival_date']:
            item['arrival_date'] = response.xpath(
                '//*[@id="mir-layout-DELIVERY_BLOCK"]//@data-csa-c-delivery-time').get()

        if not item['arrival_date']:
            item['arrival_date'] = response.xpath(
                '//div[@data-csa-c-content-id="almLogoAndDeliveryMessage"]//span[@class="a-color-base a-text-bold"]/text()').get()

        # if not item['arrival_date']:
        #     item['arrival_date'] = response.xpath(
        #         '//div[contains(@id,"DeliveryMessage_feature_div")]//span[@class="a-size-base a-color-secondary a-text-normal"]/span/text()').get()
    except:
        item['arrival_date'] = "N/A"

    # SOLD OUT
    # loader.add_value('is_sold_out', 'false')
    item['is_sold_out'] = 'false'

    unqualified_buy_box = response.xpath('//*[@id="unqualifiedBuyBox"]').getall()
    particle_buy_box = response.xpath('//div[@id="partialStateBuybox"]').getall()

    if 'To buy, select' in ' '.join(particle_buy_box).strip():
        pass
    elif unqualified_buy_box:
        item['is_sold_out'] = 'true'
    else:
        buy_box_msg = response.xpath('//div[@id="outOfStock" and @class="a-box"]').get()
        if buy_box_msg and (
                'Currently unavailable' in buy_box_msg
                or 'Temporarily out of stock' in buy_box_msg
        ):
            item['is_sold_out'] = 'true'
        else:
            stock_detail = set(
                [
                    word
                    for text in response.xpath('//*[@id="availability"]//text()').getall()
                    for word in text.lower()
                .strip()
                .strip(".")
                .replace("in stock", "in-stock")
                .split()
                ]
            )
            if stock_detail and not {'in-stock', 'only', 'dispatched', 'available'} & stock_detail:
                item['is_sold_out'] = 'true'

    pincode_not_delivery = response.xpath('//div[@id="deliveryBlockMessage"]//span[@class="a-color-error"]/text()').get(
        '')
    if 'This item cannot be shipped to your selected delivery location. Please choose a different delivery location.' in pincode_not_delivery.strip():
        item['is_sold_out'] = 'true'
    if 'product_price' not in item:
        try:
            pricing_json = json.loads(response.xpath("//script[contains(text(), 'Update cart')]//text()").get())
            pricing_json = json.loads(pricing_json['qsItems'][0]['data'])
            item['product_price'] = pricing_json['price']
        except:
            item['product_price'] = ''

    # CALCULATING THE DISCOUNTED PERCENTAGE
    try:
        if not item['mrp']:
            item['mrp'] = str(item['product_price'])
        else:
            if not item['product_price']:
                if item['mrp']:
                    item['mrp'] = str(item['product_price'])
    except:
        item['mrp'] = ''

    # CALCULATING THE DISCOUNTED PERCENTAGE
    try:
        item['product_price'] = float(item['product_price'])
    except:
        item['product_price'] = ''

    try:
        item['mrp'] = float(item['mrp'])
    except:
        item['mrp'] = ''

    try:
        if item['product_price'] and item['mrp'] > item['product_price']:
            item['discount'] = round((1 - (item['product_price'] / item['mrp'])) * 100)
        else:
            item['discount'] = "N/A"
    except:
        item['discount'] = "N/A"
    # RECALCULATING THE SHIPPING CHARGES
    try:
        if (
                "if you spend ₹499 on items shipped by amazon" in response_content.lower()
        ):
            item['shipping_charges'] = "40.0"
        else:
            item['shipping_charges'] = "0.0"

        if 'catalog_name' not in item:
            return None
    except:
        item['shipping_charges'] = "N/A"

    item['product_name'] = item.get('catalog_name')
    item['product_id'] = item.get('catalog_id')

    # GENERATING THE OTHER JSON FILED
    other_data = dict()

    try:
        if response.xpath('//span[@class="author notFaded"]//a/following-sibling::span'):
            Author_name = response.xpath('//span[@class="author notFaded"]//a/text()').getall()
            if Author_name:
                other_data['Author'] = " | ".join(Author_name).strip()
    except:
        pass

    moq = response.xpath('//*[@name="items[0.base][quantity]"]/@value').get()
    if moq:
        other_data['MOQ'] = moq
    else:
        other_data['MOQ'] = '1'

    try:
        coupon_list = list()
        coupons = response.xpath("//div[@data-csa-c-coupon]//*[contains(@id, 'couponText')]/text()").getall()
        if coupons:
            coupons = ", ".join([i.strip() for i in coupons.getall() if i.strip() and '|' not in i])
            coupon_list.append(coupons)

        coupons = response.xpath(
            '//div[@id="apex_desktop_newAccordionRow"]//div[@id="promoPriceBlockMessage_feature_div"]//div[@id="reinvent_price_desktop_newAccordionRow"]//*[contains(@id, "couponText")]/text()')
        coupons1 = response.xpath(
            '//div[@id="promoPriceBlockMessage_feature_div"]//span[contains(@id, "couponText")]/text()').getall()
        if coupons or coupons1:
            clean_coup = list()
            [clean_coup.append(i.strip()) for i in coupons.getall() if
             i.strip() and '|' not in i and i.strip() not in clean_coup]
            coupons = " ".join(clean_coup)
            if coupons:
                coupon_list.append(coupons)
            else:
                coupon_list.extend(coupons1)
        elif not coupons and coupons1:
            coupons = ", ".join([i.strip() for i in coupons1.getall() if i.strip() and '|' not in i])
            coupon_list.append(coupons)
        if not coupons and not coupons1 and login_status:
            coupons = response.xpath(
                '//div[@id="promoPriceBlockMessage_feature_div"]//*[contains(@id, "couponText")]/text()').get(
                '').strip()
        if coupons:
            if len(coupon_list) == 1:
                if ',' in coupon_list[0]:
                    compre_coupon = coupon_list[0].split(',')[0]
                    compre_coupon2 = coupon_list[0].split(',')[1]
                    if compre_coupon.strip() == compre_coupon2.strip():
                        coupon_list.pop()
                        coupon_list.append(compre_coupon)
                elif len(coupon_list) == 1:
                    compre_coupon = coupon_list[0].split(',')[0]
                    if compre_coupon.strip() == coupons.strip():
                        coupon_list.pop()
                        coupon_list.append(coupons)
                else:
                    coupon_list.append(coupons)
            else:
                coupon_list.append(coupons)
        if coupon_list:
            coupon_lst = [coupon.replace("|", "").strip() for coupon in coupon_list if coupon.strip()]
            other_data['coupon'] = ", ".join(coupon_lst).replace(",", "").strip()
    except:
        pass
    try:
        qty_discount_list = list()
        quantity_discount = response.xpath(
            '//div[@id="bmsmMessaging"]//*[@data-csa-c-owner="PromotionsDiscovery"]//span//text()').getall()
        if quantity_discount:
            qty_discount = ", ".join([i.strip() for i in quantity_discount.getall() if i.strip()])
            qty_discount_list.append(qty_discount)
        if qty_discount_list: other_data['quantity_discount'] = ", ".join(qty_discount_list)
    except:
        pass

    try:
        if image_list:
            other_data['images'] = image_list
        else:
            images = response.xpath('//*[@id="altImages"]//img/@src').getall()
            images = modifies_image_urls(images)
            if images:
                other_data['images'] = images
    except:
        pass

    try:
        if videos_list:
            other_data['videos'] = videos_list
    except:
        pass

    product_specs = dict()
    # Todo:PRODUCT SPECIFICATION OR PRODUCT TECHNICAL SPECIFICATION'
    try:
        # for row in response.xpath(('//*[@id="technicalSpecifications_section_1" or  @id="productDetails_techSpec_section_1" or  @id="productDetails_detailBullets_sections1" or @id="productDetails_db_sections" or @id="technicalSpecifications_section_2" or @id="audibleProductDetails"]//tr')):
        for row in response.xpath((
                '//*[@id="technicalSpecifications_section_1" or  @id="productDetails_techSpec_section_1" or  @id="productDetails_detailBullets_sections1" or @id="productDetails_db_sections" or @id="technicalSpecifications_section_2" or @id="audibleProductDetails" or @id="technicalSpecifications_section_3" or @id="technicalSpecifications_section_4"]//tr')):
            # tmp_loader = ItemLoader(selector=row)
            key = row.xpath('.//th/text()').get()
            key = clean_name(key)
            value = row.xpath('.//td/text()').get()
            value = clean_name(value)

            if not key and not value:
                key = row.xpath('.//th//text()').get()
                value = row.xpath('.//td//text()').get()
            if key and value:
                product_specs[key] = value

            if key:
                if 'Best Sellers Rank' in key:
                    value = row.xpath('.//td//text()').getall()
                    if key and value:
                        value1 = [i for i in value if i.strip()]
                        product_specs[key] = re.sub(r'\s+', ' ', ' '.join(value1).strip())
        if not product_specs:
            for row in response.xpath('//div[@id="prodDetails"]//tr'):
                # tmp_loads = ItemLoader(selector=row)
                key = row.xpath('.//th/text()').get()
                key = clean_name(key)
                value = row.xpath('.//td/text()').get()
                value = clean_name(value)

                if not key and not value:
                    key = row.xpath('.//th//text()').get()
                    key = clean_name(key)
                    value = row.xpath('.//td//text()').get()
                    value = clean_name(value)
                if key and value:
                    product_specs[key] = value
                if key:
                    if 'Best Sellers Rank' in key:
                        value = row.xpath('.//td//text()').getall()
                        if key and value:
                            value1 = [i for i in value if i.strip()]
                            product_specs[key] = re.sub(r'\s+', ' ', ' '.join(value1).strip())

        if product_specs:
            if 'Customer Reviews' in product_specs:
                del product_specs['Customer Reviews']

            other_data['product_specification'] = product_specs
            if 'Brand' in other_data['product_specification']:
                other_data['brand'] = other_data['product_specification']['Brand']
    except:
        pass

    # ABOUT THIS ITEM
    try:
        about_this_item = list()
        li_list = response.xpath('//*[contains(text(),"About this item")]//parent::div[@id="feature-bullets"]//li')
        if not li_list:
            li_list = response.xpath('//*[contains(text(),"About this item")]//parent::div//li')
        if not li_list:
            li_list = response.xpath('//div[@id="feature-bullets"]//li')
        for li in li_list:
            li_text = li.xpath(".//text()").get('').strip()
            if li_text:
                about_this_item.append(li_text)
        if about_this_item:
            other_data['about_this_item'] = about_this_item
    except:
        pass

    # PRODUCT ATTRIBUTE
    try:
        product_attributes = dict()
        if response.xpath('//div[@id="inline-twister-dim-title-style_name"]'):
            key = response.xpath(
                '//div[@id="inline-twister-dim-title-style_name"]//span[contains(@class,"a-color-secondary")]//text()').get(
                '').strip()
            value = response.xpath(
                '//div[@id="inline-twister-dim-title-style_name"]//span[contains(@id,"dimension-text-style_name")]//text()').get(
                '').strip()
            if key and value:
                product_attributes[key] = value
        if response.xpath('//div[contains(@id,"header-pattern_name")]'):
            key1 = response.xpath(
                '//div[contains(@id,"header-pattern_name")]/span[contains(@class,"a-color-secondary")]//text()').get(
                '').strip()
            value1 = response.xpath(
                '//div[contains(@id,"header-pattern_name")]//span[contains(@id,"dimension-text-style_name")]//text()').get(
                '').strip()
            if key1 and value1:
                product_attributes[key1] = value1

        attr_xpath = response.xpath('//div[@id="productFactsDesktop_feature_div"]'
                                    '//div[@class="a-fixed-left-grid product-facts-detail"]')
        if not attr_xpath:
            attr_xpath = response.xpath('//div[@id="productOverview_feature_div"]//tr')
        for attr in attr_xpath:
            attr1 = [i.strip() for i in attr.xpath(".//text()").getall() if i.strip()]
            if attr1 and len(attr1) == 2:
                product_attributes[attr1[0]] = attr1[1]
            elif len(attr1) > 2:
                attr_key = [i.strip() for i in attr.xpath('./td[1]//text()').getall() if i.strip()]
                attr_value = [i.strip() for i in attr.xpath('./td[2]/span//text()').getall() if i.strip()]

                if attr_key and attr_value:
                    attr_key = ''.join(attr_key).strip()
                    attr_value = ''.join(attr_value).strip().replace('See more', '')

                    if attr_key and attr_value:
                        product_attributes[attr_key] = attr_value
    except:
        pass

    ##add 23022024
    try:
        additional_information = dict()
        additional_infor = response.xpath(
            '//h3[contains(text(),"Additional Information") and @class="product-facts-title"]/following-sibling::*')
        for add_info in additional_infor:
            if 'h3' in add_info.xpath('.').get():
                break
            else:
                add_k = add_info.xpath('.//span[@class="a-color-base"][1]/text()').get('')
                add_v = add_info.xpath(
                    './/span[@class="a-color-base"][1]/../../following-sibling::div//span[@class="a-color-base"]/text()').get(
                    '')
                #################################################################################
                if add_k and add_v:
                    available = False
                    for itemdem in product_attributes.items():
                        if itemdem in {add_k.strip(): add_v.strip()}.items():
                            available = True
                    if available:
                        product_attributes.pop(add_k, None)
                        additional_information[add_k.strip()] = add_v.strip()
                    else:
                        additional_information[add_k.strip()] = add_v.strip()
            #################################################################################

        if additional_information:
            other_data['additional_information'] = additional_information
    except:
        pass

    try:
        selected_variant_loop = response.xpath('//span[@class="selection"]')
        for select_ in selected_variant_loop:
            select_key = select_.xpath('./preceding-sibling::label/text()').get('')
            select_value = clean_name(select_.xpath('./text()').get(''))
            if select_value and select_key:
                product_attributes[select_key.replace(":", "").strip()] = select_value.strip()
    except:
        pass

    ##add 22032024
    try:
        dropdown_variant = response.xpath('//div[contains(@id,"variation_") and contains(@id,"_name")]')
        if not dropdown_variant:
            dropdown_variant = response.xpath('//div[contains(@id,"variation_")]')
        for drop_v in dropdown_variant:
            drop_label = drop_v.xpath('.//label/text()').get()
            drop_value = clean_name(
                drop_v.xpath('.//span[@class="a-dropdown-container"]//option[@selected]/text()').get(''))
            if drop_label and drop_value:
                product_attributes[drop_label.replace(":", "").strip()] = drop_value
    except:
        pass
    try:
        ##add 23022024 use by xpath
        if response.xpath('//div[@data-feature-name="expiryDate"]'):
            exp_key = response.xpath('//div[@data-feature-name="expiryDate"]/span[1]/text()').get('')
            exp_val = clean_name(response.xpath('//div[@data-feature-name="expiryDate"]/span[2]/text()').get(''))

            if not exp_val and not exp_key:
                exp_key = response.xpath('//div[@data-feature-name="expiryDate"]//span[1]/text()').get('')
                exp_val = clean_name(
                    response.xpath('//div[@data-feature-name="expiryDate"]//span[2]/text()').get(''))

            if exp_key.strip() and exp_val:
                product_attributes[exp_key.replace(":", "").strip()] = exp_val
    except:
        pass

    try:
        ##add 23022024 bsr in attrib
        if response.xpath('//div[@id="glance_icons_div"]//td//span[1]'):
            for attrib in response.xpath('//div[@id="glance_icons_div"]//td//span[1]'):
                extra_key = attrib.xpath('./text()').get('')
                extra_val = clean_name(attrib.xpath('./following-sibling::span/text()').get(''))

                if extra_key.strip() and extra_val:
                    product_attributes[extra_key.replace(":", "").strip()] = extra_val.strip()
    except:
        pass

    try:
        if response.xpath('//div[contains(@id,"inline-twister-singleton-header")]//span'):
            for attrib in response.xpath('//div[contains(@id,"inline-twister-singleton-header")]//span'):
                extra_key = attrib.xpath('./text()').get('')
                extra_val = clean_name(attrib.xpath('./following-sibling::span/text()').get(''))
                if extra_key.strip() and extra_val:
                    product_attributes[extra_key.replace(":", "").strip()] = extra_val
    except:
        pass

    try:
        # size attributes
        if response.xpath(
                '//div[contains(@id,"inline-twister-dim-title")]//span[@class="a-size-base a-color-secondary"]'):
            for attrib in response.xpath('//div[contains(@id,"inline-twister-dim-title")]//span'):
                extra_key = attrib.xpath('./text()').get('')
                extra_val = clean_name(attrib.xpath('./following-sibling::span/text()').get(''))
                if extra_key.strip() and extra_val:
                    product_attributes[extra_key.replace(":", "").strip()] = extra_val
    except:
        pass

    try:
        # color attribute
        if response.xpath('//div[@id="variation_color_name"]//label'):
            for attrib in response.xpath('//div[@id="variation_color_name"]'):
                extra_key = attrib.xpath('.//label/text()').get('')
                extra_val = clean_name(attrib.xpath('.//span/text()').get(''))
                if extra_key.strip() and extra_val:
                    if 'Colour' not in product_attributes:
                        product_attributes[extra_key.replace(":", "").strip()] = extra_val
    except:
        pass

    # add 05032024
    try:
        book_specs = response.xpath(
            '//li[contains(@class,"carousel-attribute-card")]//div[contains(@class,"rpi-attribute-label")]')
        for books in book_specs:
            bk = books.xpath('./span/text()').get()
            bv = books.xpath('./following-sibling::div[contains(@class,"rpi-attribute-value")]/span/text()').get(
                '').strip()
            if not bv:
                bv = books.xpath(
                    './following-sibling::div[contains(@class,"rpi-attribute-value")]//span/text()').getall()
                if bv:
                    bv = ' '.join(bv).replace('\n', '').replace('\r', '').replace('\t', '').strip()
            if bk and bv:
                product_attributes[bk.replace(":", "").strip()] = bv.strip()
    except:
        pass

    try:
        if product_attributes:
            other_data['product_attributes'] = product_attributes
            if 'Brand' in other_data['product_attributes']:
                other_data['brand'] = other_data['product_attributes']['Brand']
    except:
        pass

    try:
        # PRODUCT DETAILS
        product_detail = dict()
        for detail in response.xpath('//*[@id="detailBullets_feature_div"]//li'):
            tmp_loader = ItemLoader(selector=detail)
            key = tmp_loader.get_xpath('.//text()', MapCompose(clean_name))
            if key:
                if not key[0].count(":"):
                    continue
                key[0] = key[0].replace(":", "").strip()
                product_detail[key[0]] = " ".join(key[1:]) if len(key) > 1 else ""
    except:
        pass

    try:
        # if not product_detail:
        for detail in response.xpath(
                '//div[@id="prodDetails"]//div[@id="productDetails_expanderSectionTables"]//tr'):
            key = detail.xpath('./th/text()').get('').strip()
            value = detail.xpath('./td/text()').get('').strip()
            if key and value:
                product_detail[key] = value
    except:
        pass

    try:
        if response.xpath(
                '//*[@id="detailBullets_feature_div"]//following-sibling::ul//span[contains(text(),"Best Sellers Rank")]'):
            bsr_text = response.xpath(
                '//*[@id="detailBullets_feature_div"]//following-sibling::ul//span[contains(text(),"Best Sellers Rank")]/..//text()').getall()
            if bsr_text:
                bsr_text = re.sub(r'\s+', ' ', ' '.join(bsr_text).replace("Best Sellers Rank:", "").strip())
                if bsr_text:
                    product_detail['Best Sellers Rank'] = bsr_text
    except:
        pass

    try:
        if product_detail:
            if 'Customer Reviews' in product_detail:
                del product_detail['Customer Reviews']

            other_data['product_detail'] = product_detail
            if 'Brand' in other_data['product_detail']:
                other_data['brand'] = other_data['product_detail']['Brand']

            ##add 12032024
            keys_to_remove = []
            for detail_key in product_detail.keys():
                if detail_key.startswith("ISBN"):
                    # Add the key-value pair to the "others" dictionary
                    other_data[detail_key.lower().replace('-', '_')] = product_detail[detail_key]
                    # Record the keys to remove from the original dictionary
                    keys_to_remove.append(detail_key)

            # Remove the keys from the original dictionary
            for key in keys_to_remove:
                del product_detail[key]
    except:
        pass

    try:
        if 'brand' not in other_data:
            brand = response.xpath('//a[@id="bylineInfo" and contains(text(), "Brand")]/text()').get('').strip()
            if brand:
                brand = brand.replace('Brand:', '').strip()
                other_data['brand'] = brand if 'Visit' not in brand else \
                    re.findall(r'Visit the (.*?) Store', brand, flags=re.IGNORECASE)[0]
    except:
        pass

    try:
        # SELLER DETAILS
        seller_detail = dict()

        seller_loop = response.xpath('//div[@class="tabular-buybox-container"]//div[@class="tabular-buybox-text"]')
        seller_loop2 = response.xpath(
            '//div[@id="almShipsFromSoldBy_feature_div"]//tr[@class="a-spacing-micro"] | //div[@id="freshShipsFromSoldBy_feature_div"]//tr[@class="a-spacing-micro"]')
        seller_loop3 = response.xpath('//div[@id="usedbuyBox"]//a[@id="sellerProfileTriggerId"]/text()')
        seller_loop4 = response.xpath('//tr[@id="Ebooks-desktop-printSoldBy"]')
        seller_loop5 = response.xpath(
            '//div[@id="offer-display-features"]//div[contains(@class,"offer-display-feature-label")]')

        if seller_loop:
            for sell in seller_loop:
                attrib_name = sell.xpath('./@tabular-attribute-name').get()
                attrib_value = sell.xpath('.//span//text()').get('').strip()
                if not attrib_value:
                    attrib_value = sell.xpath(
                        './span/a[@data-csa-c-content-id="secure-transaction-feature"]/span/text()').get('').strip()
                if attrib_name and attrib_value:
                    if attrib_name == 'Sold by':
                        seller_link = sell.xpath('.//a[@id="sellerProfileTriggerId"]/@href').get()
                        if seller_link:
                            seller_detail['Seller_link'] = seller_detail[
                                'Seller_link'] = seller_link if 'https://www.amazon.in' in seller_link else urljoin(
                                'https://www.amazon.in', seller_link)
                    seller_detail[attrib_name.strip()] = attrib_value.strip()
        elif seller_loop2:
            for sell in seller_loop2:
                attrib_name = sell.xpath('.//td[1]/span//text()').get()
                attrib_value = sell.xpath('.//td[2]/span//text()').get('').strip()
                if not attrib_value:
                    attrib_value = sell.xpath('.//td[2]/span/a/text()').get('').strip()
                if attrib_name and attrib_value:
                    if attrib_name == 'Sold by':
                        seller_link = sell.xpath('.//td[2]/span/a/@href').get()
                        if seller_link:
                            seller_detail[
                                'Seller_link'] = seller_link if 'https://www.amazon.in' in seller_link else urljoin(
                                'https://www.amazon.in', seller_link)
                    seller_detail[attrib_name.strip()] = attrib_value.strip()
        elif seller_loop3:
            seller_detail['Sold by'] = response.xpath(
                '//div[@id="usedbuyBox"]//a[@id="sellerProfileTriggerId"]/text()').get()
            seller_detail['Ships from'] = response.xpath(
                '//div[@id="usedbuyBox"]//a[@id="SSOFpopoverLink_ubb"]/text()').get()
            seller_link = response.xpath('//div[@id="usedbuyBox"]//a[@id="sellerProfileTriggerId"]/@href').get()
            seller_detail['Seller_link'] = 'https://www.amazon.in' + seller_link if seller_link else ''
        elif seller_loop4:
            for sell in seller_loop4:
                attrib_name = sell.xpath('.//td[1]//text()').get()
                attrib_value = sell.xpath('.//td[2]/span//text()').get('').strip()
                if not attrib_value:
                    attrib_value = sell.xpath('.//td[2]/span/a/text()').get('').strip()
                if attrib_name and attrib_value:
                    if attrib_name == 'Sold by':
                        seller_link = sell.xpath('.//td[2]/span/a/@href').get()
                        if seller_link:
                            seller_detail[
                                'Seller_link'] = seller_link if 'https://www.amazon.in' in seller_link else urljoin(
                                'https://www.amazon.in', seller_link)
                    seller_detail[attrib_name.strip()] = attrib_value.strip()
        elif seller_loop5:
            for sell in seller_loop5:
                attrib_name = sell.xpath('.//span//text()').get('').strip()
                attrib_value = sell.xpath(
                    './..//div[contains(@class,"offer-display-feature-text")]//span//text()').get('').strip()
                if not attrib_value:
                    attrib_value = sell.xpath(
                        './..//div[contains(@class,"offer-display-feature-text")]//a/span/text()').get('').strip()
                if attrib_name and attrib_value:
                    if attrib_name == 'Sold by':
                        seller_link = sell.xpath(
                            './..//div[contains(@class,"offer-display-feature-text")]//a/@href').get()
                        if seller_link:
                            seller_detail[
                                'Seller_link'] = seller_link if 'https://www.amazon.in' in seller_link else urljoin(
                                'https://www.amazon.in', seller_link)
                    seller_detail[attrib_name.strip()] = attrib_value.strip()

        if seller_detail:
            other_data['seller_detail'] = seller_detail
    except:
        pass

    try:
        other_seller = otherseller_details(response_sec, product_id)
        other_data['otherseller_details'] = other_seller
    except:
        pass

    try:
        offer_list = get_offer(response_sec, product_id)
        other_data['offers'] = offer_list
    except:
        pass

    other_data['deal_of_the_day'] = True if response.xpath(
        '//span[text()="Deal of the Day"]//ancestor::span[@class="dealBadge"]') else False
    other_data['deal_price'] = True if response.xpath(
        '//span[text()="Deal"]//ancestor::span[@class="dealBadge"]') else False
    other_data['bundle_list_price'] = True if response.xpath(
        '//div[@id="ppd"]//*[contains(text(),"Bundle List Price")]') else False

    try:
        if response.xpath('//span[text()="Prime Day launch"]'):
            other_data['prime_day_launch'] = True

        best_seller_badge = dict()
        best_seller_badge['is_badge_available'] = False

        badge_object = response.xpath('//a[@class="badge-link" and @title]')
        if badge_object:
            best_seller_badge['is_badge_available'] = True
            best_seller_badge['badge_text'] = badge_object.xpath('.//i/text() | ./span/text()').get('')
            best_seller_badge['badge_cat_name'] = badge_object.attrib['title']
            best_seller_badge['badge_cat_link'] = badge_object.attrib['href']

            if best_seller_badge.get('badge_cat_link'):
                if 'http' not in best_seller_badge['badge_cat_link']:
                    best_seller_badge[
                        'badge_cat_link'] = f"https://www.amazon.in{best_seller_badge['badge_cat_link']}"

        other_data['best_seller_badge'] = best_seller_badge
    except:
        pass
    # ------------------

    # ------------------ NEW

    try:
        if response.xpath('//div[@data-feature-name="acBadge"]//*[contains(@class,"ac-badge-rectangle")]'):
            other_data['amazon_choice'] = True
        else:
            other_data['amazon_choice'] = False
    except:
        pass
    # ------------------

    # ------------------ NEW
    try:
        if response.xpath('//div[@data-feature-name="shippingMessageInsideBuyBox"]//*[@aria-label="Fulfilled"]'):
            other_data['amazon_fulfilled'] = True
        else:
            other_data['amazon_fulfilled'] = False
    except:
        pass

    # ------------------
    try:
        if response.xpath('//div[@class="refurbished-badge-wrapper"]//*[contains(text(),"Refurbished")]'):
            other_data['refurbished'] = True
        else:
            other_data['refurbished'] = False
    except:
        pass

    # ------------------NEW
    try:
        if response.xpath(
                '//div[@id="dealBadge_feature_div"]//span[@id="dealBadgeSupportingText"]/span[contains(text(),"Great Freedom")]').get():
            other_data['great_freedom_sale'] = True
        else:
            other_data['great_freedom_sale'] = False
    except:
        pass

    try:
        if response.xpath(
                '//div[@id="dealBadge_feature_div"]//span[@id="dealBadgeSupportingText"]/span[contains(text(),"Kickstarter deal")]'):
            other_data['kickstarter_deal'] = True
        else:
            other_data['kickstarter_deal'] = False
    except:
        pass
    try:
        for xpath in (
                '//div[@id="productDescription_feature_div"]//div[@id="productDescription"]//text()',
                '//div[@id="productDescription"]//text()',
        ):
            description = clean_name(' '.join(response.xpath(xpath).getall()))
            if description:
                if description == 'Previous page Next page':
                    pass
                if description:
                    other_data['description'] = description

    except:
        pass

    try:
        if 'dimensionToAsinMap' not in response_content:
            other_data['variation_id'] = product_id.split()
        else:
            variation_id = list()
            variation_id.append(product_id)
            all_asin = re.findall(r'dimensionToAsinMap\" :(.*?)\n', response_content)[0]
            all_asin_json = json.loads(all_asin.strip(",").strip())
            for asin in all_asin_json:
                asin = all_asin_json[asin]
                if asin not in variation_id:
                    variation_id.append(asin)

            other_data['variation_id'] = sorted(variation_id)
    except:
        pass
    # if not self.test:
    #     other_data['delivery'] = 'daily_login_logout'
    # else:
    #     other_data['delivery'] = "amazon_test_weekly"
    # # other_data['delivery'] = 'login_logout_qa'
    #
    # if response.meta["department"] == "mall":
    #     other_data['delivery'] = 'mall_daily_login_logout'

    # other_data['delivery'] = response.meta['delivery_tag'] + '_' + db.current_time_am_pm

    rating_dict = dict()
    try:
        rating_k = 5
        for rat in response.xpath('//*[@id="histogramTable"]//*//div[@class="a-meter"]'):
            val = rat.xpath('.//@aria-valuenow').get('')
            rating_dict[rating_k] = val
            rating_k -= 1
        other_data['individualRatingsCount'] = rating_dict



        seller_policy1 = response.xpath('//div[@id="iconfarmv2_feature_div"]//*[@alt]/@alt').getall()
        seller_policy2 = [j.strip() for j in response.xpath(
            '//div[@id="iconfarmv2_feature_div"]//div[@class="a-section a-spacing-none icon-content"]/span/text()').getall()
                          if j.strip()]
        seller_policy = [j.strip() for j in response.xpath(
            '//div[@id="iconfarmv2_feature_div"]//div[@class="a-section a-spacing-none icon-content"]/a/text()').getall()
                         if j.strip()]
    except:
        pass

    try:
        if seller_policy:
            other_data['seller_return_policy'] = seller_policy
        elif seller_policy2:
            other_data['seller_return_policy'] = seller_policy2
        elif seller_policy1:
            seller_policy = [i.strip() for i in seller_policy1 if i.strip()]
            other_data['seller_return_policy'] = seller_policy
        other_data['seller_return_policy'] = list(set(other_data['seller_return_policy']))
    except:
        pass
    # new headers 23022024

    try:
        if response.xpath('//div[@id="outer-nveg"]'):
            other_data['non_veg_indicator'] = True
    except:
        pass

    try:
        if response.xpath('//div[@id="outer-veg"]'):
            other_data['veg_indicator'] = True
    except:
        pass
    ##add 26022024
    try:
        additional_services = dict()
        if response.xpath('//div[@id="ppdBundlesEnhancedBox"]//span[@id="ppdBundlesHeading"]'):
            for bundle in response.xpath('//div[@id="ppdBundlesEnhancedBox"]//span[@id="ppdBundlesHeading"]'):
                bundle_text = bundle.xpath('./b/text()').get()
                bundle_price = bundle.xpath(
                    './..//following-sibling::div//span[@id="ppdBundlesPriceValueId"]/text()').get()
                if bundle_text and bundle_price:
                    additional_services['service_name'] = bundle_text.strip()
                    additional_services['service_price'] = bundle_price.strip()
    except:
        pass
    try:
        if additional_services:
            other_data['additional_services'] = additional_services
    except:
        pass
    try:
        if response.xpath('//div[@data-feature-name="customerReviewsAttribute"]'):
            headname = response.xpath('//div[@data-feature-name="customerReviewsAttribute"]//h1/text()').get('')
            if not headname:
                headname = 'Customer ratings'
            extra_rating_dict = dict()
            for customer_rating in response.xpath(
                    '//div[@data-feature-name="customerReviewsAttribute"]//span[@class="a-size-base a-color-base"]'):
                extra_rating_key = customer_rating.xpath('./text()').get('')
                extra_rating_val = customer_rating.xpath(
                    './../../following-sibling::div//span[@class="a-icon-alt"]/text()').get('')

                if extra_rating_key and extra_rating_val:
                    extra_rating_dict[extra_rating_key.strip()] = extra_rating_val.strip()
            if extra_rating_dict:
                other_data['extra_rating'] = {headname.strip(): extra_rating_dict}
    except:
        pass

    try:
        certifications = list()
        if response.xpath('//div[@class="provenance-certifications-row-description"]'):
            for cert in response.xpath('//div[@class="provenance-certifications-row-description"]'):
                cert_k = cert.xpath('./div/text()').get('')
                cert_v = cert.xpath('.//span[contains(@class,"a-truncate-full")]//text()').get('')
                if cert_k and cert_v:
                    certifications.append({"title": cert_k.strip(), "details": cert_v.strip()})

        if certifications:
            other_data['certifications'] = certifications
    except:
        pass
    try:
        extra_description = response.xpath('//div[@id="bookDescription_feature_div"]//text()').getall()
        if extra_description:
            extra_description = [i.strip() for i in extra_description if i.strip() and i != 'Read more']
            extra_description = ' '.join(extra_description).replace('\n', '').replace('\r', '').replace('\t',
                                                                                                        '').strip()
            if extra_description:
                if 'description' in other_data:
                    del other_data['description']
                other_data['extra_description'] = extra_description
    except:
        pass

    try:
        luxury_beauty = response.xpath('//a[@id="beautyBadgeDetails"]')
        if luxury_beauty:
            other_data['luxury_beauty_badge'] = True
    except:
        pass
    try:
        deal_text = response.xpath('//div[@id="ppd"]//span[@id="dealBadgeSupportingText"]/span/text()').get()
        if deal_text:
            if 'limited time deal' in deal_text.lower().strip():
                other_data['limited_time_deal'] = True
            else:
                other_data['limited_time_deal'] = False
            if 'with prime' in deal_text.lower().strip():
                other_data['with_prime'] = True
            elif 'Great Summer Sale'.lower() in deal_text.lower().strip():
                other_data['great_summer_sale'] = True
        else:
            other_data['limited_time_deal'] = False
    except:
        other_data['limited_time_deal'] = False

    try:
        bought_text = response.xpath('//span[@id="social-proofing-faceout-title-tk_bought"]/span/text()').getall()
        if bought_text:
            other_data['sales_prediction'] = ''.join(bought_text).strip()
    except:
        pass

    try:
        digital_price = response.xpath(
            '//td[contains(text(),"Digital List Price:")]/following-sibling::td/text()').get()
        if digital_price:
            digital_price = digital_price.replace('₹', '').strip()
            other_data['digital_price'] = digital_price
    except:
        pass

    # loader.add_value('others', json.dumps(other_data))
    try:
        item['others'] = json.dumps(other_data)
    except:
        item['others'] = 'N/A'
    # item = loader.load_item()

    item['status_logout'] = "N/A"

    try:
        if (
                "Currently unavailable" in response_content and
                "We don't know when or if this item will be back in stock" in response_content
        ):
            del item['product_price']
            del item['mrp']
            del item['shipping_charges']
            del item['discount']

        # if item['product_price'] and item['mrp']:

        if 'product_price' in item and 'mrp' in item and item['product_price'] > float(item['mrp']):
            item['product_price'], item['mrp'] = item['product_price'], item['product_price']
            if 'discount' in item:
                del item['discount']
    except:
        pass
    # if not item['product_price']:
    #     item['mrp'] = '0.0'
    #     item['discount'] = '0'
    key_name = "NEW_USER" if not login_status else "OLD_USER"

    try:
        item['shipping_charges_json'] = json.dumps(
            {
                key_name: str(item['shipping_charges'])
                if 'shipping_charges' in item and item['shipping_charges'] else "N/A"
            }
        )
    except:
        item['shipping_charges_json'] = "N/A"

    try:
        item['product_price_json'] = json.dumps(
            {key_name: str(
                item['product_price'] if 'product_price' in item and item.get('product_price') else "N/A")}
        )
    except:
        item['product_price_json'] = "N/A"

    try:
        item['mrp_json'] = json.dumps({key_name: str(item['mrp'] if 'mrp' in item and item.get('mrp') else "N/A")})
    except:
        item['mrp_json'] = "N/A"

    try:
        item['discount_json'] = json.dumps(
            {key_name: str(item['discount'] if 'discount' in item and item.get('discount') else "N/A")})
    except:
        item['discount_json'] = "N/A"

    try:
        if item['is_sold_out'] == 'false' and (
                not item.get('product_price') or item.get('product_price') == '0.0' or item.get(
            'product_price') == '0'):
            if not response.xpath(
                    '//div[@id="Northstar-Buybox"]//div[@id="tmmSwatches"]//div[contains(@class,"swatchElement selected")]//img[@alt="Audible Logo"]'):
                print('price N/A issue, breaking==')
                return None
    except:
        item['is_sold_out'] = "N/A"
    try:
        two_date = identify_date_or_time(item.get('arrival_date'))
        if two_date == 'Contains DATE only':
            item['check_date'] = True
        else:
            item['check_date'] = False

        # if item['arrival_date']:
        arrival_date_item = ''
        if "-" in item['arrival_date']:
            two_arrival_date_item_min, two_arrival_date_item_max = two_process_arrival_date(item.get('arrival_date'))
        else:
            arrival_date_item = process_arrival_date(item.get('arrival_date'))

        if "-" in item['arrival_date']:
            item['arrival_date'] = two_arrival_date_item_min if two_arrival_date_item_min else "N/A"
            item['min_arraival'] = two_arrival_date_item_min if two_arrival_date_item_min else "N/A"
            item['max_arraival'] = two_arrival_date_item_max if two_arrival_date_item_max else "N/A"
        else:
            item['arrival_date'] = arrival_date_item if arrival_date_item else "N/A"

        if arrival_date_item:
            date_check = datetime.strptime(item['arrival_date'], '%Y-%m-%d %H:%M:%S')
            # Define the 'Asia/Calcutta' timezone
            tz = pytz.timezone('Asia/Calcutta')

            # Localize the offset-naive datetime object to 'Asia/Calcutta' timezone
            date_check = tz.localize(date_check)

            # Get the current date and time in 'Asia/Calcutta' timezone
            current_date = datetime.now()
            if date_check.date() < current_date.date():
                print('arrival date issue===')
                return None
    except:
        item['arrival_date'] = arrival_date_item if arrival_date_item else "N/A"

    try:
        del item['Others']['individualRatingsCount']
    except:
        pass

    if item['is_sold_out'] == 'false':
        if 'arrival_date' not in item and item['product_price'] and item.get('discount', 'N/A') == 'N/A':
            new_item = item.copy()
            try:
                item["No of Ratings"] = item.pop("# of Ratings")
            except:
                pass
            hfm = set_item(new_item)
            return hfm
        else:
            new_item = item.copy()
            try:
                item["No of Ratings"] = item.pop("# of Ratings")
            except:
                pass
            hfm = set_item(new_item)
            return hfm

    else:
        new_item = item.copy()
        try:
            item["No of Ratings"] = item.pop("# of Ratings")
        except:
            pass
        hfm = set_item(new_item)
        return hfm


if __name__ == '__main__':
    product_id = 'B0FFGW9KQX'
    response_sec = get_response(product_id)
    data = parse(product_id, response_sec, 0)
    print(json.dumps(data))
