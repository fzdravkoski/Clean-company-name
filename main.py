from flask import Flask, Response, render_template, request
import json
from scripts import get_one_company, clean_one_company, get_data_sqlite_full_data, lst_of_companies, get_cleaned_companies


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    try:
        get_data_sqlite_full_data()
        page = int(request.args.get("page", 1))
        per_page = 40
        start = (page - 1) * per_page
        end = start + per_page
        companies = lst_of_companies[start:end]
        return render_template("index.html",
                               cmps=companies,
                               page=page)
    except Exception as ex:
        return ex, 505

@app.route('/companies/<string:name>', methods=['GET'])
def companies(name):
    try:
        one_company = get_one_company(name)
        return f'{one_company}'

    except Exception as ex:
        return Response(response = json.dumps({"message": "cannot read company"}),
                        status=500,
                        mimetype = "application/json")

@app.route('/clean-company/<string:name>', methods=["GET","POST"])
def clean_company(name):
    try:
        cleaned_company = clean_one_company(name)
        return f'Succesfully cleaned the company, {cleaned_company[1]}'

    except Exception as ex:
        return str(ex), 409


@app.route('/cleaned-companies', methods=["GET"])
def cleaned_companies():
    try:
        cleaned = get_cleaned_companies()
        return json.dumps(cleaned)
    except Exception as ex:
        return "Can't read the cleaned companies"

@app.route('/clean-a-company/<string:name>', methods=["POST"])
def clean_a_company(name):
    try:
        clean_cmp = clean_one_company(name)
        return clean_cmp
    except Exception as ex:
        return str(ex)


if __name__ == '__main__':
    app.run(debug=True)



