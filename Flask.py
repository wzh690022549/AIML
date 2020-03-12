from flask import Flask

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run('0.0.0.0', 13457, debug=True)
