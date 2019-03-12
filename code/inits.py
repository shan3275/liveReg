#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from logging import handlers
import yaml
import globalvar as gl
def log_init(log_app_name, file_name):
    logger = logging.getLogger(log_app_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.handlers.TimedRotatingFileHandler(
                    filename=file_name,
                    when='midnight',
                    backupCount=3
                    )
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)

    #控制台输出
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    #logger.addHandler(sh)

    return logger

def read_yaml():
    # 你的yaml格式文件路径
    path = 'yaml.conf'
    with open(path,'r') as file:
        # 将yaml格式内容转换成 dict类型
        load_data = yaml.load(file.read())
        logger.debug(load_data)
        return load_data

##初始化设置全局变量
logger = log_init('DY', './DY.log')
conf   = read_yaml()
gl.set_logger(logger)
gl.set_conf(conf)