#!/usr/bin/python
#coding=utf-8

import urllib
import urllib2
import mimetools, mimetypes
import os, stat


f = open("test.txt", "r")
for line  in f:
  str = line.split('\t')
  print(str)