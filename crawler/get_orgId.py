#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/12 下午4:26
import os
import sys
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from api.ApiRequest import ApiRequest
from settings import BASE_URL, BASE_DIR
from auxiliary.SpiderLog import Logger
from auxiliary.DbConnect import DbService

logger = Logger().logger
dbservice = DbService()


class GetorgId(ApiRequest):
    '''
    获得orgId 插入到队列
    '''

    def __init__(self):
        super().__init__()

    def parse_orgId(self, info_list):
        '''
        :param info: the detail info list
        :return: 返回店铺id 列表
        '''
        # list
        orgId_list = []
        for org in info_list:
            orgId = org['orgCompact']['orgId']
            orgId_list.append(orgId)
        return orgId_list

    def get_orgInfo(self):
        # 判断上次中断的位置,从上次中断的start-12 开始获取
        orgId_flag = dbservice.redis_conn.get('orgId_flag')
        orgId_flag = orgId_flag.decode() if orgId_flag else 0
        for start in range(int(orgId_flag), 1000000000, 12):
            url = BASE_URL.format(str(start))
            logger.info('开始请求api:%s', url)
            response = self.answer_the_url(url)
            if response.status_code == 200:
                if response.text != '':
                    numFound = response.json()['numFound']  # 获取总数
                    if int(numFound) > 100000:  # 获取的数据大于10w,判断为正常
                        info_list = response.json()['listings']
                        if info_list:  # 还有数据
                            # 将flag标志位更新为当前 start-12 尽量减少中断后数据丢失
                            dbservice.redis_conn.set('orgId_flag', str(int(start) - 12))
                            numFetched = response.json()['numFetched']  # 记录已fetched总数
                            logger.info('本次请求返回 numFound数量为:%s,已 Fetched数量为:%s', str(numFound), str(numFetched))
                            orgId_list = self.parse_orgId(info_list)
                            if orgId_list:
                                try:
                                    for orgId in orgId_list:  # 存入redis队列
                                        dbservice.redis_conn.sadd('orgId', orgId)  # 存入set,去重,用于获取listingId
                                        dbservice.redis_conn.sadd('orgId_detail', orgId)  # 存入set,去重,用于获取org detail info
                                        logger.info('orgId 加入队列成功,%s', str(orgId))
                                    time.sleep(0.01)
                                except Exception as e:
                                    logger.error('orgId 加入队列失败,报错信息:{}'.format(str(e)))
                            else:
                                logger.info('本次解析orgId失败')
                                continue
                        else:  # 说明全部fecthed 完成
                            logger.info('orgId 获取完成')
                            dbservice.redis_conn.set('orgId_flag', '0')  # 将flag标志位置为0
                            break
                    else:  # 调用刷新token脚本
                        logger.info('token 失效,自动刷新token')
                        try:
                            script_command = 'python3 ' + BASE_DIR + '/auxiliary/RefreshToken.py'
                            os.system(script_command)
                            logger.info('刷新token成功')
                            time.sleep(2)
                        except Exception as e:
                            logger.error('刷新token失败,错误原因:%s', str(e))
                        continue
                else:
                    logger.info('本次请求返回数据为空,url:%s,返回结果:%s', url, response.text)
                    continue
            else:
                logger.info('response fail,status code is %s', str(response.status_code))
