from pymongo import MongoClient
import pandas as pd

collection_name = 'products_details_04_08_2025_13_22'
# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['nykaa']
collection = db[collection_name]

# Fetch all documents
data = list(collection.find({}))

# Remove "_id" field from each document
for doc in data:
    doc.pop("_id", None)  # Safely remove '_id' if it exists

# Convert to DataFrame
df = pd.DataFrame(data)
if 'Id' in df.columns:
    cols = ['Id'] + [col for col in df.columns if col != 'Id']
    df = df[cols]

# Save to Excel
df.to_excel(f"nykaa_fashion_{collection_name}.xlsx", index=False, engine='openpyxl')

print("✅ Data exported to output.xlsx without '_id' field.")
