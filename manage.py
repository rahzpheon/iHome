# -*- coding:utf-8 -*-

from flask import Flask

app = Flask(__name__)

@app.route('/')
def foo():
    return 'Hello Flask!'

if __name__ == "__main__":
    app.run(debug=True)