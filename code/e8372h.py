#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : e8372h.py
# Author   : Shan
# DateTime : 2019/1/07
# SoftWare : Vim

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import platform
import time
import globalvar as gl
global logger


class E8372H155():
    def __init__(self):
        self.url = 'http://192.168.8.1/html/home.html'
        self.reboot_url = 'http://192.168.8.1/html/reboot.html'
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        if platform.system() == 'Darwin':
            self.browser = webdriver.Chrome('/Applications/chromedriver')
            #self.browser = webdriver.Chrome('/Applications/chromedriver', chrome_options=chrome_options)
        else:
            self.browser = webdriver.Chrome(executable_path=r'.\chromedriver.exe', chrome_options=chrome_options)

        self.wait = WebDriverWait(self.browser, 60)
        self.browser.get(self.url)
        #self.browser.find_element(By.XPATH, "//span[@id='logout_span']").click()
        button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@id='logout_span']")))
        button.click()
        logger.debug("已经登陆4G Modeml")
        time.sleep(2)
        now = self.browser.current_window_handle
        self.switch_window(self.browser, now)
        self.browser.find_element(By.XPATH, "//input[@type='text' and @id='username']").send_keys("admin")
        self.browser.find_element(By.XPATH, "//input[@type='password' and @id='password']").send_keys("Kstr1q2w3e")
        self.browser.find_element(By.XPATH, "//input[@id='pop_login' and @value='登录']").click();
        time.sleep(2)

    def __del__(self):
        self.browser.close()

    def switch_window(self,driver, now):
        all_handles = driver.window_handles                #得到当前开启的所有窗口的句柄
        for handle in all_handles:
            if handle != now:                              #获取到与当前窗口不一样的窗口
                driver.switch_to_window(handle)            #切换

    def modem_reboot(self):
        logger.debug("准备重启4G Modeml")
        self.browser.get(self.reboot_url)
        #self.browser.find_element(By.XPATH,"//input[@id='reboot_apply_button' and @value='重启']").click();
        button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='reboot_apply_button' and @value='重启']")))
        button.click()
        now = self.browser.current_window_handle
        self.switch_window(self.browser, now)
        #self.browser.find_element(By.XPATH,"//input[@id='pop_confirm' and @value='确定']").click();
        button = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='pop_confirm' and @value='确定']")))
        button.click()
        time.sleep(40)
        logger.debug("重启4G Model完成")


logger = gl.get_logger()
#crack = E8372H155()
#crack.modem_reboot()


