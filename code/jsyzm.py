#!/usr/bin/python
# -*- coding: utf-8 -*-
# FileName : jsyzm.py
# Author   : Shan
# DateTime : 2018/12/3
# SoftWare : PyCharm

import requests,json,sys
from urllib import urlencode
from urllib import unquote
import globalvar as gl

global logger
global CONF

class JSJM():
    def __init__(self):
        if CONF['jsyzm'].has_key('user') == True and CONF['jsyzm'].has_key('pwd') == True:
            self.username = CONF['jsyzm']['user']
            self.password = CONF['jsyzm']['pwd']
        else:
            logger.error('极速接码平台未配置用户名和密码')
        self.phone = ''
        self.token = ''
        self.xmid  = '3557'  #斗鱼
        #self.xmid  = '392'  #京东
        if self.login() != True:
            logger.error('极速接码平台登陆获取Token失败')

    def login(self):
        """
        功能：接码平台登录
        输入参数：无
        返回值：  False ： 登录失败
                 token ：
        """
        url = "http://www.js-yzm.com:9180/service.asmx/UserLoginStr"
        payload = dict(name=self.username, psw=self.password)
        r = requests.get(url, params=payload)
        logger.debug('接码平台链接: '+str(r.url))
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('get 失败,r.status_code=%d', r.status_code)
            return False
        logger.debug('get 成功, r.status_code=%d', r.status_code)

        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)
        if responsed == '' :
            logger.error('调用接口超时异常')
            return False
        elif responsed == '0':
            logger.error('帐户处于禁止使用状态')
            return False
        elif responsed == '-1':
            logger.error('调用接口失败')
            return False
        elif responsed == '-2':
            logger.error('帐户信息错误')
            return False
        elif responsed == '-3':
            logger.error('用户或密码错误')
            return False
        elif responsed == '-4':
            logger.error('不是普通帐户')
            return False
        elif responsed == '-30':
            logger.error('非绑定IP')
            return False
        self.token = responsed
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
                                        : -2 提交取号任务超量，请释放占用号码
                                        : -3 获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。
                                        : -4 该项目已经被禁用，暂停取号做业务
                                        : -8 帐户余额不足
                                        : -11 端口繁忙被占用，请稍后再试
                                        : -12 该项目不能以获取号码方式工作
                                        : -15 查找不到该专属对应KEY
                                        : -100 没登陆或token过期
                                        : -101 调用接口超时异常
                                        : -200 返回选择排队获取号码任务Id编号,当返回数据包含id=****时，
                                          说明服务器繁忙不能即时分配号码，已经帮生个获取号码任务Id用来二次
                                          查询获取号码，可在延时5-20秒之后用这个任务Id值再次调用GetTaskStr
                                          接口函数获取分配的号码。
        """
        ou = dict(error=0, data=dict(), msg='ok')
        url = "http://www.js-yzm.com:9180/service.asmx/GetHM2Str"
        payload = dict(token=self.token, xmid=self.xmid, sl='1',lx='6',ks='0',rj='707399420',a1='',a2='',pk='')
        r = requests.get(url, params=payload)
        logger.debug('接码平台链接: %s', r.url)
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('get 失败,r.status_code=%d', r.status_code)
            ou['error'] = '1'
            ou['msg']   = 'HTTP GET 失败'
            return ou
        logger.debug('get 成功, r.status_code=%d', r.status_code)

        responsed = r.text
        logger.debug('返回内容：%s', responsed)
        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        elif responsed == '0':
            logger.error('没登陆或token过期')
            ou['error'] = 1
            ou['msg'] = '没登陆或token过期'
            return ou
        elif responsed == '-1':
            logger.error('当前没有合条件号码')
            ou['error'] = 1
            ou['msg'] = '当前没有合条件号码'
            return ou
        elif responsed == '-2':
            logger.error('提交取号任务超量，请释放占用号码')
            ou['error'] = 1
            ou['msg'] = '提交取号任务超量，请释放占用号码'
            return ou
        elif responsed == '-3':
            logger.error('获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。')
            ou['error'] = 1
            ou['msg'] = '获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。'
            return ou
        elif responsed == '-4':
            logger.error('该项目已经被禁用，暂停取号做业务')
            ou['error'] = 1
            ou['msg'] = '该项目已经被禁用，暂停取号做业务'
            return ou
        elif responsed == '-8':
            logger.error('帐户余额不足')
            ou['error'] = 1
            ou['msg'] = '帐户余额不足'
            return ou
        elif responsed == '-11':
            logger.error('端口繁忙被占用，请稍后再试')
            ou['error'] = 1
            ou['msg'] = '端口繁忙被占用，请稍后再试'
            return ou
        elif responsed == '-12':
            logger.error('该项目不能以获取号码方式工作')
            ou['error'] = 1
            ou['msg'] = '该项目不能以获取号码方式工作'
            return ou
        elif responsed == '-15':
            logger.error('查找不到该专属对应KEY')
            ou['error'] = 1
            ou['msg'] = '查找不到该专属对应KEY'
            return ou

        str = responsed.split('=', 1)
        if str[0] == 'id':
            logger.error('返回选择排队获取号码任务Id编号')
            ou['error'] = 1
            ou['msg']   = '返回选择排队获取号码任务Id编号'
            ou['data']['id'] = str[1]
        elif str[0] == 'hm':
            ou['error'] = 0
            ou['msg']   = 'ok'
            ou['data']['phone'] = str[1]
        return ou


    def getTaskStr(self, id):
        """
        功能:    通过任务ID获取手机号码
        输入参数：id： 任务ID
        返回值： ou：字典，包含账号信息
                ou['data']['id']        : 任务ID
                ou['data']['phone']     : 手机号码
                ou['msg']               : 信息
                ou['error']             : 0 ok
                                        : 1 HTTP GET 失败
                                        : -1 当前没有合条件号码
                                        : -2 提交取号任务超量，请释放占用号码
                                        : -3 获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。
                                        : -4 该项目已经被禁用，暂停取号做业务
                                        : -8 帐户余额不足
                                        : -11 端口繁忙被占用，请稍后再试
                                        : -12 该项目不能以获取号码方式工作
                                        : -15 查找不到该专属对应KEY
                                        : -100 没登陆或token过期
                                        : -101 调用接口超时异常
                                        : -200 返回选择排队获取号码任务Id编号,当返回数据包含id=****时，
                                          说明服务器繁忙不能即时分配号码，已经帮生个获取号码任务Id用来二次
                                          查询获取号码，可在延时5-20秒之后用这个任务Id值再次调用GetTaskStr
                                          接口函数获取分配的号码。
                                        : -300 任务Id还在等待分配号码中
        """
        ou = dict(error=0, data=dict(), msg='ok')
        url = "http://www.js-yzm.com:9180/service.asmx/GetTaskStr"
        payload = dict(token=self.token, id=id)
        r = requests.get(url, params=payload)
        logger.debug('接码平台链接: ' + str(r.url))
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('get 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg']   = 'HTTP GET 失败'
            return ou
        logger.debug('get 成功, r.status_code=%d', r.status_code)

        responsed = str(r.text)
        logger.debug('返回内容：%s', responsed)
        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        elif responsed == '0':
            logger.error('没登陆或token过期')
            ou['error'] = 1
            ou['msg'] = '没登陆或token过期'
            return ou
        elif responsed == '-1':
            logger.error('当前没有合条件号码')
            ou['error'] = 1
            ou['msg'] = '当前没有合条件号码'
            return ou
        elif responsed == '1':
            logger.error('任务Id还在等待分配号码中')
            ou['error'] = 1
            ou['msg'] = '任务Id还在等待分配号码中'
            return ou
        elif responsed == '-11':
            logger.error('端口繁忙被占用，请稍后再试')
            ou['error'] = 1
            ou['msg'] = '端口繁忙被占用，请稍后再试'
            return ou

        ou['error'] = 0
        ou['msg']   = 'ok'
        ou['data']['phone'] = responsed
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
                                        : -2 提交取号任务超量，请释放占用号码
                                        : -3 获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。
                                        : -4 该项目已经被禁用，暂停取号做业务
                                        : -8 帐户余额不足
                                        : -11 端口繁忙被占用，请稍后再试
                                        : -12 该项目不能以获取号码方式工作
                                        : -15 查找不到该专属对应KEY
                                        : -100 没登陆或token过期
                                        : -101 调用接口超时异常
                                        : -200 返回选择排队获取号码任务Id编号,当返回数据包含id=****时，
                                          说明服务器繁忙不能即时分配号码，已经帮生个获取号码任务Id用来二次
                                          查询获取号码，可在延时5-20秒之后用这个任务Id值再次调用GetTaskStr
                                          接口函数获取分配的号码。
                                        : -300 任务Id还在等待分配号码中
        """
        ou = dict(error=0, data=dict(), msg='ok')
        url = "http://www.js-yzm.com:9180/service.asmx/GetYzm2Str"
        payload = dict(token=self.token, xmid=self.xmid,hm=phone,sf='1')
        r = requests.get(url, params=payload)
        logger.debug('接码平台链接: ' + str(r.url))
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('get 失败,r.status_code=%d', r.status_code)
            ou['error'] = '1'
            ou['msg']   = 'HTTP GET 失败'
            return ou
        logger.debug('get 成功, r.status_code=%d', r.status_code)
        logger.debug(r.text)
        responsed = (r.text).encode('utf-8')
        logger.debug('返回内容：%s', responsed)

        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        elif responsed == '0':
            logger.error('没登陆或token过期')
            ou['error'] = 1
            ou['msg'] = '没登陆或token过期'
            return ou
        elif responsed == '-1':
            logger.error('该号码已经已经被卡商注销。')
            ou['error'] = 1
            ou['msg'] = '该号码已经已经被卡商注销。'
            return ou
        elif responsed == '1':
            logger.error('卡商还没接收到验证信息，等待返回验证码信息')
            ou['error'] = 1
            ou['msg'] = '卡商还没接收到验证信息，等待返回验证码信息'
            return ou
        elif responsed == '-2':
            logger.error('业务已被取消，可重试重新操作语音验证')
            ou['error'] = 1
            ou['msg'] = '业务已被取消，可重试重新操作语音验证'
            return ou
        elif responsed == '-3':
            logger.error('业务异常中止')
            ou['error'] = 1
            ou['msg'] = '业务异常中止'
            return ou
        elif responsed == '-8':
            logger.error('余额不足扣费')
            ou['error'] = 1
            ou['msg'] = '余额不足扣费'
            return ou
        elif responsed == '-9':
            logger.error('专属数据出错	')
            ou['error'] = 1
            ou['msg'] = '专属数据出错	'
            return ou

        code_str = responsed.split('：',1)[1]
        logger.debug('验证码字符串截取：'+code_str)
        code = code_str.split('，',1)[0]
        logger.debug('验证码获取成功：' + code)
        ou['error'] = 0
        ou['msg']   = 'ok'
        ou['data']['code'] = code
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
                                        : -2 提交取号任务超量，请释放占用号码
                                        : -3 获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。
                                        : -4 该项目已经被禁用，暂停取号做业务
                                        : -8 帐户余额不足
                                        : -11 端口繁忙被占用，请稍后再试
                                        : -12 该项目不能以获取号码方式工作
                                        : -15 查找不到该专属对应KEY
                                        : -100 没登陆或token过期
                                        : -101 调用接口超时异常
                                        : -200 返回选择排队获取号码任务Id编号,当返回数据包含id=****时，
                                          说明服务器繁忙不能即时分配号码，已经帮生个获取号码任务Id用来二次
                                          查询获取号码，可在延时5-20秒之后用这个任务Id值再次调用GetTaskStr
                                          接口函数获取分配的号码。
                                        : -300 任务Id还在等待分配号码中
        """
        ou = dict(error=0, data=dict(), msg='ok')
        url = "http://www.js-yzm.com:9180/service.asmx/sfHmStr"
        payload = dict(token=self.token, hm=phone)
        r = requests.get(url, params=payload)
        logger.debug('接码平台链接: ' + str(r.url))
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('get 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg'] = 'HTTP GET 失败'
            return ou
        logger.debug('get 成功, r.status_code=%d', r.status_code)
        logger.debug(r.text)
        responsed = r.text
        logger.debug('返回内容：%s', responsed)

        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        elif responsed == '0':
            logger.error('没登陆或失败')
            ou['error'] = 1
            ou['msg'] = '没登陆或失败'
            return ou
        elif responsed == '-1':
            logger.error('释放号码失败')
            ou['error'] = 1
            ou['msg'] = '释放号码失败'
            return ou
        elif responsed == '1':
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
                                        : -2 提交取号任务超量，请释放占用号码
                                        : -3 获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。
                                        : -4 该项目已经被禁用，暂停取号做业务
                                        : -8 帐户余额不足
                                        : -11 端口繁忙被占用，请稍后再试
                                        : -12 该项目不能以获取号码方式工作
                                        : -15 查找不到该专属对应KEY
                                        : -100 没登陆或token过期
                                        : -101 调用接口超时异常
                                        : -200 返回选择排队获取号码任务Id编号,当返回数据包含id=****时，
                                          说明服务器繁忙不能即时分配号码，已经帮生个获取号码任务Id用来二次
                                          查询获取号码，可在延时5-20秒之后用这个任务Id值再次调用GetTaskStr
                                          接口函数获取分配的号码。
                                        : -300 任务Id还在等待分配号码中
        """
        ou = dict(error=0, data=dict(), msg='ok')
        url = "http://www.js-yzm.com:9180/service.asmx/sfAllStr"
        payload = dict(token=self.token)
        r = requests.get(url, params=payload)
        logger.debug('接码平台链接: ' + str(r.url))
        ##判断http post返回值
        if r.status_code != requests.codes.ok:
            logger.error('get 失败,r.status_code=%d', r.status_code)
            ou['error'] = 1
            ou['msg'] = 'HTTP GET 失败'
            return ou
        logger.debug('get 成功, r.status_code=%d', r.status_code)
        logger.debug(r.text)
        responsed = r.text
        logger.debug('返回内容：%s', responsed)

        if responsed == '':
            logger.error('调用接口超时异常')
            ou['error'] = 1
            ou['msg'] = '调用接口超时异常'
            return ou
        elif responsed == '0':
            logger.error('没登陆或失败')
            ou['error'] = 1
            ou['msg'] = '没登陆或失败'
            return ou
        elif responsed == '-1':
            logger.error('释放号码失败')
            ou['error'] = 1
            ou['msg'] = '释放号码失败'
            return ou
        elif responsed == '1':
            logger.info('成功释放')
            ou['error'] = 0
            ou['msg'] = '成功释放'
            return ou
##初始化获取全局变量
logger = gl.get_logger()
CONF   = gl.get_conf()