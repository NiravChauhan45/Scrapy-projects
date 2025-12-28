import os
import shutil

# Your folder path
folder_path = r"D:\Nirav Chauhan\screenshot\big_basket_screenshot\03_08_2025"
# 31_07_2025 date to rename images
# Supported image extensions
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

# List all image files in the folder
image_files = [f for f in os.listdir(folder_path)
               if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(image_extensions)]

# Print results
for filename in image_files:
    image = filename.split('_')[0:2]
    today_date = "03_08_2025.png"
    image.append(today_date)
    images = "_".join(image)
    new_filename = images
    old_path = r"D:\Nirav Chauhan\screenshot\big_basket_screenshot\03_08_2025"
    new_path = r"D:\Nirav Chauhan\screenshot\big_basket_screenshot\03_08_2025"
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)
    os.rename(old_path, new_path)

print(f"\nTotal images found: {len(image_files)}")
