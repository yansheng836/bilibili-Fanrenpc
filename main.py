#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@desc: 爬取B站《凡人修仙传》数据
@author: yansheng
@file: main.py
@time: 2025/10/20
"""
from spider import bilibili_spider
from util import fileutil

# 类型映射：section title -> (type, type_title)
SECTION_TYPE_MAPPING = {
    '预告': (1, '预告'),
    '特别花絮': (2, '特别花絮'),
    'UP论道': (5, 'UP论道'),
    '虚天战纪': (10, '虚天战纪'),
    '2020版': (2020, '2020版'),
    '修仙之旅': (3000, '修仙之旅'),
}


def get_all_episodes(season_id: int, ep_id: int) -> list:
    """
    获取所有剧集数据（正片 + 各类型 section）

    Args:
        season_id: 番剧季节ID
        ep_id: 任意一个正片的 ep_id，用于获取 section 数据

    Returns:
        所有剧集数据列表
    """
    # 1. 获取正片列表
    print('正在获取正片列表...')
    main_episodes = bilibili_spider.get_bilibili_episodes(season_id, types=[0])
    if not main_episodes:
        print('获取正片列表失败！')
        return []

    # 标记正片类型
    for ep in main_episodes:
        ep['type'] = 0
        ep['type_title'] = '正片'

    print(f'正片数量: {len(main_episodes)}')

    # 2. 获取所有 section 数据（预测篇预告只有109集）
    print('\n正在获取 section 数据...')
    sections = bilibili_spider.get_bilibili_sections_by_ep_id(ep_id)
    print(f'section 数量: {len(sections)}')

    # 3. 从旧API获取完整的预告数据（207集，补全新API缺少的98集）
    print('\n正在从旧API获取完整预告数据...')
    old_preview_episodes = bilibili_spider.get_bilibili_episodes_old_preview(season_id)
    old_preview_ids = {ep['id'] for ep in old_preview_episodes}
    new_preview_ids = set()
    for sec in sections:
        if sec.get('title') == '预告':
            new_preview_ids = {ep['id'] for ep in sec.get('episodes', [])}
            break
    missing_count = len(old_preview_ids - new_preview_ids)
    if missing_count > 0:
        print(f'  旧API比新API多 {missing_count} 集预告，将使用旧API的数据')

    # 4. 根据 section title 映射类型
    all_episodes = list(main_episodes)

    for sec in sections:
        title = sec.get('title', '')
        episodes = sec.get('episodes', [])

        # 预告使用旧API的全部207集（替代新API的109集）
        if title == '预告' and old_preview_episodes:
            episodes = old_preview_episodes

        if title in SECTION_TYPE_MAPPING:
            type_val, type_title = SECTION_TYPE_MAPPING[title]
            print(f'  {title}: {len(episodes)} 个 (type={type_val})')

            for ep in episodes:
                ep['type'] = type_val
                ep['type_title'] = type_title

            all_episodes.extend(episodes)
        else:
            print(f'  {title}: {len(episodes)} 个 (未知类型，跳过)')

    # 5. 清理多余字段，只保留需要的
    retain_fields = ['id', 'title', 'long_title', 'type', 'type_title', 'share_url', 'link']
    all_episodes = fileutil.list_retain_attributes(all_episodes, retain_fields)

    return all_episodes


if __name__ == '__main__':
    print('程序开始了……\n')

    # season_id: 番剧季节ID
    season_id = 28747  # 凡人修仙传
    # ep_id: 任意一个正片的 ep_id，用于获取 section 数据
    ep_id = 733316  # 凡人风起天南1重制版

    # 获取所有剧集数据
    lists = get_all_episodes(season_id, ep_id)

    if not lists:
        print('获取数据失败，请排查！')
        exit(1)

    print(f'\n总计获取 {len(lists)} 个剧集')

    # 统计各类型数量
    type_counts = {}
    for item in lists:
        type_title = item.get('type_title', '未知')
        type_counts[type_title] = type_counts.get(type_title, 0) + 1

    print('\n各类型数量:')
    for type_title, count in type_counts.items():
        print(f'  {type_title}: {count}')

    # 保存完整数据到JSON
    fileutil.write_arr_to_json(lists, './bilibili_episodes.json')

    # 获取每集的统计数据
    print('\n正在获取每集统计数据...')
    for i, item in enumerate(lists):
        print(f'[{i+1}/{len(lists)}] 正在获取 item：{item["id"]} 数据...')
        item_stat = bilibili_spider.get_bilibili_episode_info(item['id'])
        if item_stat is None:
            # 部分类型（如UP论道）的 ep_id 无法通过番剧单集API获取统计数据
            # 优先尝试通过 BVID 调用标准视频 API（数据更完整）
            link = item.get('link', '')
            if '/video/' in link:
                bvid = link.split('/video/')[-1]
                video_stat = bilibili_spider.get_bilibili_video_info(bvid)
                if video_stat:
                    item_stat = video_stat
                elif item.get('stat'):
                    # 视频API也失败时，使用 section API 数据做字段映射
                    raw_stat = item['stat']
                    item_stat = {
                        'view': raw_stat.get('play', 0),
                        'like': raw_stat.get('likes', 0),
                        'coin': raw_stat.get('coin', 0),
                        'dm': raw_stat.get('danmakus', 0),
                        'reply': raw_stat.get('reply', 0),
                        'favorite': 0,
                        'share': 0,
                    }
            elif item.get('stat'):
                raw_stat = item['stat']
                item_stat = {
                    'view': raw_stat.get('play', 0),
                    'like': raw_stat.get('likes', 0),
                    'coin': raw_stat.get('coin', 0),
                    'dm': raw_stat.get('danmakus', 0),
                    'reply': raw_stat.get('reply', 0),
                    'favorite': 0,
                    'share': 0,
                }
        item['stat'] = item_stat

    # 备份旧数据
    json_file = "bilibili_episodes_infos.json"
    fileutil.move_file_by_updatetime(json_file, './backup_jsondata/')

    # 保存新数据
    fileutil.write_arr_to_json(lists, json_file)

    print('\n爬取数据完成！')
