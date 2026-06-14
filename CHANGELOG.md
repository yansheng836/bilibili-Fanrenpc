# 更新记录

## v0.4 (2026-06-14) — GitHub Pages 主题与样式优化

**变更对比**：[v0.3...v0.4](https://github.com/yansheng836/bilibili-Fanrenpc/compare/v0.3...v0.4)

### 1. GitHub Pages 主题配置
- 启用 Cayman 单栏主题（从 Minimal 双栏布局切换）
- 动漫国风自定义 CSS：Bilibili 粉蓝渐变配色、圆角卡片化设计、毛玻璃导航栏
- 宽屏布局：内容区 95% / 最大 1320px

### 2. 左侧悬浮目录导航
- 鼠标/触摸点击展开侧边目录面板，自动解析 h2/h3 生成链接
- 半透明毛玻璃面板 + 遮罩层，ESC 或点击遮罩关闭
- 手机端按钮移至底部居中，面板宽度 60%

### 3. 响应式适配
- 修复缩小屏幕时左右边距不对称
- 手机端表格字号缩小、padding 优化
- 表格列宽恢复默认自适应，手机端去掉固定宽度

### 4. 细节修复
- 修复 shields 徽章被拉伸（仅图表图片 width:100%）
- 修复点赞数列 Markdown 对齐（居中→居右）
- 修复 SCSS 缺少 @media 闭合大括号导致构建失败

### 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `_config.yml` | 新增，配置 Cayman 主题 |
| `_includes/head-custom.html` | 新增，悬浮目录导航 HTML |
| `assets/css/style.scss` | 新增，动漫国风主题 CSS |
| `assets/js/navigation.js` | 新增，目录导航 JS（点击切换） |
| `util/analyse_util.py` | 修复点赞数列对齐方式 |
| `.gitignore` | 添加 `_includes/*.html` 例外 |

---

## v0.3 (2026-06-14) — 修复播放量统计差额 & 修仙之旅纳入统计

**变更对比**：[v0.2...v0.3](https://github.com/yansheng836/bilibili-Fanrenpc/compare/v0.2...v0.3)


### 1. 修复播放量与官方数据近5亿的差额

**背景**：程序统计的总播放量约59亿，而B站官方显示65.68亿，差额约5亿。

**根因**：新API `/pgc/view/web/season?ep_id={ep_id}` 只返回109集预告，旧API `/pgc/web/season/section?season_id=28747` 返回207集。新API缺失了98集旧版预告，这些预告播放量合计约4.42亿，是差额的主要来源。

**修改**：
- `spider/bilibili_spider.py` — 新增 `get_bilibili_episodes_old_preview()` 函数，从旧API获取完整207集预告数据
- `main.py` — 在 `get_all_episodes()` 中新增旧API预告数据获取逻辑，替换新API的109集预告

**结果**：
- 统计范围（不含修仙之旅）：59.05亿 → **63.51亿**
- 全量数据（含修仙之旅）：60.68亿 → **65.13亿**
- 官方数据：65.68亿，差额从~5亿缩小至~5400万（剩余差额源于1个剧集数据不可达 + 实时计数差异）

### 2. 修仙之旅纳入统计范围

**背景**：修仙之旅类型包含799个短视频/片段，之前被排除在统计范围外。

**修改**：
- `main_analyze.py` — 在 `DEFAULT_STAT_TYPES` 中添加 `'修仙之旅'`

**结果**：统计范围从543集扩大至全量**1342集**。

### 3. 相关文件更新
- `CLAUDE.md` — 更新预告集数（109→207）和统计范围说明
- `README.md`、`B站《凡人修仙传》动漫总数据统计.md`、所有TOP10图表 → 使用新数据重新生成

### 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `spider/bilibili_spider.py` | 新增 `get_bilibili_episodes_old_preview()` |
| `main.py` | 新增旧API预告数据获取和替换逻辑 |
| `main_analyze.py` | `DEFAULT_STAT_TYPES` 添加 `'修仙之旅'` |
| `CLAUDE.md` | 更新集数和统计范围说明 |

---

## v0.2 (2025-10-23) — 扩展剧集类型统计

**变更对比**：[v0.1...v0.2](https://github.com/yansheng836/bilibili-Fanrenpc/compare/v0.1...v0.2)


### 1. 新增预告与特别花絮统计
- 正片之外，新增**预告**（207集）和**特别花絮**（105集）的统计数据
- 统计范围从单一正片扩展到多类型剧集

### 2. 数据备份
- 新增 `backup_jsondata/` 目录，自动备份历史 JSON 数据
- `spider/bilibili_spider.py` — 添加备份逻辑

### 3. CI 环境搭建
- 配置 GitHub Actions 自动运行（每天北京时间 00:00）
- 修复中文字体安装、权限等问题
- 配置 Python 依赖缓存

---

## v0.1 (2025-10-22) — 项目初始化


### 核心功能
- B站《凡人修仙传》正片数据爬取（播放量、点赞、投币、收藏、弹幕、分享、评论）
- 数据分析与 TOP10 统计图表生成（matplotlib 柱状图）
- 自动更新 README.md 的统计表格
- GitHub Actions CI 自动化

### 文件结构
| 文件 | 说明 |
|------|------|
| `main.py` | 主爬虫脚本 |
| `main_analyze.py` | 数据分析与图表生成 |
| `spider/` | 爬虫工具类 |
| `analyse_util.py` | 分析工具（数字格式化、柱状图绘制） |
| `.github/workflows/main.yml` | CI 配置 |

### 1. 修复播放量与官方数据近5亿的差额

**背景**：程序统计的总播放量约59亿，而B站官方显示65.68亿，差额约5亿。

**根因**：新API `/pgc/view/web/season?ep_id={ep_id}` 只返回109集预告，旧API `/pgc/web/season/section?season_id=28747` 返回207集。新API缺失了98集旧版预告，这些预告播放量合计约4.42亿，是差额的主要来源。

**修改**：
- `spider/bilibili_spider.py` — 新增 `get_bilibili_episodes_old_preview()` 函数，从旧API获取完整207集预告数据
- `main.py` — 在 `get_all_episodes()` 中新增旧API预告数据获取逻辑，替换新API的109集预告

**结果**：
- 统计范围（不含修仙之旅）：59.05亿 → **63.51亿**
- 全量数据（含修仙之旅）：60.68亿 → **65.13亿**
- 官方数据：65.68亿，差额从~5亿缩小至~5400万（剩余差额源于1个剧集数据不可达 + 实时计数差异）

### 2. 修仙之旅纳入统计范围

**背景**：修仙之旅类型包含799个短视频/片段，之前被排除在统计范围外。

**修改**：
- `main_analyze.py` — 在 `DEFAULT_STAT_TYPES` 中添加 `'修仙之旅'`

**结果**：统计范围从543集扩大至全量**1342集**。

### 3. 相关文件更新
- `CLAUDE.md` — 更新预告集数（109→207）和统计范围说明
- `README.md`、`B站《凡人修仙传》动漫总数据统计.md`、所有TOP10图表 → 使用新数据重新生成

### 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `spider/bilibili_spider.py` | 新增 `get_bilibili_episodes_old_preview()` |
| `main.py` | 新增旧API预告数据获取和替换逻辑 |
| `main_analyze.py` | `DEFAULT_STAT_TYPES` 添加 `'修仙之旅'` |
| `CLAUDE.md` | 更新集数和统计范围说明 |