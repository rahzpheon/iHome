# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect,CsrfProtect
import os, base64
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

class Config(object):

    DEBUG = True

    # mysql配置相关
    SQLALCHEMY_DATABASE_URI = 'mysql://root:2010116211@192.168.109.128:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置相关
    REDIS_HOST = '192.168.109.128'
    REDIS_PORT = 6379
    REDIS_DB = 4

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

# 脚本管理器,准备数据库迁移
manager = Manager(app)

# 自定义脚本命令:
# 以后可以通过脚本命令 迁移数据库
Migrate(app, db)
manager.add_command('db', MigrateCommand)

# 采用CSRF保护
# CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def foo():
    # 测试redis是否正常工作
    #redis_store.set('demo2', 'redis success2.')
    return 'Hello Flask666!'

if __name__ == "__main__":
    # 运行脚本
    manager.run()
    # app.run(host='192.168.109.128', port=5000)