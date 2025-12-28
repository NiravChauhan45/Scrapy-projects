import db_config as db
import requests
from parsel import Selector
from loguru import logger
import os
from concurrent.futures import ThreadPoolExecutor

def insertItemToSql(product_url):
    item = dict()
    item['product_url'] = product_url
    try:
        # Prepare safe value list
        value_list = [
            json.dumps(v) if isinstance(v, dict) else v
            for v in item.values()
        ]

        # Build query dynamically
        field_list = [f"`{field}`" for field in item.keys()]
        placeholders = ["%s"] * len(item)

        fields = ",".join(field_list)
        placeholders_str = ",".join(placeholders)

        insert_db = f"INSERT IGNORE INTO {db.pdp_links} ({fields}) VALUES ({placeholders_str})"

        db.cursor.execute(insert_db, value_list)
        db.connection.commit()

        logger.info("Item Successfully Inserted...")
    except Exception as e:
        print("Error:", str(e))

def process_xml_file(file_path):
    """Read + parse + insert URLs from a single XML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        selector = Selector(text=content)
        pdp_links = selector.xpath("//loc/text()").getall()

        for pdp_link in pdp_links:
            insertItemToSql(pdp_link)

        print(f"Processed: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


# if __name__ == '__main__':
#     folder_path = r"E:\Nirav\Project_code\marketplace_project\bloomingdales\product_links_pages"
#     results = os.listdir(folder_path)
#
#     file_paths = [
#         os.path.join(folder_path, file_name)
#         for file_name in results
#         if file_name.endswith(".xml")
#     ]
#
#     # Use up to 10 threads (you can change this)
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         executor.map(process_xml_file, file_paths)

if __name__ == '__main__':
    folder_path = r"E:\Nirav\Project_code\marketplace_project\bloomingdales\product_links_pages"
    results = os.listdir(folder_path)

    for file_name in results:
        file_path = os.path.join(folder_path, file_name)  # <-- FIX HERE

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        selector = Selector(text=content)
        pdp_links = selector.xpath("//loc/text()").getall()
        for pdp_link in pdp_links:
            insertItemToSql(pdp_link)
