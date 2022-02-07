import pandas as pd
import datetime
import os

df = pd.read_csv("../time_series_close.csv")
df = df.set_index('Unnamed: 0').T
df = df.rename(columns={"Unnamed: 0": "Date"})
headers = list(df.columns.values)
print(headers)


files = os.listdir("income/")
print(files)

new_headers = []

for time in headers:
    date = time.split("-")
    # print(date)
    date = "-".join(date[:-1])
    new_headers.append(date)

print(new_headers)

month_income = pd.read_csv("process/processed_multiple_month_income.csv")

new_df = None
# for index, row in month_income.iterrows():
    # print(index) 
    # print(row["日期"])
    # if row["日期"] in new_headers:
#     for j in new_headers:
#         if row["日期"] == j:
#             # print(row)
#             new_df = pd.concat([new_df, df])

# print(len(new_df))

