#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/25 下午5:47
'''
获取父类的categories and sub categories
'''
import os
import sys
import requests

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import CATEGORIES_URL, SUBCATEGORIES_URL
from auxiliary.DbConnect import DbService
from auxiliary.SpiderLog import Logger

logger = Logger().logger
dbservice = DbService()


class GetCategories(object):
    def __init__(self):
        super().__init__()
        self.headers = {
            'authority': "udaan.com",
            'origin': 'https://udaan.com',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'referer': 'https://udaan.com',
        }
        self.timeout = 20

    def get_categories_info(self):
        logger.info('开始获取categories信息,url:%s' % CATEGORIES_URL)
        response = requests.get(url=CATEGORIES_URL, headers=self.headers, timeout=self.timeout)
        if response.status_code == 200:
            info_list = response.json()
            print(info_list)
            if info_list:
                for i in info_list:
                    for categories in i['categories']:
                        sub_categories_url = SUBCATEGORIES_URL.format(targetId=categories['targetId'])
                        res = requests.get(url=sub_categories_url, headers=self.headers, timeout=self.timeout)
                        if res.status_code == 200:
                            categories['title'] = res.json()['title']  # title
                            categories['subCategories'] = res.json()['subCategories']  # subCategories
                            try:
                                res_categories = dbservice.categories_collection.find_one(
                                    {"targetId": categories['targetId']})  # 查重
                                if not res_categories:
                                    dbservice.categories_collection.insert_one(
                                        categories)  # categories detail insert db
                                    logger.info('categories info 入库成功')
                                else:
                                    logger.info('categories info already exists')
                            except Exception as e:
                                logger.error('categories info 入库失败,错误原因:%s', str(e))
                                continue
                        else:
                            logger.info('response sub categories fail,status code is %s', str(res.status_code))
                            continue
            else:
                logger.info('本次请求返回数据为空,url:%s,返回结果:%s', CATEGORIES_URL, response.text)
        else:
            logger.info('response categories fail,status code is %s', str(response.status_code))


if __name__ == '__main__':
    get_categories = GetCategories()
    get_categories.get_categories_info()
