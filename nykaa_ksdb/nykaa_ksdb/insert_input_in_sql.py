import pymysql
import requests
import xml.etree.ElementTree as ET

# URL of sitemap index
url = "https://www.nykaa.com/sitemap-v2/sitemap-products-1.xml"

# Fetch sitemap XML
response = requests.get(url)
response.raise_for_status()

# Parse XML
root = ET.fromstring(response.content)

# Define namespace (from XML root)
namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# Extract <loc> values
links = [elem.text for elem in root.findall(".//ns:loc", namespace)]
conn = pymysql.connect(
    host="localhost",
    user="root",
    passwd="actowiz",
    database="nykaa_ksdb", autocommit=True
)
# Print results
cursor = conn.cursor()

# 3. Insert links with INSERT IGNORE
query = "INSERT IGNORE INTO nykaa_ksdb_input (product_url) VALUES (%s)"
for link in links:
    cursor.execute(query, (link,))

# 4. Commit and close
conn.commit()
cursor.close()
conn.close()

print(f"Inserted {len(links)} links (duplicates ignored).")