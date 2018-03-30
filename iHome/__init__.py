# -*- coding:utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf import CSRFProtect


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

# 采用CSRF保护
CSRFProtect(app)
