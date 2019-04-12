#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : douyu.py
# Author   : Shan
import requests,json
import urllib3
import hashlib
import time
import urllib
from collections import OrderedDict
import urlparse
import random
import globalvar as gl
global logger

def RegisterGetChallenge():
    """
    功能：     注册时从斗鱼官方服务器获取极验需要的参数
    说明：     该功能从易语言客户端拷贝过来方法，试用此接口直接获取gt和challeng
    输入参数：  无
    输出参数：  False : 失败，返回False，并有日志记录
               ou    : 成功，返回数据字典，字典内容如下
                    ou.gt ：斗鱼官方的GeeTest ID，不变
                    ou.challenge：斗鱼分配给客户端的ID,每次都会变化
    """
    result = {}
    url = "https://passport.douyu.com/iframe/checkGeeTest"
    headers = {'Content-Type'   : 'application/x-www-form-urlencoded; charset=UTF-8',
               'User-Agent'     : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
               'accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'referer'        : 'https://passport.douyu.com/member/regNew?client_id=1&lang=cn'}
    data = ""

    r = requests.post(url, data=data,headers=headers)
    logger.info(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.info('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    ##判断返回数据标志位
    if responsed['error'] != 0:
        logger.error('获取数据失败 error=%d', responsed['error'])
        return False
    logger.error('获取数据成功 error=%d', responsed['error'])
    logger.info(responsed)

    ##判断返回数据中是否有gt和challenge
    rsdt = responsed['data']
    if rsdt.has_key('challenge') != True or rsdt.has_key('gt') != True :
        logger.error('challenge or gt 不存在')
        return False

    result['gt'] = rsdt['gt']
    result['challenge'] = rsdt['challenge']
    logger.info(result)
    return result

def CheckGeeTest():
    """
    功能：     注册时从斗鱼官方服务器获取极验需要的参数
    说明：     该功能是在谷歌浏览器中抓取的链接，和RegisterGetChallenge()函数功能相同，但是返回信息不一样，为最新版本
    输入参数：  无
    输出参数：  False : 失败，返回False，并有日志记录
               ou    : 成功，返回数据字典，字典内容如下
                    ou.gt ：斗鱼官方的GeeTest ID，不变
                    ou.code_token：斗鱼分配给客户端的ID,每次都会变化
                    ou.code_type : 数据类型
    """
    result = {}
    url = "https://passport.douyu.com/iframe/checkGeeTest"
    headers = {'Content-Type'   : 'application/x-www-form-urlencoded; charset=UTF-8',
               'User-Agent'     : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
               'accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'referer'        : 'https://passport.douyu.com/member/regNew?client_id=1&lang=cn'}
    data = "op_type=22&gt_version=v4&room_id=0"

    r = requests.post(url, data=data,headers=headers)
    logger.debug(r.url)
    logger.debug(data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    logger.debug(responsed)
    ##判断返回数据标志位
    if responsed['error'] != 0:
        logger.error('获取数据失败 error=%d', responsed['error'])
        return False
    logger.debug('msg:%s', responsed['msg'])

    ##判断返回数据中是否有gt和challenge
    rsdt = responsed['data']
    if rsdt.has_key('code_token') != True:
        logger.error('code_token 不存在')
        return False
    if rsdt.has_key('code_type') != True:
        logger.error('code_type 不存在')
        return False
    if rsdt.has_key('code_data') != True:
        logger.error('code_data 不存在')
        return False
    code_data = rsdt['code_data']
    if code_data.has_key('id') != True:
        logger.error('id 也即gt 不存在')
        return False

    result['code_data_id'] = code_data['id']
    result['code_token']   = rsdt['code_token']
    result['code_type']    = rsdt['code_type']
    logger.info(result)
    return result


def LoginGetChallenge():
    """
    功能：     登陆时从斗鱼官方服务器获取极验需要的参数
    输入参数：  无
    输出参数：  False : 失败，返回False，并有日志记录
               ou    : 成功，返回数据字典，字典内容如下
                    ou.gt ：斗鱼官方的GeeTest ID，不变
                    ou.challenge：斗鱼分配给客户端的ID,每次都会变化
    """
    result = {}
    url = "https://www.douyu.com/member/login/check_geetest_status"
    headers = {'Content-Type'   : 'application/x-www-form-urlencoded',
               'User-Agent'     : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
               'accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'}
    data = "op_type=3722"

    r = requests.post(url, data=data,headers=headers)
    logger.info(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.info('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    ##判断返回数据标志位
    if responsed['error'] != 0:
        logger.error('获取数据失败 error=%d', responsed['error'])
        return False
    logger.error('获取数据成功 error=%d', responsed['error'])
    logger.info(responsed)

    ##判断返回数据中是否有gt和challenge
    rsdt = responsed['data']
    if rsdt.has_key('challenge') != True or rsdt.has_key('gt') != True :
        logger.error('challenge or gt 不存在')
        return False

    result['gt'] = rsdt['gt']
    result['challenge'] = rsdt['challenge']
    logger.info(result)
    return result

def RegisterSendSecurityCode(phone,challenge,validate):
    """
    功能：     注册时触发发送验证码 V3
    输入参数：
                phone  :手机号码,字符串
                challenge :斗鱼平台分配给客户端的ID，字符串
                validate  :第三方平台返回的识别号，字符串
    输出参数：
                0  : 成功
                1  ：http status error
                2  : 130018 错误
                3  ： 其他错误

    """
    url="https://passport.douyu.com/iframe/registerCaptcha"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "phoneNum=" + phone + "&areaCode=0086&lang=cn&geetest_challenge=" + challenge + "&geetest_validate=" + validate + \
           "&geetest_seccode=" + validate + "%7Cjordan"
    logger.info(data)
    r = requests.post(url, data=data,headers=headers)
    logger.info(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return 1
    logger.info('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    logger.debug(responsed)
    if responsed.has_key('msg'):
        logger.debug('msg:'+ responsed['msg'])
    error = str(responsed['error'])

    if error == '130018':
        return 2

    if error == '0':
        logger.info('发送成功')
        return 0
    else:
        logger.error('发送失败')
        return 3


"""
功能：     注册时触发发送验证码，第2次发送
输入参数：  
            phone  :手机号码,字符串
            challenge :斗鱼平台分配给客户端的ID，字符串
            validate  :第三方平台返回的识别号，字符串
输出参数：  
            0  : 成功
            1  ：http status error
            2  : 130018 错误
            3  ： 其他错误

"""
def RegisterSecondSendSecurityCode(phone, challenge, validate):
    url = "https://passport.douyu.com/iframe/registerCaptcha"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "phoneNum=" + phone + "&areaCode=0086&lang=cn&geetest_challenge=" + challenge + "&geetest_validate=" + validate + \
           "&geetest_seccode=" + validate + "%7Cjordan&confirm=1"
    logger.info(data)
    r = requests.post(url, data=data, headers=headers)
    logger.info(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return 1
    logger.info('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    logger.debug(responsed)
    if responsed.has_key('msg'):
        logger.debug('msg:' + responsed['msg'])
    error = str(responsed['error'])

    if error == '0':
        logger.info('发送成功')
        return 0
    else:
        logger.error('发送失败')
        return 3

def RegisterSendSecurityCodeV4(phone, challenge, code_type, code_token, code_data_id):
    """
    功能：     注册时触发发送验证码 V4接口
    输入参数：
                phone  :手机号码,字符串
                challenge :斗鱼平台分配给客户端的ID，字符串
                code_type  :
                code_token :
                code_data_id: gt
    输出参数：
                0  : 成功
                1  ：http status error
                2  : 130018 错误
                3  ： 其他错误

    """
    url = "https://passport.douyu.com/iframe/registerCaptcha"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "phoneNum=" + phone + "&areaCode=0086&lang=cn&room_id=0"+\
           "&code_verify_data%5Bcode_type%5D="+code_type +\
           "&code_verify_data%5Bcode_token%5D="+code_token+\
           "&code_verify_data%5Bcode_data%5D%5Bgeetest_challenge%5D=" + challenge +\
           "&code_verify_data%5Bcode_data%5D%5Bid%5D=" + code_data_id + \
           "&code_verify_data%5Bcode_data%5D%5Bgt_version%5D=v4"
    logger.debug(data)
    r = requests.post(url, data=data, headers=headers)
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return 1
    logger.info('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    logger.debug(responsed)
    if responsed.has_key('msg'):
        logger.debug('msg:' + responsed['msg'])
    error = str(responsed['error'])

    if error == '130018':
        return 2

    if error == '0':
        logger.info('发送成功')
        return 0
    else:
        logger.error('发送失败')
        return 3


def RegisterSecondSendSecurityCodeV4(phone, challenge, code_type, code_token, code_data_id):
    """
    功能：     注册时触发发送验证码，第2次发送, V4接口
    输入参数：
                phone  :手机号码,字符串
                challenge :斗鱼平台分配给客户端的ID，字符串
                code_type  :
                code_token :
                code_data_id: gt
    输出参数：
                0  : 成功
                1  ：http status error
                2  : 130018 错误
                3  ： 其他错误

    """
    url = "https://passport.douyu.com/iframe/registerCaptcha"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "phoneNum=" + phone + "&areaCode=0086&lang=cn&room_id=0"+\
           "&code_verify_data%5Bcode_type%5D="+code_type +\
           "&code_verify_data%5Bcode_token%5D="+code_token+\
           "&code_verify_data%5Bcode_data%5D%5Bgeetest_challenge%5D=" + challenge +\
           "&code_verify_data%5Bcode_data%5D%5Bid%5D=" + code_data_id + \
           "&code_verify_data%5Bcode_data%5D%5Bgt_version%5D=v4"+"&confirm=1"
    logger.debug(data)
    r = requests.post(url, data=data, headers=headers)
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return 1
    logger.info('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    logger.debug(responsed)
    if responsed.has_key('msg'):
        logger.debug('msg:' + responsed['msg'])
    error = str(responsed['error'])

    if error == '130018':
        return 2

    if error == '0':
        logger.info('发送成功')
        return 0
    else:
        logger.error('发送失败')
        return 3


"""
功能：md5运算
"""
def get_token(md5str):
    m1 = hashlib.md5()
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    return token


def RegisterSubmitV4(phone,code,pwd,challenge,code_type,code_token,code_data_id):
    """
    功能：     向斗鱼提交注册账号，V4版本
    输入参数：  字典，包含注册信息
                    phone  :手机号
                    code   :验证码
                    pwd    :随机密码
                    challenge  :斗鱼分配给客户端的ID
                    code_type  :
                    code_token :
                    code_data_id: gt
    输出参数：  False : 失败，返回False，并有日志记录
               ou    : 成功，返回数据字典，字典内容如下
                    ou.url ：api接口
                    ou.nickname：用户名
    """
    epwd = get_token(pwd)
    url = "https://passport.douyu.com/iframe/register"
    headers = {'Content-Type'   : 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "areaCode=0086&phoneNum=" + phone + \
           "&password=" + epwd + \
           "&phoneCaptcha=" + code + \
           "&protocol=on&room_id=0" + \
           "&code_verify_data%5Bcode_type%5D=" + code_type +\
           "&code_verify_data%5Bcode_token%5D=" + code_token +\
           "&code_verify_data%5Bcode_data%5D%5Bgeetest_challenge%5D=" + challenge + \
           "&code_verify_data%5Bcode_data%5D%5Bid%5D=" + code_data_id + \
           "&code_verify_data%5Bcode_data%5D%5Bgt_version%5D=v4" + \
           "&pwdStrength=20&password2=" + epwd+ \
           "&redirect_url=https%3A%2F%2Fpassport.douyu.com%2Fmember%2FregNew%3Fclient_id%3D1%26lang%3Dcn"+\
           "&client_id=1&reg_src=web&cpsid=0&cate_id=0&tag_id=0&child_id=0&vid=0&fac=&sm_did="+\
           "WHJMrwNw1k%2FF850lJ%2BfR%2BGFf%2FDLvrNfWzVsT3cni7zXErB34w4tMmpFdRYZZWfNQs99UPErjYNGNV%2FSatQs6UrpNQn3BzQHozz3nP0jYCRmpFRwA4lt%2FwMpSD3EmPbcN1vgZFTdvyb2Uw6t30Vu0PJD6V498UuG9IEoY%2F%2BNvi9jBkhoMiJ81hY8BW2zeqX%2B06tehGNg%2F%2FPOtiNVCcw5ywKMLGx5XYwKeDD6WR0p9hAyT7wUXd7IF21U2lstx30LSbR%2Ft9WW%2FjIrA%3D1487582755342"+\
           "&did=&lang=cn"
    logger.debug(data)
    r = requests.post(url, data=data,headers=headers)
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    if responsed.has_key('msg'):
        logger.debug('msg:'+ responsed['msg'])
    logger.debug(responsed)
    error = str(responsed['error'])

    if error != '0':
        logger.debug('获取数据失败')
        return False

    logger.error('获取数据成功')
    return responsed['data']

def RegisterSubmit(phone,code,pwd,challenge,validate):
    """
    功能：     向斗鱼提交注册账号
    输入参数：  字典，包含注册信息
                    phone  :手机号
                    code   :验证码
                    pwd    :随机密码
                    challenge  :斗鱼分配给客户端的ID
                    validate   :第三方极验平台返回的识别码
    输出参数：  False : 失败，返回False，并有日志记录
               ou    : 成功，返回数据字典，字典内容如下
                    ou.url ：api接口
                    ou.nickname：用户名
    """
    epwd = get_token(pwd)
    url = "https://passport.douyu.com/iframe/register"
    headers = {'Content-Type'   : 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = "areaCode=0086&phoneNum=" + phone + "&password=" + epwd + "&geetest_challenge="\
           + challenge + "&geetest_validate=" + validate + "&geetest_seccode=" + validate + \
           "%7Cjordan&phoneCaptcha=" + code + "&protocol=on&pwdStrength=20&password2=" + epwd+ \
           "&redirect_url=https%3A%2F%2Fpassport.douyu.com%2Fmember%2FregNew%3Fclient_id%3D1%26lang%3Dcn&client_id=1&reg_src=web&cpsid=0&room_id=0&cate_id=0&tag_id=0&child_id=0&vid=0&fac=&sm_did=&did=&lang=cn"
    logger.debug(data)
    r = requests.post(url, data=data,headers=headers)
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    if responsed.has_key('msg'):
        logger.debug('msg:'+ responsed['msg'])
    logger.debug(responsed)
    error = str(responsed['error'])

    if error != '0':
        logger.debug('获取数据失败')
        return False

    logger.error('获取数据成功')
    return responsed['data']

"""
功能：获取浏览器的指纹信息
输入参数：无
输出参数：str，浏览器指纹信息
"""
def RegisterGetBrowserInfo():
    #browserinfo = 'TAVKL7rtrOSzXDFTszQJG(wO)QJzW)0EHAbNJRpYXKvJImuZwoiRMTvRKGz8VFtcmd2OxB3Q6fGSATEZYSKLliOVVmLu7PDqYAcWKwk4Dx9nz2WEi(GmEigUMJ7V(l0Lj22lmSBVABNkXugCj4PsiAJ8o45ahlzTeOGgvy4413xZeU2KDuXufjSxxXd5iiIEFqo9qyiVvZd(Q(gx06cjm9gdUPlAD)h8jLij8Ifv9Riv3w5XCVdn(Z6fbTjDBDITr1P8yNxoMHfC5mxlhLm0NosawNjVrh3TRnXjvQIdtYtqTmxVPhQ3SNkX3u8DR3FH7VcBno9LGzsUiBrBJTxWAqNCGqc6WDY5LTJQztSl(JGw9tWd473HNf3b(nju4i53qAQ0o4pFFPy)SS2uf7FsN1GOj)abZ7a)6852YNJ0MJ)UJqv)wjbgkAhVqqgl1xDXPmyYJasCH97C(oYS6zHLAbXvg(rfSW(Cx(ZT0A0i2nUfsi4HDfWuzN7UmEcI)a2sLQookC0dUsj)bDrnFV2AflX6)HFQGoWIZ0UyfI4)3TEdI(q5SQSLzUcdmoJKNCCuW3KzNEaiWocMF7ehMTrEzuNPejEAlguiY1zm1IZEt7tP87v8822ADN1VXb)ioBTkFc(bOMwO9DkvLBLhil07GMCKD1nUXmd6fKN1E63F)g18g(XA6ryFgS459MgqoWLRh3S1G6cWbM02OlNrWV5XReSjazejiUN1DQJxTTs6LqTV3f)rET1FepVT4TXVRLdUci42mTDcJM5qgiD()Ec17d7oqLuOEk0Hkfg7gLh9(C)7vM81xA4fcea7MqKbwPTMMlh5FE0WOA3GQS2GOMO5ZxWow)MxaIYjWW2gAMBQcaIX8C4ILPAwEX1Zg7wxoWAzxc8YNgHb8vzGG3FpiW)R4t0ioGIaG9BC33ycN)HAybY29HAvxCgvu6hKqJqSNDHIKgbfdmUu49xPf4cFIXgMKDUItZIbNuU()pIfmZRdP)vHBq1rfOVED83TPVGStHWtR8AXdGaiiiKXsvttY5Ro3KDOH7(ega8j96yPgxbxQmN0stMPvqD2pgul74PnWBWx1eaA2REuDQa(XWTv780Vz7QQioRE3pU4w(pEFTa0dSVNfWx3nhw8ce)X4r(fuUvqOJuPzZ5fHsu5zGDpFq9sIn(56Rfj1tLHsJIIHaOp67ir9114FXIP1XWpZstFW9xckE(VdRp1IMAGQ2uL59aWpP5nLX06b2A30kXmpKmNEdjw8evMBCXuGK9vVrAU301NAc(DCSvIlmq)2ifjNuCcgN7SEkeqizbVnHj3NCCyZ9EX7nsXZamPuwb8RdYZvFbPJD29SSVyFenZl321WbaUlwlEPJ0v6rMzH)M1Zx4aPRdfyQZCOJmzLKzw3cc7qSK3l56nT4LmF0zmdezFHMpzxiAa95CCLtNE4wfe9f5pI5gWnlbZvoJOVfWbX6hWfefqv1aJ6aHDLEj3)ZgFhLPNXXVIAVBLKRTk((z5gk6qCRTqIfo6WStUxsIRr2ZqUXDoiVxw7UfVQuPB(3SFkQ2kyCnk3h5ZdZJMtSh0xjvNcLET4g6qMLDPL5LnoW2Y49Sm(FYl6QRx8bRFDCW1v2Dg)GobwTcl9wo4aXavIeq4TynuuV1Tq(n4KLBmX0uXNl2fVEm41G6eoGMK2CiPLvb8eJ2Lnn5c1nfzuvCopGOyyp(vgqwLI3ome4g3MF693wj4qHtb7ZGvQ5z3T)8HW)892wBrGkR9alL7nbqFyh4NRPk9EgsGnNoI7R(c59aYXGNNWVRYEecJwbGO9f(tFDAPcXd2ray7YT7yrUQGHuR6ZQi7FcT8w2FeJ7KZs9aisYIUqNFgIacsJQiSjJ16u58P6OtTrmbM9av2)nt70Qh5Ko96tcH0WLraUL9KkWOA(tSzxNlB8(1Wv9tro2zms)98i8A)84DalWd8S6q9w(Y0g4UztAMJlFbOm9KW5S70Zem5GCyzu(NCmVj8D(JbEl8Ef49DGVOgzf8dGYkQPLuRurT32wY8p90tlfoMirgh(o30nG)zUekUfI7R6j0H4kIyEUvFYdm)KPFEED(TyZn85w6rnZnQkeTx1CtXsNmZEp0a1DDY5c5q6ojzxXQGCie9GhI9O0nblxtZnPeK3cjjnbrN5ZMx5l6AWBRWZznAN7AHRYw0(HIuZtHYUjLrPZM03pLbFSFx80Yu5Pw(JULShp5k68fkdsw(1vAaZN7uZqv9lD4am3csv8qCr6GC)PSmdUGRRpwrj2u9cY)Frja4T4rS)KyA0XeoJXCdSijpQlgnoj9G03kihkYAgp0jke)My1loGySZe7XbeL0cG8cgiCjh4Z8Dsr6tfQS8XZFQ3jc1FQEb6vywvp9bUQr8eU5leF3RLzAUQ7tnCe59Tt4Z0f51hCqPVpvZ0XHwGDFCERBdPRtWa7lLoRsoRVFR44cojikDGX1(G(5xhSC1HI33VqIxgV1FK2vFngkIhFOkqBRcu096qQYUaXA7g7GiyCd4EwSfQEyNvYNMBtQ4V3xtG0rHyMBrLcorm8oN5fG(yx(jAPe25EmVWuWnNSDRvzFm7aWsMMeb4Dj7u8DVDN3gD4g0p)kaMm6YRtm0GEkHcouF30AiBF)o8cVbbjM012yWIlVV2VcntHZcTFDJSdFhCKm0A(bz)E2zsgHLiaFXy5snT3V06TsndISvTLujckxM0BKXYTRsESNAXHEEvMBrsVeJHkQ8vRbKDLDP7oqnV)ma1Qa(8tj8dUh6OaQAq3oXfXwtjFJffDD6fu)0QrjiTh3k3QrbvydXu26Lt76f3vOGa38KwBD7ECbFmpDukQ0BOsEYD5qhNfKhFj7ygc2xYKM7kOM0gxWu58tMwu0adO8FTw)CGITB0ucvxStoFpWKdJXKWyI0ZjRCVHvwqr6Jag0p4aCcbJ2n7R62oB8PYvKjD7ltHJpS3CaexNZ9ry4)Q6riLr96mPmSrY8keG3RcJOToKZtVGamkOKnv)jOAIEDhhbuG72rem(k8jHz8BhDU)NeXky0ONEIQE(K5ju7FI7ck(mzls4FARGv1uDnyaufacquzHpe3Xjrl8in6t7LN07cNWLyxayEP4Q4QWo6hHm30j8OZysPOMkVVsdSNmsNqWWOJ)t2xLzzGSyb9XkHdrqoKoiiHfkR72z6LDgn0xhtiAsZ8CiX(senBxENxnRtNjQjv62lA4W9c21iyxb2HnjxxUNaalThgl9bjmHKVcJfnPEVhhZ3TRu16bYgOYsPeWaFmoigi58N4x9IHZBkNoBU5kmkUxyZIiMoNOUZQe9jN77NuPXP)cVC5X)bJDPP2VjGfYjHKYWtGy2SNTv3CBkb4G8OG76T0IF2oCJ27af5f(1ZZXda32(emJaTpCYlJC7u9UKCT7MmNM1yKnwIjk6gIc(LNY)U2usfBoErv8F93G0XaT24KGmc6UK5ViMUks9nu8XalJBoUwc(8zPmSEPSNZelhWomZ(qBqVvhUAU.65c62d500f6988b9095e25507dcd44ecf275ef022f12c3f0f6694c5f133f369f5e366c1898838bc407ee74d918cb9d9edbba691a75677cf2b0f9d521bd6a7330fcf69583909cc01cc4757fe16630974d5009fcfc10f82749c6696e692261d38995c57d0b915f0cfb20431fb99e7d0989212a55968cfee477fa818e5b69a7eb28'
    browserinfo = '1ddcS8t1orBzkaklajVhFUY5nl)2AVnT66wlRr2CPHZZBE5swQzERQwqVS2GIZO15ltGWEg)wnMlzSwrC8NjgdbvkVEsrCtLahilGQQyWiYGxK4JKmBYFJcyrcO2L13JaElKnxTTRv834ZRvMp(xJ7X(z7Qg8uXWewqfPHi2Kyr43lgwj(Ic7KRTQdPIMdJrv6XxlS3ZAAMu9xFq65vodK(DILkztN(9mjcVlXSI1Zi)uv0a0HHwuV)OqmvBs3j7iBSia7ROkpBF5r)pL)XIBd0Dqby2X7XDltZyyl37xm7uXzsBP)y7Jax47IIsGgWivMpdBTR6LDmZH7DLfybwrS1zSqMXEIaYNuCnDMvnufikZJoEEhi42PMim9Wl2RoQeMX0XpkqUwl0wj0cLHXcg5V7CEMU)cKhtNYquIba(UpHp6dHCGXvEVVhcwdpEzKxJeNRhZHaNUNMmPqxquZ3nur)YegWtiPrwEStuQ4BHDxEfxg0iCRahbK)TyQwU9WrPxTR)kONAmeqxM0hwhtUz2)x)60O5ZZHq6ucCmH8(SC(ENU7a1FyzGss41k6fKqPqFJJ4M0wybv6R4HhfiDoKZhpd2i1lNhwtDdAN6nQeJp8hai5KS3KPttMHiCt80EcjF5ZjVTuvrJaxSU3HMNOtGY0xAkcwB8xpzT)bAOmDaUiG3RxdOUM6iV3t(C0ZH7nuhTg70hr5zzRJcZvVb2Dm76iUA9i7HvCz89vi70e1HAaW39a7AspzwUz1x0ilSaBoJji0(tnPkrZ(vTHkYkGdcaSDbdwZI9FepXaN4XujjGWFlNj9PXpnwo(oD9bU8sC0LxZHclfZP2Dv1M7ILSlehJ2ibe8uaSzCNwxKhKL(tzXqBp30TlupMaH4j3)xy2n8O0Z7DA0vsT0yxYh9lMI9Yh6H1Efy4Vg4tlClNaw97qwrIhCOgR3a1s62RrduXiXhgyPL0jHNexyPxKJOK((1au883(34mGnYuRVc0IqhAltQhbBW(Ual4zPzgMfH5Lllr7qs1owx2aCvTnSXrNFZQHOeJFzuwgo7vzYguowNBJCKKkzVCXHgLVcYrqJKrG2tfyCxqDv8JqgYKfQpkqQDdSeAYiudtIy2SVkEV8xcL)DVafJxuI1JlCYgTyw1HWaDTBCAbmoXoCGQnlcqixZ0gNumjvZ2yfeeZD92lc6J9wHbwqTNKT(mEz)Qs9ui9jlYzj)o1xBqt2o1ZrokQqgt7eFX)B7eKy2hv86q59IZzEu1nAYf7VXcKvFWfEukBg1IZv(f12wTWzS9WWu8(7WO7jxpUSZPotShB9bskzExJhKyZPUgpudfsbL7VSXF5wNE6Z)2NLRouep7tESjaIxbOLQuaXC2yf8GJBNqVRjMNFYUmWJva861vJqiRjeuDiR(6YH6i8UsY10A1(SgxiJNi5GX7YxNAwKjWWlZeCV9riFfdI5xXgVRnu4vKa1GNEgRuqCTKDk(lX56H1oq1oFKsOj8qyJ)qnHsb1f8LYAL8BF4IdsTH5HPczAMhY77ItgqKT7moH5TTQo(eVm3mELd)ez4QZDmAVqzfCLIXVdwm5mU(sATkNHHHgEaJCsJdSfoCYs9I8fMRMIQbiSBl4HL928(FftiUJ4ATsIR6vRyKnwJUCk2)3AEeCK1AAlGhu453QzFSR6BtUsBE5XNCW)Uv0fYMA1vOSmjBFe65eBAPy)U1gEavx6hJN(CMXHzjth91jhMhsQL3)UHQlb3cf84Kt)dfmuxyjNQGAgB(e9zpThy23CggKhFwxll2kmNUbY4YbUEQgavwqxSwL14mTJctGZRkgRQ4kNeaGK2TF4lbU5CRi)OF8hwXE2GSNnC5odPzzFxuBkFdyE9XpiEaeoG2gMBgLMrfHYUevSJ1301k2le(EjgMM(Sk7O8ElBoT)cAxJK0BQMEsAumcBd)oLlMFDJOSzezH9yeTjgl3DSY0SJ0gkLaPurwN)XYpiHd(dp)gBRmtnl66EIqTgZFBX41llBy2FhDZKevAfrMMAeaXOXwcQ(It0y1P8UqB3gzmRdE6zBV(A8X6h4HNWJL1iNby3Nh68IklacEzJcMO6P2EKvBuAz(YrrxO9oh7WBHpLd928HGs6t3)lvSIDSheR8)YpG4w(w5yKbqsolzgf592NWDf6y6tBfbim5hAnpkfpvemX)ULm2kG1UyyDPNVn4eXIzeMWNve8ECAxGm4BK6akgJHSq40GwMUtJifKDLgw4x4o8QueGCSu82WcVpnRACNIlU0tP3YUlaW1zssJwxhFIx3ZlfxHUu4dzS8xfqgZqkZ37FwsH51VqlHI4w1lEwqrF)9FfWExVM(q(2GN9rU1cNc(kFGH7vjC7BNrykXUrNqGYmHyZjHp37DhH(VGwp1XxA9YGR3WmbxwxNlJyKuTpOgSeN4q4oGcC(cwqZpkhrJSEuR5AY5gTJHYlxTV)8c72DPeAY2FwDCVFGyAXtOJIe6BqGpJ1gog4TkqQpezlhfIETxhNIziB0wiWgtBY04Z2Un2SG8JNne7j)tpk6SuNUxH7hlXKDObfS4vANvfx(EHmeXJU9tLNsoCNwe39fV4)xaTkaXI4F2jKBGy6mh7g5aR862CuCla9H337)vIkJ)oCG30tTcNVGaDJDhWgpMJ6RIns64cKuSm9zfGCr0GNghugshgIdduNbyBJSPc68hu1psMLS4DCy1fjgIVbVJjEN)l0JbQDXjgbzlBDlv8H0AhnzigqM9AJgIMqt(DZUSky4yG5D01)dz2DXoDG5t9f)QEJp71y9pMuZNOtnQ7SRf0GCUhbyNUAMAp5mP5R6CkuGOJE1lKcg4ih80x)yEUoGy(3ArN4ah(0AluoR8gK5MhyW1dSG7yP5Rkeg6nbqgoYuuH)BrDub1be54kzD4TrXQZp(oMrigZSz0WcBKmhf3Dgq(YRHeqaRglxkHvjqZF415AhHCovJlbwjI6Ikgl7l2uaYk3SAcCkTdgn(Wmi9DnGp1r3VS4kfEKjzHifM73TQxx88yO0Y0ChZGtFSOoLCxbq9UwnivUt(KZMd9vdXDwA8KQnGqSJS)qgbtUcusI9Nz0RZDw2(T3WaD6703t(2XfRfRrpS6gq24ywUCv96VXkhnYxTXtVyYKyucGcj0bWP8ISK60iERzwmhD5m7aSEZuWR6kujOQGWar0Hax)TMQCMF894EaE15ejZaOcx4m8aWTcwTD(PneZA3L7jmxBk9m5rIryM51JX(tvNeumvC7eKSc7Ye)O2YP6wosnNkztpYCd4hh(dlHTLdqQpbtfI9w(bkuMROQKKXuS979OVfAY0Vrvjwfikbo30AnaIWW)hW56KotLOWsAuW(vpk6AaTa4PNGx8va0KSb(K4NeHC)JZJtcP9DEAc22XQw4GtkN(qfTo4RCAcldhi)GwMrGAc)gq0pUc5jP(F4aOyRzGRUE8M0Vit2s2VF8wp4otLeQcgmayodZRaf4dDpwVh96yaw46i2kcybJpoNuSh6igYfcfSWe0XoXCjpDh7TlWvu0feHbMjf)tEwTDi)DKoKmYA3t8OwxHnSL2jGoxk4(FepLGNYIsPxRBw(jTcYxa705db245d537a24b51c0f85a6163ec20d15aa5a5fa455ba78b7139897c8fd877c268bf968c2425c1d4a41842ce4e25f6817bf8427c628af5fac117241aaa59409e21e19df187fabfccfa68f36e8f8159a678ff7be77794f0f3e1c070b4a856c089bb9a18f3d243e5bde4a63cf353da792ebb9d19e9ece46cc2a88652ecc17ad'
    return browserinfo


def LoginCheckGeeTest():
    """
    功能：     登录时从斗鱼官方服务器获取极验需要的参数
    说明：     该功能是在谷歌浏览器中抓取的链接，为最新版本的登陆是需要的参数
    输入参数：  无
    输出参数：  False : 失败，返回False，并有日志记录
               ou    : 成功，返回数据字典，字典内容如下
                    ou.code_data_id ：     斗鱼官方的GeeTest ID，不变 (也就是gt)
                    ou.code_token：斗鱼分配给客户端的ID,每次都会变化
                    ou.code_type : 数据类型
{
	"error": 0,
	"msg": "\u64cd\u4f5c\u6210\u529f",
	"data": {
		"code_type": 1,
		"code_token": "d7c0e6f71545408b955b5838865daf86",
		"code_data": {
			"id": "9e296fca9afdfa4703b9f4bee02820af"
		}
	}
}
    """
    result = {}
    url = "https://passport.douyu.com/iframe/checkGeeTest"
    headers = {'Content-Type'   : 'application/x-www-form-urlencoded; charset=UTF-8',
               'User-Agent'     : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
               'accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'referer'        : 'https://passport.douyu.com/member/login?state=https%3A%2F%2Fwww.douyu.com%2Fmember%2Fcp'}
    data = "op_type=23&gt_version=v4&room_id=0"

    r = requests.post(url, data=data,headers=headers,verify=False)
    logger.debug(r.url)
    logger.debug(data)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    logger.debug(responsed)
    ##判断返回数据标志位
    if responsed['error'] != 0:
        logger.error('获取数据失败 error=%d', responsed['error'])
        return False
    logger.debug('msg:%s', responsed['msg'])

    ##判断返回数据中是否有gt和challenge
    rsdt = responsed['data']
    if rsdt.has_key('code_token') != True:
        logger.error('code_token 不存在')
        return False
    if rsdt.has_key('code_type') != True:
        logger.error('code_type 不存在')
        return False
    if rsdt.has_key('code_data') != True:
        logger.error('code_data 不存在')
        return False
    code_data = rsdt['code_data']
    if code_data.has_key('id') != True:
        logger.error('id 也即gt 不存在')
        return False

    result['code_data_id'] = code_data['id']
    result['code_token']   = rsdt['code_token']
    result['code_type']    = rsdt['code_type']
    logger.info(result)
    return result


def LoginSubmitV4(nickname,pwd,challenge,code_type,code_token,code_data_id):
    """
    功能：     向斗鱼提交注册账号，V4版本
    输入参数：  字典，包含注册信息
                    phone  :手机号
                    code   :验证码
                    pwd    :随机密码
                    challenge  :斗鱼分配给客户端的ID
                    code_type  :
                    code_token :
                    code_data_id: gt
    输出参数：  False : 失败，返回False，并有日志记录
               字典    : 成功，字典内容如下
    {
		"url": "\/\/www.douyu.com\/api\/passport\/login?code=1fffeb717a9cdb2a9faf101b7cec321d&uid=115859967&client_id=1&loginType=loginNew",
		"isAutoReg": 0,
		"nickname": "\u6b27\u8036\u5c71\u54e5"
	}
    """
    epwd = get_token(pwd)
    timestamp = int(round(time.time() * 1000))
    sm_did_str = "WHJMrwNw1k%2FHrfjgCrssdSrjihhsA83SkyaB%2BiVdXgfidKonmoVg6wiSkdyrn4JNegkd0emPJe0ygtfvT%2FrvxpKAqBC1SPRntk9sEAEljDkbV44F74wfyWJSD3EmPbcN1b2GXgZ5AQVJWVaNEUT2cSKxGrBEhU9qPitL%2Fx67TT69khoMiJ81hY22f%2FJX1g54%2FoCLJEWjWSHcRTkAd7H%2FeWujhzo%2FmQcA4YmYdNTeAx%2Ftf7bBVGhUxoxjSa0uqR%2FotPiQZ4ehYNmk%3D1487582755342"
    url = "https://passport.douyu.com/iframe/loginNew"
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
               'accept': 'application/json, text/javascript, */*; q=0.01',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'referer': 'https://passport.douyu.com/member/login?state=https%3A%2F%2Fwww.douyu.com%2Fmember%2Fcp'}
    data = OrderedDict()
    data['username'] = nickname
    data['password'] = epwd
    data['room_id'] = 0
    data['code_verify_data[code_type]'] = code_type
    data['code_verify_data[code_token]'] = code_token
    data['code_verify_data[code_data]'] = dict()
    data['code_verify_data[code_data][geetest_challenge]'] = challenge
    data['code_verify_data[code_data][id]'] = code_data_id
    data['code_verify_data[code_data][gt_version]'] = 'v4'
    data['redirect_url'] = 'https://passport.douyu.com/member/login?state=https://www.douyu.com/member/cp'
    data['t'] = timestamp
    data['client_id'] = 1
    data['sm_did'] = sm_did_str
    data['did'] = ''
    data['lang'] = 'cn'
    data = urllib.urlencode(data)
    logger.debug(data)
    r = requests.post(url, data=data,headers=headers,verify=False)
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('post 失败,r.status_code=%d', r.status_code)
        return False
    logger.debug('post 成功, r.status_code=%d', r.status_code)

    responsed = r.json()
    if responsed.has_key('msg'):
        logger.debug('msg:'+ responsed['msg'])
    logger.debug(responsed)
    error = str(responsed['error'])

    if error != '0':
        logger.debug('获取数据失败')
        return False

    logger.info('获取数据成功')
    return responsed['data']

def callbackParaGene():
    """
    产生一个回调的参数，格式：jQuery111304560208910648751_1554102116618
    jQuer+11130+16位数字+'_'+ 13位时间戳
    :return:
    """
    j = 9
    str1 = []
    str1 = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    j = 7
    str2 = []
    str2 = ''.join(str(i) for i in random.sample(range(0, 9), j))  # sample(seq, n) 从序列seq中选择n个随机且独立的元素；
    str3= 'jQuery11130' + str1 + str2 +'_%d' %(int(round(time.time() * 1000)))
    return str3


def LoginGetCookie(para):
    """
    功能：使用api接口获取cookie
    :param para: 字典，格式如下：
        {
		"url": "\/\/www.douyu.com\/api\/passport\/login?code=1fffeb717a9cdb2a9faf101b7cec321d&uid=115859967&client_id=1&loginType=loginNew",
		"isAutoReg": 0,
		"nickname": "\u6b27\u8036\u5c71\u54e5"
	    }
    需要做处理
    :return: cookie_str
    """
    url = 'https://www.douyu.com/api/passport/login'
    logger.info(url)
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
               'accept': '*/*',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
               'referer': 'https://passport.douyu.com/member/login?state=https%3A%2F%2Fwww.douyu.com%2Fmember%2Fcp'}
    result = urlparse.urlparse(para['url'])
    para_dict = urlparse.parse_qs(result.query)
    data_dict = OrderedDict()
    data_dict['code'] = para_dict['code'][0]
    data_dict['uid']  = para_dict['uid'][0]
    data_dict['client_id'] = para_dict['client_id'][0]
    data_dict['loginType'] = para_dict['loginType'][0]
    #data_dict['callback'] = 'jQuery111305212150702461193_%d' %(int(round(time.time() * 1000)))
    data_dict['callback'] = callbackParaGene()
    data_dict['url'] = para['url']
    data_dict['isAutoReg'] = para['isAutoReg']
    data_dict['nickname']  = para['nickname']
    data_dict['_']         = int(round(time.time() * 1000))
    logger.info(data_dict)
    r = requests.get(url, params=data_dict, headers=headers, verify=False)
    #r = requests.get(url, params=data_dict, headers=headers, verify='./dy.cer')
    logger.debug(r.url)
    ##判断http post返回值
    if r.status_code != requests.codes.ok:
        logger.error('get 失败,r.status_code=%d', r.status_code)
        return False
    logger.info('get 成功, r.status_code=%d', r.status_code)
    logger.info(r.text)
    logger.info(type(r.text))
    responsed = r.text

    if responsed.find(data_dict['callback']) <0 or responsed.find('"error":0') < 0:
        return False

    logger.info(r.cookies)
    logger.info(type(r.cookies))
    cookies = requests.utils.dict_from_cookiejar(r.cookies)
    logger.info(cookies)
    logger.info(type(cookies))
    i = 0
    cookie_str = ''
    for key, value in cookies.items():
        if i != 0:
            cookie_str = cookie_str + '; '
        cookie_str = cookie_str + key + '=' + value
        i = i + 1
    logger.info(cookie_str)
    return cookie_str

logger = gl.get_logger()
urllib3.disable_warnings()
