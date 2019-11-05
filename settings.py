#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/12 下午3:08
import os

# base dir
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 获取项目所在目录

# source dir
SOURCE_DIR = os.path.join(BASE_DIR, "conf")  # 存储配置信息
if not os.path.exists(SOURCE_DIR):
    os.mkdir(SOURCE_DIR)

# log dir
LOG_DIR = os.path.join(BASE_DIR, "log")  # 日志存放目录
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# 获取店铺id
BASE_URL = 'https://udaan.com/api/search/v1?start={}'

# 获取详细店铺信息
ORG_SUMMARY_URL = 'https://udaan.com/api/org/v1/summary/{orgId}'

# 获取店铺下的listingid
ORG_LISTING_URL = 'https://udaan.com/api/search/v1?orgId={orgId}&start={start}'

# listing url
LISTING_DETAIL_URL = 'https://udaan.com/api/listings/v1/{listingId}'

# refresh token url
REFRESH_TOKEN_URL = 'https://udaan.com/auth/token'
REFRESH_HEADERS = {
    'origin': 'https://udaan.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'referer': 'https://udaan.com',
    'authority': 'udaan.com',
    'cookie': '__cfduid=d754320597078bd9e609496a894943ccc1565777531; ai_user=OfWuW|2019-08-14T10:12:17.091Z; d=HpFFoyHV8W21ktNkogF6rN8aVNZnUs4p3; _csrf=e1RirRvHdnvHs15bFBQHCYjx; rt.0=qcDJeL0O6jwBACAWQgjPKHR0CbdEaoiVr5g5ySv%2BrI93plHk8y2AAJrwzRLYB7txjuHRD%2Bo8h1IIXWdf9BZmRk1Chd1IER%2BCNhaVQoZSjmG1pX8OGTi5WMrp4gcCJtpqoeIRM8ZaMU0BqhS3q5AazLIi2FFxzdnhKcmWojoJXpieqkxUR541MmY5ZDhkZg%3D%3D; at.0=t%3DeyJraWQiOiI2TW53IiwidHlwIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJhdWQiOiJodHRwczovL2FwaS51ZGFhbi5jb20vIiwic3ViIjoiVVNSNE1CNEUwOTdCUTgyUTRMNTdENThRNUY2WFYiLCJyIjpbInVzZXIiXSwibmJmIjoxNTY1OTM5NzEyLCJpc3MiOiJhdXRoLnVkYWFuLmNvbSIsImV4cCI6MTU2NTk0MDMxMiwibyI6Ik9SR0VFR1oyU0c2MFBDTDNGMFFORFlKM1lGMEdNIn0.wJ3xoCi5SledR-KTR8RNBhu-WZ1nuzFpKpSn51hUwgu5AvWlvxQT08QSATTkXEA-BrLHhSE8qS_se1gSRlTkzQ%3Ba%3D600%3Be%3D1565940312; s=r5ljsfep853euyvs2lmeinj0; mp_a67dbaed1119f2fb093820c9a14a2bcc_mixpanel=%7B%22distinct_id%22%3A%20%22USR4MB4E097BQ82Q4L57D58Q5F6XV%22%2C%22%24device_id%22%3A%20%2216c8f9f1f8b170-035029c73776c8-30760d58-1fa400-16c8f9f1f8c298%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22%24user_id%22%3A%20%22USR4MB4E097BQ82Q4L57D58Q5F6XV%22%7D; ai_session=C6W/y|1565934063096|1565939840139.985'
}

# 父类的获取URL
CATEGORIES_URL = 'https://udaan.com/api/market/v1/home'

# 子类的获取URL
SUBCATEGORIES_URL = 'https://udaan.com/api/catalog/v1/category/{targetId}'

# BEST_SELLER
BEST_SELLER_URL = 'https://udaan.com/api/search/v1?f=+tag_product_marker:BEST_SELLER&start={}'

# FAST_MOVING
FAST_MOVING_URL = 'https://udaan.com/api/search/v1?f=+tag_product_marker:FAST_MOVING&start={}'

# LATEST_ARRIVAL
LATEST_ARRIVAL_URL = 'https://udaan.com/api/search/v1?f=+tag_product_marker:LATEST_ARRIVAL&start={}'
