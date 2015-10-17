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

if __name__ == '__main__':
    app.run()
