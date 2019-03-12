#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : douyuRegister.py
# Author   : Shan
# DateTime : 2018/11/28
# SoftWare : PyCharm

import time,random
from io import BytesIO
import platform,sys,os
from PIL import Image
from PIL import ImageGrab
import urllib
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import subprocess
import inits     as inits
import globalvar as gl
global logger

"""
功能：使用网页进行账号注册
"""
class DouyuRegister():
    def __init__(self,phone,pwd):
        self.url = 'https://www.douyu.com'
        self.success_url = 'https://www.douyu.com/member/cp'
        if platform.system() == 'Darwin':
            subprocess.call(
                ["/usr/bin/open", "-W", "-n", "-a", "/Applications/Google Chrome.app", "--args", "--incognito"]
            )
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--log-level=3')
            self.browser = webdriver.Chrome(executable_path=r'.\chromedriver.exe',chrome_options=chrome_options)
            self.browser.set_window_size(1280, 733)
        self.phone = phone
        self.pwd   = pwd
        self.code  = ''
        self.pngname = 'captcha1.png'
        self.pnglenMax = 1300
        self.pnglen    = 0
        self.pngsize   = 75*1024
        self.cookie   = ''

    def __del__(self):
        if platform.system() != 'Darwin':
            self.browser.close()
        else:
            time.sleep(5)
            pyautogui.moveTo(20,45,2)
            pyautogui.click()

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        #点击短信验证按钮
        pyautogui.moveTo(710, 400, 1)
        pyautogui.click()

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        #鼠标移动到浏览器的地址栏
        pyautogui.moveTo(180,81,1,pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        #输入网址
        pyautogui.typewrite(self.url, 0.25)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)

        logger.debug('已经打开页面:%s', self.url)
        time.sleep(3)

        pyautogui.moveTo(1084, 133, 1)
        time.sleep(1)
        pyautogui.moveTo(1035, 330, 1)
        pyautogui.click()

        pyautogui.moveTo(594, 290, 1)
        pyautogui.click()
        pyperclip.copy(self.phone)
        pyautogui.hotkey("command", "v")
        logger.debug('已输入phone number')

        pyautogui.moveTo(520, 349, 1)
        pyautogui.click()
        pyperclip.copy(self.pwd)
        pyautogui.hotkey("command", "v")
        logger.debug('已输入密码')

    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        time.sleep(10)
        print('登录成功')

    def switch_window(self,driver, now):
        all_handles = driver.window_handles  # 得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:  # 获取到与当前窗口不一样的窗口
                driver.switch_to_window(handle)  # 切换

    def goonreg(self):
        """
        继续注册
        :return: None
        """
        # 手机号码也许已经注册了，解绑一下
        logger.debug('等待2秒查询是否出现 继续注册 按钮')
        time.sleep(2)
        pyautogui.moveTo(560, 455,1)
        pyautogui.click()


    def hadsend(self):
        logger.debug('等待2秒查询是否已经发送短信')
        time.sleep(2)
        try:
            hadsend = self.browser.find_element_by_xpath("//input[@class='phone-send js-sendvoice fl long']")
            logger.debug('元素已找到，已发送短信')
            return True
        except:
            logger.debug('元素未找到，没有发送短信')
            return False

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
            logger.info('png size > 75KB')
            return True
        logger.info('png size < 75KB')
        return False

    def get_position_by_name(self, classname):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        #time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        logger.info("top:%d,bottom:%d,left:%d,right:%d", top,bottom,left,right)
        return (top, bottom, left, right)

    def get_position(self):
        top, bottom, left, right = 306, 572, 503, 763
        logger.info("top:%d,bottom:%d,left:%d,right:%d", top, bottom, left, right)
        return (top,bottom,left,right)

    def get_screenshot(self):
        """
        获取屏幕
        :return: 截图对象
        """
        im = ImageGrab.grab()
        im.save('screenshot.png','png')
        screenshot = Image.open('screenshot.png')
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

    def EnsureSendCode(self):
        """
        检查验证码验证是否完成
        :return:
        """
        # 如果出现继续注册
        rv = self.goonreg()
        if rv == True:
            logger.info('点击继续注册成功')
            return True

        rv = self.hadsend()
        if rv == True:
            logger.info('短信已经发送，准备接收短信')
            return True
        logger.info('短信未发送，需要继续')
        logger.error('检查短信未发送')
        return False

    def sendcode(self):
        # 打开连接
        self.open()
        # 点击验证按钮
        time.sleep(2)
        self.get_geetest_button()

        logger.debug('已经点击短信验证')
        #查询是否出现验证码
        rv = self.hasgeetest()
        if rv == True:
            logger.debug('已经加载了验证码，需要手动验证')
            #检测
            for i in range(1, 10, 1):
                logger.debug('循环次数：%d',i)
                rv = self.EnsureSendCode()
                if rv == True:
                    logger.info('验证码 验证通过')
                    break
                else:
                    logger.debug('验证失败')
        logger.debug('未加载验证码')
        #检测
        rv = self.EnsureSendCode()
        if rv == True:
            logger.info('验证通过')
            rv = self.hadsend()
            if rv == True:
                logger.info('短信已经发送，准备接收短信')
            return True
        return False

    def get_png(self):
        # 输入用户名密码
        self.open()
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

    def click_word(self, location_str):
        """
        根据坐标点击文字，然后发送验证码
        :param location:（x,y|x,y|x,y）多个文字，2或者3或者4或者5
        :return:
        """
        #翻译坐标，将字符串转成字典
        location = self.translate_location(location_str)

        #定位鼠标
        top, bottom, left, right = self.get_position_by_name('geetest_panel_next')
        x = int((right - left  ) / 2)
        y = int((bottom  - top ) / 2)
        logger.info("偏移位置：x:%d,y:%d", x, y)

        #产生新的坐标
        location_new = list()
        for index in range(len(location)):
            for i in range(5):
                x1 = random.randint(1,x*2)
                y1 = random.randint(1,y*2)
                t1 = dict(x=x1,y=y1,click=False)
                location_new.append(t1)
            x1 = location[index]['x']
            y1 = location[index]['y']
            t1 = dict(x=x1,y=y1,click=True)
            location_new.append(t1)

        for i in range(10):
            x1 = random.randint(1, x * 2)
            y1 = random.randint(1, y * 2)
            t1 = dict(x=x1, y=y1, click=False)
            location_new.append(t1)
        logger.info(location_new)

        for index in range(len(location_new)):
            x1 = location_new[index]['x']
            y1 = location_new[index]['y']
            location_new[index]['x'] = x1 - x
            location_new[index]['y'] = y1 - y
            x = x1
            y = y1
        logger.info(location_new)
        menu = self.browser.find_element(By.CLASS_NAME, 'geetest_panel_next')
        ActionChains(self.browser).move_to_element(menu).perform()

        for array in location_new:
            x1 = array['x']
            y1 = array['y']
            logger.info("相对于上一次的偏移位置：x:%d,y:%d", x1, y1)
            ActionChains(self.browser).move_by_offset(xoffset=x1, yoffset=y1).perform()
            if array['click'] == True:
                logger.info('点击')
                ActionChains(self.browser).click().perform()
            b = 0.1
            logger.info('点击延时：%f秒', b)
            time.sleep(b)

        #点击确定
        #button = self.browser.find_element(By.CLASS_NAME, 'geetest_commit_tip')
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit_tip')))
        button.click()

        logger.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # 检测
        for i in range(1, 10, 1):
            logger.debug('循环次数：%d', i)
            rv = self.EnsureSendCode()
            if rv == True:
                logger.info('验证码 验证通过')
                break
            else:
                logger.debug('验证失败')

        #检测
        rv = self.EnsureSendCode()
        if rv == True:
            logger.info('验证通过')
            rv = self.hadsend()
            if rv == True:
                logger.info('短信已经发送，准备接收短信')
            return True
        return False

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
        x1 = 535
        y1 = 494
        pyautogui.moveTo(x1, y1, 1)
        pyautogui.mouseDown()
        pyautogui.move(x-12,0,2,pyautogui.easeOutQuad)
        pyautogui.mouseUp()
        #pyautogui.drag(x-12, 0, 2,pyautogui.easeOutQuad)
        time.sleep(15)

        return True

    def setcode(self,code):
        self.code = code
        logger.debug('收到验证码为：'+code)

    def inputcode(self):
        pyautogui.moveTo(500,405,1)
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
        #点击用户图标，打开用户页面
        pyautogui.moveTo(1084, 133, 1)
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)

        #鼠标移动到浏览器的地址栏
        pyautogui.moveTo(265, 82, 1, pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        pyautogui.hotkey("command", "c")
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
        """
        time.sleep(5)
        pyautogui.mouseDown(479, 340, 1)
        pyautogui.mouseUp(568, 339, 1)
        time.sleep(1)
        pyautogui.hotkey("command", "c")
        nickname = pyperclip.paste()
        return nickname

    def _get_cookie(self):
        """
        获取cooke
        :return: cookie
        """
        cookie_str = 'None'
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

        #点击立即注册
        time.sleep(1)
        pyautogui.moveTo(610,477,0.6)
        pyautogui.click()

        #页面跳转到登陆页面
        rv = self.checklogin()
        if rv == True:
            logger.info('注册成功')
            return True
        else:
            logger.debug('注册失败')
        return False

    def get_umes(self):
        """
        获取站内信数量，一封OK，两封异常
        :return: True  正常
                 False 异常
        """
        self.url = 'https://www.douyu.com/member/cp'
        self.browser.get(self.url)
        logger.debug('已经打开页面:%s', self.url)
        #有可能出现没有站内信的情况
        logger.debug('延迟60秒钟，等待获取信息')
        time.sleep(60)
        letters = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "letter_num")))
        letters_num =  letters.text
        logger.debug("letters number: " + letters_num)
        logger.debug(type(letters_num))
        if letters_num == '1':
            return True
        else:
            return False

logger = gl.get_logger()

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
    crack.setcode(code)
    crack.register()
    nickname = crack.get_nickname()
    cookie   = crack.get_cookie()
    print('nickname:%s ,pwd:aDdeS3aBC, cookie:%s',nickname, cookie)
"""




