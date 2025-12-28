file_name: cat_link.py

    ->first need to run this file you can change db_config as per your requirement

    request_name : navigation?.....
    you can find request at nykaa homepage by entering any subcategory name in network tab


file_name: pdp_link.py
    -> after cat_link you need to run the run.bat file
    * divide the parts as per the data count

after running the pdp_link.py the products having status partial_done need to scrape again:
    example:

            URL:https://www.nykaa.com/jewellery-accessories/earrings/c/11364?page_no=1&sort=popularity&eq=desktop&price_range_filter=500-999&segment_filter=214440

            IN the above given url I have applied segment filter in the earrings category

            also I have provided the dump of that extra table in this file(file_name: partial_done_products.sql) for your reference
