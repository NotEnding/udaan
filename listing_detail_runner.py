#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/17 下午2:37
import os
import random
import sys
import time
from multiprocessing.pool import Pool

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from crawler.get_listing_detail import GetlistingDetail
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger

logger = Logger().logger

dbservice = DbService()
listingdetail = GetlistingDetail()


def listing_detail(listingid):
    listingdetail.get_listing_info(listingid)


if __name__ == "__main__":
    while True:
        listing_length = dbservice.redis_conn.scard('listingId')
        if listing_length != 0:
            po = Pool(3)
            for i in range(100):
                listingid = dbservice.redis_conn.spop('listingId').decode()
                po.apply_async(listing_detail, args=(listingid,))
            time.sleep(random.random() * 2)
            po.close()
            po.join()
        else:
            logger.info('listing detail info 全部获取完成')
            break
