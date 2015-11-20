from flask import Flask, render_template, jsonify, make_response, abort, request, Response
from flask.ext.cors import CORS, cross_origin
from api import api

import subprocess
import database as db
import json
from marvel import call_marvel

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(api, url_prefix='/api/v1')

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/sitemap.xml')
def sitemap():
    sitemap_xml = render_template('sitemap.xml')
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')

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
    try:
        person = db.get_legislator_by_id(legislator_id, True)
        person['gender'] = 'Male' if person['gender'] == 'male' else 'Female'
        print(person)
    except Exception as e:
        print(e)
    return render_template('legislator.html', person=person)

@app.route('/committee/id/<int:committee_id>')
def committee(committee_id):
    # TODO: handle invalid ids
    try:
        committee = db.get_committee_by_id(committee_id, True)
        committee['chamber_url'] = committee['chamber']
        committee['chamber'] = 'House' if committee['chamber'] == 'house' else 'Senate'
        committee['juridicition'] = committee['jurisdiction'] if committee['jurisdiction'] else 'No Jurisdiction'
        committee['is_subcommittee'] = 'Yes' if committee['is_subcommittee'] else 'No'
    except Exception as e:
        print(e)
    return render_template('committee.html', committee=committee)

@app.route('/bills/id/<int:bill_id>')
def bill(bill_id):
    try:
        bill = db.get_bill_by_id(bill_id, True)
        if 'house_status' in bill:
            bill['house_status'] = 'Pass' if bill['house_status'] == 'pass' else 'Fail'
        else:
            bill['house_status'] = 'N/A'
        if 'senate_status' in bill:
            bill['senate_status'] = 'Pass' if bill['senate_status'] == 'pass' else 'Fail'
        else:
            bill['senate_status'] = 'N/A'
    except Exception as e:
        print(e)
    return render_template('bill.html', bill = bill)

@app.route('/search',  methods=['GET'])
def search():
    query = request.args.get('q')
    page = request.args.get('page')
    searchType = request.args.get('searchType')
    return render_template('search.html', query=query, page=page, searchType=searchType)

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
