import datetime
import sqlite3

from dateutil.relativedelta import relativedelta


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

    def add_customer(self, name: str, passport: int):
        query = """ INSERT INTO customers(name, passport_number) VALUES (?,?)"""
        self._sql_query(query, name, passport)

    def test(self):
        query = """SELECT * FROM customers"""
        data = self._sql_query(query)
        return data

    def get_cust_by_passport(self, passport: int):
        query = """SELECT id FROM customers
               WHERE passport_number = ?"""
        data = self._sql_query(query, passport)
        return data

    def get_credit_by_passport(self):
        query = """SELECT id FROM credits"""
        data = self._sql_query(query)[-1][0]
        return data

    def add_credit(self, passport: int, sum: int, tern: int):
        id = self.get_cust_by_passport(passport)[0][0]
        query = """INSERT INTO credits(sum, term, customer_id, date) VALUES (?, ?, ?, date("now"))"""
        self._sql_query(query, sum, tern, id)
        pay = sum * (0.1 * ((1 + 0.1) ** tern) / (((1 + 0.1) ** tern) - 1))
        id = self.get_credit_by_passport()
        date = datetime.date.today()
        query = """INSERT INTO payments(date, sum, credit_id) VALUES (?, ?, ?)"""
        for i in range(tern):
            date = date + relativedelta(months=1)
            self._sql_query(query, str(date), int(pay), id)

    def create_fee(self):
        query = """SELECT id, sum, date FROM payments WHERE date < date("now") AND state = 0"""
        data = self._sql_query(query)
        query = """UPDATE payments SET fee = ? WHERE id = ?"""
        for payment in data:
            date_object = datetime.datetime.strptime(payment[2], "%Y-%m-%d").date()
            days_delta = datetime.date.today() - date_object
            fee = payment[1] / 100 * days_delta.days
            self._sql_query(query, fee, payment[0])

    def get_customers_list(self):
        query = """SELECT * FROM customers"""
        data = self._sql_query(query)
        return data

    def get_credit_list(self):
        query = """SELECT * FROM credits"""
        data = self._sql_query(query)
        return data

    def get_credit_list_by_passport(self, passport_number:int):
        id = self.get_cust_by_passport(passport_number)[0][0]
        query = """SELECT * FROM credits WHERE customer_id = ?"""
        data = self._sql_query(query, id)
        return data

    def get_payments_list_by_id(self, credit_id:int):
        query = """SELECT * FROM payments WHERE credit_id = ?"""
        return self._sql_query(query, credit_id)

    def get_payments_list_by_id_pay(self, credit_id:int):
        query = """SELECT id, sum, fee FROM payments WHERE credit_id = ? AND state = 0"""
        data = self._sql_query(query, credit_id)
        return data

    def close_pay(self, pay_id:int):
        query = """UPDATE payments SET state = 1, date = date("now") WHERE id = ?"""
        self._sql_query(query, pay_id)

    def chek_customer_abbility(self, passport: int):
        data = self.get_credit_list_by_passport(passport)
        cnt = 0
        for credit in data:
            query = """SELECT * FROM payments WHERE credit_id = ? AND state = 0 AND date < date("now")"""
            data_1 = self._sql_query(query,credit[0])
            print(data_1)
            cnt += len(data_1)
        return False if cnt > 0 else True

    def is_enough_maney(self, sum: int):
        query = """SELECT sum FROM credits"""
        data = self._sql_query(query)
        maney = 0
        for credit in data:
            maney -= credit[0]
        query = """SELECT sum, fee FROM payments WHERE state = 1"""
        data = self._sql_query(query)
        for pay in data:
            maney += pay[0] + pay[1]
        return False if maney < sum else True

    def check_credit_fp(self, credit_id: int):
        self.create_fee()
        query = """SELECT sum, fee FROM payments WHERE credit_id = ? AND state = 0"""
        data = self._sql_query(query, credit_id)
        sum = 0
        for cred in data:
            sum += cred[0] + cred[1]
        return sum

    def close_credit(self, credit_sum: int, credit_id: int):
        query = """DELETE FROM payments WHERE credit_id = ? AND state = 0"""
        self._sql_query(query, credit_id)
        query = """INSERT INTO payments(date, credit_id, sum, state) VALUES (date("now"), ?, ?, 1)"""
        self._sql_query(query, credit_id, credit_sum)

    def close_credit_by_sum(self, pay_sum: int, credit_id: int):
        query = """SELECT id, sum FROM payments WHERE credit_id = ? AND state = 0"""
        data = self._sql_query(query, credit_id)
        query = """DELETE FROM payments WHERE id = ?"""
        i = len(data) - 1
        sum_ = pay_sum
        while sum_ > data[i][1] and i > 0:
            sum_ -= data[i][1]
            self._sql_query(query, data[i][0])
            i -= 1
        query = """UPDATE payments SET sum = ? WHERE id = ?"""
        self._sql_query(query, data[i][1] - sum_, data[i][0])
        query = """INSERT INTO payments(date, sum, credit_id, state) VALUES (date("now"), ?, ?, 1)"""
        self._sql_query(query, pay_sum, credit_id)

    def check_credit(self, credit_id: int):
        query = """SELECT * FROM payments WHERE credit_id = ? AND state = 0"""
        data = self._sql_query(query, credit_id)
        return data

    def check_customers(self):
        data = self.get_customers_list()
        result = []
        for cust in data:
            data1 = self.get_credit_list_by_passport(cust[2])
            cnt = 0
            for credit in data1:
                query = """SELECT sum FROM payments WHERE credit_id = ? AND state = 0 AND date < date("now")"""
                cnt += len(self._sql_query(query, credit[0]))
            if cnt >= 3:
                result.append(cust)
        return result

    def fin_upd(self):
        date = datetime.date.today() - relativedelta(days=365)
        query = """SELECT sum FROM credits WHERE date < ?"""
        data = self._sql_query(query, date)
        maney = 0
        for credit in data:
            maney -= credit[0]
        query = """SELECT sum, fee FROM payments WHERE state = 1 AND date < ?"""
        data = self._sql_query(query, date)
        for pay in data:
            maney += pay[0] + pay[1]
        points = []
        query = """SELECT sum, date FROM credits WHERE date > ?"""
        data = self._sql_query(query, date)
        res = "Финансовый отчет за прошлый год:\nСумма на начало отчетного периода: " + str(maney) + "\n"
        for cred in data:
            a = [-cred[0], cred[1]]
            maney -= cred[0]
            points.append(a)
        query = """SELECT sum, fee, date FROM payments WHERE state = 1 AND date > ?"""
        data = self._sql_query(query, date)
        for pay in data:
            a = [pay[0] + pay[1], pay[2]]
            maney += pay[0] + pay[1]
            points.append(a)
        points = sorted(points, key=lambda x: x[1])
        for cc in points:
            res += "Сумма: " + str(cc[0]) + " Дата: " + str(cc[1]) + "\n"
        res += "Сумма на конец отчетного периода:  " + str(maney)
        return res


def create_db() -> DBHelper:
    if not hasattr(create_db, 'db'):
        setattr(create_db, 'db', DBHelper())
    return create_db.db


def format_list_cust(lst):
    result = 'Имя   Паспорт:\n'
    for item in lst:
        result += f'{item[1]}   {item[2]}\n'
    return result


def format_list_credit(lst):
    result = 'id сумма срок:\n'
    for item in lst:
        result += f'{item[0]}   {item[1]}   {item[2]}\n'
    return result


def format_list_payment(lst):
    result = 'дата      сумма пени статус: \n'
    for item in lst:
        result += f'{item[1]}   {item[2]}   {item[3]}   {item[5]}\n'
    return result
