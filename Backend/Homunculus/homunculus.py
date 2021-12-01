from flask import Flask, jsonify, request
import os, sys
sys.path.append(os.path.join(sys.path[0], "..", "FileServer", "SheetsDB"))

app = Flask(__name__)

# Routes
@app.route('/')
def index():
   return jsonify(200)


# Functions
def request_DB_Record(email: str) -> tuple[list[dict], dict]:
    from DBHandler import DBHandler
    record: dict
    record_all_streams: list[dict]
    DB = DBHandler()
    DB.choose_sheet(0)
    record = DB.find_record_by_email(email)
    record_all_streams = record[email]
    return record_all_streams, record

def idkyet():
    UserEmails: list[str]
    TotalNumQuestions: int
    TopNSongs: int
    UserRecords: list[dict]

    UserEmails = ["maxwellkret@gmail.com", "notmaxwellkret@gmail.com"]

    UserRecords = [request_DB_Record(email)[1] for email in UserEmails]

    TopNSongs = 5
    #                   grab only Top n Songs
    UserRecords = [{key:value[:TopNSongs] for (key, value) in record.items()} for record in UserRecords]

    TotalNumQuestions = len(UserEmails) * TopNSongs
    



if __name__ == "__main__":
    idkyet()
    app.run(debug=True)