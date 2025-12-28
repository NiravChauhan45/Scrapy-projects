import requests
from parsel import Selector

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'device-memory': '8',
    'downlink': '10',
    'dpr': '1.35',
    'ect': '4g',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'rtt': '50',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'viewport-width': '1422',
    'cookie': 'x-amz-captcha-1=1740064659874893; x-amz-captcha-2=odk+bw8e4WQAhUKpt2xPWA==; session-id=131-7967661-8597542; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=131-4199319-4736135; regStatus=pre-register; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C20159%7CMCMID%7C14261673283856433932800593299618800155%7CMCAAMLH-1742278675%7C12%7CMCAAMB-1742278675%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1741681076s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; lc-main=en_US; session-token=cs9I81uB7LEhThUM5ZLPuKKbvru/XTaHKrKTXdlTFQrUlT0jF+yaMy32x09909jlpwJcl4vYQuhjWEKOTbBOdN6h6CZ0wI6lbqkjdziihtqPA6p17GMR81W7CTpF+uyJJESq6I5IpVQ6h8SVOlN8ytlxatAbo26ghUi5qky45ef+wXp86EKzdR4KeFaP36loFYebg+ZwuA9KVEaDRaUCMgndOYBY+gSoNK7RRnPTp5LOi5X89bebgjUR35hYu20N9hVkj4+H2ssZX0brRUn8U+XbG2McG4JNl0odktIzc93py88Gkwi5dmOPTTSkKUWB9ZebjdDjepo9hcUE6raVpl/CRK3MKdJt; csm-hit=tb:Z1E2VGX11D3M0CBQ0DMK+s-Z1E2VGX11D3M0CBQ0DMK|1742792869311&t:1742792869311&adb:adblk_no',
}

response = requests.get('https://www.amazon.com/b?node=3760911', headers=headers)

selector = Selector(text=response.text)

for category_data in selector.xpath("//li[@class='a-spacing-micro apb-browse-refinements-indent-2']//a"):
    main_category_name = 'Beauty & Personal Care'
    category_name = category_data.xpath("./span/text()").get('').strip()
    category_url = "https://www.amazon.com" + category_data.xpath("./@href").get('').strip()
    response1 = requests.get(category_url, headers=headers)
    selector1 = Selector(text=response1.text)
    for sub_category_data in selector1.xpath("//li[@class='a-spacing-micro apb-browse-refinements-indent-2']//a"):
        sub_category_name = sub_category_data.xpath("./span/text()").get('').strip()
        sub_category_url = "https://www.amazon.com" + sub_category_data.xpath("./@href").get('').strip()
        response2 = requests.get(sub_category_url, headers=headers)
        selector2 = Selector(text=response2.text)
        for child_category_data in selector2.xpath("//li[@class='a-spacing-micro s-navigation-indent-2']//a"):
            child_category_name = child_category_data.xpath("./span/text()").get('').strip()
            child_category_url = "https://www.amazon.com" + child_category_data.xpath("./@href").get('').strip()
