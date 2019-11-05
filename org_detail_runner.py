# -*- coding: utf-8 -*- 
# @Time : 2019/7/25 上午10:36 
# @Site :  
# @File : org_detail_runner.py
import os
import random
import sys
import time
from multiprocessing.pool import Pool

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from crawler.get_org_detail import GetOrgDetail
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger

logger = Logger().logger

dbservice = DbService()
orgdetail = GetOrgDetail()

# task
def org_detail(orgId):
    orgdetail.get_org_info(orgId)


if __name__ == "__main__":
    while True:
        org_length = dbservice.redis_conn.scard('orgId_detail')
        if org_length != 0:
            po = Pool(2)
            for i in range(10):
                orgid = dbservice.redis_conn.spop('orgId_detail').decode()
                po.apply_async(org_detail, args=(orgid,))
            time.sleep(random.random() * 2)
            po.close()
            po.join()
        else:
            logger.info('org detail info 全部获取完成')
            break
