# semos_final_project
Requirements - Python 3.8

Modules used - Flask, Pymongo, Json, Cleanco, re.

This project contains 3 python files and 2 HTML files, which work together to clear company names from a SQLite3 database and upload them to MongoDB.

# File Descriptions

main.py: This file contains the routes used for the Flask application.

scripts.py: This file contains the functions used for clearing company names from the database and uploading them to MongoDB. These functions include getting a company by name from the database and clearing the name, as well as uploading it to MongoDB.

requestapi.py: This file contains two functions: a get function for getting the cleared companies out of MongoDB and a post function which is used to clear a company name entered by the user.

# HTML File Descriptions

base.html: This file contains the navigation bar from Bootstrap, which is used in the index.html file.

index.html: This file extends the base.html file and contains a DataTables table displaying the uncleared companies from the SQLite3 database. 
The table has a search bar and a button at the end of each row,
which is used for clearing the selected company from the table and uploading it to MongoDB.


# How to Use
To use this project, follow these steps:

Run the Flask application using the command python main.py.
Navigate to localhost:5000 in your browser.
The index.html file will be displayed, showing the uncleared companies in a table.
To clear a company name, click the 'Clean the company' button at the end of the row of the company you wish to clear.
The cleared company will be uploaded to MongoDB.