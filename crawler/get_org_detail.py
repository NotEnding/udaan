# -*- coding: utf-8 -*- 
# @Time : 2019/7/25 上午10:26 
# @Site :  
# @File : get_org_detail.py
import os
import sys
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from api.ApiRequest import ApiRequest
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger
from settings import ORG_SUMMARY_URL

logger = Logger().logger
dbservice = DbService()

class GetOrgDetail(ApiRequest):

    def __init__(self):
        super().__init__()

    def get_org_info(self, orgId):
        # 根据orgId获取店铺信息
        url = ORG_SUMMARY_URL.format(orgId=str(orgId))
        response = self.answer_the_url(url)
        if response.status_code == 200:
            info_list = response.json()
            if info_list:
                try:
                    # 店铺信息数据做去重处理
                    dbservice.org_collection.find_one_and_delete({"orgId": info_list['orgId']})
                    time.sleep(0.0001)
                    dbservice.org_collection.insert_one(info_list)
                    logger.info('org detail 入库成功,orgId:%s', str(orgId))
                except Exception as e:
                    logger.error('org detail 入库失败,orgId:%s,错误原因:%s', str(orgId), str(e))
            else:
                logger.info('未获取到店铺 %s 信息', str(orgId))
        else:
            logger.info('response fail,status code is %s', str(response.status_code))