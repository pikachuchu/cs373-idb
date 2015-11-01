from flask import Blueprint, jsonify, make_response, abort

# RESTful API

api = Blueprint('api', __name__)

dummy_data = [
    {
        'id': 0,
        'first_name': 'foo',
        'last_name': 'bar'
    },
    {
        'id': 1,
        'first_name': 'meow',
        'last_name': 'cat'
    }
]

"""
GET all legislators
"""
@api.route('/legislators', methods=['GET'])
def get_legislators():
    return jsonify({'legislators': dummy_data})

"""
GET all committees
"""
@api.route('/committees', methods=['GET'])
def get_committees():
    return jsonify({'committees': dummy_data})

"""
GET all bills
"""
@api.route('/bills', methods=['GET'])
def get_bills():
    return jsonify({'bills': dummy_data})

"""
GET a legislator by id
"""
@api.route('/legislators/<int:legislator_id>', methods=['GET'])
def get_legislator(legislator_id):
    legislator = [v for v in dummy_data if v['id'] == legislator_id]
    if len(legislator) == 0:
        abort(404)
    return jsonify({'legislator': legislator[0]})


"""
GET a committee by id
"""
@api.route('/committees/<int:committee_id>', methods=['GET'])
def get_committee(committee_id):
    committee = [v for v in dummy_data if v['id'] == committee_id]
    if len(committee) == 0:
        abort(404)
    return jsonify({'committee': committee[0]})


"""
GET a bill by id
"""
@api.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    bill = [v for v in dummy_data if v['id'] == bill_id]
    if len(bill) == 0:
        abort(404)
    return jsonify({'bill': bill[0]})

"""
Handle 404 errors
"""
@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

