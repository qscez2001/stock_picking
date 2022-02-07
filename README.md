
# crawling

python basic.py
python chips.py
python income.py
python price.py
python time_series.py

# preprocessing data

python only_compony.py
python modify.py
data/modify_month_income.py
data/process/rename.py

# create db

cd data
rm my.db
csvs-to-sqlite process/*.csv my.db
cd ..

# process table
python create_join_month_income.py

# main application
python sql_flask.py

# static folder
UI images and css