import sqlite3
from flask import Flask, request, render_template, Response, jsonify
import pymongo
import json
from bson.objectid import ObjectId
import re



app = Flask(__name__)


def get_db_mongo():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['Company']
    collection = db['companies']
    return collection


table_dict = {}
lst_of_companies = []

def sqlite_conn():
    conn = sqlite3.connect('data.db')
    return conn
def get_data_sqlite():
    conn = sqlite_conn()
    cursor = conn.cursor()
    table_data = conn.execute('SELECT * FROM companies')
    i = 0
    for data in list(table_data):
        company_id = data[0]
        table_dict = {
            "Name" : data[1],
            "Country": data[2],
            "City" : data[3],
            "Nace" : data[4],
            "Website": data[5]
            }
        lst_of_companies.append({str(company_id) : table_dict})



def upload_files(db, lst):
    db.insert_many(lst)

sqlite_conn()
get_data_sqlite()
db = get_db_mongo()
# upload_files(db, lst_of_companies)



@app.route('/')
def index():
   return 'W'

@app.route('/companies/', methods=['GET'])
def companies():
    conn = sqlite_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM companies')
    try:
        data = c.fetchall()
        return str(data)

    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message": "cannot read users"}), status=500, mimetype = "application/json")


@app.route('/company/', methods = ['GET'])
def one_company():
    conn = sqlite_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM companies')
    try:
        data = c.fetchone()
        return str(data)

    except Exception as ex:
        print(ex)
        return Response(response=json.dumps({"message": "cannot read users"}), status=500, mimetype="application/json")







if __name__ == '__main__':
    app.run()

