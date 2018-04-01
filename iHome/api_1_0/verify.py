# -*- coding:utf-8 -*-
from . import api
from iHome.utils.captcha.captcha import captcha
from flask import make_response, request, abort, jsonify
from iHome import redis_store
from .. import constants
from iHome.utils.response_code import RET

@api.route('/image_code')
def get_image_code():
    '''获取图片验证码'''

    # 获取url中的uuid
    uuid = request.args.get('uuid')

    # 校验
    if not uuid:
        abort(403)

    # 生成图片验证码
    name, text, image = captcha.generate_captcha()

    # 使用uuid标识验证码txt,uuid代表用户浏览器即其身份,并设置过期事件:300s
    try:
        redis_store.set('ImageCode' + uuid, text, constants.SMS_CODE_REDIS_EXPIRES)

    except Exception as e:
        print e
        return jsonify(errno=RET.DBERR, errmsg=u'保存验证码失败')

    # 响应
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response