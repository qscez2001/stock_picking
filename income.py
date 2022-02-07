# https://www.finlab.tw/%E8%B6%85%E7%B0%A1%E5%96%AE%E7%94%A8python%E6%8A%93%E5%8F%96%E6%AF%8F%E6%9C%88%E7%87%9F%E6%94%B6/
# https://ithelp.ithome.com.tw/articles/10204849

import pandas as pd
import requests
from io import StringIO
import time
import datetime

def monthly_report(year, month):
    year_str = year
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    # 上市
    url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    # 上櫃
    # url = 'https://mops.twse.com.tw/nas/t21/otc/t21sc03_'+str(year)+'_'+str(month)+'_1.html'

    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'

    dfs = pd.read_html(StringIO(r.text), encoding='big-5')

    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']

    if month < 12:
        month += 1
    elif month == 12:
        month = 1
    date = datetime.date(year_str, month, 25)
    datestr = date.strftime('%Y-%m')
    print(datestr)

    df['日期'] = datestr 
    
    # 偽停頓
    time.sleep(5)

    return df


# 民國100年1月
# print(monthly_report(109,2))
i = 11
while i != 0:
    monthly_report(2020, i).to_csv('data/income/month_income_{}.csv'.format(i+1), index=False)
    i -= 1