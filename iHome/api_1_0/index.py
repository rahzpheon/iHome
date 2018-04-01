# -*- coding:utf-8 -*-
from . import api
from iHome import redis_store

# 蓝图注册路由
@api.route('/', methods=['GET', 'POST'])
def foo():
    # 测试redis是否正常工作
    # from iHome import redis_store
    redis_store.set('demo3', 'redis success3.')

    # from flask import session
    # session['1232'] = 'hahaha'

    return 'Hello Blueprint999!'