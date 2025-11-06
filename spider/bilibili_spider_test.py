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


def get_json_data():
    """
    临时用
    :return:
    """
    arr = []
    j = 0
    for i in range(734362, 734384):
        j = j + 1
        if i > 734362:
            i = i + 1
        print(i)
        item = {
            "id": i,
            "long_title": "第%s话 凡人风起天南%s" % (str(j), str(j)),
            "share_url": "https://www.bilibili.com/bangumi/play/ep" + str(i),
            "title": str(j),
            "type": 2020,
            "type_title": "2020版"
        }
        arr.append(item)
    print(len(arr))
    print(arr)
    fileutil.write_arr_to_json(arr, './test_temp.json')


if __name__ == '__main__':
    print('程序开始了……\n')

    # season_id: 番剧季节ID
    season_id = 28747  # 凡人修仙传

    # 测试爬取页面
    # lists = bilibili_spider.get_bilibili_episode_info_html(season_id)
    # lists = bilibili_spider.get_bilibili_episode_info_selenium(season_id)
    lists = bilibili_spider.get_bilibili_episode_info_selenium_improved(season_id)

    # get_json_data()
