#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@desc: 爬取B站《凡人修仙传》数据
@author: yansheng
@file: main.py
@time: 2025/10/20
"""
from spider import bilibili_spider
from util import fileutil

if __name__ == '__main__':
    print('程序开始了……\n')

    # season_id: 番剧季节ID
    season_id = 28747

    blogList = []
    lists = bilibili_spider.get_bilibili_episodes(season_id)
    print('lists数量：' + str(len(lists)))

    fileutil.write_arr_to_json(lists,'./bilibili_episodes.json')
    for item in lists:
        # print(item)
        print(item['id'])
        # continue
        # break
        # 获取该分类的所有博客列表
        item_stat = bilibili_spider.get_bilibili_episode_info(item['id'])
        print(item_stat)
        item['stat'] = item_stat
        print(item)
        # break
    fileutil.write_arr_to_json(lists, './bilibili_episodes_infos.json')

    print('\n程序结束！')
