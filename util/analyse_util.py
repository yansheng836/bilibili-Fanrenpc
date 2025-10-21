#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# 文件工具类
@author: yansheng
@file: analyse_util.py
@time: 2025/10/21
"""

import os


def format_number_string1(number_str):
    """
    将数字字符串格式化为每4位加逗号的形式

    参数:
        number_str: 数字字符串，如'123456789'

    返回:
        格式化后的字符串，如'1,2345,6789'
    """
    if type(number_str) == int:
        number_str = str(number_str)
    # 反转字符串以便从右向左处理
    reversed_str = number_str[::-1]

    # 每4位分组
    chunks = [reversed_str[i:i + 4] for i in range(0, len(reversed_str), 4)]

    # 将每组反转回正常顺序并拼接
    formatted = ','.join(chunk[::-1] for chunk in chunks)

    return formatted


def format_number_string(number_str):
    """
    将数字字符串格式化为每4位加逗号的形式

    参数:
        number_str: 数字字符串，如'123456789'

    返回:
        格式化后的字符串，如'1,2345,6789'
    """
    if type(number_str) == int:
        number_str = str(number_str)
    # 从右向左每4位分组
    reversed_str = number_str[::-1]  # 先反转字符串
    chunks = [reversed_str[i:i+4] for i in range(0, len(reversed_str), 4)]
    formatted = ','.join(chunk for chunk in chunks)  # 保持反转状态连接
    return formatted[::-1]  # 整体反转回正常顺序


def get_md_content_table(data, title):
    """
    辅助函数：创建文件夹
    :param path: 文件夹名
    :return:
    """
    content = '## ' + title + '\n\n'
    content = content + '| 集数 |        名称         |    播放量 | 点赞数 | 投币数 | 收藏数 | 弹幕数 | 分享数 | 评论数 |\n'
    content = content + '| :--: | :-----------------: | --------: | :----: | -----: | -----: | -----: | -----: | -----: |\n'
    for item in data:
        content = content + '|   %s   |         %s            |       %s    |     %s   |    %s    |    %s    |    %s    |   %s     |   %s     |\n' \
                  % (
                      item['title'], item['long_title'], format_number_string(item['stat']['view']),
                      format_number_string(item['stat']['like']), format_number_string(item['stat']['coin']),
                      format_number_string(item['stat']['favorite']), format_number_string(item['stat']['dm']),
                      format_number_string(item['stat']['share']), format_number_string(item['stat']['reply']))

    # print(format_number_string('122'))
    # print(format_number_string('12233333'))
    return content
