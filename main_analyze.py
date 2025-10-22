#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@desc: 处理数据
@author: yansheng
@file: main_analyze.py
@time: 2025/10/21
"""
import re
import json
from util import fileutil
from util import analyse_util

if __name__ == "__main__":
    print('程序开始了……\n')
    # 数据文件
    json_file = "./bilibili_episodes_infos.json"

    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        lists = json.load(f)

    # print(lists)
    # 1. 总
    project_title = 'B站《凡人修仙传》动漫总数据统计'
    md_content = analyse_util.get_md_content_table(lists, project_title)
    # print(md_content)
    # analyse_util.draw_bar(lists, '总数据统计')

    # with open('./temp.md', 'w', encoding='utf-8') as f:
    #     f.write(md_content)

    # 单个，后面改用for
    # 测试按 view 排序
    # print("按 view 排序结果:")
    # lists_by_view = fileutil.process_bilibili_data(lists, ['stat.view'], 10)
    # # for item in lists_by_view:
    # #     print(f"ID: {item['id']}, view: {item['stat']['view']}")
    # lists_by_view_md_content = analyse_util.get_md_content_table(lists_by_view, '播放量TOP10')
    # print(lists_by_view_md_content)
    # # 画图
    # analyse_util.draw_bar(lists_by_view, 'view', '播放量TOP10')

    # 测试按多个属性排序
    # print("\n按coin和dm排序结果:")
    # result = fileutil.process_bilibili_data(lists, ['stat.coin', 'stat.dm'])
    # for item in result:
    #     print(f"ID: {item['id']}, Coin: {item['stat']['coin']}, DM: {item['stat']['dm']}")

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
        # break
        print(item['value_type'])
        # print("按 view 排序结果:")
        # 转成md格式
        # lists_by_view = fileutil.process_bilibili_data(lists, ['stat.%s'] % str(item['value_type']), 10)
        lists_by_temp = fileutil.process_bilibili_data(lists, ['stat.' + str(item['value_type'])], 10)
        lists_by_temp_md_content = analyse_util.get_md_content_table(lists_by_temp, item['title'])
        # print(lists_by_view_md_content)

        # 画图
        analyse_util.draw_bar(lists_by_temp, item['value_type'], item['title'])
        image_md_content = '### 数据可视化\n\n![%s](./images/%s.png)\n\n' % (item['title'], item['title'])

        all_md_content = all_md_content + lists_by_temp_md_content + image_md_content

    with open('./%s.md' % project_title, 'w', encoding='utf-8') as f:
        f.write(md_content + '\n' + all_md_content)

    #将数据写到README文件中
    readme_path = 'README.md'

    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_md_content =f.read()
    # print(readme_md_content)
    pattern = r'<!-- START_TOC_GENERATED -->\n\n.*?<!-- END_TOC_GENERATED -->'
    replacement = '<!-- START_TOC_GENERATED -->\n\n'+(md_content + '\n' + all_md_content)+'<!-- END_TOC_GENERATED -->'
    readme_md_content = re.sub(pattern, replacement, readme_md_content, count=1, flags=re.DOTALL)
    print(readme_md_content)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_md_content)

    print('\n程序结束！')
