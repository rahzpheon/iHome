# -*- coding:utf-8 -*-
from flask import Blueprint

# 首页视图蓝图
api = Blueprint('api', __name__)

# 蓝图注册路由
@api.route('/', methods=['GET', 'POST'])
def foo():
    # 测试redis是否正常工作
    # from iHome import redis_store
    # redis_store.set('demo2', 'redis success2.')

    # from flask import session
    # session['1232'] = 'hahaha'

    return 'Hello Blueprint666!'