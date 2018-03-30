# -*- coding:utf-8 -*-
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf import CSRFProtect,CsrfProtect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_session import Session



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