# https://www.finlab.tw/%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E7%88%AC%E8%9F%B2/
import datetime
import requests
from io import StringIO
import pandas as pd
import time
import random

def crawler(date):

    datestr = date.strftime('%Y%m%d')

    r = requests.get('http://www.tse.com.tw/fund/T86?response=csv&date='+datestr+'&selectType=ALLBUT0999')
    
    df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any')
    df['date'] = date
    df.sort_index()

    return df


# df = crawler(datetime.date(2020,3,12))
# df.to_csv('data/chips.csv', index=False)

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
        df.to_csv('data/chips/chips_{}.csv'.format(date1), index=False)

    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            break
    date1 = date1 + day
    time.sleep(random.randint(5,10))

'''
股票：1~31
<select name="selectType">
          <option value="ALL">全部</option>
          <option value="ALLBUT0999">全部(不含權證、牛熊證、可展延牛熊證)</option>
          <option value="0049">封閉式基金</option>
          <option value="0099P">ETF</option>
          <option value="029999">ETN</option>
          <option value="019919T">受益證券</option>
          <option value="0999">認購權證(不含牛證)</option>
          <option value="0999P">認售權證(不含熊證)</option>
          <option value="0999C">牛證(不含可展延牛證)</option>
          <option value="0999B">熊證(不含可展延熊證)</option>
          <option value="0999X">可展延牛證</option>
          <option value="0999Y">可展延熊證</option>
          <option value="0999GA">附認股權特別股</option>
          <option value="0999GD">附認股權公司債</option>
          <option value="0999G9">認股權憑證</option>
          <option value="01" selected="">水泥工業</option>
          <option value="02">食品工業</option>
          <option value="03">塑膠工業</option>
          <option value="04">紡織纖維</option>
          <option value="05">電機機械</option>
          <option value="06">電器電纜</option>
          <option value="07">化學生技醫療</option>
          <option value="21">化學工業</option>
          <option value="22">生技醫療業</option>
          <option value="08">玻璃陶瓷</option>
          <option value="09">造紙工業</option>
          <option value="10">鋼鐵工業</option>
          <option value="11">橡膠工業</option>
          <option value="12">汽車工業</option>
          <option value="13">電子工業</option>
          <option value="24">半導體業</option>
          <option value="25">電腦及週邊設備業</option>
          <option value="26">光電業</option>
          <option value="27">通信網路業</option>
          <option value="28">電子零組件業</option>
          <option value="29">電子通路業</option>
          <option value="30">資訊服務業</option>
          <option value="31">其他電子業</option>
          <option value="14">建材營造</option>
          <option value="15">航運業</option>
          <option value="16">觀光事業</option>
          <option value="17">金融保險</option>
          <option value="18">貿易百貨</option>
          <option value="23">油電燃氣業</option>
          <option value="9299">存託憑證</option>
          <option value="19">綜合</option>
          <option value="20">其他</option>
          <option value="CB">可轉換公司債</option>
        </select>
'''