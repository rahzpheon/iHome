# -*- coding:utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from iHome import db, app


# 脚本管理器,准备数据库迁移
manager = Manager(app)

# 自定义脚本命令:
# 以后可以通过脚本命令 迁移数据库
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@app.route('/', methods=['GET', 'POST'])
def foo():
    # 测试redis是否正常工作
    #redis_store.set('demo2', 'redis success2.')

    # from flask import session
    # session['1232'] = 'hahaha'

    return 'Hello Flask888!'

if __name__ == "__main__":
    # 运行脚本
    manager.run()
    # app.run(host='192.168.109.128', port=5000)