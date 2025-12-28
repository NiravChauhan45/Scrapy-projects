import sys
import time
from DrissionPage import Chromium, ChromiumOptions
from loguru import logger
from parsel import Selector

# Set up Chromium options
co = ChromiumOptions()
co.incognito()  # Enable incognito mode

# (Optional) Add extension if it's allowed in incognito mode
co.add_extension(r'C:\Users\nirav.chauhan\AppData\Local\Google\Chrome\User Data\Default\Extensions\eifflpmocdbdmepbjaopkkhbfmdgijcc')

# You should NOT connect to existing browser if using incognito (i.e., remove addr)
browser = Chromium(co)

# Open a new tab
tab = browser.new_tab()

# Visit the BigBasket product page
tab.get('https://www.bigbasket.com/pd/40136337/true-elements-seeds-berries-breakfast-muesli-1-kg/')

# Wait for page to load
time.sleep(1)

# Parse the page content
res = Selector(text=tab.html)
print(tab.html)
match_zipcode = res.xpath(
                "//button[@class='AddressDropdown___StyledMenuButton2-sc-i4k67t-3 ZpLbn']/span/text()|//button[@class='AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW']/span/text()").get()


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
                    from_input.input("110001")
                    time.sleep(2)
                    tab.actions.key_down('DOWN').key_down('ENTER')
                else:
                    print("Pincode input field not found.")


        update_button = tab.ele(
            f"xpath:(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 cTJSLV'])[{i}]|(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX'])[{i}]|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 ggMOKv']|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN']")
        if update_button:
            update_button.click()
            response = Selector(text=tab.html)   #----------till here -----------------------
            service_not_available = response.xpath(
                "//span[contains(text(),'The selected city is not serviceable at the moment')]")
            if service_not_available:
                tab.refresh()

        else:
            print("Update button not found.")

    except Exception as e:
        logger.error(f"Error entering pincode or clicking update: {e}")

i=1
while True:
    update_button = tab.ele(f"xpath:(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 cTJSLV'])[{i}]|(//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 dzmzlX'])[{i}]|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-7 ggMOKv']|//li[@class='AddressDropdown___StyledMenuItem-sc-i4k67t-9 eVKPXN']")
    if update_button:
        update_button.click()
        response = Selector(text=tab.html)   #----------till here -----------------------
        service_not_available = response.xpath(
            "//span[contains(text(),'The selected city is not serviceable at the moment')]")
        if service_not_available:
            tab.refresh()
        i += 1
    else:
        break
        print("Update button not found.")
