# -*- coding:utf-8 -*-
import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from iHome.utils.common import RegexConverter
from config import configs


# 部分参数由于封装在方法内,需要提取出来方便manage导入使用

# mysql连接对象,空参,随后通过方法设置app,原因与其在manage.py的调用顺序有关
db = SQLAlchemy()
# redis连接对象,空参,通过赋值设置app,要指定其为全局变量
redis_store = None

# 建立日志工厂,在初始化时调用
def setupLogging(level):
    '''日志工厂:根据输入设置日志等级'''

    # 日志相关设置
    import logging
    from logging.handlers import RotatingFileHandler

    # # 设置日志的记录等级
    # logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    # file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # # 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
    # formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # # 为刚创建的日志记录器设置日志记录格式
    # file_log_handler.setFormatter(formatter)
    # # 为全局的日志工具对象（flask app使用的）添加日志记录器
    # logging.getLogger().addHandler(file_log_handler)


def get_app(config_name):
    '''工厂方法:根据不同的配置信息,实例化出不同的app'''

    # 原材料——生产——使用
    # 根据传入的名字找到指定Config类
    Config = configs[config_name]

    # 根据config_name设置日志等级
    log_level = configs[config_name]
    setupLogging(log_level)

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
    # CSRFProtect(app)

    # 注册自定义转换器,写在使用它的代码之前
    app.url_map.converters["re"] = RegexConverter

    # 注册蓝图
    from iHome.api_1_0 import api
    app.register_blueprint(api)
    from iHome.web_html import html_blue
    app.register_blueprint(html_blue)



    # 返回应用实例
    return app