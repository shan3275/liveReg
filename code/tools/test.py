#!/usr/bin/python
#coding=utf-8

import urllib
import urllib2
import mimetools, mimetypes
import os, stat
import random
import time

account = list()
f = open('tmp.txt', "r")
for line in f:
        line = line.strip('\r\n')
        str = line.split('----')
        t = dict(nickname=str[0], pwd=str[1])
        account.append(t)

print len(account)
print(account)