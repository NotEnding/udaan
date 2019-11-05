#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/14 下午1:46
import os
import sys
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from api.ApiRequest import ApiRequest
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger
from settings import LISTING_DETAIL_URL

logger = Logger().logger
dbservice = DbService()

'''
标题、主图、品类路径、根品类、销量、长描、短描、产品参数、图片列表、店铺名称、店铺id、店铺链接、
运费(目的地+价格)、重量、属性图、变体信息、变体价格，另外看是否有阶梯价
'''


class GetlistingDetail(ApiRequest):

    def __init__(self):
        super().__init__()

    def get_listing_info(self, listingId):
        url = LISTING_DETAIL_URL.format(listingId=listingId)
        logger.info('开始获取listing detail info:%s', url)
        response = self.answer_the_url(url)
        if response.status_code == 200:
            if response.text != '':
                info_dict = response.json()
                try:
                    # 商品信息做去重处理
                    dbservice.listing_collection.find_one_and_delete({"listingId": info_dict['listingId']})
                    # time.sleep(0.0001)
                    dbservice.listing_collection.insert_one(info_dict)  # listing detail insert db
                    logger.info('listing detail 入库成功,listingId:%s', str(listingId))
                except Exception as e:
                    logger.error('listing detail 入库失败,listingId:%s,错误原因:%s', str(listingId), str(e))
            else:
                logger.info('本次请求返回数据为空,url:%s,返回结果:%s', url, response.text)
        else:
            logger.info('response fail,status code is %s', str(response.status_code))


if __name__ == "__main__":
    listingId = 'TLSARB7HS55QERPDHLFT3NS5V30XFNX'
    GetlistingDetail().get_listing_info(listingId)