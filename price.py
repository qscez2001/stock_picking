# https://www.finlab.tw/%E8%B6%85%E7%B0%A1%E5%96%AE%E5%8F%B0%E8%82%A1%E6%AF%8F%E6%97%A5%E7%88%AC%E8%9F%B2%E6%95%99%E5%AD%B8/
import datetime
import requests
from io import StringIO
import pandas as pd
import numpy as np
import random
import time

def crawler(date):

    datestr = date.strftime('%Y%m%d')

    # 下載股價
    r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999')

    # 整理資料，變成表格
    df = pd.read_csv(StringIO(r.text.replace("=", "")), header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)
    df['date'] = date

    return df


# date1 = datetime.date(2020,3,12)
# print(date1)
# df = crawler(date1)

fail_count = 0
allow_continuous_fail_count = 5
date1 = datetime.date(2020,9,22)
date2 = datetime.date(2020,12,22)
day = datetime.timedelta(days=1)
while date1 <= date2:
    
    print('parsing', date1)
    try:
        
        df = crawler(date1)
        print('success!')
        fail_count = 0
        # save to csv
        df.to_csv('data/price/price_{}.csv'.format(date1), index=False)

    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            break
    date1 = date1 + day
    time.sleep(random.randint(5,10))

# 顯示出來
# print(df)
# df.to_csv('data/price/price_{}.csv'.format(date1), index=False)