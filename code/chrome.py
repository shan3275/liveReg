#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

import sys
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import urllib

import random

path = sys.argv[1]

room = "1808117"
if len(sys.argv) > 2:
    room = sys.argv[2]

home = "https://www.douyu.com"

rurl = "%s/%s" %(home, room)

def cookie_parse(line):
    
    fields = line.split(';')

    #print 'fields: ', fields

    cookie = {}
    for field in fields:
        pair = field.split('=')
        key = pair[0].strip()
        val = pair[1].strip()
        cookie[key] = val

    return cookie
 
def load_cookies(path):
    cookies = []

    FILE = open(path, 'rb')

    for line in FILE:
        line = line.strip('\n')
        if len(line) < 10:
            continue

        cookie = cookie_parse(line)
        cookies.append(cookie)

    return cookies


def send_msg(browser, ustr, msg, url):
    telem  = browser.find_element_by_class_name("ChatSend-txt")
    time.sleep(3)
    
    telem.send_keys(msg)

    time.sleep(3)
    belem = browser.find_element_by_class_name("ChatSend-button")
    time.sleep(3)
    belem.click()


    print " %s send MSG \"%s\" to %s" %(ustr, msg, url)


def login(chromeOpitons, home, url, cookie):
    #browser = webdriver.Chrome(executable_path = '/STR/source/zb/drv/chromedriver', chrome_options=chromeOpitons)
    browser = webdriver.Chrome(executable_path = '/Volumes/USB/work/out/Default/chromedriver', chrome_options=chromeOpitons)
    browser.get(home)


    browser.delete_all_cookies()

    for key in cookie:
        #print "driver.add_cookie({'name':%s, 'value':%s})" %(key, cookie[key])
     
        browser.add_cookie({'name':key, 'value':cookie[key]})

    #browser.refresh()


    nn = urllib.unquote(cookie['acf_nickname'])

    uid = cookie['acf_username']

    ustr = "%s(%s)"  %(nn, uid)

    print " %s login to %s." %(ustr, url)
  
    browser.get(url)
    time.sleep(20)


    rval1 = random.randint(1, 100000)
    rval2 = random.randint(1, 100000)

    msg1 = "%s: %d" %(u"弹幕1", rval1)

    msg2 = "%s: %d" %(u"弹幕2", rval2)


    send_msg(browser, ustr, msg1, url)
    time.sleep(10)
    send_msg(browser, ustr, msg2, url)


chromeOpitons = Options()
     
prefs = {
    "profile.managed_default_content_settings.images":1,
    "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
    "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,
}
 
 
chromeOpitons.add_experimental_option('prefs', prefs)


#chromeOpitons.add_argument('--headless')
#chromeOpitons.add_argument('--disable-gpu')

cookies = load_cookies(path) 

CNT  = 0
for cookie in cookies:
    t = threading.Thread(target=login,args=(chromeOpitons, home, rurl, cookie,))
    t.start()

    time.sleep(3)

    CNT += 1

while 1:
    time.sleep(5)    
  
