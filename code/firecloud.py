#!/usr/bin/python
# -*- coding: utf-8 -*-
# FileName : firecloud.py
# Author   : Shan
# DateTime : 2019/3/1
# SoftWare : PyCharm

import requests,json,sys
from urllib import urlencode
from urllib import unquote
import globalvar as gl

global logger
global CONF

class FireCloud():
    def __init__(self):
        if CONF['firecloud'].has_key('user') == True and CONF['firecloud'].has_key('pwd') == True:
            self.username = CONF['firecloud']['user']
            self.password = CONF['firecloud']['pwd']
        else:
            logger.error('FireCloud 接码平台未配置用户名和密码')
        self.phone   = ''
        self.token   = ''
        self.url     = 'http://huoyun888.cn/api/do.php'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.xmid    = '71'  #斗鱼
        if self.login() != True:
            logger.error('FireCloud 接码平台登陆获取Token失败')

    def login(self):
        """
        功能：接码平台登录
        测试连接：curl -d "action=loginIn&name=kstr2019&password=d1ruSRiN85ZSDo2srA" -X POST http://huoyun888.cn/api/do.php
        输入参数：无
        返回值：  False ： 登录失败
                 token ：
        """
        data = "action=loginIn&name=%s&password=%s" % (self.username, self.password)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('接码平台链接: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            return False
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)
        responsedArray = responsed.split('|', 1)
        logger.debug(responsedArray)
        ok = responsedArray[0]
        token = responsedArray[1]
        if responsed == '' :
            logger.error('调用接口超时异常')
            return False
        if ok == '0':
            logger.error('登录失败，用户不存在或密码不正确')
            return False

        self.token = token
        return True

    def getPhone(self):
        """
        功能：从接码平台获取手机号码
        输入参数：无
                 location：字典，格式{'province': '\xe6\xb9\x96\xe5\x8c\x97', 'city': '\xe6\xad\xa6\xe6\xb1\x89'}
        返回值： ou：字典，包含账号信息
                ou['data']['id']        : 任务ID
                ou['data']['phone']     : 手机号码
                ou['msg']      : 信息
                ou['error']             : 0 ok
                                        : 1 HTTP GET 失败
                                        : -1 当前没有合条件号码
        """
        ou = dict(error=0, data=dict(), msg='ok')
        data = "action=getPhone&sid=%s&token=%s&vno=0" % (self.xmid, self.token)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('接码平台链接: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg'] = 'HTTP GET 失败'
            return ou
        logger.debug('post 成功, r.status_code=%d', r.status_code)

        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)
        responsedArray = responsed.split('|')
        logger.debug(responsedArray)
        ok = responsedArray[0]
        info = responsedArray[1]
        if responsed == '' :
            logger.error('调用接口超时异常')
            ou['error'] = 100
            ou['msg'] = '调用接口超时异常'
            return ou
        if ok == '0':
            logger.error(info)
            ou['error'] = 1
            ou['msg'] = info
            return ou

        if  ok == '1':
            ou['error'] = 0
            ou['msg']   = 'ok'
            ou['data']['phone'] = info
        return ou

    def getCode(self,phone):
        """
        功能：从接码平台获取验证码并不再使用本号码
        输入参数：phone ：手机号码
        返回值： ou：字典，包含账号信息
                ou['data']['id']        : 任务ID
                ou['data']['phone']     : 手机号码
                ou['data']['code']      : 验证码
                ou['msg']               : 信息
                ou['error']             : 0 ok
                                        : 1 HTTP GET 失败
                                        : -1 当前没有合条件号码
        """
        ou = dict(error=0, data=dict(), msg='ok')
        data = "action=getMessage&sid=%s&token=%s&phone=%s" % (self.xmid,self.token, phone)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('接码平台链接: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg'] = 'HTTP GET 失败'
            return ou
        logger.debug('post 成功, r.status_code=%d', r.status_code)
        logger.debug(r.text)
        responsed = (r.text).encode('utf-8')
        logger.debug('返回内容：%s', responsed)
        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)

        responsedArray = responsed.split('|', 1)
        logger.debug(responsedArray)
        ok = responsedArray[0]
        info = responsedArray[1]

        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        if ok == '0':
            logger.error(info)
            ou['error'] = 1
            ou['msg'] = info
            return ou

        code_str = info.split('：',1)[1]
        logger.debug('验证码字符串截取：'+code_str)
        code = code_str.split('，',1)[0]
        logger.debug('验证码获取成功：' + code)
        ou['error'] = 0
        ou['msg']   = 'ok'
        ou['data']['code'] = code
        return ou

    def addBlackList(self,phone):
        """
        手机号加入黑名单
        参数：phone，手机号码
        返回值： ou：字典，包含账号信息
                ou['data']['id']        : 任务ID
                ou['data']['phone']     : 手机号码
                ou['data']['code']      : 验证码
                ou['msg']               : 信息
                ou['error']             : 0 ok
                                        : 1 HTTP GET 失败
                                        : -1 当前没有合条件号码
        """
        ou = dict(error=0, data=dict(), msg='ok')
        data = "action=addBlacklist&sid=%s&token=%s&phone=%s" % (self.xmid, self.token, phone)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('接码平台链接: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg'] = 'HTTP GET 失败'
            return ou
        logger.debug('post 成功, r.status_code=%d', r.status_code)
        logger.debug(r.text)
        responsed = (r.text).encode('utf-8')
        logger.debug('返回内容：%s', responsed)
        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)

        responsedArray = responsed.split('|', 1)
        logger.debug(responsedArray)
        ok = responsedArray[0]
        info = responsedArray[1]

        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        if ok == '0':
            logger.error(info)
            ou['error'] = 1
            ou['msg'] = info
            return ou

        if ok == '1':
            logger.info('成功释放')
            ou['error'] = 0
            ou['msg'] = '成功释放'
            return ou

    def releasePhone(self,phone):
        """
        释放占用手机号码
        参数：phone，手机号码
        返回值： ou：字典，包含账号信息
                ou['data']['id']        : 任务ID
                ou['data']['phone']     : 手机号码
                ou['data']['code']      : 验证码
                ou['msg']               : 信息
                ou['error']             : 0 ok
                                        : 1 HTTP GET 失败
                                        : -1 当前没有合条件号码
        """
        ou = dict(error=0, data=dict(), msg='ok')
        data = "action=cancelRecv&sid=%s&token=%s&phone=%s" % (self.xmid,self.token, phone)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('接码平台链接: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg'] = 'HTTP GET 失败'
            return ou
        logger.debug('post 成功, r.status_code=%d', r.status_code)
        logger.debug(r.text)
        responsed = (r.text).encode('utf-8')
        logger.debug('返回内容：%s', responsed)
        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)

        responsedArray = responsed.split('|', 1)
        logger.debug(responsedArray)
        ok = responsedArray[0]
        info = responsedArray[1]

        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        if ok == '0':
            logger.error(info)
            ou['error'] = 1
            ou['msg'] = info
            return ou

        if ok == '1':
            logger.info('成功释放')
            ou['error'] = 0
            ou['msg'] = '成功释放'
            return ou

    def releaseAllPhone(self):
        """
        释放占用手机号码
        参数：phone，手机号码
        返回值： ou：字典，包含账号信息
                ou['data']['id']        : 任务ID
                ou['data']['phone']     : 手机号码
                ou['data']['code']      : 验证码
                ou['msg']               : 信息
                ou['error']             : 0 ok
                                        : 1 HTTP GET 失败
                                        : -1 当前没有合条件号码
        """
        ou = dict(error=0, data=dict(), msg='ok')
        data = "action=cancelAllRecv&token=%s" % (self.token)
        r = requests.post(self.url, data=data, headers=self.headers)
        logger.debug('接码平台链接: ' + str(r.url))
        logger.debug('命令字: ' + data)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('post 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg'] = 'HTTP GET 失败'
            return ou
        logger.debug('post 成功, r.status_code=%d', r.status_code)
        logger.debug(r.text)
        responsed = (r.text).encode('utf-8')
        logger.debug('返回内容：%s', responsed)
        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)

        responsedArray = responsed.split('|', 1)
        logger.debug(responsedArray)
        ok = responsedArray[0]
        info = responsedArray[1]

        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        if ok == '0':
            logger.error(info)
            ou['error'] = 1
            ou['msg'] = info
            return ou

        if ok == '1':
            logger.info('成功释放所有')
            ou['error'] = 0
            ou['msg'] = '成功释放'
            return ou

##初始化获取全局变量
logger = gl.get_logger()
CONF   = gl.get_conf()