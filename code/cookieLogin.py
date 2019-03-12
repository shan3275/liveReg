#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import sys
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import urllib
import random
import inits
import globalvar as gl
global logger

class CookieLogin():
    def __init__(self,cookie_str):
        self.room = '1808117'
        self.home = "https://www.douyu.com"
        self.url  = "%s/%s" %(self.home, self.room)
        self.chromeOpitons = Options()
        self.prefs = {
            "profile.managed_default_content_settings.images": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        }
        self.chromeOpitons.add_experimental_option('prefs', self.prefs)
        self.browser = webdriver.Chrome(executable_path='/Applications/chromedriver', chrome_options=self.chromeOpitons)
        self.cookie = self.cookie_parse(cookie_str)

    def __del__(self):
        self.browser.close()

    def cookie_parse(self,line):
        fields = line.split(';')
        # print 'fields: ', fields
        cookie = {}
        for field in fields:
            pair = field.split('=')
            key = pair[0].strip()
            val = pair[1].strip()
            cookie[key] = val
        return cookie

    def load_cookies(self, path):
        cookies = []
        FILE = open(path, 'rb')
        for line in FILE:
            line = line.strip('\n')
            if len(line) < 10:
                continue
            cookie = self.cookie_parse(line)
            cookies.append(cookie)
        return cookies


    def send_msg(self, ustr, msg):
        telem = self.browser.find_element_by_class_name("ChatSend-txt")
        time.sleep(3)

        telem.send_keys(msg)

        time.sleep(3)
        belem = self.browser.find_element_by_class_name("ChatSend-button")
        time.sleep(3)
        belem.click()

        print " %s send MSG \"%s\" to %s" % (ustr, msg, self.url)


    def login(self):
        self.browser.get(self.home)
        self.browser.delete_all_cookies()

        for key in self.cookie:
            self.browser.add_cookie({'name': key, 'value': self.cookie[key]})

        # self.browser.refresh()

        nn = urllib.unquote(self.cookie['acf_nickname'])

        uid = self.cookie['acf_username']

        ustr = "%s(%s)" % (nn, uid)

        print " %s login to %s." % (ustr, self.url)

        self.browser.get(self.url)
        time.sleep(20)

        rval1 = random.randint(1, 100000)
        rval2 = random.randint(1, 100000)

        msg1 = "%s: %d" % (u"钉钉", rval1)

        msg2 = "%s: %d" % (u"信息", rval2)

        self.send_msg(ustr, msg1)
        time.sleep(10)
        self.send_msg(ustr, msg2)
        time.sleep(600)

        return True

logger = gl.get_logger()

