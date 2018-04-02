# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import current_app, make_response
from flask_wtf.csrf import generate_csrf

html_blue = Blueprint('html_blue', __name__)

# 向浏览器返回静态页面
@html_blue.route('/<re(".*"):file_name>')
def get_static_html(file_name):

    # 拼接文件url
    # send_static_file会自动添加/static/作为前缀
    if not file_name:
        # 如果没有传入文件名,访问首页
        file_name = 'index.html'

    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name

    # 在响应中加入csrf信息
    response = make_response(current_app.send_static_file(file_name))

    token = generate_csrf()
    response.set_cookie('csrf_token', token)

    return response