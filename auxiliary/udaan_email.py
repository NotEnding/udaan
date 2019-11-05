#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/20 上午9:12
'''
定时发送邮件报告入库及获取详情
'''
import os
import sys
import time

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)
from settings import BASE_DIR
from auxiliary.DbConnect import DbService

dbservice = DbService()

# 当前已fetched总数
fetched_count = int(dbservice.redis_conn.get('orgId_flag').decode())

# 当前队列中的已获取的orgId数量，待获取店铺详细信息
orgId_queue_count = dbservice.redis_conn.scard('orgId')  # int
# 当前数据库中已入库的orgId 店铺详细信息
orgId_database_count = dbservice.org_collection.find({}).count()  # int

# 当前队列中的以获取的listingId数量，待获取商品详细信息
listingId_queue_count = dbservice.redis_conn.scard('listingId')
# 当前数据库中已入库的listingId 商品详细信息
listingId_database_count = dbservice.listing_collection.find({}).count()

###################################### 邮件发送 ######################################
udaan_content = BASE_DIR + '/auxiliary/udaan_content.txt'
with open(udaan_content, 'w', encoding='utf-8') as f:
    # 已 fecthed 数量
    f.write('截止到当前时间 {} udaan 网站已Fetched数量：{} 条\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                          str(fetched_count)))
    # 商品 & 店铺详情信息
    f.write('截止到当前时间 {} 待获取的店铺详情数量：{} 条\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                  str(orgId_queue_count)))
    f.write('截止到当前时间 {} 已获取的店铺详情数量：{} 条\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                  str(orgId_database_count)))
    f.write('截止到当前时间 {} 待获取的商品详情数量：{} 条\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                  str(listingId_queue_count)))
    f.write('截止到当前时间 {} 已获取的商品详情数量：{} 条\n'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                  str(listingId_database_count)))

# 发送邮件，将统计数据发送到邮箱
# send_mail_commad = "mail -s 'udaan spider:detail information' 'zhengke@starmerx.com' 'mingliang@starmerx.com' 'zhaolei@starmerx.com' < " + udaan_content
# os.system(send_mail_commad)