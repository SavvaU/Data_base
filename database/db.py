import datetime
import sqlite3

class DBHelper:
    def __init__(self):
        self.db_file = "database.db"

    def _sql_query(self, query, *args):
        with sqlite3.connect(database=self.db_file) as connect:
            cursor = connect.cursor()
            cursor.execute(query, args)
            data = cursor.fetchall()
            connect.commit()
            return data

    def add_customer(self, name:str , passport:int):
        query = """ INSERT INTO customers(name, pasport_number) VALUES (?,?)"""
        self._sql_query(query,name, passport)


    def test(self):
        query = """SELECT * FROM customers"""
        data = self._sql_query(query)
        return data
db = DBHelper()
db.add_customer("Ильсаф", 1234567)
# print(db.test())