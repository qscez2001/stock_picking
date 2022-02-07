import pandas as pd
import re
import os

path = 'data/process/'

def chips():

    df = pd.read_csv('data/chips.csv')
    # print(df)
    for i in range(len(df)):
        code = df.loc[i, "證券代號"]
        df.loc[i, "證券代號"] = re.sub(r'^="(\w+)"', r'\1', code)

        if len(df.loc[i, "證券代號"]) != 4:
            df.drop(i, inplace=True)

    df = df.sort_values(by=["證券代號"])
    df = df.reset_index(drop=True)
    # print(len(df))
    # print(df)
    df.to_csv(path + 'processed_chip.csv', index_label="id")

# chips()

def multiple_chips():
    file_path = 'data/chips/'
    files = os.listdir(file_path)
    whole_df = None
    for f in files:
        df = pd.read_csv(file_path + f)
        # print(df)
        for i in range(len(df)):
            code = df.loc[i, "證券代號"]
            df.loc[i, "證券代號"] = re.sub(r'^="(\w+)"', r'\1', code)

            if len(df.loc[i, "證券代號"]) != 4:
                df.drop(i, inplace=True)

        df = df.sort_values(by=["證券代號"])

        whole_df = pd.concat([whole_df, df])
    whole_df = whole_df.sort_values(by=["證券代號"])
    whole_df = whole_df.reset_index(drop=True)
    whole_df.to_csv(path + 'processed_multiple_chips.csv', index_label="id")

# multiple_chips()

def price():
    df = pd.read_csv('data/price.csv')
    # print(df)
    for i in range(len(df)):
        code = df.loc[i, "證券代號"]
        df.loc[i, "證券代號"] = re.sub(r'^="(\w+)"', r'\1', code)

        if len(df.loc[i, "證券代號"]) != 4:
            df.drop(i, inplace=True)

    df = df.sort_values(by=["證券代號"])
    # print(len(df))
    # print(df)

    df.to_csv(path + 'processed_price.csv', index_label="id")

# price()

def multiple_prices():
    file_path = 'data/price/'
    files = os.listdir(file_path)
    # print(files)
    whole_df = None
    for f in files:
        df = pd.read_csv(file_path + f)
        # print(df)
        for i in range(len(df)):
            code = df.loc[i, "證券代號"]
            df.loc[i, "證券代號"] = re.sub(r'^="(\w+)"', r'\1', code)

            if len(df.loc[i, "證券代號"]) != 4:
                df.drop(i, inplace=True)

        df = df.sort_values(by=["證券代號"])

        whole_df = pd.concat([whole_df, df])
        # print(len(whole_df))
        # print(whole_df)
        # whole_df = whole_df.sort_values(by=["證券代號"])
        # whole_df = whole_df.reset_index(drop=True)
        # whole_df.to_csv(path + 'small_processed_multiple_price.csv', index_label="id")

    whole_df = whole_df.sort_values(by=["證券代號"])
    whole_df = whole_df.reset_index(drop=True)
    whole_df.to_csv(path + 'processed_multiple_price.csv', index_label="id")

# multiple_prices()

def basic():
    df = pd.read_csv('data/basic.csv')
    # print(df["證券代號"])
    # print(df.loc["證券代號"])
    for i in range(len(df)):
        code = df.loc[i, "證券代號"]
        if len(str(code)) != 4:
            df.drop(i, inplace=True)

    df = df.sort_values(by=["證券代號"])
    # print(len(df))
    # print(df)

    df.to_csv(path + 'processed_basic.csv', index_label="id")

# basic()

def multiple_basic():
    file_path = 'data/basic/'
    files = os.listdir(file_path)
    # print(files)
    whole_df = None
    for f in files:
        df = pd.read_csv(file_path + f)
        # print(df["證券代號"])
        # print(df.loc["證券代號"])
        for i in range(len(df)):
            code = df.loc[i, "證券代號"]
            if len(str(code)) != 4:
                df.drop(i, inplace=True)

        df = df.sort_values(by=["證券代號"])
        whole_df = pd.concat([whole_df, df])

    whole_df = whole_df.sort_values(by=["證券代號"])
    whole_df = whole_df.reset_index(drop=True)
    whole_df.to_csv(path + 'processed_multiple_basic.csv', index_label="id")

# multiple_basic()

def month_income():
    df = pd.read_csv('data/month_income.csv', encoding='utf-8')
    # print(df)
    for i in range(len(df)):
        code = df.loc[i, "公司代號"]

        if len(str(code)) != 4:
            df.drop(i, inplace=True)

    df = df.sort_values(by=["公司代號"])
    # print(len(df))
    # print(df)

    df.to_csv(path + 'processed_month_income.csv', index_label="id")

# month_income()

def multiple_month_income():
    file_path = 'data/income/'
    files = os.listdir(file_path)
    # print(files)
    whole_df = None
    for f in files:
        df = pd.read_csv(file_path + f)
        for i in range(len(df)):
            code = df.loc[i, "公司代號"]

            if len(str(code)) != 4:
                df.drop(i, inplace=True)

        # df = df.sort_values(by=["公司代號"])
        whole_df = pd.concat([whole_df, df])

    whole_df = whole_df.sort_values(by=["公司代號"])
    whole_df = whole_df.reset_index(drop=True)
    whole_df.to_csv(path + 'processed_multiple_month_income.csv', index_label="id")

multiple_month_income()