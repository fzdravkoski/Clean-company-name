import sqlite3
import pymongo
from cleanco import basename
import re


#Empty dictionary and 2 lists used in the functions below.
table_dict = {}
lst_of_companies = []
all_companies =[]


def get_db_mongo():
    """
    Connecting to MongoDB and creating the database called Company with 'Companies' collection.
    :return: Returning the collection in Company database.
    """
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['Company']
    collection = db['companies']
    return collection


def sqlite_conn():
    """
    Establishing a connection to the data.db file.
    :return: returning the connection
    """
    conn = sqlite3.connect('data.db')
    return conn


def get_one_company(name):
    """
    If statement for checking for empty spaces in the name
    :data: Executing a query that searches the sqlite database for a specific name
    :param name: passing a name of a company
    :return: Query return
    """
    if ' ' in name:
        conn = sqlite_conn()
        c = conn.cursor()
        data = c.execute('SELECT * FROM companies WHERE name="{get_name}"'.format(get_name=name)).fetchone()
    return data


def get_data_sqlite_full_data():
    """
    Connecting to the sqlite database
    Query for selecting 1000 companies from data.db
    A FOR loop to iterate the query
    :table-dict: Used to store the data in a dictionary and then append them in an empty list.
    :return: returning the list of companies.
    """
    conn = sqlite_conn()
    table_data = conn.execute('SELECT * FROM companies LIMIT 1000')
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
    """
    :one_company: Getting one company for clearing from the get_one_company function
    :db: Establishing a connection to Mongo.
    :param name: passing the name of the company we want to clear
    :db.create.index: Making the name a unique index since the primary key in Mongo is always the _id
    :upload_files: Using the upload_files function to upload the dictionary containing the company info in MongoDB.
    :return: returning the company that we have cleaned.
    """
    one_company = list(get_one_company(name))
    db = get_db_mongo()
    db.create_index([("Name", pymongo.TEXT)], unique=True)
    cleaned_name = re.sub("(^|[.?!&])\s*([a-zA-Z])", lambda name: name.group().upper(), one_company[1])
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
    """
    :param db: Db is a passed variable used for the Company database in Mongo
    :param table_dict: The dict that contains info of the cleaned company that we need to upload to Mongodb.
    :return:
    """
    db.insert_one(table_dict)


def get_cleaned_companies():
    """
    Connecting to MongoDB using the get_db_mongo function
    Iterating through the data in the database, in which we remove the _id from displaying
    Uploading the files in an empty list
    :return: returning the list.
    """
    db = get_db_mongo()
    for companies in db.find({},{"_id": 0}):
        all_companies.append(companies)
    return all_companies


