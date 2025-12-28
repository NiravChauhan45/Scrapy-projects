import pandas as pd
import json

# Load JSON
with open("amazon_links.json", "r") as f:
    data = json.load(f)

# Flatten JSON into rows
rows = []
for main_cat, subcats in data.items():
    for sub_cat, url in subcats.items():
        rows.append({
            "main_category_name": main_cat,
            "sub_category_name": sub_cat,
            "sub_category_url": url
        })

# Convert to DataFrame
df = pd.DataFrame(rows, columns=["main_category_name", "sub_category_name", "sub_category_url"])

# Save to CSV
df.to_csv("categories.csv", index=False)
print("CSV file created successfully!")
