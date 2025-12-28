from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client['prectice_db']
collection = db['prectice']

print("Connected to MongoDB!")