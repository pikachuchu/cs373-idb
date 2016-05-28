from flask import Blueprint, jsonify, make_response, abort, request
from flask.ext.cors import CORS, cross_origin
import database as db

# RESTful API

api = Blueprint('api', __name__)

legislator_fields = {
    'id',
    'first_name',
    'last_name',
    'chamber',
    'gender',
    'birthday',
    'state',
    'twitter',
    'bio_guide'
}

committee_fields = {
    'id',
    'name',
    'chamber',
    'is_subcommittee',
    'committee_id',
    'chair'
}

bill_fields = {
    'id',
    'name',
    'bill_id',
    'bill_type',
    'date_intro',
    'house_status',
    'senate_status',
    'current_status',
    'sponsor'
}

"""
GET all legislators
"""
@api.route('/legislators', methods=['GET'])
@cross_origin()
def get_legislators():
    verbose = request.args.get('verbose')
    args = {}
    for v in request.args:
        if v in legislator_fields:
            args[v] = request.args.get(v)
    legislators = db.get_legislators(args, verbose == 'true')
    return jsonify({'legislators': legislators})

"""
GET all committees
"""
@api.route('/committees', methods=['GET'])
@cross_origin()
def get_committees():
    verbose = request.args.get('verbose')
    args = {}
    for v in request.args:
        if v in committee_fields:
            args[v] = request.args.get(v)
    committees = db.get_committees(args, verbose == 'true')
    return jsonify({'committees': committees})

"""
GET all bills
"""
@api.route('/bills', methods=['GET'])
@cross_origin()
def get_bills():
    verbose = request.args.get('verbose')
    args = {}
    for v in request.args:
        if v in bill_fields:
            args[v] = request.args.get(v)
    bills = db.get_bills(args, verbose == 'true')

    return jsonify({'bills': bills})

"""
GET a legislator by id
"""
@api.route('/legislators/<int:legislator_id>', methods=['GET'])
@cross_origin()
def get_legislator(legislator_id):
    verbose = request.args.get('verbose')
    legislator = db.get_legislator_by_id(legislator_id, verbose == 'true')
    if not legislator:
        abort(404)
    return jsonify(legislator)

"""
GET a committee by id
"""
@api.route('/committees/<int:committee_id>', methods=['GET'])
@cross_origin()
def get_committee(committee_id):
    verbose = request.args.get('verbose')
    committee = db.get_committee_by_id(committee_id, verbose == 'true')
    if not committee:
        abort(404)
    return jsonify(committee)


"""
GET a bill by id
"""
@api.route('/bills/<int:bill_id>', methods=['GET'])
@cross_origin()
def get_bill(bill_id):
    verbose = request.args.get('verbose')
    bill = db.get_bill_by_id(bill_id, verbose == 'true')
    if not bill:
        abort(404)
    return jsonify(bill)

"""
Handle 404 errors
"""
@api.errorhandler(404)
@cross_origin()
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

