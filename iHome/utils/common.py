# -*- coding:utf-8 -*-

from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    '''路由匹配转换器'''
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)

        self.regex = args[0]
