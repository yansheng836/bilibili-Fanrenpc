#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# 数据分析工具类
@author: yansheng
@file: analyse_util.py
@time: 2025/10/21
"""


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
    chunks = [reversed_str[i:i + 4] for i in range(0, len(reversed_str), 4)]
    formatted = ','.join(chunk for chunk in chunks)  # 保持反转状态连接
    return formatted[::-1]  # 整体反转回正常顺序


def get_md_content_table(data, title):
    """
    将数组数据转成markdown格式的表格数据
    :param data: 数组
    :param title: 表头
    :return:
    """
    content = '## ' + title + '\n\n'
    content = content + '### 表格数据\n\n'
    content = content + '|类型|集数|名称|播放量|点赞数|投币数|收藏数|弹幕数|分享数|评论数|\n'
    content = content + '| :--: | :--: | :-------------: | --------: | :----: | -----: | -----: | -----: | -----: | -----: |\n'

    for item in data:
        content = content + '|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|\n' \
                  % (
                      item['type_title'],
                      item['title'],
                      item['long_title'],
                      format_number_string(item['stat']['view']),
                      format_number_string(item['stat']['like']),
                      format_number_string(item['stat']['coin']),
                      format_number_string(item['stat']['favorite']),
                      format_number_string(item['stat']['dm']),
                      format_number_string(item['stat']['share']),
                      format_number_string(item['stat']['reply']))
    # 如果是汇总的，添加汇总行
    if 'TOP10' not in title:
        # print('汇总行')
        content = content + '|汇总|||播放量|点赞数|投币数|收藏数|弹幕数|分享数|评论数|\n'
        content = content + '|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|\n' \
                  % (
                      '汇总', ' ',' ',
                      format_number_string(sum(item["stat"]["view"] for item in data)),
                      format_number_string(sum(item["stat"]["like"] for item in data)),
                      format_number_string(sum(item["stat"]["coin"] for item in data)),
                      format_number_string(sum(item["stat"]["favorite"] for item in data)),
                      format_number_string(sum(item["stat"]["dm"] for item in data)),
                      format_number_string(sum(item["stat"]["share"] for item in data)),
                      format_number_string(sum(item["stat"]["share"] for item in data)))

    content = content + '\n'
    # print(format_number_string('122'))
    # print(format_number_string('12233333'))
    return content


def draw_bar(data, value_type='view', title='这是默认图标名，也是文件名', x_title='集数', y_title='数量'):
    """
    将数组数据转成图片
    :param data: 数据
    :param value_type: 数据类型
    :param title: 这是默认图标名，也是文件名
    :param x_title: x轴默认名称
    :param y_title: y轴默认名称
    :return:
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # 设置中文字体支持（解决中文显示问题）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK JP', 'WenQuanYi Zen Hei', ]
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False

    # 创建示例数据
    # print(data)
    # categories = ['产品A', '产品B', '产品C', '产品D', '产品E']
    # 尽量简化x轴的中文，避免互相重叠
    categories = [item["title"] + '.' + item["long_title"].replace('凡人风起天南', '风起天南').replace(' ', '') for item in data]
    # values = [230, 450, 560, 780, 320]
    # values = [item["stat"]["view"] for item in data]
    values = [item["stat"][value_type] for item in data]
    # 使用色彩映射
    colors = plt.cm.tab10(np.arange(len(values)))

    # 创建图形和坐标轴，设置大小
    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制柱状图：柱子宽度用 width=0.5
    bars = ax.bar(categories, values, color=colors, edgecolor='black', alpha=0.8)

    # 设置x轴刻度字体大小
    plt.xticks(fontsize=7)

    # 设置标题和标签
    ax.set_title(title, fontsize=12, pad=20)
    ax.set_xlabel(x_title, fontsize=12)
    ax.set_ylabel(y_title, fontsize=12)

    # 在柱子上方添加数据标签
    for bar, value in zip(bars, values):
        height = bar.get_height()
        # 转成万分位加逗号格式 1,2345；后面发现处理之后数字不好看，先不处理了
        # value = format_number_string(value)
        ax.text(bar.get_x() + bar.get_width() / 2., height + 10, f'{value}', ha='center', va='bottom', fontsize=11)

    # 设置y轴范围，使图表更美观
    ax.set_ylim(0, max(values) * 1.15)

    # 添加网格线
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    # 优化布局(自动调整布局)并保存
    plt.tight_layout()
    image_path = './images/' + title + '.png'
    plt.savefig(image_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')  # 设置背景
    print("进阶柱状图已保存为 %s" % image_path)
    # plt.show()
