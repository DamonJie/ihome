#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

# from CCPRestSDK import REST
from libs.yuntongxun.CCPRestSDK import REST
import configparser
import logging

#���ʺ�
accountSid= '8a216da866f71d04016706e25f6605d5';

#���ʺ�Token
accountToken= '37bdff1a56564f4fa31cdcaf295bfdc3';

#Ӧ��Id
appId='8a216da866f71d04016706e2601d05db';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort=8883;

#REST�汾��
softVersion='2013-12-26';

  # ����ģ�����
  # @param to �ֻ�����
  # @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

# def sendTemplateSMS(to,datas,tempId):
#
#
#     #��ʼ��REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


class CCP(object):

    def __init__(self):
        self.rest = REST(serverIP, serverPort, softVersion)
        self.rest.setAccount(accountSid, accountToken)
        self.rest.setAppId(appId)

    @staticmethod
    def instance():
        if not hasattr(CCP, "_instance"):
            CCP._instance = CCP()
        return CCP._instance

    def sendTemplateSMS(self, to, datas, tempId):
        try:
            result = self.rest.sendTemplateSMS(to, datas, tempId)
            print(result)
        except Exception as e:
            logging.error(e)
            raise e

        # print result
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        if result.get("statusCode") == "000000":
            return True
        else:
            print(result.get("statusCode"))
            return False

ccp = CCP.instance()

if __name__ == "__main__":
    ccp = CCP.instance()
    ccp.sendTemplateSMS("17372897591", ["1234", 5], 1)



   
#sendTemplateSMS(�ֻ�����,��������,ģ��Id)