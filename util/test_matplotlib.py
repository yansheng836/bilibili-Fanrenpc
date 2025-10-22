#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# 分析工具类
@author: yansheng
@file: analyse_util.py
@time: 2025/10/21
"""


import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体支持（解决中文显示问题）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建示例数据
categories = ['产品A', '产品B', '产品C', '产品D', '产品E']
values = [230, 450, 560, 780, 320]
colors = plt.cm.tab10(np.arange(len(values)))  # 使用色彩映射

# 创建图形和坐标轴，设置大小
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制柱状图
bars = ax.bar(categories, values, color=colors, edgecolor='black', alpha=0.8)

# 设置标题和标签
ax.set_title('2024年第一季度产品销售情况', fontsize=16, pad=20)
ax.set_xlabel('产品类别', fontsize=12)
ax.set_ylabel('销售额 (万元)', fontsize=12)

# 在柱子上方添加数据标签
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 10,
            f'{value}', ha='center', va='bottom', fontsize=11)

# 设置y轴范围，使图表更美观
ax.set_ylim(0, max(values) * 1.15)

# 添加网格线
ax.grid(axis='y', alpha=0.3, linestyle='--')

# 优化布局并保存
plt.tight_layout()
plt.savefig('./advanced_bar_chart.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')  # 设置背景
print("进阶柱状图已保存为 'advanced_bar_chart.png'")
plt.show()
