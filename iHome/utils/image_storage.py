# -*- coding:utf-8 -*-
import qiniu
from iHome import constants

access_key = "yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW"
secret_key = "bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW"
bucket_name = 'ihome'
# 拼接访问全路径 ： http://oyucyko3w.bkt.clouddn.com/FtEAyyPRhUT8SU3f5DNPeejBjMV5

# 上传文件至七牛云
def upload_image(img_data):

    # 1.使用ak,sk,获取连接对象
    q = qiniu.Auth(access_key, secret_key)

    # 2.获取空间的密钥
    token = q.upload_token(bucket_name)

    # 3.上传文件至云空间,返回生成的key
    ret, info = qiniu.put_data(token, None, img_data)

    # print ret
    # print info

    # 4.判断状态码,成功时返回key
    if 200 == info.status_code:
        return ret.get('key')
    else:
        raise Exception('上传图片失败')

if __name__ == '__main__':
    url = '/home/python/PycharmProjects/iHome/iHome/static/images/home01.jpg'
    with open(url, 'rb') as f:
        upload_image(f.read())