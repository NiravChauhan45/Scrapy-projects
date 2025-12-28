import os
import time


end = 107461
start = 68359
num_parts = 20


def id_between():
    # Calculate the number of items in each part
    items_per_part = (end - start + 1) // num_parts

    # Initialize a list to store the range parts
    range_parts = []

    # Generate the range parts
    for i in range(num_parts):
        part_start = start + i * items_per_part
        part_end = start + (i + 1) * items_per_part - 1 if i < num_parts - 1 else end
        range_parts.append((part_start, part_end))

    # Print the range parts
    for i, (part_start, part_end) in enumerate(range_parts):
        cmd = f'start "Part:{i + 1}" python get_data_indonesia.py {part_start} {part_end}'
        # cmd = f'start "Part:{i+1}" python get_data_indonesia_hair_care.py {part_start} {part_end}'
        os.system(cmd)
        print(cmd)
        # time.sleep(5)


def limit():
    part_size = (end - start + 1) // num_parts

    # Generate the commands
    for part in range(num_parts):
        part_start = start + (part * part_size)
        part_end = part_start + part_size - 1
        if part == num_parts - 1:  # Ensure the last part goes to the end
            part_end = end
        # cmd = f'start "Part:{part + 1}" scrapy crawl links_product -a start={part_start} -a end={part_end - part_start + 1}'
        # cmd = f'start "Part:{part + 1} img" python image_download2.py {part_start} {part_end - part_start + 1}'
        cmd = f'start "Part:{part + 1} img" python image_download2.py {part_start} {part_end}'
        print(cmd)
        os.system(cmd)


# id_between()
limit()