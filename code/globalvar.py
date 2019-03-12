#!/usr/bin/python
# -*- coding: utf-8 -*-


class GlobalVar:
  CONF = dict()
  logger = None

def set_logger(value):
    GlobalVar.logger = value

def get_logger():
    return GlobalVar.logger

def set_conf(value):
    GlobalVar.CONF = value

def get_conf():
    return GlobalVar.CONF