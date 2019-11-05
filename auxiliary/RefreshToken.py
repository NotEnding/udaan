#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/13 下午3:18
import os
import sys
import requests
import yaml

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from settings import SOURCE_DIR, REFRESH_TOKEN_URL, REFRESH_HEADERS
from auxiliary.SpiderLog import Logger

logger = Logger().logger

'''
定时刷新token，获取authorization，7分钟为间隔
'''


def refresh_token():
    res = requests.post(url=REFRESH_TOKEN_URL, headers=REFRESH_HEADERS,timeout=20)  # 需要判断session是否expired
    if res.status_code == 200:
        response = res.json()
        if 'accessToken' in response.keys():  # 如果accessToken 在，则说明刷新token成功
            authorization = 'Bearer ' + response['accessToken'].strip('')
            with open(SOURCE_DIR + '/source.yaml', 'r') as f:  # 读取，更新authorization
                content = yaml.load(f, Loader=yaml.FullLoader)
                content['headers'].update({"authorization": authorization})
            with open(SOURCE_DIR + '/source.yaml', 'w') as fp:  # 再重新写入
                yaml.dump(content, fp)  # 重新写入
        elif 'error_description' in response.keys():
            logger.error(response['error_description'])
        else:
            logger.error(response['error'])
    else:
        logger.info('refresh token failed,status_code is %s', str(res.status_code))


refresh_token()
