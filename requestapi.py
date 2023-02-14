import requests

def getCompanies():
    companies = requests.get('http://127.0.0.1:5000/cleaned-companies')
    cmps = companies.json()
    return cmps


def postCompanies():
    name = input('Input a valid name for cleaning from database: ')
    data = {'name': name.upper()}
    companies = requests.post('http://127.0.0.1:5000/clean-company/' + data['name'])
    return companies


cmps = postCompanies()
print(getCompanies())
