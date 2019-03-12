#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : douyuLogin.py
# Author   : Shan
# DateTime : 2018/11/28
# SoftWare : PyCharm

import sys
import time
import random
import platform
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import globalvar as gl
global logger

"""
功能：使用网页进行账号注册
"""
class DouyuLogin():
    def __init__(self,nickname,pwd):
        self.url = 'https://passport.douyu.com/member/login?state=https%3A%2F%2Fwww.douyu.com%2Fmember%2Fcp'
        if platform.system() == 'Darwin':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.browser = webdriver.Chrome('/Applications/chromedriver',chrome_options=chrome_options)
            #self.browser = webdriver.Chrome("/STR/chromedriver/chromedriver")
            self.browser.set_window_size(1200, 733)
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--log-level=3')
            self.browser = webdriver.Chrome(executable_path=r'.\chromedriver.exe',chrome_options=chrome_options)
            self.browser.set_window_size(1280, 733)
        self.wait = WebDriverWait(self.browser, 60)
        self.nickname = nickname
        self.pwd   = pwd
        self.phone = ''
        self.pngname = 'captcha1.png'
        self.pnglenMax = 1300
        self.pnglen    = 0

    def __del__(self):
        self.browser.close()

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        logger.debug('已经打开页面:%s', self.url)
        login = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='scanicon-toLogin js-qrcode-switch']")))
        #login = self.browser.find_element_by_xpath("//div[@class='scanicon-toLogin js-qrcode-switch']")
        login.click()

        nicklogin = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-i18n='Login.Subtype.nickname' and @data-subtype='login-by-nickname']")))
        nicklogin.click()

    def inputphone(self):
        phone = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='phoneNum' and @placeholder='请输入手机号码']")))
        phone.send_keys(self.phone)
        logger.debug('已输入手机号码')

    def inputpwd(self):
        pwd = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password' and @placeholder='输入密码']")))
        pwd.send_keys(self.pwd)
        logger.debug('已输入密码')

    def inputnickname(self):
        nickname = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username' and @placeholder='输入昵称']")))
        if platform.system() == 'Darwin':
            nickname.send_keys(self.nickname.decode())
        else:
            #nickname.send_keys(self.nickname.decode('gbk'))
            nickname.send_keys(self.nickname.decode())
        logger.debug('已输入昵称')

    def get_submit(self):
        """
        获取初始验证按钮
        :return:
        """
        #button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@data-i18n='Login' and @value='登录' and @type='submit']")))
        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@class='loginbox-sbt btn-sub' and @value='登录' and @type='submit']")))
        return button

    def hasgeetest(self):
        """
        检查是否蹦出验证的框
        :return: True  False
        """
        logger.debug('等待2秒查询是否已经加载验证码')
        time.sleep(2)
        try:
            hadsend = self.browser.find_element(By.CLASS_NAME, "geetest_window")
            logger.debug('元素已找到，已经加载了验证码')
            return True
        except:
            logger.debug('元素未找到，没有加载验证码')
            return False

    def switch_window(self,driver, now):
        all_handles = driver.window_handles  # 得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:  # 获取到与当前窗口不一样的窗口
                driver.switch_to_window(handle)  # 切换

    def checklogin(self):
        """
        检查在验证码通过之后，登陆是否成功，
        :return:
        """
        logger.debug('等待5秒，查询是否登陆成功')
        time.sleep(5)
        self.switch_window(self.browser, self.browser.current_window_handle)
        try:
            hadsend = self.browser.find_element(By.XPATH, "//span[@class='user_top js_nickname']")
            logger.debug('元素已找到，登陆成功')
            return True
        except:
            logger.debug('元素未找到，登陆未成功')
            return False

    def get_cookie(self):
        """
        获取cooke
        :return: cookie
        """
        cookies = self.browser.get_cookies()
        logger.info(cookies)
        i=0
        cookie_str = ''
        for cookie in cookies:
            if cookie.has_key('name') == True and cookie.has_key('value') == True:
                if i != 0:
                    cookie_str = cookie_str + '; '
                cookie_str = cookie_str + cookie['name']+'='+cookie['value']
            i = i + 1
        logger.info(cookie_str)
        return cookie_str

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
        top1, bottom1, left1, right1 = self.get_position_by_name('geetest_head')
        top2, bottom2, left2, right2 = self.get_position_by_name('geetest_table_box')
        top,bottom,left,right = top1,bottom2,left1,right2
        logger.info("top:%d,bottom:%d,left:%d,right:%d", top, bottom, left, right)
        return (top,bottom,left,right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        #screenshot = self.browser.get_screenshot_as_png('screen.png')
        #screenshot = Image.open(BytesIO(screenshot))

        self.browser.save_screenshot('screenshot.png')
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

    def login(self):
        """
        登陆斗鱼，需要手动点击验证码
        :return: True False
        """
        #打开页面
        self.open()

        #输入用户名和密码
        self.inputnickname()
        self.inputpwd()
        time.sleep(3)
        submit = self.get_submit()
        submit.click()
        rv = self.hasgeetest()
        if rv == True:
            logger.debug('已经加载了验证码，需要手动验证')
            for i in range(1, 5, 1):
                rv = self.checklogin()
                if rv == True:
                    logger.info('登陆成功')
                    return True
                else:
                    logger.debug('登陆失败')
        logger.debug('未加载验证码')
        rv = self.checklogin()
        if rv == True:
            logger.info('登陆成功')
            return True
        else:
            logger.debug('登陆失败')
        return False

    def get_png(self):
        """
        打开页面，输入用户名和密码，获取验证码，保存验证码为图片，并返回图片名。
        :return: True False
        """
        #打开页面
        self.open()

        #输入用户名和密码
        self.inputnickname()
        self.inputpwd()
        time.sleep(3)
        submit = self.get_submit()
        submit.click()
        rv = self.hasgeetest()
        if rv == True:
            logger.debug('已经加载了验证码，保存验证码')
            # 获取验证码图片,并保存
            image1 = self.get_geetest_image(self.pngname)
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
        根据坐标点击文字，
        :param location:（x,y|x,y|x,y）多个文字，2或者3或者4或者5
        :return:
        """
        #翻译坐标，将字符串转成字典
        location = self.translate_location(location_str)

        #定位鼠标
        top, bottom, left, right = self.get_position_by_name('geetest_panel_next')
        x = int((right - left  ) / 2)
        y = int((bottom  - top ) / 2)
        logger.info("偏移位置：x:%f,y:%f", x, y)

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
        logger.info(location_new)

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

        rv = self.checklogin()
        if rv == True:
            logger.info('登陆成功')
            return True
        else:
            logger.debug('登陆失败')
        return  False

    def get_nickname(self):
        """
        获取登陆之后的用户名
        :return: 用户名
        """
        nickname = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='user_top js_nickname']")))
        username =  nickname.text
        logger.debug("username: " + username)
        logger.debug(type(username))
        return username

    def get_umes(self):
        """
        获取站内信数量，一封OK，两封异常
        :return: True  正常
                 False 异常
        """
        #有可能出现没有站内信的情况
        logger.debug('延迟10秒钟，等待获取信息')
        time.sleep(10)
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
    logger = gl.get_logger()
    crack = DouyuLogin('18711836842','D5fYJz70')
    rv = crack.login()
    if rv == False:
        logger.error('登陆失败')
        sys.exit()
    nickname = crack.get_nickname()
    time.sleep(60)
"""
