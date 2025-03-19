from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello, DevOps World!"


@app.route('/<name>')
def print_name(name):
    return "Hi, {}".format(name)


if __name__ == '__main__':
    app.run()
