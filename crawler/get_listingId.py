#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/13 上午10:52
'''
获取1个店铺下的全部商品的listingId，并存入到redis
'''
import os
import sys
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from api.ApiRequest import ApiRequest
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger
from settings import ORG_LISTING_URL

logger = Logger().logger
dbservice = DbService()

'''
获取一个店铺下的全部listingId
'''


class GetlistingId(ApiRequest):

    def __init__(self):
        super().__init__()

    def parse_listingId(self, info_list):
        '''
        :param info_list:
        :return:
        '''
        listingsId_list = []
        for org in info_list:
            listingId = org['listingId']
            listingsId_list.append(listingId)
        return listingsId_list

    def get_listingId(self, orgId):
        # 将上一次最后pop的orgId,并将其重新加入到队列中,避免中断程序后数据有丢失
        last_req_orgId = dbservice.redis_conn.get('last_req_orgId').decode()
        if last_req_orgId != '0':
            dbservice.redis_conn.sadd('orgId', last_req_orgId)
        for start in range(0, 1000000000, 12):
            url = ORG_LISTING_URL.format(orgId=str(orgId), start=str(start))
            logger.info('开始请求api:%s', url)
            res = self.answer_the_url(url)
            if res.status_code == 200:
                if res.text != '':
                    info_list = res.json()['listings']
                    if info_list:
                        # 把最后获取的orgId 记录下来，避免异常中断，而redis已经pop掉
                        dbservice.redis_conn.set('last_req_orgId', orgId)
                        numFound = res.json()['numFound']  # 记录总数
                        numFetched = res.json()['numFetched']  # 记录Fetched数
                        logger.info('该店铺 %s 下listings numFound数量为:%s,已 Fetched数量为:%s', str(orgId), str(numFound),
                                    str(numFetched))
                        listingsId_list = self.parse_listingId(info_list)
                        if listingsId_list:
                            try:
                                for listingId in listingsId_list:  # 存入redis队列
                                    dbservice.redis_conn.sadd("listingId", listingId)  # 存入redis 集合中
                            except Exception as e:
                                logger.error('orgId 加入队列失败,报错信息:{}'.format(str(e)))
                        else:
                            logger.info('解析listingId失败')
                            continue
                    else:  # 说明fecthed 完了
                        dbservice.redis_conn.set('last_req_orgId', '0')  # orgId下的全部listingId 获取完成则将其置为'0'
                        logger.info('店铺 %s 下 全部listingId 获取完成', str(orgId))
                        break
                else:
                    logger.info('本次请求返回数据为空,url:%s,返回结果:%s', url, res.text)
                    continue
            else:
                logger.info('response fail,status code is %s', str(res.status_code))
