#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : dyconsole.py
# Author   : Shan
# 说明：联众识别接口
# DateTime : 2019/1/11
# SoftWare : PyCharm

import requests,json,sys
import tempfile
from urllib import urlencode
from urllib import unquote
import base64
import globalvar as gl

global logger
global CONF

class DYConApi():
    def __init__(self):
        self.url = CONF['dyconsole']['url']
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def queryOne(self):
        data = 'action=queryOne'
        logger.debug(data)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return None
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = r.json()
        logger.debug('返回内容：%s', responsed)
        if responsed['error'] == 0:
            str = base64.b64decode(responsed['data']['acc'])
            return str
        else:
            return None

    def queryOneByDate(self,day):
        data = 'action=queryOneByDate&day=' +day
        logger.debug(data)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return None
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = r.json()
        logger.debug('返回内容：%s', responsed)
        if responsed['error'] == 0:
            str = base64.b64decode(responsed['data']['acc'])
            return str
        else:
            return None

    def queryOneOutDate(self):
        data = 'action=queryOneOutDate'
        logger.debug(data)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return None
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = r.json()
        logger.debug('返回内容：%s', responsed)
        if responsed['error'] == 0:
            str = base64.b64decode(responsed['data']['acc'])
            return str
        else:
            return None

    def insertOne(self, entry):
            """
            :param id：错误id
            :return:
            """
            entry_encry = base64.b64encode(entry)
            data = 'action=insertOne&entry='+entry_encry
            r = requests.post(self.url, data=data, headers=self.headers)
            logger.debug('DY Console url: ' + str(r.url))
            logger.debug('命令字: ' + data)
            ##判断http post返回值
            if r.status_code != requests.codes.ok:
                logger.error('post 失败,r.status_code=%d', r.status_code)
                return False
            logger.debug('post 成功, r.status_code=%d', r.status_code)

            responsed = r.json()
            logger.debug('返回内容：%s', responsed)
            if responsed['error'] == 0:
                return True
            else:
                return False

    def queryOneByNickname(self,nickname):
        """
        :param :
        :return:
        """
        data = 'action=queryOneByNickname&nick=' + nickname
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('DY Console url: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return None
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = r.json()
        logger.debug('返回内容：%s', responsed)
        if responsed['error'] == 0:
            return responsed['data']
        else:
            return None

    def updateOne(self,entry):
        entry_encry = base64.b64encode(entry)
        entry_encry = entry_encry.replace("+", "%2B")
        data = 'action=updateOne&entry=' + entry_encry
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('DY Console url: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return False
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = r.json()
        logger.debug('返回内容：%s', responsed)
        if responsed['error'] == 0:
            return True
        else:
            return False

##初始化获取全局变量
logger = gl.get_logger()
CONF   = gl.get_conf()