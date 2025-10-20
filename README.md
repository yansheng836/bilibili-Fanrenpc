# B站《凡人修仙传》数据统计

B站《凡人修仙传》数据统计。

## 相关信息

https://www.bilibili.com/bangumi/media/md28223043#detail

## 爬取相关逻辑

### 爬取集数列表

https://www.bilibili.com/bangumi/media/md28223043#detail

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

https://www.bilibili.com/bangumi/play/ep1231573?from_spmid=666.19.0.0

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

