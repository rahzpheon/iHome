# -*- coding:utf-8 -*-
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from iHome import get_app,db


# 提供参数,使用工厂生产的app
app = get_app('develop')

# 脚本管理器,准备数据库迁移
manager = Manager(app)

# 自定义脚本命令:
# 以后可以通过脚本命令 迁移数据库
Migrate(app, db)
manager.add_command('db', MigrateCommand)




if __name__ == "__main__":

    # 测试路由是否成功添加
    # print app.url_map
    # 运行脚本
    manager.run()
    # app.run(host='192.168.109.128', port=5000)