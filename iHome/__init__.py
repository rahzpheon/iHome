# -*- coding:utf-8 -*-
from flask import Flask
from config import configs
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect
from iHome.index import api

# 部分参数由于封装在方法内,需要提取出来方便manage导入使用

# mysql连接对象,空参,app在方法内设置,原因与其在manage.py的调用顺序有关
db = SQLAlchemy()
#
redis_store = None

def get_app(config_name):
    '''工厂方法:根据不同的配置信息,实例化出不同的app'''

    # 原材料——生产——使用
    # 根据传入的名字找到指定Config类
    Config = configs[config_name]

    # 创建应用
    app = Flask(__name__)

    # 应用基础设置
    app.config.from_object(Config)

    # 应用关联mysql
    db.init_app(app)
    # 应用关联redis
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST,
                                    port=Config.REDIS_PORT,
                                    db=Config.REDIS_DB)

    # session的redis存储
    Session(app)

    # 采用CSRF保护
    CSRFProtect(app)

    # 应用注册蓝图
    app.register_blueprint(api)

    # 返回应用实例
    return app