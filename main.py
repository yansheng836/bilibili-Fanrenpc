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
    season_id = 28747  # 凡人修仙传
    # season_id = 21082961 #牧神记，todo 一开始想观察下是否兼容其他剧，发现接口没数据，如果需要支持，需要进一步排查。

    # lists = bilibili_spider.get_bilibili_episodes(season_id,[2,10,2020])
    # exit()
    # 1.获取主列表信息
    lists = bilibili_spider.get_bilibili_episodes(season_id)
    print('lists数量：' + str(len(lists)))

    # 如果未爬取到数据，直接返回，避免置空JSON数据
    if lists is None or len(lists) == 0:
        print('爬取数据失败，结果为空，请排查！')
        exit(1)

    fileutil.write_arr_to_json(lists, './bilibili_episodes.json')

    for item in lists:
        # break
        # print(item)
        print('正在获取 item：%s 数据...' % str(item['id']))
        # continue
        # break
        # 2.获取每集的统计数据
        item_stat = bilibili_spider.get_bilibili_episode_info(item['id'])
        # print(item_stat)
        item['stat'] = item_stat
        # print(item)
        # break

    # 3.备份文件
    # 如果正常爬取，而且之前已经后了JSON文件，备份旧数据到 backup_jsondata 目录中
    # 数据文件
    json_file = "bilibili_episodes_infos.json"
    fileutil.move_file_by_updatetime(json_file, './backup_jsondata/')

    # 4.写数据到json文件中
    fileutil.write_arr_to_json(lists, json_file)

    print('\n爬取数据完成！')
