from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('index.html')

@app.route('/submitted', methods=['GET', 'POST'])
def hello():
    return render_template('submitted.html', file=request.form['jsonupload'])

if __name__ == "__main__":
    app.run()