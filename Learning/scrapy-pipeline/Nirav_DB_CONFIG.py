import hashlib
from datetime import datetime
import pymysql as sql
from loguru import logger
from pymongo import MongoClient
from pathlib import Path


class ConfigDatabase:
    def __init__(self, database, table, host="localhost", user="root", password="actowiz"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.con1 = sql.connect(host=self.host, user=self.user, password=self.password)
        self.con1.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.connSql = sql.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database, autocommit=True
        )
        self.connSql.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.crsrSql = self.connSql.cursor(sql.cursors.DictCursor)
        self.connMongo = MongoClient(f"mongodb://{host}:27017/")
        self.dbmongo = self.connMongo[self.database]

    # Todo: SQL Section
    def fetchResultsfromSql(self, fields=[], conditions={}, not_conditions={}, start=0, end=100000000):
        fieldtofetch = ",".join(fields) if fields else "*"
        cond = [f"`{key}`='{value}'" for key, value in conditions.items() if conditions]
        not_cond = [f"`{key}` NOT LIKE '%{value}%'" for key, value in not_conditions.items() if not_conditions]
        cond = f'{" and ".join(cond)} and' if cond else ""
        not_cond = f'{" and ".join(not_cond)} and' if not_cond else ""

        # Todo: Between Query
        if not_conditions:
            self.crsrSql.execute(
                f"select {fieldtofetch} from {self.table} where {cond} {not_cond} id between {start} and {end}")
        else:
            self.crsrSql.execute(f"select {fieldtofetch} from {self.table} where {cond} id between {start} and {end}")

        # Todo: Limit Query
        # self.crsrSql.execute(f"select {fieldtofetch} from {self.table} {cond} limit {start},{end}")
        results = self.crsrSql.fetchall()
        return results

    # Todo: Insert Data
    def insertItemToSql(self, item):
        try:
            field_list = []
            value_list = []
            for field in item:
                field_list.append(str(f"`{field}`"))
                value_list.append(str(item[field]).replace("'", "''"))
            fields = ','.join(field_list)
            values = "','".join(value_list)
            insert_db = f"insert into {self.table}" + "( " + fields + " ) values ( '" + values + "' )"
            self.crsrSql.execute(insert_db)
            self.connSql.commit()
            logger.success(f"Item Successfully Inserted...")
        except Exception as e:
            logger.error(e)

    # Todo: Update Data
    def updateStatusSql(self, item):
        try:
            update = f"update {self.table} set status='done' where cat = '{item['StoreId']}'"
            self.crsrSql.execute(update)
            self.connSql.commit()
        except Exception as e:
            logger.error(e)

    # Todo: Insert Using MongoDB
    def insertItemToMongo(self, item):
        try:
            self.dbmongo[self.table].insert_one(item)
        except Exception as e:
            logger.error(e)

    # Todo: Make HashID
    def makeHashId(self, *args):
        try:
            hash_id = str(
                int(hashlib.md5(bytes(str(args[0]) + str(args[1]) + str(args[2]), "utf8")).hexdigest(), 16) % (
                        10 ** 10))
            return hash_id
        except Exception as e:
            logger.error(e)

    # Todo: Get CurrentDate
    def getCurrentDate(self):
        current_time = datetime.now().strftime("%d_%m_%Y")
        return current_time

    # Todo: pageSave
    def makePageSave(self, pagesave_path, filename, response_text):
        pagesave = Path(pagesave_path, filename)
        pagesave.write_text(response_text)

    # Todo: ReadPageSave
    def readPageSave(self, pagesave_path, filename):
        pagesave = Path(pagesave_path, filename)
        return pagesave.read_text()

    def ExpressVPNChangeLocation(self):
        from evpn import ExpressVpnApi
        import random
        import time

        # Define the target countries (case-insensitive match)
        TARGET_COUNTRIES = ["india", "uk", "usa"]

        # Define how long to wait before switching (in seconds)
        SWITCH_INTERVAL = 15 * 60  # 15 minutes

        with ExpressVpnApi() as api:
            # Filter available locations by country
            available_locations = [
                loc for loc in api.locations
                if any(country.lower() in loc["name"].lower() for country in TARGET_COUNTRIES)
            ]

            if not available_locations:
                print("No matching VPN locations for India, UK, or USA.")
            else:
                while True:
                    # Select a random target location
                    selected_location = random.choice(available_locations)

                    try:
                        # Connect to the selected location
                        result = api.connect(selected_location["id"])
                        print(f"[CONNECTED] {selected_location['name']} - Success: {result}")
                    except Exception as e:
                        print(f"[ERROR] Failed to connect to {selected_location['name']}: {e}")

                    # Wait for the next switch
                    print(f"Waiting for {SWITCH_INTERVAL // 60} minutes before next switch...\n")
                    time.sleep(SWITCH_INTERVAL)
