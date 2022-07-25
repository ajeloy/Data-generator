import mysql.connector
from mysql.connector import *
import random
import string
import decimal
from datetime import timedelta
from datetime import datetime
from random import randrange
import argparse

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    new_date = start + timedelta(seconds=random_second)
    return new_date.strftime("%Y-%m-%d %H:%M:%S")

def generate_fake_data(types):
    fake_data = []
    for type in types:
        if "int" in type: 
            fake_data.append(str(random.randint(3, 9)))
        if "varchar" in type: 
            letters = string.ascii_lowercase
            fake_data.append(''.join(random.choice(letters) for i in range(4)))
        if "datetime" in type: 
            d1 = datetime.strptime('2020-05-06 09:55:22', "%Y-%m-%d %H:%M:%S")
            d2 = datetime.strptime('2022-07-20 18:01:22', "%Y-%m-%d %H:%M:%S")
            fake_data.append(random_date(d1, d2))  
        if "text" in type: 
            letters = string.ascii_lowercase
            fake_data.append(''.join(random.choice(letters) for i in range(15)))
        if "decimal" in type: 
            fake_data.append(str(float(decimal.Decimal(random.randrange(155, 389))/100)))
        if "float" in type: 
            fake_data.append(str(float(decimal.Decimal(random.randrange(103, 749))/100)))
    return "', '".join(fake_data)

def prepare_column_names(column_names):
    col_names_data = []
    for col in column_names:
        sub1 = "('"
        sub2 = "',)"

        idx1 = str(col).find(sub1)
        idx2 = str(col).find(sub2)

        res = ''
        for idx in range(idx1 + len(sub1), idx2):
            res = res + str(col)[idx]
        col_names_data.append(res)
    return '`, `'.join(col_names_data)

parser = argparse.ArgumentParser(description="Arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("user", help="Username")
parser.add_argument("password", help="Password")
parser.add_argument("database", help="Database name")
parser.add_argument("table", help="Table name")
parser.add_argument("rows", help="Number of rows to insert")
args = parser.parse_args()
config = vars(args)

con = False

con = connection = create_server_connection("localhost", args.user, args.password)

query_get_cols_type = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='" + args.database + "' AND TABLE_NAME='" + args.table + "'"
result_col_types = read_query(connection, query_get_cols_type)
result_col_types.pop(0)

query_get_cols_name = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='" + args.database + "' AND TABLE_NAME='" + args.table + "'"
result_col_names = read_query(connection, query_get_cols_name)
result_col_names.pop(0)

col_names = prepare_column_names(result_col_names)
col_names = '`' + col_names + '`'

for i in range(int(args.rows)):
    fake_data = generate_fake_data(result_col_types)
    fake_data = "'" + fake_data + "'"
    query = "insert into " + args.database + "." + args.table + " (" + col_names + ") values (" + fake_data + ")"
    execute_query(con, query)
