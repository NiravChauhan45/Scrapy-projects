import sys

# start_part = 000000
start_part = 0
try:
    # end_part = int(sys.argv[1])
    end_part = 204941
except:
    end_part = 204941

all_parts = list()
all_parts.append('taskkill /F /FI "WindowTitle eq big_basket_*"')

vertical = True if len(sys.argv) > 2 else False

parts = 15
step = (end_part - start_part) // parts
zfill_step = len(str(end_part))

for i in range(start_part, end_part, step):
    start = str(i + 1).zfill(zfill_step)
    end = str(i + step).zfill(zfill_step)
    part = f'start "big_basket_{start}_{end}" scrapy crawl download_image -a start={start} -a end={end}'
    # part = f'start "meesho_product_master_{start}_{end}" scrapy crawl meesho_pro_data_final -a start={start} -a end={end}'
    # part = f'start python new_app_req.py {start} {end}'
    all_parts.append(part)

# open(r"D:\siraj\meesho_des\meesho_des\spiders\run.bat", "w").write("\n".join(all_parts))
open(r"../download_images/spiders/run_big_basket_image.bat", "w").write("\n".join(all_parts))
# open(r"D:\siraj\meesho\meesho\page_save_run.bat", "w").write("\n".join(all_parts))