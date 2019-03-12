#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : douyuRegisterTest3.py
# Author   : Shan
# DateTime : 2018/11/28
# SoftWare : PyCharm

import time,random,json
from io import BytesIO
import platform,sys,os
from PIL import Image
from PIL import ImageGrab
import urllib
import pyautogui
import pyperclip
import subprocess
import inits     as inits
import globalvar as gl
global logger
global CONF

"""
功能：使用网页进行账号注册
"""
class DouyuRegister():
    def __init__(self):
        self.url = 'https://passport.douyu.com/member/regNew?client_id=1&lang=cn&state=https%3A%2F%2Fwww.douyu.com%2Fmember%2Fcp'
        self.success_url = 'https://www.douyu.com/member/cp'
        self.location = dict()
        self.size = pyautogui.size()
        #macos 13.3
        if self.size == (1280,800):
            # macos 13.3
            self.location = CONF['LCD1280x800']
        elif self.size == (1920, 1080):
            #windows
            self.location = CONF['LCD1920x1080']
        elif self.size == (1440, 900):
            # macos 15
            self.location = CONF['LCD1440x900']
        logger.info(self.location)
        if platform.system() == 'Darwin':
            subprocess.call(
                ["/usr/bin/open", "-W", "-n", "-a", "/Applications/Google Chrome.app", "--args", "--incognito"]
            )
        else:
            subprocess.Popen(['C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', '-incognito'], shell=True)
        self.phone = ''
        self.pwd   = ''
        self.code  = ''
        self.timestr = time.strftime('%Y%m%d%H%M%S')
        if platform.system() == 'Darwin':
            self.screenshot    = 'png/' + self.timestr + 'screenshot.png'
            self.pngname       = 'png/' + self.timestr + '.png'
            self.pngnameAfter  = 'png/' + self.timestr + 'drag.png'
        else:
            self.screenshot    = 'png\\' + self.timestr + 'screenshot.png'
            self.pngname       = 'png\\' + self.timestr + '.png'
            self.pngnameAfter  = 'png\\' + self.timestr + 'drag.png'
        self.pnglenMax = 2000
        self.pnglen    = 0
        if platform.system() == 'Darwin':
            self.pngsize   = 75*1024
        else:
            self.pngsize   = 30*1024
        self.cookie   = ''
        self.open()

    def __del__(self):
        time.sleep(5)
        if platform.system() != 'Darwin':
            pyautogui.moveTo(self.location['close']['x'],self.location['close']['y'],self.location['close']['t'])
            pyautogui.click()
        else:
            pyautogui.moveTo(self.location['close']['x'],self.location['close']['y'],self.location['close']['t'])
            pyautogui.click()

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        #点击  短信验证  按钮
        pyautogui.moveTo(self.location['codeValidate']['x'],\
                         self.location['codeValidate']['y'],\
                         self.location['codeValidate']['t'])
        pyautogui.click()

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        #鼠标移动到浏览器的地址栏
        pyautogui.moveTo(self.location['url']['x'],\
                         self.location['url']['y'],\
                         self.location['url']['t'],\
                         pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        #输入网址
        #pyautogui.typewrite(self.url)
        pyperclip.copy(self.url)
        if platform.system() == 'Darwin':
            pyautogui.hotkey("command", "v")
        else:
            pyautogui.hotkey("ctrl", "v")
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        logger.debug('已经打开页面:%s', self.url)
        time.sleep(5)

    def input_nickname_pwd(self,phone,pwd):
        self.phone = phone
        self.pwd   = pwd

    def fill_nickname_pwd(self):
        #输入手机号码
        pyautogui.moveTo(self.location['nickname']['x'],self.location['nickname']['y'],self.location['nickname']['t'])
        pyautogui.click()
        pyperclip.copy(self.phone)
        if platform.system() == 'Darwin':
            pyautogui.hotkey("command", "v")
        else:
            pyautogui.hotkey("ctrl", "v")
        logger.debug('已输入phone number')

        #输入密码
        pyautogui.moveTo(self.location['pwd']['x'],self.location['pwd']['y'],self.location['pwd']['t'])
        pyautogui.click()
        pyperclip.copy(self.pwd)
        if platform.system() == 'Darwin':
            pyautogui.hotkey("command", "v")
        else:
            pyautogui.hotkey("ctrl", "v")
        logger.debug('已输入密码')

    def goonreg(self):
        """
        继续注册
        :return: None
        """
        # 手机号码也许已经注册了，解绑一下
        logger.debug('等待2秒查询是否出现 继续注册 按钮')
        time.sleep(2)
        pyautogui.moveTo(self.location['goonReg']['x'],self.location['goonReg']['y'],self.location['goonReg']['t'])
        pyautogui.click()

    def hasgeetest(self):
        """
        检查是否蹦出验证的框
        :return: True  False
        """
        logger.debug('等待2秒查询是否已经加载验证码')
        time.sleep(2)
        self.get_geetest_image(self.pngname)
        size = os.path.getsize(self.pngname)
        logger.info('%s size: %dKB', self.pngname,size/1024)
        if size > self.pngsize:
            logger.info('png size > %dKB', self.pngsize/1024)
            return True
        logger.info('png size < %dKB', self.pngsize/1024)
        return False

    def get_position(self):
        top, bottom, left, right = self.location['geetestLeftUp']['y'], \
                                   self.location['geetestRightDn']['y'],\
                                   self.location['geetestLeftUp']['x'], \
                                   self.location['geetestRightDn']['x']
        logger.info("top:%d,bottom:%d,left:%d,right:%d", top, bottom, left, right)
        return (top,bottom,left,right)

    def get_screenshot(self):
        """
        获取屏幕
        :return: 截图对象
        """
        im = ImageGrab.grab()
        im.save(self.screenshot,'png')
        screenshot = Image.open(self.screenshot)
        return screenshot

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        logger.info("top:%d,bottom:%d,left:%d,right:%d", top, bottom, left, right)
        screenshot = self.get_screenshot()
        imgSize = screenshot.size
        logger.info('图片分辨率' + str(imgSize))
        self.pnglen = max(imgSize)
        # 针对mac显示器
        if self.pnglen > self.pnglenMax:
            captcha = screenshot.crop((int(left*2), int(top*2), int(right*2), int(bottom*2)))
        else:
            captcha = screenshot.crop((int(left), int(top), int(right), int(bottom)))
        captcha.save(name)
        return captcha

    def get_png(self):
        # 输入用户名密码
        self.fill_nickname_pwd()
        # 点击验证按钮
        time.sleep(2)
        self.get_geetest_button()
        logger.debug('已经点击短信验证')
        logger.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #查询是否出现验证码
        rv = self.hasgeetest()
        if rv == True:
            logger.debug('已经加载了验证码，保存验证码')
            # 获取验证码图片,并保存
            return self.pngname
        return False

    def translate_location(self, location_str):
        """
        翻译坐标为字典形式
        :param location_str:字符串坐标，形似： 146,242|110,172
        :return: [{x:val,y:val},{{x:val,y:val}]
        """
        logger.debug(location_str)
        arrays = location_str.split('|')
        location = list()
        for array in arrays:
            xy = array.split(',')
            #针对mac显示器
            if self.pnglen > self.pnglenMax:
                x  = int(xy[0])/2
                y  = int(xy[1])/2
            else: #针对非mac显示器，显示器分辨率是1920 x 1080
                x  = int(xy[0])
                y  = int(xy[1])
            t  = dict(x=x, y=y)
            location.append(t)
        logger.debug(location)
        return location

    def drag_slider(self, location_str):
        """
        拖动滑块
        :param location:（x,y）滑块的坐标
        :return:
        """
        #翻译坐标，将字符串转成字典
        location = self.translate_location(location_str)
        logger.info(location)
        x = location[0]['x']
        y = location[0]['y']
        logger.info('x: %d  y: %d', x,y)
        pyautogui.moveTo(self.location['dragSlider']['x'], self.location['dragSlider']['y'], self.location['dragSlider']['t'])
        pyautogui.mouseDown()
        pyautogui.move(x-12,0,2,pyautogui.easeOutQuad)
        self.get_geetest_image(self.pngnameAfter)
        pyautogui.mouseUp()
        time.sleep(13)

        return True

    def setcode(self,code):
        self.code = code
        logger.debug('收到验证码为：'+code)

    def inputcode(self):
        pyautogui.moveTo(self.location['inputCode']['x'],self.location['inputCode']['y'],self.location['inputCode']['t'])
        pyautogui.click()
        pyautogui.typewrite(self.code)
        logger.debug('已输入验证码')

    def checklogin(self):
        """
        检查在验证码通过之后，登陆是否成功，
        :return:
        """
        logger.debug('等待3秒，查询注册登陆成功')
        time.sleep(10)

        #鼠标移动到浏览器的地址栏
        pyautogui.moveTo(self.location['url']['x'], self.location['url']['y'], self.location['url']['t'], pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        if platform.system() == 'Darwin':
            pyautogui.hotkey("command", "c")
        else:
            pyautogui.hotkey("ctrl", "c")
        url = pyperclip.paste()
        logger.info('user info url:%s', url)
        if url == self.success_url:
            logger.debug('元素已找到，登陆成功')
            return True
        else:
            logger.debug('元素未找到，登陆未成功')
            return False

    def get_nickname(self):
        """
        获取登陆之后的用户名
        :return: 用户名

        time.sleep(5)
        pyautogui.mouseDown(self.location['copyNicknameBegin']['x'], \
                            self.location['copyNicknameBegin']['y'], \
                            self.location['copyNicknameBegin']['t'])
        pyautogui.mouseUp(self.location['copyNicknameEnd']['x'], \
                            self.location['copyNicknameEnd']['y'], \
                            self.location['copyNicknameEnd']['t'])
        time.sleep(1)
        if platform.system() == 'Darwin':
            pyautogui.hotkey("command", "c")
        else:
            pyautogui.hotkey("ctrl", "c")
        nickname = pyperclip.paste()
        if platform.system() == 'Darwin':
            nickname = nickname.replace("\n", "")
        else:
            nickname = nickname.replace("\n", "")
            nickname = nickname.strip()
        logger.info('nickname:%s', nickname)
        logger.info('nickname len:%d', len(nickname))
        return nickname
         """
        if self.cookie == '':
            self.cookie = self._get_cookie()
        aa = self.cookie.split('acf_nickname=')
        bb = aa[1].split(';', 1)
        cc = bb[0].encode('utf8')
        nickname = urllib.unquote(cc)
        logger.debug("username: " + nickname)
        logger.debug(type(nickname))
        return nickname

    def _get_cookie(self):
        """
        获取cooke
        :return: cookie
        """
        time.sleep(2)
        pyautogui.moveTo(self.location['editCookie']['x'], \
                         self.location['editCookie']['y'],  \
                         self.location['editCookie']['t'],  \
                         pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(6)
        pyautogui.moveTo(self.location['copyCookie']['x'], \
                        self.location['copyCookie']['y'], \
                        self.location['copyCookie']['t'], \
                         pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(2)
        data = pyperclip.paste()
        cookies = json.loads(data)
        cookie_str = ''
        i = 0
        for cookie in cookies:
            if cookie.has_key('name') == True and cookie.has_key('value') == True:
                if i != 0:
                    cookie_str = cookie_str + '; '
                cookie_str = cookie_str + cookie['name'] + '=' + cookie['value']
            i = i + 1
        return cookie_str

    def get_cookie(self):
        """
        返回cookie
        :return:
        """
        if self.cookie == '':
            self.cookie = self._get_cookie()
        return self.cookie

    def register(self):
        #输入验证码
        self.inputcode()

        #点击  立即注册
        time.sleep(1)
        pyautogui.moveTo(self.location['register']['x'], \
                         self.location['register']['y'], \
                         self.location['register']['t'])
        pyautogui.click()

        #页面跳转到登陆页面
        rv = self.checklogin()
        if rv == True:
            logger.info('注册成功')
            return True
        else:
            logger.debug('注册失败')
        return False

logger = gl.get_logger()
CONF   = gl.get_conf()

"""
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    logger = gl.get_logger()
    CONF   = gl.get_conf()
    phone = raw_input('Enter phone-->')
    print('phone:%s',phone)
    crack = DouyuRegister(phone, phone)
    rv= crack.get_png()
    if rv != False:
        logger.info('获取验证码成功，准备识别')
        time.sleep(20)
    crack.goonreg()
    code = raw_input('Enter code-->')
    print("code: %s", code)
    time.sleep(10)
    crack.setcode(code)
    crack.register()
    nickname = crack.get_nickname()
    cookie   = crack.get_cookie()
    print('nickname:%s ,pwd:aDdeS3aBC, cookie:%s',nickname, cookie)
"""




