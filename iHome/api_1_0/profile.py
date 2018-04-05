# -*- coding:utf-8 -*-
from flask import session, jsonify, request, current_app, g
from iHome import db, constants
from iHome.api_1_0 import api
from iHome.models import User
from iHome.utils.response_code import RET
from iHome.utils.image_storage import upload_image
from iHome.utils.common import login_required

# 个人中心
@api.route('/users')
@login_required
def get_user_info():
    # 0.验证用户登陆
    # 1.获取参数:用户id
    # user_id = session.get('user_id')
    user_id = g.user_id

    if not user_id:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 2.获取用户
    try:
        user = User.query.get(user_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="用户不存在")

    # 3.获取用户信息
    user_dict = user.to_dict()

    # 4.返回响应
    return jsonify(errno=RET.OK, errmsg="获取信息成功", data=user_dict)

# 上传用户头像功能
@api.route('/users/avatar', methods=['POST'])
@login_required
def upload_avatar():
    """提供用户头像上传
        0.先判断用户是否登录 @login_required
        1.接受请求参数:avatar对应的图片数据，并校验
        2.调用上传图片的工具方法
        3.存储图片的key到user.avatar_url属性中
        4.响应上传结果，在结果中传入avatar_url，方便用户上传完成后立即刷新头像
        """

    # 1.接受参数
    try:
        img_data = request.files.get('avatar')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="头像参数错误")

    # 2.调用方法,将文件上传至云
    try:
        key = upload_image(img_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传头像失败")

    # 3.存储key至用户对象中
    try:
        user_id = g.user_id
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="查询用户数据失败")

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="用户不存在")

    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='存储用户头像地址失败')

    # 4.返回图片地址,方便页面显示头像
    # 注意地址需要key与接口地址拼接
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg="上传头像成功", data=avatar_url)

# 修改用户名
@api.route('/users/name', methods=['PUT'])
@login_required
def set_user_name():
    '''
    0.判断用户登陆状态
    1.接收用户传入新用户名, new_name
    2.校验参数
    3.查询当前登陆用户
    4.为当前用户赋值新用户名
    5.修改写入数据库
    6.返回响应'''

    # 1.
    json_dict = request.json
    new_name = json_dict.get('name')

    # 2
    if not new_name:
        return jsonify(errno=RET.PARAMERR, errmsg="缺少参数")

    # 3.
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询用户数据失败')
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='用户不存在')

    # 4.
    user.name = new_name

    # 5.
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='存储用户名失败')

        # 6.响应结果
    return jsonify(errno=RET.OK, errmsg='修改用户名成功')