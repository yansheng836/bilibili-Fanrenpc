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
    # print(md_content)

    with open('./temp.md', 'w', encoding='utf-8') as f:
        f.write(md_content)

    # 测试按 view 排序
    print("按 view 排序结果:")
    lists_by_view = fileutil.process_bilibili_data(lists, ['stat.view'], 10)
    # for item in lists_by_view:
    #     print(f"ID: {item['id']}, view: {item['stat']['view']}")
    lists_by_view_md_content = analyse_util.get_md_content_table(lists_by_view, '播放量TOP10')
    print(lists_by_view_md_content)

    lists_by_like = fileutil.process_bilibili_data(lists, ['stat.like'], 10)
    lists_by_like_md_content = analyse_util.get_md_content_table(lists_by_like, '点赞数TOP10')
    print(lists_by_like_md_content)

    lists_by_coin = fileutil.process_bilibili_data(lists, ['stat.coin'], 10)
    lists_by_coin_md_content = analyse_util.get_md_content_table(lists_by_coin, '投币数TOP10')
    print(lists_by_coin_md_content)

    lists_by_favorite = fileutil.process_bilibili_data(lists, ['stat.favorite'], 10)
    lists_by_favorite_md_content = analyse_util.get_md_content_table(lists_by_favorite, '收藏数TOP10')
    print(lists_by_favorite_md_content)

    lists_by_dm = fileutil.process_bilibili_data(lists, ['stat.dm'], 10)
    lists_by_dm_md_content = analyse_util.get_md_content_table(lists_by_dm, '弹幕数TOP10')
    print(lists_by_dm_md_content)

    lists_by_share = fileutil.process_bilibili_data(lists, ['stat.share'], 10)
    lists_by_share_md_content = analyse_util.get_md_content_table(lists_by_share, '分享数TOP10')
    print(lists_by_share_md_content)

    lists_by_reply = fileutil.process_bilibili_data(lists, ['stat.reply'], 10)
    lists_by_reply_md_content = analyse_util.get_md_content_table(lists_by_reply, '评论数TOP10')
    print(lists_by_reply_md_content)


    with open('./temp-all.md', 'w', encoding='utf-8') as f:
        f.write(md_content+lists_by_view_md_content+lists_by_like_md_content+lists_by_coin_md_content+lists_by_favorite_md_content
                +lists_by_dm_md_content+lists_by_share_md_content+lists_by_reply_md_content)

    exit()

    # 测试按多个属性排序
    print("\n按coin和dm排序结果:")
    result = fileutil.process_bilibili_data(lists, ['stat.coin', 'stat.dm'])
    for item in result:
        print(f"ID: {item['id']}, Coin: {item['stat']['coin']}, DM: {item['stat']['dm']}")


    print('\n程序结束！')
