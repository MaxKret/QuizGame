from flask import Flask, render_template, request
from DBHandler import DBHandler

app = Flask(__name__)

# Routes
@app.route('/')
def upload_page():
   return "Home Page"


# Functions
def request_DB_Record(email: str) -> tuple[list, dict]:
    record: dict
    record_streams: list
    DB = DBHandler()
    DB.choose_sheet(0)
    record = DB.find_record_by_email(email)
    record_streams = record[email]
    return record_streams, record


if __name__ == "__main__":
    app.run(debug=True)