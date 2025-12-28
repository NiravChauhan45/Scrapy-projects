

for i in range(1,8009,500):
    print(f"start scrapy crawl pdp_data -a start={i} -a end={500+i}")