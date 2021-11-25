from flask import Flask, jsonify, request
import os, sys
sys.path.append(os.path.join(sys.path[0], "SheetsDB"))
# sys.path.append(os.path.join(sys.path[0], "..", "SheetsDB"))

app = Flask(__name__)

# Routes
@app.route('/')
def index():
   return jsonify(200)


# Functions
def request_DB_Record(email: str) -> tuple[list, dict]:
    from DBHandler import DBHandler
    record: dict
    record_streams: list
    DB = DBHandler()
    DB.choose_sheet(0)
    record = DB.find_record_by_email(email)
    record_streams = record[email]
    return record_streams, record

def idkyet():
    NumPlayers: int
    UserEmails: list
    TotalNumQuestions: int
    TopNSongs: int
    UserRecords: list[dict]

    UserEmails = ["maxwellkret@gmail.com", "savvysra@yahoo.com"]

    UserRecords1 = [request_DB_Record(email)[1] for email in UserEmails]
    print()

    UserRecords2 = []
    for email in UserEmails:
        UserRecords2.append(request_DB_Record(email)[1])
    print()

    assert(UserRecords1 is UserRecords2)
    print()



if __name__ == "__main__":
    idkyet()
    app.run(debug=True)