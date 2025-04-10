# -*- coding: utf-8 -*-
import re
import sys
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import unpad
sys.path.append("..")
import json
import time
from pyquery import PyQuery as pq
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        self.host = 'https://www.xiaohys.com'
        self.api_url = 'https://www.xiaohys.com/index.php/api/vod'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': self.host,
            'Referer': f"{self.host}/",
        }

    def init(self, extend=""):
        pass

    def destroy(self):
        pass

    def isVideoFormat(self, url):
        return False

    def manualVideoCheck(self):
        return False

    def localProxy(self, param):
        return None

    def getName(self):
        return "XiaoHYS"

    def homeContent(self, filter):
        data = self.getpq(self.fetch(self.host, headers=self.headers).text)
        print(f"Home HTML length: {len(data.text())}")
        result = {}
        classes = [
            {"type_id": "movie", "type_name": "电影"},
            {"type_id": "tv", "type_name": "电视剧"},
            {"type_id": "variety", "type_name": "综艺"},
            {"type_id": "anime", "type_name": "动漫"}
        ]
        filters = {
            "movie": [
                {"key": "class", "name": "類型", "value": [
                    {"n": "全部", "v": ""}, {"n": "喜剧", "v": "喜剧"}, {"n": "爱情", "v": "爱情"}, {"n": "恐怖", "v": "恐怖"},
                    {"n": "动作", "v": "动作"}, {"n": "科幻", "v": "科幻"}, {"n": "剧情", "v": "剧情"}, {"n": "战争", "v": "战争"}
                ]},
                {"key": "area", "name": "地區", "value": [
                    {"n": "全部", "v": ""}, {"n": "大陆", "v": "大陆"}, {"n": "香港", "v": "香港"}, {"n": "台湾", "v": "台湾"},
                    {"n": "美国", "v": "美国"}, {"n": "日本", "v": "日本"}, {"n": "韩国", "v": "韩国"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"}
                ]},
                {"key": "lang", "name": "語言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"}
                ]},
                {"key": "by", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}
                ]}
            ],
            "tv": [
                {"key": "class", "name": "類型", "value": [
                    {"n": "全部", "v": ""}, {"n": "古装", "v": "古装"}, {"n": "战争", "v": "战争"}, {"n": "青春偶像", "v": "青春偶像"}
                ]},
                {"key": "area", "name": "地區", "value": [
                    {"n": "全部", "v": ""}, {"n": "内地", "v": "内地"}, {"n": "韩国", "v": "韩国"}, {"n": "香港", "v": "香港"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"}
                ]},
                {"key": "lang", "name": "語言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}
                ]},
                {"key": "by", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}
                ]}
            ]
        }
        result['class'] = classes
        result['filters'] = filters if filter else {}
        video_list = self.getlist(data('.border-box.diy-center .public-list-div'))
        print(f"Home videos found: {len(video_list)}")
        result['list'] = video_list
        return result

    def homeVideoContent(self):
        data = self.getpq(self.fetch(self.host, headers=self.headers).text)
        video_list = self.getlist(data('.border-box.diy-center .public-list-div'))
        print(f"HomeVideoContent videos found: {len(video_list)}")
        return {"list": video_list}

    def categoryContent(self, tid, pg, filter, extend):
        t = int(time.time())
        key = MD5.new(f"DS{t}DCC147D11943AF75".encode('utf-8')).hexdigest()
        type_map = {"movie": "1", "tv": "2", "variety": "3", "anime": "4"}
        body = {
            'ac': 'videolist',
            't': type_map.get(tid, tid),
            'class': extend.get('class', ''),
            'area': extend.get('area', ''),
            'year': extend.get('year', ''),
            'lang': extend.get('lang', ''),
            'by': extend.get('by', 'time'),
            'pg': str(pg),
            'time': str(t),
            'key': key
        }
        print(f"Category request params: {json.dumps(body, ensure_ascii=False)}")
        try:
            response = self.post(self.api_url, headers=self.headers, data=body)
            print(f"Raw API response: {response.text}")
            data = response.json()
            print(f"Category API response: {json.dumps(data, ensure_ascii=False)}")
            
            # 本地過濾：根據 tid 和 vod_class
            filtered_list = []
            type_classes = {
                "movie": ["电影"],
                "tv": ["国产", "剧"],  # 電視劇可能包含 "国产" 或 "剧"
                "variety": ["综艺"],
                "anime": ["动漫", "动画"]
            }
            expected_classes = type_classes.get(tid, [])
            for item in data.get('list', []):
                vod_class = item.get('vod_class', '')
                # 如果 vod_class 包含預期類型，則保留
                if any(cls in vod_class for cls in expected_classes) or not vod_class:
                    filtered_list.append({
                        'vod_id': item.get('vod_id'),
                        'vod_name': item.get('vod_name', '未知'),
                        'vod_pic': item.get('vod_pic', ''),
                        'vod_remarks': item.get('vod_remarks', '')
                    })
            
            result = {
                'list': filtered_list,
                'page': int(data.get('page', pg)),
                'pagecount': data.get('pagecount', 9999),
                'limit': int(data.get('limit', 20)),
                'total': data.get('total', len(filtered_list)) if filtered_list else 0
            }
            print(f"Filtered list size: {len(filtered_list)}")
        except Exception as e:
            print(f"Category error: {e}")
            result = {'list': [], 'page': int(pg), 'pagecount': 9999, 'limit': 20, 'total': 0}
        return result

    def detailContent(self, ids):
        data = self.getpq(self.fetch(f"{self.host}/detail/{ids[0]}/", headers=self.headers).text)
        v = data('.detail-info.lightSpeedIn .slide-info')
        vod = {
            'vod_year': v.eq(-1).text(),
            'vod_remarks': v.eq(0).text(),
            'vod_actor': v.eq(3).text(),
            'vod_director': v.eq(2).text(),
            'vod_content': data('.switch-box #height_limit').text()
        }
        np = data('.anthology.wow.fadeInUp')
        ndata = np('.anthology-tab .swiper-wrapper .swiper-slide')
        pdata = np('.anthology-list .anthology-list-box ul')
        play, names = [], []
        for i in range(len(ndata)):
            n = ndata.eq(i)('a')
            n('span').remove()
            names.append(n.text())
            vs = []
            for v in pdata.eq(i)('li').items():
                vs.append(f"{v.text()}${self.host}{v('a').attr('href')}")
            play.append('#'.join(vs))
        vod["vod_play_from"] = "$$$".join(names)
        vod["vod_play_url"] = "$$$".join(play)
        return {"list": [vod]}

    def searchContent(self, key, quick, pg="1"):
        data = self.fetch(f"{self.host}/index.php/ajax/suggest?mid=1&wd={key}&limit=9999×tamp={int(time.time()*1000)}", headers=self.headers).json()
        videos = [{
            'vod_id': i['id'],
            'vod_name': i['name'],
            'vod_pic': i['pic']
        } for i in data['list']]
        return {'list': videos, 'page': pg}

    def playerContent(self, flag, id, vipFlags):
        h = {"User-Agent": "okhttp/3.14.9"}
        url = id if id.startswith('http') else f"{self.host}{id}"
        data = self.getpq(self.fetch(url, headers=self.headers).text)
        try:
            jstr = data('.player .player-left script').eq(0).text()
            jsdata = json.loads(jstr.split('=', 1)[-1])
            body = {'url': jsdata['url'], 'referer': url}
            data = self.post(f"{self.host}/static/player/artplayer/api.php?ac=getdate", headers=self.headers, data=body).json()
            l = self.aes(data['data'], data['iv'])
            url = l.get('url') or l['data'].get('url')
            parse = 0 if url else 1
        except Exception as e:
            print(f"Player error: {e}")
            url = id
            parse = 1
        return {"parse": parse, "url": url, "header": h}

    def getlist(self, data):
        videos = []
        for i in data.items():
            id = i('a').attr('href')
            if id:
                id = re.search(r'\d+', id).group(0)
                img = i('img').attr('data-src')
                if img and 'url=' in img and 'http' not in img:
                    img = f'{self.host}{img}'
                videos.append({
                    'vod_id': id,
                    'vod_name': i('img').attr('alt') or "未知",
                    'vod_pic': img or "",
                    'vod_remarks': i('.public-prt').text() or i('.public-list-prb').text() or ""
                })
        return videos[:10]

    def getpq(self, data):
        try:
            return pq(data)
        except Exception as e:
            print(f"Parse error: {e}")
            return pq(data.encode('utf-8'))

    def aes(self, text, iv):
        key = b"d978a93ffb4d3a00"
        iv = iv.encode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(b64decode(text)), AES.block_size)
        return json.loads(pt.decode("utf-8"))

if __name__ == "__main__":
    spider = Spider()
    print(json.dumps(spider.homeContent(filter=True), ensure_ascii=False))
    print(json.dumps(spider.homeVideoContent(), ensure_ascii=False))
    print("測試電視劇篩選:")
    print(json.dumps(spider.categoryContent("tv", "1", True, {"class": "古装", "area": "内地", "year": "2024", "lang": "国语", "by": "score"}), ensure_ascii=False))
    print("測試僅類型篩選:")
    print(json.dumps(spider.categoryContent("tv", "1", True, {"class": "古装"}), ensure_ascii=False))
    print("測試無篩選條件:")
    print(json.dumps(spider.categoryContent("tv", "1", True, {}), ensure_ascii=False))
    print(json.dumps(spider.detailContent(["49751"]), ensure_ascii=False))