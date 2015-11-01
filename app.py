from flask import Flask, render_template, jsonify, make_response, abort

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/senate')
def senate():
    return render_template('senate.html')

@app.route('/house')
def house():
    return render_template('house.html')

@app.route('/committees')
def committees():
    return render_template('committees.html')

@app.route('/bills')
def bills():
    return render_template('bills.html')

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/senator/id/<int:sen_id>')
# def senator(sen_id):
#     return render_template('senator.html', sen_id = sen_id)

@app.route('/senator/id/1')
def senator1():
    return render_template('senator1.html')

@app.route('/senator/id/2')
def senator2():
    return render_template('senator2.html')

@app.route('/senator/id/3')
def senator3():
    return render_template('senator3.html')

@app.route('/representative/id/1')
def representative1():
    return render_template('representative1.html')

@app.route('/representative/id/2')
def representative2():
    return render_template('representative2.html')

@app.route('/representative/id/3')
def representative3():
    return render_template('representative3.html')

@app.route('/committee/id/1')
def committee1():
    return render_template('committee1.html')

@app.route('/committee/id/2')
def committee2():
    return render_template('committee2.html')

@app.route('/committee/id/3')
def committee3():
    return render_template('committee3.html')

@app.route('/bills/id/1')
def bills1():
    return render_template('bills1.html')

@app.route('/bills/id/2')
def bills2():
    return render_template('bills2.html')

@app.route('/bills/id/3')
def bills3():
    return render_template('bills3.html')

# RESTful API

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
@app.route('/api/v1/legislators', methods=['GET'])
def get_legislators():
    return jsonify({'legislators': dummy_data})

"""
GET all committees
"""
@app.route('/api/v1/committees', methods=['GET'])
def get_committees():
    return jsonify({'committees': dummy_data})

"""
GET all bills
"""
@app.route('/api/v1/bills', methods=['GET'])
def get_bills():
    return jsonify({'bills': dummy_data})

"""
GET a legislator by id
"""
@app.route('/api/v1/legislators/<int:legislator_id>', methods=['GET'])
def get_legislator(legislator_id):
    legislator = [v for v in dummy_data if v['id'] == legislator_id]
    if len(legislator) == 0:
        abort(404)
    return jsonify({'legislator': legislator[0]})


"""
GET a committee by id
"""
@app.route('/api/v1/committees/<int:committee_id>', methods=['GET'])
def get_committee(committee_id):
    committee = [v for v in dummy_data if v['id'] == committee_id]
    if len(committee) == 0:
        abort(404)
    return jsonify({'committee': committee[0]})


"""
GET a bill by id
"""
@app.route('/api/v1/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    bill = [v for v in dummy_data if v['id'] == bill_id]
    if len(bill) == 0:
        abort(404)
    return jsonify({'bill': bill[0]})

"""
Handle 404 errors
"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
