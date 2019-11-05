#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/7/5 下午2:36
import os
import sys
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from api.ApiRequest import ApiRequest
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger
from settings import FAST_MOVING_URL

logger = Logger().logger
dbservice = DbService()




class FAST_MOVING(ApiRequest):

    def __init__(self):
        super().__init__()

    def get_fast_moving_seller_info(self):
        for start in range(0, 1000000000, 12):
            url = FAST_MOVING_URL.format(str(start))
            logger.info('开始获取 FAST_MOVING listing INFO :%s', url)
            response = self.answer_the_url(url)
            if response.status_code == 200:
                if response.text != '':
                    info_dict = response.json()
                    numFound = response.json()['numFound']
                    listing_info = info_dict['listings']
                    if listing_info:
                        numFetched = response.json()['numFetched']  # 记录已fetched总数
                        logger.info('本次请求返回 numFound数量为:%s,已 Fetched数量为:%s', str(numFound), str(numFetched))
                        for listings in listing_info:
                            listing_id = listings['listingId']  #
                            try:
                                # 如果已存在记录，直接删除
                                dbservice.fast_moving_collection.find_one_and_delete({"listingId": listing_id})
                                # 再更新为新数据
                                time.sleep(0.0001)
                                dbservice.fast_moving_collection.insert_one(listings)
                                logger.info('FAST_MOVING listing info 入库成功,listingId:%s', str(listing_id))
                            except Exception as e:
                                logger.error('FAST_MOVING listing info 入库失败,listingId:%s,错误原因:%s', str(listing_id),
                                             str(e))
                    else:
                        logger.info('FAST_MOVING listings 获取完成')
                        break
                else:
                    logger.info('本次请求返回数据为空,url:%s,返回结果:%s', url, response.text)
            else:
                logger.info('response fail,status code is %s', str(response.status_code))


if __name__ == '__main__':
    fats_moving = FAST_MOVING()
    fats_moving.get_fast_moving_seller_info()