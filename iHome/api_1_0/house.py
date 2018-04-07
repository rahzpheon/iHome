# -*- coding:utf-8 -*-
from flask import current_app, g, jsonify, request, session
from iHome import constants
from iHome.api_1_0 import api
from iHome.models import Area, House, Facility, HouseImage
from iHome.utils.response_code import RET
from iHome.utils.common import login_required
from iHome.utils.image_storage import upload_image
from iHome import db,redis_store

# 查询地区信息
@api.route('/areas')
def get_areas():

    # 尝试从缓存中读取地区信息
    try:
        area_dict_list = redis_store.get('Areas')
    except Exception as e:
        current_app.logger.error(e)

    if not area_dict_list:

        # 获取所有地区对象
        areas = Area.query.all()

        # 将所有地区对象的信息放入列表
        area_dict_list = []
        for area in areas:
            area_dict_list.append(area.to_dict())

        # 将内容进行缓存
        redis_store.set('Areas', area_dict_list, constants.AREA_INFO_REDIS_EXPIRES)

    else:
        area_dict_list = eval(area_dict_list)

    # 放入字典中,在前端调用时更加直观
    params = {'area_dict_list':area_dict_list}

    # 返回响应(当地区信息为空时返回空数据)
    return jsonify(errno=RET.OK, errmsg="成功", data=params)

# 上传房屋信息
@api.route('/houses', methods=['POST'])
@login_required
def pub_house():

    # 1.获取所有参数
    json_dict = request.json
    if not json_dict:
        return jsonify(errno=RET.PARAMERR, errmsg='请输入参数')

    title = json_dict.get('title')
    price = json_dict.get('price')
    address = json_dict.get('address')
    area_id = json_dict.get('area_id')
    room_count = json_dict.get('room_count')
    acreage = json_dict.get('acreage')
    unit = json_dict.get('unit')
    capacity = json_dict.get('capacity')
    beds = json_dict.get('beds')
    deposit = json_dict.get('deposit')
    min_days = json_dict.get('min_days')
    max_days = json_dict.get('max_days')

    if not all(
            [title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    # 校验小数,避免产生精度问题
    price = int(float(price)* 100)
    deposit = int(float(deposit)* 100)

    # 实例化对象并赋值
    house = House()
    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 为关联对象赋值
    facilities = json_dict.get('facility')
    facilities = Facility.query.filter(Facility.id.in_(facilities)).all()
    house.facilities = facilities

    # 保存到数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="新建房屋失败")

    # 返回响应
    data = {'house_id':house.id}
    return jsonify(errno=RET.OK, errmsg="OK", data=data)

# 上传房屋图片
@api.route('/houses/image', methods=['POST'])
@login_required
def upload_house_image():
    # 获取参数
    house_id = request.form.get('house_id')
    if not house_id:
        return jsonify(errno=RET.PARAMERR, errmsg="缺少必要参数")
    try:
        img_data = request.files.get('house_image')
    except Exception as e:
        return jsonify(errno=RET.PARAMERR, errmsg="无法接受图片")

    # 校验参数
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询房屋数据失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    # 调用方法,将文件上传至七牛云,获取返回的key
    try:
        key = upload_image(img_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传失败")

    # 将house_id与key保存至数据库
    house_img = HouseImage()
    house_img.house_id = house_id
    house_img.url = key

    # 尝试选择房屋默认图片
    if not house.index_image_url:
        house.index_image_url = key

    try:
        db.session.add(house_img)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errms='存储房屋图片失败')

    # 返回响应,因为要实时刷新图片,拼接url
    params = {
        'img_url':constants.QINIU_DOMIN_PREFIX + key
    }

    return jsonify(errno=RET.OK, errmsg="OK", data=params)

# 获取房屋信息
@api.route('/houses/detail/<int:house_id>')
def get_house_detail(house_id):

    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋不存在")

    params = {
        'house' : house.to_full_dict()
    }

    # 传递当前用户id
    login_user_id = session.get('user_id', -1)

    return jsonify(errno=RET.OK, errmsg="OK", data=params, login_user_id=login_user_id)

# 首页获取房屋信息
@api.route('/houses/index')
def get_house_index():
    # 获取最新的5条房屋信息
    try:
        index_houses = House.query.order_by(House.create_time.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")

    house_dict_list = []
    for house in index_houses:
        house_dict_list.append(house.to_basic_dict())

    return jsonify(errno=RET.OK, errmsg="", data={'house_dict_list':house_dict_list})


#

# 搜索房屋信息
@api.route('/houses/search')
def get_houses_search():

    # 获取参数
    aid = request.args.get('aid')   #　地区id
    sk = request.args.get('sk')     # 排序方式
    p = request.args.get('p', 1)    # 页数

    # 校验参数
    try:
        p = int(p)  # 清除非法值
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    house_query = House.query

    try:
        # 根据参数进行过滤
        if aid:
            house_query = house_query.filter(House.area_id==aid)

        # 排序
        if sk:
            if sk == 'booking':
                house_query = house_query.order_by(House.order_count.desc())
            elif sk == 'price-inc':
                house_query = house_query.order_by(House.price)
            elif sk == 'price-desc':
                house_query = house_query.order_by(House.price.desc())
            else:
                house_query = house_query.order_by(House.create_time.desc())

        # 分页
        # 参数: 当前页码,总页数,为空时是否输出错误
        paginate = house_query.paginate(p, constants.HOUSE_LIST_PAGE_CAPACITY, False)
        total_page = paginate.pages     # 总页数
        houses = paginate.items        # 当前页对象列表

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="房屋信息为空")



    # houses = house_query.all()

    house_dict_list = []
    for house in houses:
        house_dict_list.append(house.to_basic_dict())

    params = {
        'house_dict_list':house_dict_list,
        'total_page':total_page
    }

    return jsonify(errno=RET.OK,errmsg='OK', data=params)