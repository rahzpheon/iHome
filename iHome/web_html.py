# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import current_app

html_blue = Blueprint('html_blue', __name__)
@html_blue.route('/<re(".*"):file_name>')
def get_static_html(file_name):

    # 拼接文件url
    # send_static_file会自动添加/static/作为前缀
    if not file_name:
        # 如果没有传入文件名,访问首页
        file_name = 'index.html'

    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name



    return current_app.send_static_file(file_name)