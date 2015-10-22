from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run()
