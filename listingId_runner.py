#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/17 下午2:24
import os
import sys

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from crawler.get_listingId import GetlistingId
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger

logger = Logger().logger

dbservice = DbService()
getlistingId = GetlistingId()

if __name__ == "__main__":
    while True:
        orgId_length = dbservice.redis_conn.scard('orgId')
        if orgId_length != 0:
            orgid = dbservice.redis_conn.spop('orgId').decode()
            getlistingId.get_listingId(orgid)
        else:
            logger.info('listingId 全部获取完成')
            break
