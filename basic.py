# https://www.finlab.tw/one-line-info-dataframe/

import datetime
import pandas as pd
import warnings
import requests
from io import StringIO
import time
import random


n_days = 9
date = datetime.datetime.now()

def crawler(date):

    datestr = date.strftime('%Y%m%d')
    print(datestr)

    url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date='+datestr+'&selectType=ALL'
    res = requests.get(url)
    df = pd.read_csv(StringIO(res.text), header=1)
    # print(df)
    df['本益比'] = pd.to_numeric(df['本益比'], errors='coerce')
    df['date'] = date
    
    return df.dropna(thresh=3).dropna(thresh=0.8, axis=1)


# df = crawler(datetime.date(2020,3,12))
# df.to_csv('data/basic.csv', index=False)

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
        df.to_csv('data/basic/basic_{}.csv'.format(date1), index=False)

    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            break
    date1 = date1 + day
    time.sleep(random.randint(5,10))


# https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=20210312&selectType=ALL