#!/sh
# crawling

# python basic.py
# python chips.py
# python income.py
# python price.py

# processing data

# python only_compony.py

# crawing time_series data

# python time_series.py

# processing time_series data

# python modify.py

# create db

cd data
rm my.db
csvs-to-sqlite process/*.csv my.db
cd ..

python create_join_month_income.py
python sql_flask.py
