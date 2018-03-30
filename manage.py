# -*- coding:utf-8 -*-

from flask import Flask

class Config(object):

    DEBUG = True

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def foo():
    return 'Hello Flask666!'

if __name__ == "__main__":
    app.run()