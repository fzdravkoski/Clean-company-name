from flask import Flask, Response, render_template, request
import json
from scripts import get_one_company, clean_one_company, get_data_sqlite_full_data, lst_of_companies, get_cleaned_companies

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    :get_data_sqlite_full_data: Connecting and taking data from query
    :return: returning the index.html
    :cmps=companies: = Used for iteration in the front end
    """
    try:
        get_data_sqlite_full_data()
        companies = lst_of_companies
        return render_template('index.html', cmps=companies)


    except Exception as ex:
        return ex, 505

@app.route('/companies/<string:name>', methods=['GET'])
def companies(name):
    """
    :GET: method for returning the uncleared company name from sqlite3
    :get_one_company: Connecting and filtering one company from a query
    :param name: passing the name from the get_one_company function
    :return: returning the uncleared name.
    """
    try:
        one_company = get_one_company(name)
        return f'{one_company}'

    except Exception as ex:
        return Response(response = json.dumps({"message": "cannot read company"}),
                        status=500,
                        mimetype = "application/json")

@app.route('/clean-company/<string:name>', methods=["GET","POST"])
def clean_company(name):
    """
    :clean_one_company: Connecting and pulling a company from sqlite, clearing it and uploading the result to MongoDB
    :param name: Passing the name from the clean_one_company function
    :return: Returning a simple message about which company was cleaned.
    """
    try:
        cleaned_company = clean_one_company(name)
        return f'Succesfully cleaned the company, {cleaned_company[1]}'

    except Exception as ex:
        return str(ex), 409


@app.route('/cleaned-companies', methods=["GET"])
def cleaned_companies():
    """
    :get_cleaned_companies: Used for getting all the companies we have cleaned from mongodb
    :return: Displaying them as json results using the get method in requestapi.py.
    """
    try:
        cleaned = get_cleaned_companies()
        return json.dumps(cleaned)
    except Exception as ex:
        return "Can't read the cleaned companies"

@app.route('/clean-a-company/<string:name>', methods=["POST"])
def clean_a_company(name):
    """
    :clean_one_company: Connecting and pulling a company from sqlite, clearing it and uploading the result to MongoDB
    :param name: Passing the name from the clean_one_company function
    :return: returning the results. Used for the post method in the requestapi.py file.
    """
    try:
        clean_cmp = clean_one_company(name)
        return clean_cmp
    except Exception as ex:
        return str(ex)


if __name__ == '__main__':
    app.run(debug=True)





