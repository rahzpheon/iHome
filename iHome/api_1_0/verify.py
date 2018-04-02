# -*- coding:utf-8 -*-
from . import api
from iHome.utils.captcha.captcha import captcha
from flask import make_response, request, abort, jsonify, current_app
from iHome import redis_store
from .. import constants
from iHome.utils.response_code import RET
import re

import random
from iHome.utils.SendTemplateSMS import CCP



@api.route('/image_code')
def get_image_code():
    '''获取图片验证码'''

    # 获取url中的uuid
    uuid = request.args.get('uuid')

    # 获取url中的last_uuid
    last_uuid = request.args.get('last_uuid')

    # 校验
    if not uuid:
        # abort(403)
        return jsonify(errno=RET.NODATA, errmsg=u'uuid不存在')

    # 生成图片验证码
    name, text, image = captcha.generate_captcha()

    # 如果存在旧uuid,删除对应数据
    if last_uuid:
        try:
            redis_store.delete('ImageCode' + last_uuid)

        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=u'删除旧验证码失败')

    # 使用uuid标识验证码txt,uuid代表用户浏览器即其身份,并设置过期事件:300s
    try:
        redis_store.set('ImageCode' + uuid, text, constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'保存验证码失败')

    # 响应
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response

@api.route('/sms_code', methods=['POST'])
def get_sms_code():
    '''获取短信验证码'''

    # 获取参数
    json_dict = request.get_json()

    uuid = json_dict.get('uuid');current_app.logger.debug('uuid:' + uuid)
    mobile = json_dict.get('mobile');current_app.logger.debug('uuid:' + uuid)
    imageCode = json_dict.get('imageCode');current_app.logger.debug('uuid:' + uuid)

    # 校验参数
    # 1.验证参数完整性
    if not all([uuid, mobile, imageCode]):
        return jsonify(errno=RET.PARAMERR, errmsg=u'参数错误')

    # 2.验证手机号码有效性
    if not re.match(r"^1[34578][0-9]{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg=u'手机号不合法')

    #　3.验证图片验证码是否正确

    # 获取
    try:
        real_image_code = redis_store.get('ImageCode' + uuid)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'查询异常')

    # 判断是否存在
    if not real_image_code:
        return jsonify(errno=RET.DATAERR, errmsg=u'图片验证码已过期')

    # 比较是否一致
    if imageCode != real_image_code:
        return jsonify(errno=RET.DATAERR, errmsg=u'图片验证码错误')

    # 业务逻辑:发送短信

    # 先删除redis中的验证码数据
    try:
        redis_store.delete('ImageCode_' + uuid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg=u'删除本地图片验证码失败')

    # 生成短信验证码,并调用模块发出
    sms_code = '%06d' %random.randint(0, 999999)
    # 发送
    try:
        redis_store.setex('SMSCode' + mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=u'保存短信验证码失败')

    result = CCP().send_template_sms(mobile, [sms_code, constants.HOME_PAGE_DATA_REDIS_EXPIRES / 60], '1')
    if result == 0:
        return jsonify(errno=RET.OK, errmsg=u'发送验证码成功')
    else:
        return jsonify(errno=RET.THIRDERR, errmsg=u'发送验证码失败')


