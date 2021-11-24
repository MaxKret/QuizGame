from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os, sys
sys.path.append(os.path.join(sys.path[0], "SheetsDB"))

app = Flask(__name__)

@app.route('/')
def upload_page():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f, f_name = (request.files['file'], request.files['file'].filename)
      f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), "SheetsDB", secure_filename(f.filename)))
      user_email = request.form['email']
      import_json(email=user_email, file_name=f_name)
      return f'file {f_name} uploaded successfully'

def import_json(email, file_name):
   from DBHandler import DBHandler
   db_handler = DBHandler()
   db_handler.choose_sheet(0)
   if db_handler.find_file(file_name):
      db_handler.import_json_record(user_email=email)
      print("File Found fileserver.py")



if __name__ == "__main__":
    app.run(debug=True)