import sqlite3
from flask import Flask, request, render_template
import pymongo
import json



app = Flask(__name__)

conn = sqlite3.connect('data.db')
print('opened database successfully.')

conn.execute('SELECT * FROM companies')
print('Selected everything from the table')


def get_db_mongo():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['companies']
    return db



@app.route('/')
def index():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * from companies')
    rows = cur.fetchall()
    return render_template('index.html', companies = rows)

if __name__ == '__main__':
    app.run()

