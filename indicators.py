import pickle
import pandas as pd

infile = open("time_series_data.pk",'rb')
data = pickle.load(infile)
infile.close()

close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
close.index = pd.to_datetime(close.index)
# print(close)
close.to_csv("time_series_close.csv")

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

tsmc['close'].plot()

# KD
from talib import abstract

def talib2df(talib_output):
    if type(talib_output) == list:
        ret = pd.DataFrame(talib_output).transpose()
    else:
        ret = pd.Series(talib_output)
    ret.index = tsmc['close'].index
    return ret;

talib2df(abstract.STOCH(tsmc)).plot()
fig = tsmc['close'].plot(secondary_y=True).get_figure()
fig.savefig('kd.pdf')
# MACD
talib2df(abstract.MACD(tsmc)).plot()
fig = tsmc['close'].plot(secondary_y=True).get_figure()
fig.savefig('MACD.pdf')

talib2df(abstract.OBV(tsmc)).plot()
fig = tsmc['close'].plot(secondary_y=True).get_figure()
fig.savefig('OBV.pdf')

talib2df(abstract.WILLR(tsmc)).plot()
fig = tsmc['close'].plot(secondary_y=True).get_figure()
fig.savefig('WILLR.pdf')

talib2df(abstract.ATR(tsmc)).plot()
fig = tsmc['close'].plot(secondary_y=True).get_figure()
fig.savefig('ATR.pdf')
