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
      f = request.files['file']
      f.save(os.path.join("SheetsDB", secure_filename(f.filename)))
      import_json()
      return 'file uploaded successfully'

def import_json():
   from DBHandler import DBHandler
   db_handler = DBHandler()
   db_handler.choose_sheet(0)

   file = None
   with open(sys.stdin) as std_in:
         file = std_in
   db_handler.import_json_record(file)
   db_handler.import_json_record(file)


if __name__ == "__main__":
    app.run(debug=True)