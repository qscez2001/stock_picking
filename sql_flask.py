# https://blog.liang2.tw/posts/2015/09/flask-draw-member/
import sqlite3
from flask import Flask, g
from flask import render_template
from flask_table import Table, Col
import pandas as pd

app = Flask(__name__)
DATABASE = 'data/my.db'


# Declare your table
class ItemTable(Table):
    classes = ['table']
    id = Col('證券代號')
    name = Col('證券名稱')
    price = Col('收盤價')
    本益比 = Col('本益比')
    股價淨值比 = Col('股價淨值比')
    殖利率 = Col('殖利率')
    上月比較增減 = Col('上月比較增減')
    去年同月增減 = Col('去年同月增減')
    前期比較增減 = Col('前期比較增減')
    三大法人買賣超股數 = Col('三大法人買賣超股數')
    成交金額 = Col('成交金額')
    日期 = Col('日期')

# Get some objects
class Item(object):
    def __init__(self, list):
        self.id = list[0]
        self.name = list[1]
        self.price = list[2]
        self.本益比 = list[3]
        self.股價淨值比 = list[4]
        self.殖利率 = list[5]
        self.上月比較增減 = list[6]
        self.去年同月增減 = list[7]
        self.前期比較增減 = list[8]
        self.三大法人買賣超股數 = list[9]
        self.成交金額 = list[10]
        self.日期 = list[11]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')


import random
from flask import request


@app.route('/draw', methods=['POST'])
def draw():
    # Get the database connection
    db = get_db()

    # Draw member ids from given group
    # If ALL is given then draw from all members
    group_name = request.form.get('group_name')
    date = request.form.get('date')
    
    valid_members_sql = "SELECT p.證券代號,p.證券名稱,p.收盤價,b.本益比, b.股價淨值比, b.[殖利率(%)], m.[上月比較增減(%)], m.[去年同月增減(%)] , m.[前期比較增減(%)], \
        c.三大法人買賣超股數, p.成交金額, p.日期 FROM processed_multiple_basic as b \
        join processed_multiple_chips as c on (b.日期 = c.日期 AND b.證券代號 = c.證券代號) \
        join processed_multiple_price as p on (b.日期 = p.日期 AND b.證券代號 = p.證券代號) \
        join joined_multiple_month_income as m on (b.日期 = m.d AND b.證券代號 = m.公司代號) \
        WHERE p.日期 = '{}' ".format(date)
    
    if group_name == 'ALL':
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]
    elif group_name == "本益比":
        valid_members_sql += "AND b.本益比 < 15 ORDER BY b.本益比 LIMIT 150"
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]
    elif group_name == "股價淨值比":
        valid_members_sql += 'AND 股價淨值比 < 1.2 ORDER BY b.股價淨值比 LIMIT 150'
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]
    elif group_name == "殖利率(%)":
        valid_members_sql += 'AND [殖利率(%)] > 5 ORDER BY b.[殖利率(%)] desc LIMIT 150'
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]

    elif group_name == "上月比較增減(%)":
        valid_members_sql += 'AND m.[上月比較增減(%)] > 20 ORDER BY m.[上月比較增減(%)] desc LIMIT 150'
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]
    elif group_name == "去年同月增減(%)":
        valid_members_sql += 'AND m.[去年同月增減(%)] > 20 ORDER BY m.[去年同月增減(%)] desc LIMIT 150'
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]
    elif group_name == "前期比較增減(%)":
        valid_members_sql += 'AND m.[前期比較增減(%)] > 20 ORDER BY m.[前期比較增減(%)] desc LIMIT 150'
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]

    elif group_name == "三大法人買賣超股數":
        valid_members_sql += 'ORDER BY c.三大法人買賣超股數 desc LIMIT 150'
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]   

    elif group_name == "成交金額":
        valid_members_sql += 'ORDER BY p.成交金額 desc LIMIT 150'
        cursor = db.execute(valid_members_sql).fetchall()
        valid_member_ids = [row[0] for row in cursor]  

    elif group_name == "連續上漲3天":
        df = pd.read_sql_query("SELECT * FROM time_series_close_v1", db)
        headers = list(df.columns.values)
        headers = headers[1:]

        original_date = date
        date = date.split("-")
        date = "_".join(date)
        date = "Column_" + date

        if date in headers:
            i = headers.index(date)
            if i >= 2:
                today = headers[i]
                prev_day = headers[i-1]
                pprev_day = headers[i-2]

                valid_members_sql = "SELECT pr.證券代號,pr.證券名稱,pr.收盤價,b.本益比,b.股價淨值比,b.[殖利率(%)],m.[上月比較增減(%)],m.[去年同月增減(%)],m.[前期比較增減(%)],c.三大法人買賣超股數,pr.成交金額,pr.日期 \
                FROM time_series_close_v1 as p \
                JOIN processed_multiple_basic as b on p.[Unnamed: 0] = b.證券代號\
                JOIN processed_multiple_chips as c on (p.[Unnamed: 0] = c.證券代號 AND b.日期 = c.日期 ) \
                JOIN processed_multiple_price as pr on (p.[Unnamed: 0] = pr.證券代號 AND b.日期 = pr.日期) \
                JOIN joined_multiple_month_income as m on (p.[Unnamed: 0] = m.公司代號 AND b.日期 = m.d) \
                WHERE {} > {} AND {} > {} AND pr.日期 = '{}'\
                ".format(today, prev_day, prev_day, pprev_day, original_date) 


                cursor = db.execute(valid_members_sql).fetchall()

                valid_member_ids = [row[0] for row in cursor]  
        else:
            print("No data, it's holiday")

    # If no valid members return 404 (unlikely)
    if not valid_member_ids:
        err_msg = "<p>No Results</p>"
        return err_msg, 404
        
    filtered = []
    for i in range(len(cursor)):

        table_ele = Item(cursor[i])
        filtered.append(table_ele)


    table = ItemTable(filtered)

    return render_template(
        'draw.html',
        res_table = table.__html__()
    )
    '''
    收盤價
    本益比, 股價淨值比, 殖利率(%), 
    上月比較增減(%), 去年同月增減(%), 前期比較增減(%), 
    三大法人買賣超股數, 成交金額
    '''

if __name__ == '__main__':
    app.static_folder = 'static'
    app.run(debug=True)

