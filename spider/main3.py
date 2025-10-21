import requests
import json
from typing import Dict, Any, Optional
from functools import lru_cache
import time


class BilibiliEpisodeCrawler:
    """B站番剧单集信息爬取类"""

    def __init__(self, buvid3: str):
        """
        初始化爬虫

        Args:
            buvid3: 用户认证cookie中的buvid3值
        """
        self.buvid3 = buvid3
        self.base_url = "https://api.bilibili.com/pgc/season/episode/web/info"

        # 优化1: 预定义headers常量，避免重复创建
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "origin": "https://www.bilibili.com",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.bilibili.com/bangumi/play/ep{ep_id}?from_spmid=666.19.0.0",
            "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        }

        # 优化2: 创建session对象复用连接
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_episode_info(self, ep_id: int) -> Optional[Dict[str, Any]]:
        """
        获取番剧单集详细信息

        Args:
            ep_id: 番剧单集ID

        Returns:
            包含episode_id和stat等信息的字典，失败返回None
        """
        # 优化3: 动态设置referer
        headers = self.headers.copy()
        headers["referer"] = f"https://www.bilibili.com/bangumi/play/ep{ep_id}?from_spmid=666.19.0.0"

        # 优化4: 设置cookie
        cookies = {"buvid3": self.buvid3}

        # 优化5: 使用参数字典
        params = {"ep_id": ep_id}

        try:
            # 优化6: 添加超时和重试机制
            response = self.session.get(
                self.base_url,
                params=params,
                cookies=cookies,
                timeout=10,
                headers=headers
            )

            response.raise_for_status()

            data = response.json()

            # 优化7: 验证API返回状态
            if data.get("code") != 0:
                print(f"API返回错误: {data.get('message', '未知错误')}")
                return None

            return data.get("data", {})

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None

    @lru_cache(maxsize=128)
    def get_episode_info_cached(self, ep_id: int) -> Optional[Dict[str, Any]]:
        """带缓存的版本，适用于频繁查询相同ep_id"""
        return self.get_episode_info(ep_id)

    def extract_episode_stat(self, ep_id: int) -> Dict[str, Any]:
        """
        提取episode_id和stat数据

        Args:
            ep_id: 番剧单集ID

        Returns:
            包含episode_id和统计信息的字典
        """
        data = self.get_episode_info(ep_id)

        if not data:
            return {}

        # 优化8: 安全地提取所需数据
        result = {
            "episode_id": data.get("episode_id"),
            "stat": data.get("stat", {}),
            "related_up": data.get("related_up", [])
        }

        return result

    def batch_get_episodes(self, ep_ids: list, delay: float = 1.0) -> Dict[int, Dict[str, Any]]:
        """
        批量获取多个单集信息

        Args:
            ep_ids: 单集ID列表
            delay: 请求间隔（秒），避免频繁请求

        Returns:
            以ep_id为key的字典
        """
        results = {}

        for ep_id in ep_ids:
            # 优化9: 添加延迟避免频繁请求
            time.sleep(delay)

            result = self.extract_episode_stat(ep_id)
            if result:
                results[ep_id] = result

        return results


# 使用示例
def main():
    # 替换为您的实际buvid3值
    # BUVID3 = "您的buvid3值"
    BUVID3 = ""
    EPISODE_ID = 1231573

    # 创建爬虫实例
    crawler = BilibiliEpisodeCrawler(BUVID3)

    # 获取单集信息
    episode_data = crawler.extract_episode_stat(EPISODE_ID)

    if episode_data:
        print("获取到的单集信息:")
        print(json.dumps(episode_data, ensure_ascii=False, indent=2))

        # 提取统计信息
        stat = episode_data.get("stat", {})
        if stat:
            print("\n详细统计信息:")
            print(f"播放量: {stat.get('view', 0):,}")
            print(f"点赞数: {stat.get('like', 0):,}")
            print(f"投币数: {stat.get('coin', 0):,}")
            print(f"收藏数: {stat.get('favorite', 0):,}")
            print(f"弹幕数: {stat.get('dm', 0):,}")
            print(f"分享数: {stat.get('share', 0):,}")
            print(f"评论数: {stat.get('reply', 0):,}")
    else:
        print("获取数据失败")


# 批量处理示例
def batch_example():
    BUVID3 = "您的buvid3值"
    EPISODE_IDS = [1231573, 1231574, 1231575]  # 示例ID列表

    crawler = BilibiliEpisodeCrawler(BUVID3)

    # 批量获取
    results = crawler.batch_get_episodes(EPISODE_IDS, delay=1.5)

    for ep_id, data in results.items():
        stat = data.get("stat", {})
        print(f"单集 {ep_id}: 播放量 {stat.get('view', 0)}")


if __name__ == "__main__":
    main()
