# https://www.finlab.tw/Python-%E6%99%82%E9%96%93%E5%BA%8F%E5%88%97%E5%AF%A6%E4%BD%9C%EF%BC%81/
import requests
from io import StringIO
import pandas as pd
import numpy as np
import random

def crawl_price(date):

    datestr = date.strftime('%Y%m%d')

    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in r.text.split('\n') 
                                        if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
    ret['成交金額'] = ret['成交金額'].str.replace(',','')
    ret['成交股數'] = ret['成交股數'].str.replace(',','')
    return ret


import datetime
import time
import pickle

data = {}
date1 = datetime.date(2020,9,22)
date2 = datetime.date(2020,12,22)
# date2 = datetime.date(2020,2,15)
fail_count = 0
allow_continuous_fail_count = 5
day = datetime.timedelta(days=1)
while date1 <= date2:

    print('parsing', date1)
    # 使用 crawPrice 爬資料
    try:
        # 抓資料
        data[date1] = crawl_price(date1)
        print('success!')
        fail_count = 0

    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            break
    
    # 減一天
    # date -= datetime.timedelta(days=1)
    date1 = date1 + day
    time.sleep(random.randint(5,10))

# print(data)

outfile = open("time_series_data.pk",'wb')
pickle.dump(data, outfile)
outfile.close()

close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
close.index = pd.to_datetime(close.index)
# print(close)
close.to_csv("time_series_close.csv")

'''
open = pd.DataFrame({k:d['開盤價'] for k,d in data.items()}).transpose()
open.index = pd.to_datetime(open.index)

high = pd.DataFrame({k:d['最高價'] for k,d in data.items()}).transpose()
high.index = pd.to_datetime(high.index)

low = pd.DataFrame({k:d['最低價'] for k,d in data.items()}).transpose()
low.index = pd.to_datetime(low.index)

volume = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
volume.index = pd.to_datetime(volume.index)


tsmc = {
    'close':close['2330']['2020'].dropna().astype(float),
    'open':open['2330']['2020'].dropna().astype(float),
    'high':high['2330']['2020'].dropna().astype(float),
    'low':low['2330']['2020'].dropna().astype(float),
    'volume': volume['2330']['2020'].dropna().astype(float),
}

fig = tsmc['close'].plot().get_figure()
fig.savefig('test.pdf')
'''
