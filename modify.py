import pandas as pd
import datetime

df = pd.read_csv("time_series_close.csv")
print(df)
# df = df.transpose()
df = df.set_index('Unnamed: 0').T
print(df)
df = df.rename(columns={"Unnamed: 0": "Date"})
# df.to_csv("time_series_close_v1.csv", index=False)


# df = pd.read_csv("data/process/time_series_close_v1.csv")

headers = list(df.columns.values)
print(headers)

new_headers = []

for time in headers:
    date = time.split("-")
    print(date)
    date = "_".join(date)
    date = "Column_" + date
    print(date)
    new_headers.append(date)

print(new_headers)

df.columns = new_headers

print(df)

df.to_csv("data/process/time_series_close_v1.csv")

