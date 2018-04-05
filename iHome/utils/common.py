# -*- coding:utf-8 -*-
from flask import session, jsonify, g
from werkzeug.routing import BaseConverter
from functools import wraps
from iHome.utils.response_code import RET

class RegexConverter(BaseConverter):
    '''路由匹配转换器'''
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)

        self.regex = args[0]


def login_required(view_func):
    '''登陆验证装饰器'''
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # 验证用户是否登陆
        try:
            user_id = session.get('user_id')
        except Exception as e:
            return jsonify(errno=RET.DBERR, errmsg="查询session信息失败")
        if not user_id:
            return jsonify(errno=RET.SESSIONERR, errmsg="请先登陆!")
        else:
            g.user_id = user_id

        return view_func(*args, **kwargs)

    return wrapper
