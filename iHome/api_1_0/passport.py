# -*- coding:utf-8 -*-
from flask import request, current_app, jsonify, session

from iHome.api_1_0 import api
from iHome import redis_store,db
from iHome.utils.response_code import RET
from iHome.models import User

# 注册视图
@api.route('/users', methods=['POST'])
def register():
    '''注册视图'''

    # 获取参数
    json_dict = request.json

    mobile = json_dict.get('mobile')
    sms_code = json_dict.get('sms_code')
    password = json_dict.get('password')
    # password2 = json_dict.get('password2')

    # 临时测试代码
    # mobile = '15817293003'
    # sms_code = redis_store.get('SMSCode' + mobile)
    # password = '123456'


    # 校验
    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.NODATA, errmsg='参数不完整')

    server_sms_code = redis_store.get('SMSCode' + mobile)
    if server_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码错误')

    # 判断该用户是否已经注册
    if User.query.filter(User.mobile == mobile).first():
        return jsonify(errno=RET.DATAEXIST, errmsg='用户已注册')

    # 业务逻辑
    user = User()
    user.name = mobile
    # password = generate_password_hash(password)
    user.password = password
    user.mobile = mobile

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存注册信息失败')

    # 返回
    return jsonify(errno=RET.OK, errmsg='注册成功')

# 登陆视图
@api.route('/sessions', methods=['POST'])
def login():
    # 0.判断用户是否已登陆
    # 1.获取用户输入信息
    json_dict = request.json
    mobile = json_dict.get('mobile')
    password = json_dict.get('passwd')

    # 2.判断校验
    # 完整性
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 用户
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户失败')

    if user is None:
        return jsonify(errno=RET.DATAEXIST, errmsg='用户名或密码错误')

    # 密码(不能直接加密后比较,要通过werkzeug的方法check_password_hash)
    # 封装在模型类中
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')

    # 3.业务逻辑:登陆成功,记录用户session信息(登陆状态)
    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['name'] = user.name

    return jsonify(errno=RET.OK, errmsg='登陆成功')

# 退出登陆
@api.route('/sessions', methods=['DELETE'])
def logout():

    try:
        session.pop('user_id')
        session.pop('name')
        session.pop('mobile')

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.SESSIONERR, errmsg="登出失败")

    return jsonify(errno=RET.OK, errmsg="退出登陆成功")

# 登陆验证视图,同时为首页提供用户名
@api.route('/sessions')
def login_check():

    user_id = session.get('user_id')
    name = session.get('name')

    return jsonify(errno=RET.OK, errmsg="OK", data={'user_id':user_id, 'name':name})