#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : aritel.py
# Author   : Shan
# DateTime : 2018/11/08 
# SoftWare : Vim

from selenium import webdriver
from selenium.webdriver.common.by import By
import platform
import time
import globalvar as gl
global logger

url = 'http://192.168.8.1/html/reboot.html'

def login():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    if platform.system() == 'Darwin':
        driver = webdriver.Chrome('/Applications/chromedriver', chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe', chrome_options=chrome_options)
    driver.get(url)
    time.sleep(2)
    logger.debug("已经登陆4G Modeml")
    return driver

def switch_window(driver, now):
    all_handles = driver.window_handles                #得到当前开启的所有窗口的句柄
    for handle in all_handles:
        if handle != now:                              #获取到与当前窗口不一样的窗口
            driver.switch_to_window(handle)            #切换

def modem_reboot(driver):
    logger.debug("准备重启4G Modeml")
    driver.find_element(By.XPATH,"//input[@id='undefined' and @value='重启']").click();
    now = driver.current_window_handle
    switch_window(driver, now)
    #driver.find_element_by_css_selector("[class='pop_window_action bg_color_main']").click()
    driver.find_element(By.XPATH,"//input[@id='pop_confirm' and @value='确定']").click();
    time.sleep(40)
    logger.debug("重启4G Model完成")
    driver.quit()

def AirtelReboot():
    driver = login()
    modem_reboot(driver)


logger = gl.get_logger()
"""
if __name__ == "__main__":
    driver = login()
    modem_reboot(driver)
"""

