from flask import Flask, render_template, jsonify, make_response, abort
from flask.ext.cors import CORS, cross_origin
from api import api
import subprocess

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(api, url_prefix='/api/v1')

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/senate')
@cross_origin()
def senate():
    return render_template('senate.html')

@app.route('/house')
@cross_origin()
def house():
    return render_template('house.html')

@app.route('/committees')
@cross_origin()
def committees():
    return render_template('committees.html')

@app.route('/bills')
@cross_origin()
def bills():
    return render_template('bills.html')

@app.route('/about')
@cross_origin()
def about():
    return render_template('about.html')

# @app.route('/senator/id/<int:sen_id>')
# def senator(sen_id):
#     return render_template('senator.html', sen_id = sen_id)

@app.route('/senator/id/1')
@cross_origin()
def senator1():
    return render_template('senator1.html')

@app.route('/senator/id/2')
@cross_origin()
def senator2():
    return render_template('senator2.html')

@app.route('/senator/id/3')
@cross_origin()
def senator3():
    return render_template('senator3.html')

@app.route('/representative/id/1')
@cross_origin()
def representative1():
    return render_template('representative1.html')

@app.route('/representative/id/2')
@cross_origin()
def representative2():
    return render_template('representative2.html')

@app.route('/representative/id/3')
@cross_origin()
def representative3():
    return render_template('representative3.html')

@app.route('/committee/id/1')
@cross_origin()
def committee1():
    return render_template('committee1.html')

@app.route('/committee/id/2')
@cross_origin()
def committee2():
    return render_template('committee2.html')

@app.route('/committee/id/3')
@cross_origin()
def committee3():
    return render_template('committee3.html')

@app.route('/bills/id/1')
@cross_origin()
def bills1():
    return render_template('bills1.html')

@app.route('/bills/id/2')
@cross_origin()
def bills2():
    return render_template('bills2.html')

@app.route('/bills/id/3')
@cross_origin()
def bills3():
    return render_template('bills3.html')

@app.route('/tests')
def tests():
    p = subprocess.Popen(["python", "tests.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
    out, err = p.communicate()
    return render_template('tests.html', output=err)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
