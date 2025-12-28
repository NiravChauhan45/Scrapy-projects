import re


def get_product_name(response):
    product_name = ""
    try:
        product_name = response.xpath("//span[@id='productTitle']/text()").get()
        if not product_name:
            product_name = response.xpath("//input[@name='productTitle']/@name").get()

        product_name = re.sub("\\s+", " ", product_name).strip()
        return product_name
    except Exception as e:
        print(e)


def get_currency(response):
    currency = ""
    try:
        currency = response.xpath(
            "//span[@class='a-price aok-align-center reinventPricePriceToPayMargin priceToPay']//span[@class='a-price-symbol']/text()")
        return currency
    except Exception as e:
        print(e)


def get_mrp(response):
    mrp = ''
    try:
        mrp = response.xpath(
            "//span[@class='a-size-small a-color-secondary aok-align-center basisPrice']//span[@class='a-price a-text-price']/span[@class='a-offscreen']/text()").get()
        if not mrp:
            mrp = "N/A"
    except:
        mrp = "N/A"
    return mrp


def get_ratings(response):
    rating = response.xpath("//span[@id='acrCustomerReviewText']/text()").getall()
    rating = "".join(list(set(rating)))
    return rating
