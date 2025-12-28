import hashlib
import json

import pymysql as sql


# import pymongo as mongo


class ConfigDatabase():

    def __init__(self, database, table, host="localhost", user="root", password="actowiz", type1="sql"):
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
        # if type1 == 'mongo':
        #     self.connMongo = mongo.MongoClient(f"mongodb://{host}:27017/")
        #     self.dbmongo = self.connMongo[self.database]
        self.crsrSql = self.connSql.cursor(sql.cursors.DictCursor)

    # def hash_generate(self, fields):
    #     hashid = int(hashlib.md5(bytes("".join(fields) , "utf8")).hexdigest(),16) % (10 ** 30)
    #     return hashid

    def fetchResultsfromSql(self, fields=[], conditions={},conditions1={}, not_conditions={}, start=0, end=100000000):

        fieldtofetch = ",".join(fields) if fields else "*"
        cond = [f"`{key}`='{value}'" for key, value in conditions.items() if conditions]
        cond1 = [f"`{key}`='{value}'" for key, value in conditions1.items() if conditions1]
        not_cond = [f"`{key}` NOT LIKE '%{value}%'" for key, value in not_conditions.items() if not_conditions]
        cond = f'{" and ".join(cond)} and' if cond else ""
        cond1 = f'{" and ".join(cond1)} and' if cond1 else ""
        not_cond = f'{" and ".join(not_cond)} and' if not_cond else ""
        # cond = f'{" and ".join(cond)} and' if cond else ""
        # print(f"select {fieldtofetch} from {self.table} {cond} and id between {start} and {end}")
        if not_conditions:
            self.crsrSql.execute(
                f"select {fieldtofetch} from {self.table} where {cond} {not_cond} id between {start} and {end}")
        else:
            # self.crsrSql.execute(f"select {fieldtofetch} from {self.table} where {cond} id between {start} and {end}")
            self.crsrSql.execute(f"select {fieldtofetch} from {self.table} where {cond} {cond1} id between {start} and {end}")

        # self.crsrSql.execute(f"select {fieldtofetch} from {self.table} where {cond} id between {start} and {end}")
        # self.crsrSql.execute(f"select {fieldtofetch} from {self.table} {cond} limit {start},{end}")
        results = self.crsrSql.fetchall()
        return results

    # def fetchResultsfromSqlone(self, fields=[], conditions={}, start=0, end=1):
    #
    #     fieldtofetch = ",".join(fields) if fields else "*"
    #     cond = [f"`{key}`='{value}'" for key, value in conditions.items() if conditions]
    #     cond = f'where {" and ".join(cond)} ' if cond else ""
    #     # print(f"select {fieldtofetch} from {self.table} {cond} and id between {start} and {end}")
    #
    #     # self.crsrSql.execute(f"select {fieldtofetch} from {self.table} {cond} and id between {start} and {end}")
    #     self.crsrSql.execute(f"select {fieldtofetch} from {self.table} {cond} limit {start},{end}")
    #     results = self.crsrSql.fetchone()
    #     return results

    def fetchResultsfromSql_2(self, fields=[], ):

        fieldtofetch = ",".join(fields) if fields else "*"
        self.crsrSql.execute(f"select {fieldtofetch} from {self.table} ")
        results = self.crsrSql.fetchall()
        return results

    def insertItemToSql(self, item):
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

            insert_db = f"INSERT IGNORE INTO {self.table} ({fields}) VALUES ({placeholders_str})"

            self.crsrSql.execute(insert_db, value_list)
            self.connSql.commit()

            print("Item Successfully Inserted...")

        except Exception as e:
            print("Error:", str(e))
    def insertItemToMongo(self, item):

        try:
            self.dbmongo[self.table].insert_one(item)
        except Exception as e:
            print(e)

    def updateStatusSql(self, item, ):

        try:
            update = f"update {self.table} set status='done' where cat = '{item['StoreId']}'"
            self.crsrSql.execute(update)
            self.connSql.commit()
        except Exception as e:
            print(e)
