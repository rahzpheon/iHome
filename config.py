# -*- coding:utf-8 -*-
import os, base64
import redis
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


class DevelopConfig(Config):
    '''开发环境'''
    pass


class UnitTestConfig(Config):
    '''单元测试环境'''
    pass


class ProductionConfig(Config):
    '''生产环境'''
    pass



# 工厂材料:提供给工厂的参数-类映射表
configs = {
    'default':Config,
    'develop':DevelopConfig,
    'unittest':UnitTestConfig,
    'product':ProductionConfig
}