import datetime
import sqlite3

class DBHelper:
    def __init__(self):
        self.db_file = "database/database.db"

    def _sql_query(self, query, *args):
        with sqlite3.connect(database=self.db_file) as connect:
            cursor = connect.cursor()
            cursor.execute(query, args)
            data = cursor.fetchall()
            connect.commit()
            return data

    def add_customer(self, name:str , passport:int):
        query = """ INSERT INTO customers(name, passport_number) VALUES (?,?)"""
        self._sql_query(query,name, passport)


    def test(self):
        query = """SELECT * FROM customers"""
        data = self._sql_query(query)
        return data

    def get_cust_by_passport(self, passport:int):
        query = """SELECT * FROM customers
                WHERE passport_number = ?"""
        data = self._sql_query(query, passport)
        return data

    def get_customers_list(self):
        query = """SELECT * FROM customers"""
        data = self._sql_query(query)
        return data

    #нерабочие шаблоны
    def chek_customer_abbility(self, passport:int):
        query = """SELECT * FROM payments 
        WHERE credit_id = ? AND status = 0 AND date < ?"""
        return True

    def is_this_customer_in_db(self,passport:int):
        queue = """SELECT * FROM customers WERE passport = ?"""
        data = self._sql_query(queue,int(passport))
        return data
def create_db() -> DBHelper:
    if not hasattr(create_db, 'db'):
        setattr(create_db, 'db', DBHelper())
    return create_db.db


def format_list(lst):
    result = 'Имя   Паспорт:\n'
    for item in lst:
        result += f'{item[1]}   {item[2]}\n'
    return result
