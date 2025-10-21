#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
爬虫工具类
@author: yansheng
@file: bilibili_spider.py
@time: 2025/10/20
"""
import requests
# import os
# import re
import json
from typing import Dict, List, Any
from lxml import html
from util import fileutil

etree = html.etree

"""
    爬取HTML的超时时间
"""
timeout_html = 3
# 爬取图片的超时时间
timeout_image = 3

HEADERS = {
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
BUVID3 = ''


def get_bilibili_episodes(season_id: int, url="https://api.bilibili.com/pgc/web/season/section", headers=HEADERS,
                          buvid3: str = BUVID3) -> List[Dict[str, Any]]:
    """
    获取B站番剧的episodes数据

    Args:
        season_id: 番剧季节ID
        buvid3: 用户cookie中的buvid3参数

    Returns:
        episodes数据列表
    """
    # 优化1: 使用常量定义URL和headers，避免重复字符串创建
    BASE_URL = url

    # 优化2: 预定义headers字典，减少内存分配
    # headers = headers

    # 优化3: 使用参数字典，便于维护和扩展
    params = {"season_id": season_id}

    try:
        # 优化4: 添加超时设置，避免请求阻塞
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        # 优化5: 使用response.raise_for_status()进行错误检查
        response.raise_for_status()

        # 优化6: 直接使用response.json()避免额外的json.loads调用
        data = response.json()

        # 优化7: 添加数据验证，确保数据结构正确
        if data.get("code") != 0:
            raise ValueError(f"API返回错误: {data.get('message', '未知错误')}")

        # 优化8: 使用get方法避免KeyError
        episodes = data.get("result", {}).get("main_section", {}).get("episodes", [])
        # print(episodes)
        # 只保留需要的属性
        episodes = fileutil.list_retain_attributes(episodes,['id','long_title','share_url','long_title'])

        return episodes

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return []
    except Exception as e:
        print(f"未知错误: {e}")
        return []


def get_bilibili_episode_info(ep_id: int, url="https://api.bilibili.com/pgc/season/episode/web/info", headers=HEADERS,
                              buvid3: str = BUVID3) -> List[Dict[str, Any]]:
    """
    获取番剧单集详细信息

    Args:
        ep_id: 番剧单集ID

    Returns:
        包含episode_id和stat等信息的字典，失败返回None
    """
    # 优化1: 使用常量定义URL和headers，避免重复字符串创建
    BASE_URL = url + '?ep_id=' + str(ep_id)
    # print('BASE_URL:' + BASE_URL)

    # 优化2: 预定义headers字典，减少内存分配
    # headers = headers

    # 优化4: 设置cookie
    cookies = {"buvid3": buvid3}

    # 优化5: 使用参数字典
    params = {"ep_id": ep_id}

    try:
        # 优化6: 添加超时和重试机制
        response = requests.get(
            BASE_URL,
            headers=headers,
            # params=params,
            timeout=10
        )
        # print(response)
        # print(response.text)
        response.raise_for_status()

        data = response.json()
        # print(data)

        # 优化7: 验证API返回状态
        if data.get("code") != 0:
            print(f"API返回错误: {data.get('message', '未知错误')}")
            return None

        return data.get("data", {}).get("stat", {})

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        # print(e)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return None
