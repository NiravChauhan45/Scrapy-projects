import os

from Nirav_DB_CONFIG import ConfigDatabase

db = ConfigDatabase(database='prectice', table='friends')

item = {
    "id": 1,
    "Name": "Nirav",
    "Age": 22,
}

# db.insertItemToSql(item)

db.makeHashId("Nirav", "Kiran", "Kalpesh")
print(db.getCurrentDate())

pagesave_path = "E:/Nirav/Learning/scrapy-pipeline/Pagesave"
os.makedirs(pagesave_path, exist_ok=True)

filename = "main.text"
# db.makePageSave(pagesave_path, filename, "Hello, Nirav")
# response = db.readPageSave(pagesave_path, filename)

db.ExpressVPNChangeLocation()