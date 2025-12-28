import requests
from parsel import Selector


def get_pl_response(keyword):
    for i in range(0, 5):
        url = f"https://www.amazon.in/s?k={keyword}&ref=nb_sb_noss_2"
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'device-memory': '8',
            'downlink': '10',
            'dpr': '0.75',
            'ect': '4g',
            'priority': 'u=0, i',
            'referer': 'https://www.amazon.in/s?k=saree&crid=3PHZX8T1B23DC&sprefix=saree%2Caps%2C307&ref=nb_sb_noss_2',
            'rtt': '200',
            'sec-ch-device-memory': '8',
            'sec-ch-dpr': '0.75',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"19.0.0"',
            'sec-ch-viewport-width': '2560',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'viewport-width': '2560',
            'Cookie': 'csm-sid=972-3354754-9330928; x-amz-captcha-1=1755085180285785; x-amz-captcha-2=0NV29xsjJZ/si6x+KYSriw==; session-id=257-9392320-3016515; i18n-prefs=INR; lc-acbin=en_IN; ubid-acbin=261-3741531-2688330; session-id-time=2082787201l; csm-hit=tb:1FJ98X9BC8D9EXPQVAR6+s-R3EFWZCG91GDKZDCTBV2|1755755779221&t:1755755779222&adb:adblk_no; session-token=q5sNq5B+Ds+yYOQ4J8WP9nHUVoAR2A0epHDd9gSlhOWOQak7xRXf2YbgJ9tjwi7xIjyqwLJEM/4S/IFlN5Dgk3PVZOBwqZt6lwYiuMwHkfQQSHlPX9QXmMlHOJ0HjmYoFAq0vqZwcUx6T2O0Ky7XHf4LnMASFxTCvQpPDAHBcGzwyWYNZk5doHcgGom1jNxNbq1Uh6QyR3SZV5A7aHr1RA49f0c2cNsSnRYqku9V/grbBW0z13csy0n3Db3hHbFuxcdrbtxTeJ4pvIkHZXCZvrAbG+hCZm9tsFhbTvUyLfb/8SWDfE/5VU0tiVBNOQ8qnUNpAmjPd1HmiS691yfmcDWkBwPlft4f; rxc=AE39nc823nafD4ZLDdc; i18n-prefs=INR; lc-acbin=en_IN; session-id=258-3853371-4374257; session-id-time=2082787201l; session-token=G8oQeIaRs3PnQ8h5OUkN753D4RFPqwEUfq5aombQf+MvulOibRA0u/RQw8qplegRre2iKQ+v5AQE6AQqYwzs1vZp+rZtPe7KC5onZx9SBLxI2XX4wRI7V/pgQ2mKtrqdxs6UtzgTepA0NchfKEbxxHKGtj13zFoOLCEriJsCf2lyRqhAC4fv6WTXMJtg9U9J+44agx6J0laGB8MArGa2Bk7rFc/clSoLsOtSFm2qGeCdcxZWzGxDsJvBng3xJZQZ9F7s5YaRHJixHmz/3UfwZ8pWh2yR5HF8GPTcZdLOdfmFN5QriLMhbGhP/y7ZhvZmcsYMBbldMb+HOKDoeDyGsJycE6DZ1dWh; ubid-acbin=259-5207049-2336510'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            break
    return response.text


def get_pl_links(response):
    selector = Selector(text=response)
    product_links_list = selector.xpath("//a[@class='a-link-normal s-no-outline']/@href").getall()


if __name__ == '__main__':
    keyword = "saree"
    response = get_pl_response(keyword)
    pl_links = get_pl_links(response)
    print(response)
