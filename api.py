from flask import Blueprint, jsonify, make_response, abort
import database as db

# RESTful API

api = Blueprint('api', __name__)

"""
GET all legislators
"""
@api.route('/legislators', methods=['GET'])
def get_legislators():
    return jsonify({'legislators': db.get_legislators()})

"""
GET all committees
"""
@api.route('/committees', methods=['GET'])
def get_committees():
    return jsonify({'committees': db.get_committees()})

"""
GET all bills
"""
@api.route('/bills', methods=['GET'])
def get_bills():
    return jsonify({'bills': db.get_bills()})

"""
GET a legislator by id
"""
@api.route('/legislators/<int:legislator_id>', methods=['GET'])
def get_legislator(legislator_id):
    legislator = db.get_legislator_by_id(legislator_id)
    if not legislator:
        abort(404)
    return jsonify(legislator)


"""
GET a committee by id
"""
@api.route('/committees/<int:committee_id>', methods=['GET'])
def get_committee(committee_id):
    committee = db.get_committee_by_id(committee_id)
    if not committee:
        abort(404)
    return jsonify(committee)


"""
GET a bill by id
"""
@api.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    bill = db.get_bill_by_id(bill_id)
    if not bill:
        abort(404)
    return jsonify(bill)

"""
Handle 404 errors
"""
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

