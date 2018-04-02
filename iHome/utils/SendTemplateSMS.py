#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from iHome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= '8aaf0708627645a801628133b3dd01b7';

#���ʺ�Token
accountToken= '0a73a803b6494cc0a7e901df940c2a8c';

#Ӧ��Id
appId='8aaf0708627645a801628133b44401be';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='sandboxapp.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';




#sendTemplateSMS(�ֻ�����,��������,ģ��Id)

class CCP(object):
    '''���Ͷ��ŵĸ�����'''

    def __new__(cls, *args, **kwargs):
        # �ж��Ƿ����������_instance��_instance����CCP��Ψһ���󣬼�����
        if not hasattr(CCP, "instance"):
            cls.instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls.instance.rest = REST(serverIP, serverPort, softVersion)
            cls.instance.rest.setAccount(accountSid, accountToken)
            cls.instance.rest.setAppId(appId)
        return cls.instance

    def send_template_sms(self, to, datas, temp_id):
        """����ģ�����"""
        # @param to �ֻ�����
        # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
        # @param temp_id ģ��Id
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # �����ͨѶ���Ͷ��ųɹ������ص��ֵ�����result��statuCode�ֶε�ֵΪ"000000"
        if result.get("statusCode") == "000000":
            # ����0 ��ʾ���Ͷ��ųɹ�
            return 0
        else:
            # ����-1 ��ʾ����ʧ��
            return -1


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id


def sendTemplateSMS(to, datas, tempId):
    # ��ʼ��REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():

        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)