import scrapy


class PdpDataSpider(scrapy.Spider):
    name = "pdp_data"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
