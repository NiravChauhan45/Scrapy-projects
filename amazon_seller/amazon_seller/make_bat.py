bat_file_name = "get_variation_id"

count = 27126
# count = 100

jump_iterate = int(count / 5)

for part in range(1, count, jump_iterate):
    print(f"start scrapy crawl {bat_file_name} -a start_index={part} -a end={jump_iterate + part}")
