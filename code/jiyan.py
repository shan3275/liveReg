#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests,json
from collections import OrderedDict
import globalvar as gl

global logger
"""
功能：    查询点数接口
输入参数： para : dict{}字典，内容如下：
            para.user:  第三方极验平台用户名
            para.pwd:   第三方极验平台密码
输出参数： False : 失败，返回False，并有日志记录
          dianshu:  返回用户所剩点数
"""
def InquiryGeetestPoints(para):
    if para.has_key('user') != True or para.has_key('pwd') != True :
        logger.error('参数错误')
        return False

    payload = {'user': para['user'], 'pass': para['pwd'], 'format':'utf8'}
    r = requests.get("http://jiyanapi.c2567.com/chaxundianshu", params=payload)
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('get 失败,r.status_code=%d', r.status_code)
        return False
    logger.info('get 成功, r.status_code=%d', r.status_code)
    logger.info(r.text)

    data = r.json()
    if data['status'] != 'ok':
        logger.error('返回数据有问题')
        return False
    logger.info('查询点数为：%d', data['dianshu'])
    return data['dianshu']

"""
功能：     通过第三方平台接口进行极验
输入参数：  para=dict() 单个字典参数，字典中包含如下元素
               para.user: 第三方极验平台用户名
               para.pwd： 第三方极验平台密码
               para.gt    斗鱼官方的GeeTest ID，不变
               para.challenge  斗鱼分配给客户端的ID,每次都会变化
输出参数：  False : 失败，返回False，并有日志记录
           out   : 成功，返回数据字典，字典内容如下
                out.validate ：第三方极验平台返回的识别号
                out.challenge：斗鱼分配给客户端的ID,每次都会变化
"""
def JiYanGeetest(para):
    if para == False:
        logger.error('输入参数为空')
        return False

    ##判断点数是否足够
    GeetestInfo = dict(user=para['user'], pwd=para['pwd'])
    logger.info(GeetestInfo)
    points = InquiryGeetestPoints(GeetestInfo)
    if points == False:
        logger.info('获取点数失败')
        return False
    if points < 50:
        logger.info('点数过低，请及时充值')
    if points < 10:
        logger.info('点数基本耗尽，请充值后再尝试')
        return False
    logger.info(points)

    payload = OrderedDict(gt=para['gt'],challenge=para['challenge'],referer='https://www.douyu.com/', \
                          devuser='707399420',user=para['user'])
    payload['pass'] = para['pwd']
    payload['return'] = 'json'
    payload['model'] = '3'
    payload['format'] = 'utf8'
    logger.info(payload)

    r = requests.get("http://jiyanapi.c2567.com/shibie", params=payload)
    logger.info(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('get 失败,r.status_code=%d', r.status_code)
        return False
    logger.info('get 成功, r.status_code=%d', r.status_code)
    logger.info(r.text)

    data = r.json()
    status = data['status']
    if  status == 'no':
        logger.error('请重新获取验证码参数，并重新提交识别')
        return False
    elif status == 'stop':
        logger.error('请停止程序并提示错误信息。该状态是账号有问题的情况')
        return False
    else:
        logger.info('接口返回成功，请带着识别成功的数据提交')

    out = dict(challenge=data['challenge'], validate=data['validate'])
    logger.info(out)
    return out


def JiYanDeepKnowGeetest(user,pwd,gt):
    """
    功能：     通过第三方平台深知接口进行极验，深知接口为最新接口
    输入参数：      user: 第三方极验平台用户名
                   pwd： 第三方极验平台密码
                   gt :  斗鱼官方的GeeTest ID，不变
    输出参数：  False : 失败，返回False，并有日志记录
               challenge   : 成功，返回数据 斗鱼分配给客户端的ID,每次都会变化
    """
    ##判断点数是否足够
    GeetestInfo = dict(user=user, pwd=pwd)
    logger.info(GeetestInfo)
    points = InquiryGeetestPoints(GeetestInfo)
    if points == False:
        logger.info('获取点数失败')
        return False
    if points < 50:
        logger.info('点数过低，请及时充值')
    if points < 10:
        logger.info('点数基本耗尽，请充值后再尝试')
        return False
    logger.debug(points)

    payload = OrderedDict(user=user)
    payload['pass'] = pwd
    payload['referer'] = 'https://passport.douyu.com'
    payload['gt'] = gt
    payload['supportclick'] = 'ruokuai'
    payload['supportuser']  = '707399420'
    payload['supportpass']  = 'a5vufatcWZHYbjd'
    payload['format'] = 'utf8'
    #payload['devuser'] = '707399420'
    logger.debug(payload)
    NETWORK_STATUS  = True
    REQUEST_TIMEOUT = False
    try:
        r = requests.get("http://jiyanapishenzhi.c2567.com/shibie_shenzhi", params=payload, timeout=20)
    except requests.exceptions.ConnectTimeout:
        NETWORK_STATUS = False
    except requests.exceptions.Timeout:
        REQUEST_TIMEOUT = True

    if NETWORK_STATUS == False or REQUEST_TIMEOUT == True:
        logger.error('timeout')
        return False
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('get 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('get 成功, r.status_code=%d', r.status_code)
    logger.debug(r.text)

    data = r.json()
    if data.has_key('msg'):
        logger.error('msg:%s', data['msg'])
    status = data['status']
    if  status == 'no':
        logger.error('识别失败请重试')
        return False
    elif status == 'stop':
        logger.error('用户账号有问题，请停止软件，并提示错误信息')
        return False
    elif status == 'ok':
        logger.info('识别成功')

    if data.has_key('validate'):
        return data['validate']
    logger.error('返回数据中没有challenge')
    return False


logger = gl.get_logger()