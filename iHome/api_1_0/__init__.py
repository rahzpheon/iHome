# -*- coding:utf-8 -*-
from flask import Blueprint

# 首页视图蓝图
api = Blueprint('api_1_0', __name__, url_prefix='/api/1.0')

# 导入一次蓝图路由
from . import index,verify, passport
