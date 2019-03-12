#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests,json
from urllib import urlencode
from urllib import unquote
import globalvar as gl

global logger
global CONF
"""
功能：接码平台登录
输入参数：user ：用户名
         pwd  ：密码    
返回值：  False ： 登录失败
         token ：
"""
def JieMaLogin(user,pwd):
    url = "http://api.jmyzm.com/http.do"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "action=loginIn&uid=%s&pwd=%s" %(user, pwd)
    r = requests.post(url, data=data, headers=headers)
    logger.debug('接码平台链接: '+str(r.url))
    logger.debug('命令字: '+data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = str(r.text)
    logger.debug('返回内容：%s', responsed)
    if responsed == 'account_is_stoped' :
        logger.error('账号被停用')
        return False
    elif responsed == 'account_is_locked':
        logger.error('账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
        return False
    elif responsed == 'account_is_closed':
        logger.error('账号被关闭（登录官网进入安全中心开启）')
        return False
    elif responsed == 'message|to_fast_try_again':
        logger.error('访问过快，限制1秒一次。')
        return False
    elif responsed == 'login_error':
        logger.error('用户名密码错误')
        return False
    responsedArray = responsed.split('|', 1 )
    logger.debug(responsedArray)
    acc = responsedArray[0]
    token = responsedArray[1]
    if acc.lower() == user.lower():
        logger.debug('Token 获取成功：'+token)
        return token


"""
功能：获取本机IP
输入参数：无
输出参数：False :获取IP失败
         IP    :获取IP,返回字符串
"""
def GetCurrentIP():
    r = requests.get(r"http://jsonip.com")
    if r.status_code != requests.codes.ok:
        logger.error('get 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('get 成功, r.status_code=%d', r.status_code)
    logger.debug(r.text)
    ip = str(r.json()['ip'])
    logger.debug('本机IP：'+ip)
    return ip

"""
功能：获取地理位置
输入参数：ip
输出参数：False  :获取地理位置失败
         location ：dict
            location.province  :省份
            location.city      :城市
"""
def GetCurrentLocation(ip):
    ###post方式不太稳定，故使用get方式
    #url = "http://ip.taobao.com/service/getIpInfo.php"
    #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #data = 'ip=' + ip
    #r = requests.post(url, data=data, headers=headers)
    r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
    logger.debug(r.url)
    if r.status_code != requests.codes.ok:
        logger.error('get 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('get 成功, r.status_code=%d', r.status_code)
    logger.debug(r.text)
    responsed = r.json()
    statusCode = str(responsed['code'])
    if statusCode != '0':
        logger.error("返回信息错误")
        return False
    region = responsed['data']['region'].encode("utf-8")
    city   = responsed['data']['city'].encode("utf-8")
    location = dict(province=region,city=city)
    logger.debug('location : %s', location)
    logger.debug(urlencode(location))
    return location


"""
功能：从接码平台获取手机号码
输入参数：user  : 用户名，字符串
         token ：用户登陆返回的token，字符串
         pid   ：项目id，string格式
         location：字典，格式{'province': '\xe6\xb9\x96\xe5\x8c\x97', 'city': '\xe6\xad\xa6\xe6\xb1\x89'}
返回值：  False ： 登录失败
         phone ： 如果成功，返回手机号码
"""
def JieMaGetPhone(user,token,pid,location):
    url = "http://api.jmyzm.com/http.do"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    #data = "action=getMobilenum&uid=%s&token=%s&pid=%s&%s&vno=0" % (user, token,pid,urlencode(location))
    data = "action=getMobilenum&uid=%s&token=%s&pid=%s&vno=0" % (user, token, pid )
    r = requests.post(url, data=data, headers=headers)
    logger.debug('接码平台链接: ' + str(r.url))
    logger.debug('命令字: ' + data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = str(r.text)
    logger.debug('返回内容：%s', responsed)
    if responsed == 'account_is_stoped':
        logger.error('账号被停用')
        return False
    elif responsed == 'account_is_locked':
        logger.error('账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
        return False
    elif responsed == 'account_is_closed':
        logger.error('账号被关闭（登录官网进入安全中心开启）')
        return False
    elif responsed == 'message|to_fast_try_again':
        logger.error('访问过快，限制1秒一次。')
        return False
    elif responsed == 'no_data':
        logger.error('系统暂时没有可用号码了')
        return False
    elif responsed == 'parameter_error':
        logger.error('传入参数错误')
        return False
    elif responsed == 'not_login':
        logger.error('没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
        return False
    elif responsed == 'you_cannot_get':
        logger.error('使用了项目绑定（登录官网进入安全中心解除绑定或添加该项目绑定）')
        return False
    elif responsed == 'not_found_project':
        logger.error('没有找到项目,项目ID不正确')
        return False
    elif responsed == 'Lack_of_balance':
        logger.error('可使用余额不足')
        return False
    elif responsed == 'max_count_disable':
        logger.error('已经达到了当前等级可以获取手机号的最大数量，请先处理完您手上的号码再获取新的号码（处理方式：能用的号码就获取验证码，不能用的号码就加黑）')
        return False
    elif responsed == 'unknow_error':
        logger.error('未知错误,再次请求就会正确返回')
        return False
    responsedArray = responsed.split('|', 1)
    logger.debug(responsedArray)
    phone = responsedArray[0]
    token = responsedArray[1]
    if token.lower() == token.lower():
        logger.debug('手机号码获取成功：' + phone)
        return phone

"""
功能：从接码平台获取验证码并不再使用本号码
输入参数：user  : 用户名，字符串
         token ：用户登陆返回的token，字符串
         phone ：手机号码
返回值：  False ： 登录失败
         code ： 如果成功，返回验证码，并释放手机号码
"""
def JieMaGetCode(user,token,phone):
    url = "http://api.jmyzm.com/http.do"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "action=getVcodeAndReleaseMobile&uid=%s&token=%s&mobile=%s" % (user, token, phone)
    r = requests.post(url, data=data, headers=headers)
    logger.debug('接码平台链接: ' + str(r.url))
    logger.debug('命令字: ' + data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)
    logger.debug(r.text)
    responsed = (r.text).encode('utf-8')
    logger.debug('返回内容：%s', responsed)
    if responsed == 'account_is_stoped':
        logger.error('账号被停用')
        return False
    elif responsed == 'account_is_locked':
        logger.error('账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
        return False
    elif responsed == 'account_is_closed':
        logger.error('账号被关闭（登录官网进入安全中心开启）')
        return False
    elif responsed == 'message|to_fast_try_again':
        logger.error('访问过快，限制1秒一次。')
        return False
    elif responsed == 'not_receive':
        logger.error('还没有接收到验证码,请让程序等待几秒后再次尝试')
        return False
    elif responsed == 'parameter_error':
        logger.error('传入参数错误')
        return False
    elif responsed == 'not_login':
        logger.error('没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
        return False
    elif responsed == 'not_found_moblie':
        logger.error('没有找到手机号')
        return False
    elif responsed == 'not_found_project':
        logger.error('没有找到项目,项目ID不正确')
        return False
    elif responsed == 'Lack_of_balance':
        logger.error('可使用余额不足')
        return False
    responsedArray = responsed.split('|', 1)
    logger.debug(responsedArray)
    mobile = responsedArray[0]
    code_str = responsedArray[1].split('：',1)[1]
    logger.debug('验证码字符串截取：'+code_str)
    code = code_str.split('，',1)[0]
    if phone.lower() == mobile.lower():
        logger.debug('验证码获取成功：' + code)
        return code

"""
功能：在接码平台加黑无用号码
输入参数：user  : 用户名，字符串
         token ：用户登陆返回的token，字符串
         phone ：手机号码
返回值：  False ： 登录失败
         code ： 如果成功，返回验证码，并释放手机号码
"""
def JieMaAddIgnoreList(user,token,phone):
    url = "http://api.jmyzm.com/http.do"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "action=addIgnoreList&uid=%s&token=%s&mobile=%s" % (user, token, phone)
    r = requests.post(url, data=data, headers=headers)
    logger.debug('接码平台链接: ' + str(r.url))
    logger.debug('命令字: ' + data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = str(r.text)
    logger.debug('返回内容：%s', responsed)
    if responsed == 'account_is_stoped':
        logger.error('账号被停用')
        return False
    elif responsed == 'account_is_locked':
        logger.error('账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
        return False
    elif responsed == 'account_is_closed':
        logger.error('账号被关闭（登录官网进入安全中心开启）')
        return False
    elif responsed == 'message|to_fast_try_again':
        logger.error('访问过快，限制1秒一次。')
        return False
    elif responsed == 'parameter_error':
        logger.error('传入参数错误')
        return False
    elif responsed == 'not_login':
        logger.error('没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
        return False
    elif responsed == 'unknow_error':
        logger.error('未知错误,再次请求就会正确返回')
        return False
    logger.debug('加黑成功的号码数量：' + responsed)
    return responsed

"""
功能：从接码平台获取用户点数
输入参数： user:  用户ID
         token ：用户登陆返回的token    
返回值：  False ： 登录失败
         points ： 如果成功，返回用户点数
"""
def JieMaetGetUserPoints(user, token):
    url = "http://api.jmyzm.com/http.do"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "action=getUserInfos&uid=%s&token=%s" % (user, token)
    r = requests.post(url, data=data, headers=headers)
    logger.debug('接码平台链接: ' + str(r.url))
    logger.debug('命令字: ' + data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = str(r.text)
    logger.debug('返回内容：%s', responsed)
    if responsed == 'account_is_stoped':
        logger.error('账号被停用')
        return False
    elif responsed == 'account_is_locked':
        logger.error('账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
        return False
    elif responsed == 'account_is_closed':
        logger.error('账号被关闭（登录官网进入安全中心开启）')
        return False
    elif responsed == 'message|to_fast_try_again':
        logger.error('访问过快，限制1秒一次。')
        return False
    elif responsed == 'not_login':
        logger.error('没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
        return False
    elif responsed == 'parameter_error':
        logger.error('传入参数错误')
        return False
    elif responsed == 'unknow_error':
        logger.error('未知错误,再次请求就会正确返回')
        return False
    responsedArray = responsed.split(';')
    logger.debug(responsedArray)
    logger.debug('用户名：'+responsedArray[0]+', 积分：'+responsedArray[1]+', 用户币：'+responsedArray[2]+', 可同时获取号码数：'+responsedArray[3])
    return responsedArray[2]  #返回用户币数


"""
功能：从接码平台获取已经获取的号码列表
输入参数： user:  用户ID
         token ：用户登陆返回的token 
         pid   : 项目ID   
返回值：  False ： 登录失败
         info ： 如果成功，返回：
                没有获取号码记录:[ ] 
                单条：[{"Pid":项目ID,"Recnum":号码,"Timeout":号码超时释放所剩时间,"Start_time":获取号码时间}]（*"Timeout"以秒为单位） 
                多条：[{"Pid":项目ID,"Recnum":号码,"Timeout":号码超时释放所剩时间,"Start_time":获取号码时间},
                      {"Pid":项目ID,"Recnum":号码,"Timeout":号码超时释放所剩时间,"Start_time":获取号码时间},
                      {...}
                     ]（*"Timeout"以秒为单位）
"""
def JieMaetGetRecvInfo(user, token, pid):
    url = "http://api.jmyzm.com/http.do"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "action=getRecvingInfo&uid=%s&token=%s&pid=%s" % (user, token,pid)
    r = requests.post(url, data=data, headers=headers)
    logger.debug('接码平台链接: ' + str(r.url))
    logger.debug('命令字: ' + data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = str(r.text)
    logger.debug('返回内容：%s', responsed)
    if responsed == 'account_is_stoped':
        logger.error('账号被停用')
        return False
    elif responsed == 'account_is_locked':
        logger.error('账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
        return False
    elif responsed == 'account_is_closed':
        logger.error('账号被关闭（登录官网进入安全中心开启）')
        return False
    elif responsed == 'message|to_fast_try_again':
        logger.error('访问过快，限制1秒一次。')
        return False
    elif responsed == 'not_login':
        logger.error('没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
        return False
    elif responsed == 'parameter_error':
        logger.error('传入参数错误')
        return False
    elif responsed == 'unknow_error':
        logger.error('未知错误,再次请求就会正确返回')
        return False
    #logger.debug('用户名：'+responsedArray[0]+', 积分：'+responsedArray[1]+', 用户币：'+responsedArray[2]+', 可同时获取号码数：'+responsedArray[3])
    #return responsedArray[2]  #返回用户币数

"""
功能：     获取手机号码
输入参数：  无
返回值：  phone:  手机号码，类型字符串
"""
def RecvCodeGetPhone():
    user = CONF['jiema']['user']
    pwd = CONF['jiema']['pwd']
    token = JieMaLogin(user, pwd)
    if token == False:
        logger.error('接码平台Token获取失败')
        return False
    #ip = GetCurrentIP()
    #if ip == False:
    #    logger.error('获取本机IP失败')
    #    return False
    #logger.info("客户端本机IP获取成功")
    location = ''
    #location = GetCurrentLocation(ip)
    #if location == False:
    #    logger.error('获取本机位置失败')
    #    return False
    pid = '3737' #斗鱼
    #pid = '1867' #京东
    phone = JieMaGetPhone(user, token, pid, location)
    if phone == False:
        logger.error('获取手机号码失败')
        return False
    #if PhoneJudge(phone) == False:
    #    logger.error('手机号码无效')
    #    return False
    return phone

"""
功能：获取验证码
输入参数：phone
返回值：  code：验证码，字符串
"""
def RecvCodeGetCode(phone):
    user = CONF['jiema']['user']
    pwd = CONF['jiema']['pwd']
    token = JieMaLogin(user, pwd)
    if token == False:
        logger.error('接码平台Token获取失败')
        return False
    code = JieMaGetCode(user, token, phone)
    if code == False:
        logger.error('接码平台验证码获取失败')
        return False
    logger.debug('接码平台验证码获取成功, ' + phone + ' ' + code)
    return code

##初始化获取全局变量
logger = gl.get_logger()
CONF   = gl.get_conf()