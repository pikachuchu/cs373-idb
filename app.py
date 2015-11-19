from flask import Flask, render_template, jsonify, make_response, abort, Response
from flask.ext.cors import CORS, cross_origin
from api import api
import subprocess
import json
from marvel import call_marvel

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

@app.route('/comics')
@cross_origin()
def comics():
    return render_template('comics.html')

@app.route('/marvel')
@cross_origin()
def marvel():
    data = list(call_marvel())
    return Response(json.dumps(data), mimetype='application/json')

@app.route('/about')
@cross_origin()
def about():
    return render_template('about.html')

# @app.route('/senator/id/<int:sen_id>')
# def senator(sen_id):
#     return render_template('senator.html', sen_id = sen_id)

@app.route('/legislator/id/<int:legislator_id>')
def legislator(legislator_id):
    return render_template('legislator.html', legislator_id = legislator_id)

@app.route('/committee/id/<int:committee_id>')
def committee(committee_id):
    return render_template('committee.html', committee_id = committee_id)

@app.route('/bills/id/<int:bill_id>')
def bill(bill_id):
    return render_template('bill.html', bill_id = bill_id)

@app.route('/tests')
def tests():
    p = subprocess.Popen(["make", "test"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
    out, err = p.communicate()
    return render_template('tests.html', output=err+out)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8000)
