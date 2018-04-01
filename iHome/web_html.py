# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import current_app

html_blue = Blueprint('html_blue', __name__)
@html_blue.route('/<file_name>')
def get_static_html(file_name):

    # 拼接文件url
    # send_static_file会自动添加/static/作为前缀
    file_path = 'html/' + file_name

    # try:
    #

    return current_app.send_static_file(file_path)