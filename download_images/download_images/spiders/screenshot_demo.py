import scrapy
from scrapy import cmdline
from scrapy_splash import SplashRequest


class YourSpider(scrapy.Spider):
    name = "your_spider_name"
    start_urls = ["https://www.bigbasket.com/"]  # Replace with your target URL

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 10})  # Adjust wait time as needed

    def parse(self, response, **kwargs):
        # Example: Capture a screenshot of the entire page
        screenshot_name = f"screenshot_{response.url.replace(':', '_').replace('/', '_')}.png"
        with open(screenshot_name, "wb") as f:
            f.write(response.body)  # response.body contains the HTML content.
        print(f"Screenshot saved to: {screenshot_name}")

        # Example: Capture a screenshot of a specific element
        # Use CSS selector to target the element
        # screenshot_element_name = f"screenshot_element_{response.url.replace(':', '_').replace('/', '_')}.png"
        # element = response.css("body") # Replace with your desired element
        # with open(screenshot_element_name, "wb") as f:
        #     f.write(element.extract()) # element.extract() gets the HTML for the element.
        # print(f"Screenshot saved to: {screenshot_element_name}")

        # ... Your parsing logic ...
        yield {  # This is just an example of a scraped item
            "url": response.url,
            "title": response.css("title::text").get(),
            # ... other scraped data ...
        }


if __name__ == '__main__':
    cmdline.execute("scrapy crawl your_spider_name".split())
