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


def get_bilibili_episodes(season_id: int, types=[0, 1, 2, 10, 2020],
                          url="https://api.bilibili.com/pgc/web/season/section",
                          headers=HEADERS, buvid3: str = BUVID3) -> List[Dict[str, Any]]:
    """
    获取B站番剧的episodes数据

    Args:
        season_id: 番剧季节ID
        types: 类型（数组）
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
        # print(response.text)

        # 优化6: 直接使用response.json()避免额外的json.loads调用
        data = response.json()

        # 优化7: 添加数据验证，确保数据结构正确
        if data.get("code") != 0:
            raise ValueError(f"API返回错误: {data.get('message', '未知错误')}")

        # 优化8: 使用get方法避免KeyError
        # 用于区分类型：0 正片 ，1 预告，2 特别花絮
        if types == []:
            print(' type 不能为[]!')
            return []
        else:
            episodes = []
            if 0 in types:
                print('0 in type')
                episodes_tmp = data.get("result", {}).get("main_section", {}).get("episodes", [])
                # 优化代码：添加类型属性
                for obj in episodes_tmp:
                    obj['type'] = 0
                    obj['type_title'] = '正片'
                episodes = episodes + episodes_tmp
            if 1 in types:
                print('1 in type')
                episodes_tmp = (data.get("result", {}).get("section", []))[0].get("episodes", [])
                # 优化代码：添加类型属性
                for obj in episodes_tmp:
                    obj['type'] = 1
                    obj['type_title'] = '预告'
                episodes = episodes + episodes_tmp
            if 2 in types:
                print('2 in type')
                episodes_tmp = (data.get("result", {}).get("section", []))[1].get("episodes", [])
                # print(episodes_tmp)
                # 优化代码：添加类型属性
                for obj in episodes_tmp:
                    obj['type'] = 2
                    obj['type_title'] = '特别花絮'
                episodes = episodes + episodes_tmp
            # 这个暂时没找到数据，临时手动写的
            filename = './bilibili_episodes_manual.json'
            if 10 in types:
                print('10 in type')
                with open(filename, 'r', encoding='utf-8') as tmp_file:
                    episodes_json = json.load(tmp_file)
                # print(episodes_json)
                episodes_tmp = []
                for item in episodes_json:
                    if item['type'] == 10:
                        episodes_tmp.append(item)
                # print(episodes_tmp)
                episodes = episodes + episodes_tmp
            if 2020 in types:
                print('10 in type')
                with open(filename, 'r', encoding='utf-8') as tmp_file:
                    episodes_json = json.load(tmp_file)
                # print(episodes_json)
                episodes_tmp = []
                for item in episodes_json:
                    if item['type'] == 2020:
                        episodes_tmp.append(item)
                # print(episodes_tmp)
                episodes = episodes + episodes_tmp

        # print(episodes)
        # 只保留需要的属性
        episodes = fileutil.list_retain_attributes(episodes,
                                                   ['id', 'long_title', 'share_url', 'long_title', 'title', 'type',
                                                    'type_title'])

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


def get_bilibili_episode_info_html(ep_id: int,
                                   url="https://www.bilibili.com/bangumi/play/ep1231564?from_spmid=666.25.episode.0",
                                   headers=HEADERS,
                                   buvid3: str = BUVID3) -> List[Dict[str, Any]]:
    """
    本来想从单级的播放列表中，获取官方的系列剧的详细；爬取后发现，右侧栏的数据不是纯页面，是后面动态加载的，暂时没找到具体接口，不知道怎么处理 todo
    """
    # 优化1: 使用常量定义URL和headers，避免重复字符串创建
    BASE_URL = url
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
        print(response.text)

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


def get_bilibili_episode_info_selenium(
        ep_id: int,
        url_template: str = "https://www.bilibili.com/bangumi/play/ep{}",
        headless: bool = True  # 默认使用无头模式以提高效率
) -> List[Dict[str, Any]]:
    """
    使用Selenium模拟Chrome浏览器爬取Bilibili剧集信息，处理JS动态加载内容。

    Args:
        ep_id: 剧集ID
        url_template: URL模板，使用ep_id动态生成地址
        headless: 是否使用无头模式（无界面浏览器），True可节省资源

    Returns:
        List[Dict[str, Any]]: 剧集信息列表，每个剧集为字典形式
    """
    
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup
    from typing import List, Dict, Any
    
    # 动态生成URL，避免硬编码[5](@ref)
    target_url = url_template.format(ep_id)
    print('target_url:' + target_url)
    target_url = 'https://www.bilibili.com/bangumi/play/ep1231564'
    print('target_url:' + target_url)

    # 配置Chrome选项[2,6](@ref)
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器界面
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")  # 提高兼容性
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 初始化浏览器驱动（请确保ChromeDriver已安装并配置到PATH）[2](@ref)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 访问目标页面
        driver.get(target_url)

        # 使用显式等待，确保动态内容加载完成（等待特定元素出现）[2,6](@ref)
        wait = WebDriverWait(driver, timeout=10)  # 最多等待10秒
        # 示例：等待剧集列表容器加载（需根据实际页面调整选择器）
        episode_container = wait.until(
            # EC.presence_of_element_located((By.CLASS_NAME, "episode-list"))  # 替换为实际类名
            # EC.presence_of_element_located((By.CLASS_NAME, "eplist_ep_list_wrapper__Sy5N8"))  # 替换为实际类名
            EC.presence_of_element_located((By.CLASS_NAME, "eplist_module"))  # 替换为实际类名
        )

        # 可选：模拟滚动或点击操作以触发更多动态加载[2](@ref)
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(2)  # 短暂等待滚动加载

        # 获取渲染完成的页面HTML
        page_html = driver.page_source
        print('page_html')
        print(page_html)

        # 使用BeautifulSoup解析HTML（替代原JSON解析）[3,6](@ref)
        soup = BeautifulSoup(page_html, 'html.parser')
        print('soup')
        print(soup)

        # 提取剧集信息（需根据Bilibili实际页面结构调整选择器）
        episodes = []
        episode_elements = soup.find_all('div', class_='episode-item')  # 示例类名，需替换

        for ep_element in episode_elements:
            episode_info = {}
            # 示例提取字段（根据页面元素调整）
            title_elem = ep_element.find('span', class_='title')
            if title_elem:
                episode_info['title'] = title_elem.get_text(strip=True)
            # 添加其他字段（如播放量、时长等）
            episodes.append(episode_info)

        return episodes if episodes else []  # 确保返回空列表而非None

    # except Exception as e:
    #     print(f"Selenium爬取失败: {e}")
    #     return []
    finally:
        driver.quit()  # 确保关闭浏览器释放资源[6](@ref)
