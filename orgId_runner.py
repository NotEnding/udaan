#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/17 下午2:20
import os
import sys

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from crawler.get_orgId import GetorgId
from auxiliary.SpiderLog import Logger

logger = Logger().logger

if __name__ == "__main__":
    getorg = GetorgId()
    getorg.get_orgInfo()
    logger.info('orgId 全部获取完成')
