#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@desc: 处理数据
@author: yansheng
@file: main.py
@time: 2025/10/21
"""
import json
from util import analyse_util
from util import fileutil

if __name__ == "__main__":
    print('程序开始了……\n')
    # 数据文件
    json_file = "./bilibili_episodes_infos.json"

    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        lists = json.load(f)

    # print(lists)
    # 1. 总
    md_content = analyse_util.get_md_content_table(lists, '总数据统计')
    print(md_content)

    with open('./temp.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    exit()

    # 测试按coin排序
    print("按coin排序结果:")
    lists_by_coin = fileutil.process_bilibili_data(lists, ['stat.coin'])
    for item in lists_by_coin:
        print(f"ID: {item['id']}, Coin: {item['stat']['coin']}")

    # 测试按多个属性排序
    print("\n按coin和dm排序结果:")
    result = fileutil.process_bilibili_data(lists, ['stat.coin', 'stat.dm'])
    for item in result:
        print(f"ID: {item['id']}, Coin: {item['stat']['coin']}, DM: {item['stat']['dm']}")

    print('\n程序结束！')
