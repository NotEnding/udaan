# -*- coding: utf-8 -*- 
# @Time : 2019/7/25 上午10:01 
# @Site :  
# @File : ListingInfoUpdate.py
import os
import random
import sys
import time
from multiprocessing.pool import Pool

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from api.ApiRequest import ApiRequest
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger
from settings import LISTING_DETAIL_URL

logger = Logger().logger
dbservice = DbService()


class UpdateListingInfo(ApiRequest):

    def __init__(self):
        super().__init__()

    def update_listingInfo(self, listingId):
        # 根据listingId更新商品信息
        url = LISTING_DETAIL_URL.format(listingId=str(listingId))
        response = self.answer_the_url(url)
        if response.status_code == 200:
            info_dict = response.json()
            if info_dict:
                # 商品信息数据做去重处理
                dbservice.listing_collection.find_one_and_delete({"listingId": info_dict['listingId']})
                # time.sleep(0.0001)
                dbservice.listing_collection.insert_one(info_dict)
                logger.info('%s detail info update success', str(info_dict['listingId']))
            else:
                logger.info('未获取到商品 %s 信息', str(listingId))
        else:
            logger.info('response fail,status code is %s', str(response.status_code))


# 更新任务
def update_task(listingId):
    UpdateListingInfo().update_listingInfo(listingId)


# 初始化，将待更新商品信息的listingId加入到队列中
# listingId_list = dbservice.listing_collection.find({}, {"listingId": 1})
# for listingId_info in listingId_list:
#     listingId = listingId_info['listingId']
#     print(listingId)
#     dbservice.redis_conn.sadd('to_be_update_listingId', listingId)
############################################################################


if __name__ == "__main__":
    t1 = time.time()
    ############## start update ##############
    while True:
        update_length = dbservice.redis_conn.scard('to_be_update_listingId')
        logger.info('开始进行商品信息更新,当前剩余{} 件商品待更新'.format(str(update_length)))
        if update_length != 0:
            po = Pool(4)
            for i in range(10):  # 一次取10个商品进行更新
                listingId_info = dbservice.redis_conn.spop('to_be_update_listingId')
                if listingId_info:
                    listingId = listingId_info.decode()
                    po.apply_async(update_task, args=(listingId,))
                else:
                    continue
            time.sleep(random.random() * 2)
            po.close()
            po.join()
        else:
            logger.info('全部商品更新完成')
            break
    t2 = time.time()
    print('更新全部商品信息完成，总耗时：%s' % (str(t2 - t1)))
