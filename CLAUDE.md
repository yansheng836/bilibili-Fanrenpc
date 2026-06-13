# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

B站《凡人修仙传》动漫数据统计工具。通过B站API爬取各集播放数据（播放量、点赞、投币、收藏、弹幕、分享、评论），生成TOP10统计表格和可视化图表，自动更新到README.md。

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行数据爬取（生成 bilibili_episodes_infos.json）
python main.py

# 运行数据分析（生成统计表格和图表，更新README.md）
python main_analyze.py

# 完整流程（先爬取再分析）
python main.py && python main_analyze.py
```

## 架构说明

### 数据流

```
B站API → main.py(爬取) → bilibili_episodes_infos.json → main_analyze.py(分析) → README.md + images/
```

1. `main.py` 调用 `spider/bilibili_spider.py` 爬取剧集列表和每集统计数据
2. 数据保存到 `bilibili_episodes_infos.json`，旧数据自动备份到 `backup_jsondata/`
3. `main_analyze.py` 读取JSON，生成Markdown表格和柱状图
4. README.md 中 `<!-- START_TOC_GENERATED -->` 和 `<!-- END_TOC_GENERATED -->` 之间的内容会被自动替换

### 关键API端点

- **正片列表**: `https://api.bilibili.com/pgc/web/season/section?season_id=28747`
- **所有类型数据**: `https://api.bilibili.com/pgc/view/web/season?ep_id={ep_id}` (返回6个section)
- **单集统计**: `https://api.bilibili.com/pgc/season/episode/web/info?ep_id={id}`

### 剧集类型

| type | type_title | 数量 | 说明 |
|------|------------|------|------|
| 0 | 正片 | 178 | 主剧情 |
| 1 | 预告 | 207 | 预告片（旧API返回207集，含新API缺失的98集） |
| 2 | 特别花絮 | 105 | 花絮、PV等 |
| 5 | UP论道 | 30 | UP主相关 |
| 10 | 虚天战纪 | 2 | 导演剪辑版 |
| 2020 | 2020版 | 21 | 2020年版本 |
| 3000 | 修仙之旅 | 799 | 修仙之旅系列 |

**统计范围**: 默认统计全部7种类型（正片、预告、特别花絮、UP论道、虚天战纪、2020版、修仙之旅），可在 `main_analyze.py` 的 `DEFAULT_STAT_TYPES` 中配置。

### 数据格式

数字使用中文四位分组：`1,2345,6789`（万、亿单位），由 `analyse_util.format_number_string()` 实现。

## 注意事项

- Python 版本需兼容 3.8（CI环境限制）
- matplotlib 需要中文字体支持（SimHei/WenQuanYi Zen Hei）
- CI每天北京时间00:00自动运行（UTC 16:00），通过 `.github/workflows/main.yml` 配置
- `bilibili_episodes_manual.json` 已废弃，虚天战纪和2020版现在可从API获取
- 用 `ep_id` 参数调用 `/pgc/view/web/season` 可获取完整的section数据（6种类型）
