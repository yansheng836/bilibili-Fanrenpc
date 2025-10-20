#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
爬虫工具类
@author: yansheng
@file: SpiderUtil.py
@time: 2025/10/20
"""
import requests
import os
import re
from lxml import html

etree = html.etree

domain = "https://wang399.com"
"""
    爬取HTML的超时时间
"""
timeout_html = 3
# 爬取图片的超时时间
timeout_image = 3

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "origin": "https://www.bilibili.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.bilibili.com",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    # "cookie": f"buvid3={buvid3}"
}


def getList(photoType, pageIndex):
    """
    获取该用户的非空的分类列表。（注意这里要进行异常判断，如用户名输入错误等。后面不在进行处理。）
    :param photoType: 照片类型（1..n）
    :param pageIndex: 页数（1..n）
    :return: list
    """



    return


def getListDetail(category):
    """
    获取该用户的非空的分类列表。
    :param category: 分类
    :return: list
    """



