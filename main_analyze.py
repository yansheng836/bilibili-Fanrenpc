#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@desc: 处理数据
@author: yansheng
@file: main_analyze.py
@time: 2025/10/21
"""
import os
import re
import json
import datetime
from util import fileutil
from util import analyse_util

# 默认参与统计的类型（排除修仙之旅等大量非正片内容）
DEFAULT_STAT_TYPES = ['正片', '预告', '特别花絮', 'UP论道', '虚天战纪', '2020版', '修仙之旅']


def filter_by_type(data, type_titles=None):
    """
    按 type_title 筛选数据

    Args:
        data: 原始数据列表
        type_titles: 要保留的 type_title 列表，None 表示全部保留

    Returns:
        筛选后的数据列表
    """
    if type_titles is None:
        return data
    return [item for item in data if item.get('type_title') in type_titles]


if __name__ == "__main__":
    print('程序开始了……\n')
    # 数据文件
    json_file = "./bilibili_episodes_infos.json"

    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        lists = json.load(f)

    # 统计各类型数量
    type_counts = {}
    for item in lists:
        type_title = item.get('type_title', '未知')
        type_counts[type_title] = type_counts.get(type_title, 0) + 1

    print('各类型数量:')
    for type_title, count in type_counts.items():
        print(f'  {type_title}: {count}')

    # 筛选参与统计的类型
    lists_filtered = filter_by_type(lists, DEFAULT_STAT_TYPES)
    print(f'\n参与统计的类型: {DEFAULT_STAT_TYPES}')
    print(f'筛选后数量: {len(lists_filtered)}')

    # 1. 总数据转成md
    project_title = 'B站《凡人修仙传》动漫总数据统计'
    # 添加更新时间，方便知道数据是什么时候更新的
    mtime = (datetime.datetime.fromtimestamp(os.path.getmtime(json_file))).strftime('%Y-%m-%d %H:%M:%S')
    md_content = analyse_util.get_md_content_table(lists_filtered, project_title + '(更新时间：%s)' % mtime)

    # 2. 计算数据的TOP10
    key_values = [
        {'value_type': 'view', 'title': '播放量TOP10'},
        {'value_type': 'like', 'title': '点赞数TOP10'},
        {'value_type': 'coin', 'title': '投币数TOP10'},
        {'value_type': 'favorite', 'title': '收藏数TOP10'},
        {'value_type': 'dm', 'title': '弹幕数TOP10'},
        {'value_type': 'share', 'title': '分享数TOP10'},
        {'value_type': 'reply', 'title': '评论数TOP10'},
    ]
    all_md_content = ''
    for item in key_values:
        print('处理数据类型为 %s 的数据' % item['value_type'])
        # 转成md格式
        lists_by_temp = fileutil.process_bilibili_data(list(lists_filtered), ['stat.' + str(item['value_type'])], 10)
        lists_by_temp_md_content = analyse_util.get_md_content_table(lists_by_temp, item['title'])

        # 3.数据可视化，画图
        analyse_util.draw_bar(lists_by_temp, item['value_type'], item['title'])
        image_md_content = '### 数据可视化\n\n![%s](./images/%s.png)\n\n' % (item['title'], item['title'])

        all_md_content = all_md_content + lists_by_temp_md_content + image_md_content

    # 4. 所有数据写到md文件
    last_md_content = md_content + '\n' + all_md_content
    with open('./%s.md' % project_title, 'w', encoding='utf-8') as f:
        f.write(last_md_content)

    # 5.将数据更新到README文件中
    readme_path = 'README.md'
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_md_content = f.read()

    # 替换关键字之间的数据
    pattern = r'<!-- START_TOC_GENERATED -->\n\n.*?<!-- END_TOC_GENERATED -->'
    replacement = '<!-- START_TOC_GENERATED -->\n\n' + last_md_content + '<!-- END_TOC_GENERATED -->'
    readme_md_content = re.sub(pattern, replacement, readme_md_content, count=1, flags=re.DOTALL)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_md_content)

    print('\n将数据更新到README文件完成！')

    print('\n统计数据完成！')
