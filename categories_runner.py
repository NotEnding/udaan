#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2019/6/25 下午7:40
import os
import sys

current_path = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(current_path)[0]
sys.path.append(rootPath)

from crawler.get_categories import GetCategories

if __name__ == "__main__":
    get_categories = GetCategories()
    get_categories.get_categories_info()