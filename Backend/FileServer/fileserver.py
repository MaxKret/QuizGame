from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os, sys
sys.path.append(".")
sys.path.append("./SheetsDB")
from DBHandler import *

app = Flask(__name__)

@app.route('/')
def upload_page():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join("SheetsDB", secure_filename(f.filename)))
      
      return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(debug=True)