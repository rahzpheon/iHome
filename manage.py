# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect,CsrfProtect
import os, base64
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_session import Session
from datetime import timedelta

class Config(object):

    DEBUG = True

    # mysql配置相关
    SQLALCHEMY_DATABASE_URI = 'mysql://root:2010116211@192.168.109.128:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置相关
    REDIS_HOST = '192.168.109.128'
    REDIS_PORT = 6379
    REDIS_DB = 4

    # session-redis相关
    SESSION_TYPE = 'redis'  # 存储方式
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,
                                port=REDIS_PORT,
                                db=REDIS_DB)
    #SESSION_KEY_PREFIX     # 存储前缀,默认为'session:'
    SESSION_USE_SIGNER = True   # 是否对session使用密钥签名
    SESSION_PERMANENT = True    # 设置session生命周期,默认关闭浏览器后消失
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)  # 全局设置session生命


    # 密钥,提供session,csrf等使用
    SECRET_KEY = base64.b64encode(os.urandom(48))

# 应用设置
app = Flask(__name__)
app.config.from_object(Config)
# 应用关联mysql
db = SQLAlchemy(app)
# 应用关联redis
redis_store = redis.StrictRedis(host=Config.REDIS_HOST,
                                port=Config.REDIS_PORT,
                                db=Config.REDIS_DB)

# session的redis存储
Session(app)


# 脚本管理器,准备数据库迁移
manager = Manager(app)

# 自定义脚本命令:
# 以后可以通过脚本命令 迁移数据库
Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 采用CSRF保护
CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def foo():
    # 测试redis是否正常工作
    #redis_store.set('demo2', 'redis success2.')

    from flask import session
    session['1232'] = 'hahaha'

    return 'Hello Flask666!123123123'

if __name__ == "__main__":
    # 运行脚本
    manager.run()
    # app.run(host='192.168.109.128', port=5000)