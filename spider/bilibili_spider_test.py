#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
爬虫工具类 测试
@author: yansheng
@file: bilibili_spider_test.py
@time: 2025/10/24
"""

from spider import bilibili_spider
from util import fileutil

if __name__ == '__main__':
    print('程序开始了……\n')

    # season_id: 番剧季节ID
    season_id = 28747 #凡人修仙传

    # 测试爬取页面
    lists = bilibili_spider.get_bilibili_episode_info_html(season_id)
