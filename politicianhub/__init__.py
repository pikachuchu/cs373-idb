from flask import Flask, render_template, jsonify, make_response, abort, request, Response
from flask.ext.cors import CORS, cross_origin
from api import api

import subprocess
import database as db
import json
from marvel import call_marvel

def create_app():
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

    @app.route('/legislator/id/<int:legislator_id>')
    def legislator(legislator_id):
        return render_template('legislator.html', legislator_id=legislator_id)

    @app.route('/committee/id/<int:committee_id>')
    def committee(committee_id):
        return render_template('committee.html', committee_id=committee_id)

    @app.route('/bills/id/<int:bill_id>')
    def bill(bill_id):
        return render_template('bill.html', bill_id = bill_id)

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

    return app
