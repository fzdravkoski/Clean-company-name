import sqlite3
import pymongo
from cleanco import basename
import string
import re
import requests

def get_db_mongo():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['Company']
    collection = db['companies']
    return collection


table_dict = {}
lst_of_companies = []
all_companies =[]
search = ''
def sqlite_conn():
    conn = sqlite3.connect('data.db')
    return conn


def get_one_company(name):
    if ' ' in name:
        conn = sqlite_conn()
        c = conn.cursor()
        data = c.execute('SELECT * FROM companies WHERE name="{get_name}"'.format(get_name=name)).fetchone()
    return data


def get_data_sqlite_full_data():
    conn = sqlite_conn()
    table_data = conn.execute('SELECT * FROM companies')
    i = 0
    for data in list(table_data):
        table_dict = {
            "Id" : data[0],
            "Name" :data[1],
            "Country": data[2],
            "City" : data[3],
            "Nace" : data[4],
            "Website": data[5]
            }
        lst_of_companies.append(table_dict)

    return lst_of_companies


def clean_one_company(name):
    one_company = list(get_one_company(name))
    db = get_db_mongo()
    db.create_index([("Name", pymongo.TEXT)], unique=True)
    cleaned_name = re.sub("(^|[.?!&])\s*([a-zA-Z])", lambda name: name.group().upper(), one_company[1])
    name = cleaned_name.title()
    table_dict = {
        "Id" : one_company[0],
        "Name": basename(cleaned_name.title().strip().replace('.','').replace('‰','').replace(':','').replace('(','').replace(')','')),
        "Country": one_company[2],
        "City": one_company[3],
        "Nace": one_company[4],
        "Website": one_company[5]
        }
    upload_files(db, table_dict)
    return one_company



def upload_files(db, table_dict):
    db.insert_one(table_dict)


def get_cleaned_companies():
    db = get_db_mongo()
    for companies in db.find({},{"_id": 0}):
        all_companies.append(companies)
    return all_companies


