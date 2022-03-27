from flask import Flask, jsonify, request
import os, sys, random
from userquestion import user_check
sys.path.append(os.path.join(sys.path[0], "..", "FileServer", "SheetsDB"))

app = Flask(__name__)

# Routes
@app.route('/')
def index():
   return jsonify(GetFinalQuestionList(["",""]))


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

def GetFinalQuestionList(UserEmails: list[str]) -> list[dict]:
    UserEmails: list[str]
    TotalNumQuestions: int
    QuestionsPerUser: int
    numUsers: int
    TopNSongs: int
    UserRecords: list[dict]
    FinalQuestionList: list[dict]
    
    UserEmails = ["maxwellkret@gmail.com", "katiemiller@gmail.com"]


    TotalNumQuestions = 10
    numUsers = len(UserEmails)

    FinalQuestionList = []
    QuestionsPerUser = int(TotalNumQuestions / numUsers)

    UserRecords = [request_DB_Record(email)[1] for email in UserEmails]

    TopNSongs = lambda leng: int(leng/4) 
    #                   grab only Top n Songs
    UserRecords = [{key:value[:TopNSongs(len(value))] for (key, value) in record.items()} for record in UserRecords]

    for i in range(numUsers):
        streams = [value for (key, value) in UserRecords[i].items()][0]
        FinalQuestionList.append({UserEmails[i]: streams[0]})
        for _ in range(QuestionsPerUser-1):
            randomint = random.randrange(len(streams))
            questionstream = streams[randomint]
            FinalQuestionList.append({UserEmails[i]: questionstream})

    return FinalQuestionList

def unit_test():
    try:
        assert GetFinalQuestionList(["",""]) == GetFinalQuestionList(["",""])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    GetFinalQuestionList()
    unit_test()
    app.run(debug=True)