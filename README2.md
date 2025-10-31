# B站《凡人修仙传》数据统计

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/yansheng836/bilibili-Fanrenpc/main.yml?style=flat&label=gen) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/yansheng836/bilibili-Fanrenpc) [![GitHub Issues](https://img.shields.io/github/issues/yansheng836/bilibili-Fanrenpc)](https://github.com/yansheng836/bilibili-Fanrenpc/issues) [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/yansheng836/bilibili-Fanrenpc)](https://github.com/yansheng836/bilibili-Fanrenpc/pulls) [![GitHub Tag](https://img.shields.io/github/v/tag/yansheng836/bilibili-Fanrenpc)](https://github.com/yansheng836/bilibili-Fanrenpc/tags) [![GitHub Release](https://img.shields.io/github/v/release/yansheng836/bilibili-Fanrenpc)](https://github.com/yansheng836/bilibili-Fanrenpc/releases) ![GitHub Repo stars](https://img.shields.io/github/stars/yansheng836/bilibili-Fanrenpc) ![GitHub forks](https://img.shields.io/github/forks/yansheng836/bilibili-Fanrenpc) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/4460db83948f4592ab825e8e900ec79f)](https://app.codacy.com/gh/yansheng836/bilibili-Fanrenpc/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade) [![GitHub License](https://img.shields.io/github/license/yansheng836/bilibili-Fanrenpc)](https://github.com/yansheng836/bilibili-Fanrenpc/blob/main/LICENSE.txt)

B站《凡人修仙传》数据统计，并对部分TOP数据进行了可视化。每天晚上0点自动更新。

B站爬虫协议：<https://www.bilibili.com/robots.txt>，看了下本项目不违反该规则。如有侵权，请及时联系我进行删除。

GitHub：<https://github.com/yansheng836/bilibili-Fanrenpc>

GitHub README详见：<https://github.com/yansheng836/bilibili-Fanrenpc/blob/main/README2.md>

在线网站：<https://yansheng836.github.io/bilibili-Fanrenpc>

## B站《凡人修仙传》动漫主页

B站《凡人修仙传》动漫主页：<https://www.bilibili.com/bangumi/media/md28223043>

简介：【每周六11:00更新正片，11:15更新下集预告】看机智的凡人小子韩立如何稳健发展、步步为营，战魔道、夺至宝、驰骋星海、快意恩仇，成为纵横三界的强者。他日仙界重相逢，一声道友尽沧桑。

## 爬取相关逻辑

### 爬取集数列表

<https://www.bilibili.com/bangumi/media/md28223043>

#### 请求

```shell
curl ^"https://api.bilibili.com/pgc/web/season/section?season_id=28747^" ^
  -H ^"accept: application/json, text/plain, */*^" ^
  -H ^"accept-language: zh-CN,zh;q=0.9,en;q=0.8^" ^
  -H ^"cache-control: no-cache^" ^
  -b ^"buvid3=……^" ^
  -H ^"origin: https://www.bilibili.com^" ^
  -H ^"pragma: no-cache^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"referer: https://www.bilibili.com/^" ^
  -H ^"sec-ch-ua: ^\^"Not;A=Brand^\^";v=^\^"99^\^", ^\^"Google Chrome^\^";v=^\^"139^\^", ^\^"Chromium^\^";v=^\^"139^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36^"
```

#### 返回

```json
{
    "code": 0,
    "message": "success",
    "result": {
        "main_section": {
            "episodes": [
                {
                    "aid": 478818261,
                    "badge": "",
                    "badge_info": {
                        "bg_color": "#FB7299",
                        "bg_color_night": "#D44E7D",
                        "text": ""
                    },
                    "badge_type": 0,
                    "cid": 1022370693,
                    "cover": "http://i0.hdslb.com/bfs/archive/5ac571880f996eead5af559de2509228e20164cf.jpg",
                    "from": "bangumi",
                    "id": 733316,
                    "is_premiere": 0,
                    "long_title": "凡人风起天南1重制版",
                    "share_url": "https://www.bilibili.com/bangumi/play/ep733316",
                    "status": 2,
                    "title": "1",
                    "vid": ""
                },
                {
                    "aid": 778837300,
                    "badge": "限免",
                    "badge_info": {
                        "bg_color": "#FF7F24",
                        "bg_color_night": "#D66011",
                        "text": "限免"
                    },
                    "badge_type": 3,
                    "cid": 1022370020,
                    "cover": "http://i0.hdslb.com/bfs/archive/90ccd86f772635d556ea4b1395480cac6e3d13c4.jpg",
                    "from": "bangumi",
                    "id": 733317,
                    "is_premiere": 0,
                    "long_title": "凡人风起天南2重制版",
                    "share_url": "https://www.bilibili.com/bangumi/play/ep733317",
                    "status": 2,
                    "title": "2",
                    "vid": ""
                }
            ],
            "id": 38618,
            "title": "正片",
            "type": 0
        }
    }
}
```

### 爬取单个数据

<https://www.bilibili.com/bangumi/play/ep1231573?from_spmid=666.19.0.0>

#### 请求

```shell
curl ^"https://api.bilibili.com/pgc/season/episode/web/info?ep_id=1231573^" ^
  -H ^"accept: application/json, text/plain, */*^" ^
  -H ^"accept-language: zh-CN,zh;q=0.9,en;q=0.8^" ^
  -H ^"cache-control: no-cache^" ^
  -b ^"buvid3=……^" ^
  -H ^"origin: https://www.bilibili.com^" ^
  -H ^"pragma: no-cache^" ^
  -H ^"priority: u=1, i^" ^
  -H ^"referer: https://www.bilibili.com/bangumi/play/ep1231573?from_spmid=666.19.0.0^" ^
  -H ^"sec-ch-ua: ^\^"Not;A=Brand^\^";v=^\^"99^\^", ^\^"Google Chrome^\^";v=^\^"139^\^", ^\^"Chromium^\^";v=^\^"139^\^"^" ^
  -H ^"sec-ch-ua-mobile: ?0^" ^
  -H ^"sec-ch-ua-platform: ^\^"Windows^\^"^" ^
  -H ^"sec-fetch-dest: empty^" ^
  -H ^"sec-fetch-mode: cors^" ^
  -H ^"sec-fetch-site: same-site^" ^
  -H ^"user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36^"
```

#### 返回

```json
{
    "code": 0,
    "data": {
        "episode_id": 1231573,
        "like_animation": {
            "like_animation": ""
        },
        "related_up": [
            {
                "attribute": 2,
                "avatar": "https://i2.hdslb.com/bfs/face/ae8149db0fe146563cdbf7ff346eb9bb3dc25a12.jpg",
                "is_follow": 1,
                "mid": 98627270,
                "uname": "哔哩哔哩国创"
            }
        ],
        "stat": {
            "coin": 273094,
            "dm": 156389,
            "favorite": 37176,
            "like": 200639,
            "reply": 12018,
            "share": 2279,
            "view": 7097724
        },
        "up_like_img": {
            "content": "",
            "pre_img": "",
            "suc_img": ""
        },
        "user_community": {
            "coin_number": 0,
            "favorite": 0,
            "is_original": 1,
            "like": 0
        }
    },
    "message": "success"
}
```

## 一些问题

### 1.数据不准确

2025年10月22日10:01:28 统计了下，总的播放量是35亿左右，但是官方10-18发了51亿的海报，不知道具体是在哪里有缺漏（不知道是不是一些预告、或者是花絮之类的、因为部分章节进行了重置，也有可能是这个原因。），待进一步排查。

2025年10月23日17:08:26 发现确实是有区分的，加入预告、特别花絮之后，播放量是43亿。

2025年10月24日16:22:23 添加《虚天战纪》、《2020版 1-21集》之后，播放量是49亿。

#### 进一步分析

根目录没有这些相关的剧情，但是在具体播放也有，例如：<https://www.bilibili.com/bangumi/play/ep733316?from_spmid=666.19.0.0> 的右侧列表中有对应的剧情清单，需要搞清楚这部分数据来源。

抓到了相关的js来源（不确定是否正确）：

https://s1.hdslb.com/bfs/static/ogv/video3/_next/static/chunks/1437.b659c162c4897b1d.js

网页上看最外层是：`eplist_ep_list_wrapper__Sy5N8`，具体可参考如下内容：

```html
<div class="eplist_ep_list_wrapper__Sy5N8">
    正剧标签
</div>

<div class="eplist_ep_list_wrapper__Sy5N8" id="eplist_module">
    <div class="SectionSelector_SectionSelector__TZ_QZ">类型</div>
    <div class="imageList_wrap___f73Z">列表</div>
</div>
```

根据`imageList_wrap___f73Z`找到了上面这个js文件（但是看不懂……）。

```js
    569: function (e) {
        e.exports = {
            wrap: "imageList_wrap___f73Z"
        }
    },
```

相关腾讯元宝问答：https://yuanbao.tencent.com/chat/naQivTmsDa/229ec9af-29fe-4951-b2d1-f819c91e2e5c

---

页面上看：最外层 eplist_ep_list_wrapper__Sy5N8，但是爬取这个 html 发现，都没有这个标签！

最接近的标签 plp-r sticky，是 eplist_ep_list_wrapper__Sy5N8 的上一层。

```html
<div class="plp-r sticky">
    <div id="pc-cashier-wrapper-normal" style="width:100%;margin-bottom:14px"></div>
    <div id="danmukuBox" style="display:block" class="DanmukuBox_wrap___eG0H"></div>
    <div class="EpListSkeleton_blockWrap__h8zw6"></div>
    <div class="RecommendSkeleton_blockWrap__lKeue"></div>
</div>
<div class="navTools_floatNavExp__iNll7" style="bottom:224px">
    <div class="navTools_navMenu__I5qkt"></div>
</div>
```





### 2.CI问题：Matplotlib画图中文乱码

<https://github.com/yansheng836/bilibili-Fanrenpc/actions/runs/18737555742/job/53447278813>

存在比较多类似下面的日志，查了下，缺少对应的字体（图片中文乱码），需要安装`apt-get install -y fonts-wqy-zenhei fonts-wqy-microhei fonts-noto-cjk`。

```plain
findfont: Generic family 'sans-serif' not found because none of the following families were found: SimHei, Noto Sans CJK JP, Consolas
/home/runner/work/bilibili-Fanrenpc/bilibili-Fanrenpc/util/analyse_util.py:128: UserWarning: Glyph 20961 (\N{CJK UNIFIED IDEOGRAPH-51E1}) missing from current font.
  plt.tight_layout()
```

尝试后，发现还会报错，权限不够，加sudo：`sudo apt-get install -y fonts-wqy-zenhei fonts-wqy-microhei fonts-noto-cjk`。

详见：<https://github.com/yansheng836/bilibili-Fanrenpc/actions/runs/18739846288/job/53453705577>

```plain
  # matplotlib中文乱码，需要安装字体包
  apt-get install -y fonts-wqy-microhei
  python3 -m pip install --upgrade pip setuptools wheel
  python3 -m pip install -r requirements.txt
  shell: /usr/bin/bash -e {0}
  env:
    pythonLocation: /opt/hostedtoolcache/Python/3.8.18/x64
    PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.8.18/x64/lib/pkgconfig
    Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.8.18/x64
    Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.8.18/x64
    Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.8.18/x64
    LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.8.18/x64/lib
E: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
E: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?
Error: Process completed with exit code 100.
```

### 3.CI问题：git status 中文乱码

<https://github.com/yansheng836/bilibili-Fanrenpc/actions/runs/18737555742/job/53447278813>

git status中文乱码，需要配置环境`git config --global core.quotepath false`。

```plain
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   "B\347\253\231\343\200\212\345\207\241\344\272\272\344\277\256\344\273\231\344\274\240\343\200\213\345\212\250\346\274\253\346\200\273\346\225\260\346\215\256\347\273\237\350\256\241.md"
	modified:   README.md
	modified:   bilibili_episodes.json
	modified:   bilibili_episodes_infos.json
	modified:   "images/\345\210\206\344\272\253\346\225\260TOP10.png"
	modified:   "images/\345\274\271\345\271\225\346\225\260TOP10.png"
	modified:   "images/\346\212\225\345\270\201\346\225\260TOP10.png"
	modified:   "images/\346\222\255\346\224\276\351\207\217TOP10.png"
	modified:   "images/\346\224\266\350\227\217\346\225\260TOP10.png"
	modified:   "images/\347\202\271\350\265\236\346\225\260TOP10.png"
	modified:   "images/\350\257\204\350\256\272\346\225\260TOP10.png"
```

## 统计逻辑

### 总数据统计

| 集数 |        名称         |    播放量 | 点赞数 | 投币数 | 收藏数 | 弹幕数 | 分享数 | 评论数 |
| :--: | :-----------------: | --------: | :----: | -----: | -----: | -----: | -----: | -----: |
|  1   | 凡人风起天南1重制版 | 145668244 | 486504 |        |        |        |        |        |
|  2   | 凡人风起天南2重制版 |  28146733 | 143472 |        |        |        |        |        |
|  ……  |         ……          |           |        |        |        |        |        |        |
| 汇总 |                     |           |        |        |        |        |        |        |

### 播放量TOP10

### 点赞数TOP10

### 投币数TOP10

### 收藏数TOP10

### 弹幕数TOP10

### 分享数TOP10

### 评论数TOP10
