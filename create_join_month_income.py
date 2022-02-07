# db is from https://github.com/simonw/csvs-to-sqlite
import sqlite3
import pandas as pd
import datetime
# Create your connection.
sql_connect = sqlite3.connect('data/my.db')

# version of raw SQL
cursor = sql_connect.cursor()

# sql_command = "SELECT * FROM joined_multiple_month_income"
# cursor.execute(sql_command) 

# for row in cursor:
#     print(row)

sql_command = "CREATE TABLE joined_multiple_month_income AS select * from processed_multiple_month_income as a join month_to_date as b on a.日期 = b.fk"

cursor.execute(sql_command) 
print(len(list(cursor)))
# for row in cursor:
#     print(row)

sql_connect.close()
