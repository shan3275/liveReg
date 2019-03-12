#!/usr/bin/python
#-*- coding: UTF-8 -*-
# FileName : tmp_test.py
# Author   : Shan
# DateTime : 2019/3/6
# SoftWare : PyCharm

import pyautogui
import pyperclip
import time


success_url = 'https://www.douyu.com/member/cp'
time.sleep(10)
# 鼠标移动到浏览器的地址栏
pyautogui.moveTo(265, 82, 1, pyautogui.easeInOutQuad)
pyautogui.click()
time.sleep(1)
pyautogui.hotkey("command", "c")
url = pyperclip.paste()
print(url)
if url == success_url:
    print('元素已找到，登陆成功')
else:
    print('元素未找到，登陆未成功')

pyautogui.mouseDown(479, 340,1)
pyautogui.mouseUp(568, 339,1)
time.sleep(1)
pyautogui.hotkey("command", "c")
nickname = pyperclip.paste()
print(nickname)
