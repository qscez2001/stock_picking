import pandas as pd

df = pd.read_csv("processed_multiple_basic.csv")
df = df.rename(columns={"date": "日期"})
df.to_csv("processed_multiple_basic.csv", index=False)

df = pd.read_csv("processed_multiple_chips.csv")
df = df.rename(columns={"date": "日期"})
df.to_csv("processed_multiple_chips.csv", index=False)

df = pd.read_csv("processed_multiple_price.csv")
df = df.rename(columns={"date": "日期"})
df.to_csv("processed_multiple_price.csv", index=False)

df = pd.read_csv("processed_multiple_month_income.csv")
df = df.rename(columns={"date": "日期"})
df.to_csv("processed_multiple_month_income.csv", index=False)
