# -*- coding: utf-8 -*- 
# @Time : 2019/7/19 下午3:29 
# @Site :  
# @File : OrgInfoUpdate.py
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
from settings import ORG_SUMMARY_URL

logger = Logger().logger
dbservice = DbService()


class UpdateOrgInfo(ApiRequest):

    def __init__(self):
        super().__init__()

    def update_orginfo(self, orgId):
        # 根据orgId更新店铺信息
        url = ORG_SUMMARY_URL.format(orgId=str(orgId))
        response = self.answer_the_url(url)
        if response.status_code == 200:
            info_list = response.json()
            if info_list:
                # 店铺信息数据做去重处理
                dbservice.org_collection.find_one_and_delete({"orgId": info_list['orgId']})
                time.sleep(0.0001)
                dbservice.org_collection.insert_one(info_list)
                logger.info('org %s detail update success', str(info_list['orgId']))
            else:
                logger.info('未获取到店铺 %s 信息', str(orgId))
        else:
            logger.info('response fail,status code is %s', str(response.status_code))


# update func
def update_info(orgId):
    UpdateOrgInfo().update_orginfo(orgId)


#  初始化，将待更新的店铺ID加入到队列
# orgId_list = dbservice.org_collection.find({},{"orgId":1})
# for orgIds in orgId_list:
#     orgId = orgIds['orgId']
#     dbservice.redis_conn.sadd('to_be_update_orgId',orgId)
# ###############################################


if __name__ == "__main__":
    t1 = time.time()
    ################ start update #################
    while True:
        update_length = dbservice.redis_conn.scard('to_be_update_orgId')
        logger.info('开始进行供应商信息更新,当前剩余{} 家店铺待更新'.format(str(update_length)))
        if update_length != 0:
            po = Pool(4)
            for i in range(10):  # 一次取10个店铺信息进行更新
                orgId_info = dbservice.redis_conn.spop('to_be_update_orgId')
                if orgId_info:
                    orgId = orgId_info.decode()
                    po.apply_async(update_info, args=(orgId,))
                else:
                    continue
            time.sleep(random.random() * 2)
            po.close()
            po.join()
        else:
            logger.info('全部店铺更新完成')
            break
    t2 = time.time()
    print('更新全部供应商信息完成，总耗时：%s' % (str(t2 - t1)))
