# -*- coding:utf-8 -*-
from . import api
from iHome.utils.captcha.captcha import captcha
from flask import make_response

@api.route('/image_code')
def get_image_code():
    '''获取图片验证码'''

    # 生成图片验证码
    name, text, image = captcha.generate_captcha()

    # 响应
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response