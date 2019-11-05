# -*- coding: utf-8 -*- 
# @Time : 2019/8/16 下午6:16 
# @Site :  
# @File : get_delivery_in.py
'''
获取供应商 delivery in信息
'''

import os, sys
import requests

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from auxiliary.SpiderLog import Logger
from auxiliary.DbConnect import DbService

logger = Logger().logger

dbservice = DbService()

delivery_collection = dbservice.db['delivery_in_v2']

data_cursor = dbservice.org_collection.find({})

base_delivery_url = 'https://udaan.com/mapi/sla/{orgId}?'

headers = {
    'authority': "udaan.com",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "cookie": "__cfduid=d754320597078bd9e609496a894943ccc1565777531; ai_user=OfWuW|2019-08-14T10:12:17.091Z; d=HpFFoyHV8W21ktNkogF6rN8aVNZnUs4p3; rt.0=qcDJeL0O6jwBACAWQgjPKHR0CbdEaoiVr5g5ySv%2BrI93plHk8y2AAJrwzRLYB7txjuHRD%2Bo8h1IIXWdf9BZmRk1Chd1IER%2BCNhaVQoZSjmG1pX8OGTi5WMrp4gcCJtpqoeIRM8ZaMU0BqhS3q5AazLIi2FFxzdnhKcmWojoJXpieqkxUR541MmY5ZDhkZg%3D%3D; s=r5ljsfep853euyvs2lmeinj0; mp_a67dbaed1119f2fb093820c9a14a2bcc_mixpanel=%7B%22distinct_id%22%3A%20%22USR4MB4E097BQ82Q4L57D58Q5F6XV%22%2C%22%24device_id%22%3A%20%2216c8f9f1f8b170-035029c73776c8-30760d58-1fa400-16c8f9f1f8c298%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22USR4MB4E097BQ82Q4L57D58Q5F6XV%22%7D"
}

# 初始化
if __name__ == "__main__":
    # for data in data_cursor:
    #     orgId = data['orgId']
    #     delivery_url = base_delivery_url.format(orgId=orgId.strip())
    #     try:
    #         response = requests.get(url=delivery_url, headers=headers, timeout=60)
    #         if response.status_code == 200:
    #             data = response.json()
    #             print(data)
    #             for key, value in data.items():
    #                 insert_data = {
    #                     key: value,
    #                     "orgId": orgId
    #                 }
    #                 delivery_collection.find_one_and_delete({"orgId": orgId})
    #                 delivery_collection.insert_one(insert_data)
    #                 logger.info("orgId:{} delivery in 插入成功".format(orgId))
    #     except Exception as e:
    #         logger.error("请求api失败,错误原因:{}".format(str(e)))
    #         dbservice.redis_conn.sadd("still_error_delivery_url", delivery_url)

    delivery_url = 'https://udaan.com/mapi/sla/ORG047ER1L8RTC1Q4NS2954RG30B2?'
    try:
        response = requests.get(url=delivery_url, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(data)
            for key, value in data.items():
                insert_data = {
                    key: value,
                    "orgId": 'ORG047ER1L8RTC1Q4NS2954RG30B2'
                }
                delivery_collection.find_one_and_delete({"orgId": 'ORG047ER1L8RTC1Q4NS2954RG30B2?'})
                delivery_collection.insert_one(insert_data)
                logger.info("orgId:{} delivery in 插入成功".format('ORG047ER1L8RTC1Q4NS2954RG30B2?'))
    except Exception as e:
        logger.error("请求api失败,错误原因:{}".format(str(e)))
        dbservice.redis_conn.sadd("still_error_delivery_url", delivery_url)

