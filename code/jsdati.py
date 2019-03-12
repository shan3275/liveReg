#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : jsdati.py
# Author   : Shan
# 说明：联众识别接口
# DateTime : 2018/12/26
# SoftWare : PyCharm

import requests,json,sys
import tempfile
from urllib import urlencode
from urllib import unquote
import globalvar as gl

global logger
global CONF

class JSDATI():
    def __init__(self,upload):
        if CONF['jsdati'].has_key('user') == True and CONF['jsdati'].has_key('pwd') == True:
            self.username = CONF['jsdati']['user']
            self.password = CONF['jsdati']['pwd']
        else:
            logger.error('联众打码平台账号未设置')
        self.dragmode = '1318'
        self.wordmode = '1303'
        self.upload   = upload

    def verifyPic(self, mode):
        """
        :param mode: drag or word
        :return:
        """
        url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=upload"
        if mode == 'drag':
            data = dict(user_name=self.username, user_pw=self.password, yzmtype_mark=self.dragmode)
        else:
            data = dict(user_name=self.username, user_pw=self.password,yzmtype_mark=self.wordmode)
        logger.info(self.upload)
        file_obj = open(self.upload, 'rb')
        img_file  = {'upload':file_obj}
        logger.info(data)
        logger.info(img_file)
        r = requests.post(url, data, files=img_file)
        file_obj.close()
        logger.debug('打码平台链接: ' + str(r.url))
        #logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return False
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = r.json()
        logger.debug('返回内容：%s', responsed)
        if responsed['result'] == True:
            return responsed['data']['val']
        else:
            return False

    def submitError(self, id):
            """
            :param id：错误id
            :return:
            """
            url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=error"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            data = "user_name=%s&user_pw=%s&yzm_id=%s" % (self.username, self.password, id)
            r = requests.post(url, data=data, headers=headers)
            logger.debug('打码平台链接: ' + str(r.url))
            logger.debug('命令字: ' + data)
            ##判断http post返回值
            if r.status_code != requests.codes.ok:
                logger.error('post 失败,r.status_code=%d', r.status_code)
                return False
            logger.debug('post 成功, r.status_code=%d', r.status_code)

            responsed = r.json()
            logger.debug('返回内容：%s', responsed)
            if responsed['result'] == True:
                return True
            else:
                return False

    def getPoints(self):
        """
        :param :
        :return:
        """
        url = "http://v1-http-api.jsdama.com/api.php?mod=php&act=point"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = "user_name=%s&user_pw=%s" % (self.username, self.password)
        r = requests.post(url, data=data, headers=headers)
        logger.debug('打码平台链接: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return False
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = r.json()
        logger.debug('返回内容：%s', responsed)
        if responsed['result'] == True:
            return responsed['data']
        else:
            return False

##初始化获取全局变量
logger = gl.get_logger()
CONF   = gl.get_conf()