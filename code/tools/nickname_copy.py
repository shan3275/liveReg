#!/usr/bin/python
#-*- coding: UTF-8 -*-
import pyautogui
import pyperclip
import sys
import time
import platform


def checklogin():
    """
    检查在验证码通过之后，登陆是否成功，
    :return:
    """
    time.sleep(10)
    # 鼠标移动到浏览器的地址栏
    if platform.system() == 'Darwin':
        pyautogui.moveTo(265, 81, 1,pyautogui.easeInOutQuad)
    else:
        pyautogui.moveTo(265, 50, 1, pyautogui.easeInOutQuad)
    pyautogui.click()
    time.sleep(1)
    if platform.system() == 'Darwin':
        pyautogui.hotkey("command", "c")
    else:
        pyautogui.hotkey("ctrl", "c")
    url = pyperclip.paste()
    if url == 'https://www.douyu.com/member/cp':
        print('Sucess')
        return True
    else:
        print ('Fail')
        return False

def get_nickname():
    """
    获取登陆之后的用户名
    :return: 用户名
    """
    time.sleep(5)
    if platform.system() == 'Darwin':
        pyautogui.mouseDown(479, 340, 1)
        pyautogui.mouseUp(600, 340, 1)
    else:
        pyautogui.mouseDown(798, 307, 1)
        pyautogui.mouseUp(910, 307, 1)

    time.sleep(1)
    if platform.system() == 'Darwin':
        pyautogui.hotkey("command", "c")
    else:
        pyautogui.hotkey("ctrl", "c")
    nickname = pyperclip.paste()
    if platform.system() == 'Darwin':
        nickname = nickname.replace("\n","")
    else:
        nickname = nickname.replace("\n","")
        nickname = nickname.strip()

    return nickname

if __name__ == '__main__':
    if checklogin() == True:
        nickname = get_nickname()
        print('nickname: '+ nickname)
        print(len(nickname))
    print('over')