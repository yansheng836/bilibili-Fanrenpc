import requests
import json
from typing import Dict, List, Any


def get_bilibili_episodes(season_id: int, buvid3: str) -> List[Dict[str, Any]]:
    """
    获取B站番剧的episodes数据

    Args:
        season_id: 番剧季节ID
        buvid3: 用户cookie中的buvid3参数

    Returns:
        episodes数据列表
    """
    # 优化1: 使用常量定义URL和headers，避免重复字符串创建
    BASE_URL = "https://api.bilibili.com/pgc/web/season/section"

    # 优化2: 预定义headers字典，减少内存分配
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


# 优化9: 添加缓存功能，避免重复请求相同数据
from functools import lru_cache


@lru_cache(maxsize=128)
def get_bilibili_episodes_cached(season_id: int, buvid3: str) -> List[Dict[str, Any]]:
    """带缓存的版本，适用于频繁调用相同season_id的情况"""
    return get_bilibili_episodes(season_id, buvid3)


# 使用示例
if __name__ == "__main__":
    # 替换为实际的buvid3值
    buvid3_cookie = "你的buvid3值"
    season_id = 28747

    episodes = get_bilibili_episodes(season_id, buvid3_cookie)

    # 优化10: 使用生成器表达式处理大量数据
    if episodes:
        print("获取到的episodes数据:")
        # for episode in episodes:
        #     # 只提取关键信息，避免输出过多数据
        #     episode_info = {
        #         "id": episode.get("id"),
        #         "title": episode.get("title"),
        #         "long_title": episode.get("long_title"),
        #         "aid": episode.get("aid")
        #     }
        #     print(json.dumps(episode_info, ensure_ascii=False, indent=2))
        print(json.dumps(episodes, ensure_ascii=False, indent=2))
    else:
        print("未获取到数据")
