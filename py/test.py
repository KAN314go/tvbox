# -*- coding: utf-8 -*-
# @Author  : 老王叔叔 for 華視頻
# @Time    : 2025/04/06

import sys
import requests
from lxml import etree
import re
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        self.home_url = 'https://hlove.tv'
        self.api_url = "https://app.ymedium.top/v3/web/api/filter"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://hlove.tv/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Sec-Ch-Ua": '"Chromium";v="134", "Not-A.Brand";v="24", "Google Chrome";v="134"'
        }
        self.default_pic = 'https://hlove.tv/api/images/default'
        # 配置帶重試的會話
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def init(self, extend):
        pass

    def getName(self):
        return "華視界"

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        categories = "电影$movie#电视剧$drama#动漫$animation#综艺$variety#儿童$children"
        class_list = [{'type_id': v.split('$')[1], 'type_name': v.split('$')[0]} for v in categories.split('#')]

        # 電影篩選條件
        movie_classes = "全部$all#剧情$juqing#喜剧$xiju#动作$dongzuo#惊悚$jingsong#爱情$aiqing#恐怖$kongbu#犯罪$fanzui#冒险$maoxian#奇幻$qihuan#悬疑$xuanyi#科幻$kehuan#家庭$jiating#动画$donghua#历史$lishi#战争$zhanzheng#音乐$yinyue#动漫$dongman#电视电影$dianshidianying#西部$xibu#网络电影$wangluodianying#纪录$jilu#同性$tongxing#歌舞$gewu#灾难$zainan#动作冒险$dongzuomaoxian#战争政治$zhanzhengzhengzhi"
        movie_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        movie_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 電視劇篩選條件
        drama_classes = "全部$all#国产剧$guochanju#韩剧$hanju#欧美剧$oumeiju#港台剧$gangtaiju#英剧$yingju#新马泰$xinmataiju#剧情$juqing#喜剧$xiju#悬疑$xuanyi#犯罪$fanzui#科幻&奇幻$kehuanqihuan#动作冒险$dongzuomaoxian#动作&冒险$dongzuoandmaoxian#家庭$jiating#战争&政治$zhanzhengandzhengzhi#爱情$aiqing#肥皂剧$feizaoju#短剧$duanju#同性$tongxing#西部$xibu#儿童$ertong#真人秀$zhenshixiu#动画$donghua#惊悚$jingsong#脱口秀$tuokouxiu#动作$dongzuo#罪案$zuian#古装$guzhuang#都市$dushi#奇幻$qihuan#科幻$kehuan#历史$lishi#青春$qingchun#新闻$xinwen#穿越$chuanyue#军旅$junlv#歌舞$gewu#玄幻$xuanhuan#纪录$jilu#言情$yanqing#警匪$jingfei#音乐剧$yinyueju#商战$shangzhan#武侠$wuxia#电视电影$dianshidianying"
        drama_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#其他地区$others"
        drama_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2015$2015#2014-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 綜藝篩選條件
        variety_classes = "全部$all#真人秀$zhenshixiu#喜剧$xiju#脱口秀$tuokouxiu#家庭$jiating#剧情$juqing#动作冒险$dongzuomaoxian#悬疑$xuanyi#动作&冒险$dongzuoandmaoxian#犯罪$fanzui#儿童$ertong#晚会$wanhui#音乐$yinyue#动画$donghua#纪录$jilu#纪录片$jilupian"
        variety_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        variety_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2015$2015#2014-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 動漫篩選條件
        animation_classes = "全部$all#动画$donghua#喜剧$xiju#科幻&奇幻$kehuanqihuan#动作冒险$dongzuomaoxian#动作&冒险$dongzuoandmaoxian#剧情$juqing#悬疑$xuanyi#家庭$jiating#魔幻$mohuan#热血$rexue#犯罪$fanzui#战争&政治$zhanzhengandzhengzhi#冒险$maoxian#剧场版$juchangban#其它$qita#恋爱$lianaiju#科幻$kehuan#爆笑$baoxiao#儿童$ertong#校园$xiaoyuan#竞技$jingji#少女$shaonv#爱情$aiqing#泡面$paomian#西部$xibu#穿越$chuanyue#格斗$gedou#治愈$zhiyu#机战$jizhan#推理$tuili#耽美$danmei#肥皂剧$feizaoju"
        animation_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        animation_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2015$2015#2014-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 兒童篩選條件
        children_classes = "全部$all#儿童$ertong#动画$donghua#喜剧$xiju#动作冒险$dongzuomaoxian#科幻&奇幻$kehuanqihuan#家庭$jiating#动作&冒险$dongzuoandmaoxian#剧情$juqing#悬疑$xuanyi#犯罪$fanzui#冒险$maoxian#科幻$kehuan#动作$dongzuo#动漫$dongman#历史$lishi#奇幻$qihuan"
        children_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        children_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2015$2015#2014-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        filters = {
            'movie': [
                {'name': '分类', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in movie_classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in movie_areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in movie_years.split('#')]}
            ],
            'drama': [
                {'name': '分类', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in drama_classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in drama_areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in drama_years.split('#')]}
            ],
            'animation': [
                {'name': '分类', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in animation_classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in animation_areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in animation_years.split('#')]}
            ],
            'variety': [
                {'name': '分类', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in variety_classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in variety_areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in variety_years.split('#')]}
            ],
            'children': [
                {'name': '类型', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in children_classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in children_areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in children_years.split('#')]}
            ]
        }
        return {'class': class_list, 'filters': filters}

    def homeVideoContent(self):
        d = []
        try:
            # 增加超時時間並使用帶重試的會話
            res = self.session.get(self.home_url, headers=self.headers, timeout=20)
            res.encoding = 'utf-8'
            html_text = res.text

            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html_text)
            if not next_data:
                print("未找到 __NEXT_DATA__")
                return {'list': [], 'parse': 0, 'jx': 0}

            next_json = json.loads(next_data.group(1))
            cards = next_json['props']['pageProps'].get('cards', [])
            print(f"找到 {len(cards)} 個分類區塊")

            for section in cards:
                section_title = section.get('name', '未知分類')
                section_cards = section.get('cards', [])
                for card in section_cards:
                    vod_id = card.get('id', '')
                    vod_name = card.get('name', '')
                    vod_pic = card.get('img', '')
                    vod_remarks = card.get('countStr', section_title)

                    if not vod_id or not vod_name:
                        continue

                    vod_path = f"/vod/detail/{vod_id}"

                    if not vod_pic or vod_pic == '/api/images/init':
                        vod_pic = self.default_pic

                    d.append({
                        'vod_id': vod_path,
                        'vod_name': vod_name,
                        'vod_pic': vod_pic,
                        'vod_remarks': vod_remarks
                    })

            # 簡化去重，直接返回列表
            print(f"最終返回 {len(d)} 個影片")
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def infer_category(self, section_title):
        category_mapping = {
            '電影': 'movie',
            '电视剧': 'drama',
            '动漫': 'animation',
            '综艺': 'variety',
            '儿童': 'children'
        }
        for key, value in category_mapping.items():
            if key in section_title:
                return value
        return 'movie'

    def categoryContent(self, cid, page, filter, ext):
        _year = ext.get('year', 'all')
        _class = ext.get('class', 'all')
        _area = ext.get('area', 'all')
        
        # 映射字段值為中文
        chName_map = {
            "movie": "电影",
            "drama": "电视剧",
            "animation": "动漫",
            "variety": "综艺",
            "children": "动画片"
        }

        # 劇情分類映射
        label_map = {
            # 通用分類
            "juqing": "剧情",
            "xiju": "喜剧",
            "dongzuo": "动作",
            "jingsong": "惊悚",
            "aiqing": "爱情",
            "kongbu": "恐怖",
            "fanzui": "犯罪",
            "maoxian": "冒险",
            "qihuan": "奇幻",
            "xuanyi": "悬疑",
            "kehuan": "科幻",
            "jiating": "家庭",
            "donghua": "动画",
            "lishi": "历史",
            "zhanzheng": "战争",
            "yinyue": "音乐",
            "dongman": "动漫",
            "dianshidianying": "电视电影",
            "xibu": "西部",
            "wangluodianying": "网络电影",
            "jilu": "纪录",
            "tongxing": "同性",
            "gewu": "歌舞",
            "zainan": "灾难",
            "dongzuomaoxian": "动作冒险",
            "dongzuoandmaoxian": "动作&冒险",
            "zhanzhengandzhengzhi": "战争&政治",
            # 電視劇特有
            "feizaoju": "肥皂剧",
            "duanju": "短剧",
            "ertong": "儿童",
            "zhenshixiu": "真人秀",
            "tuokouxiu": "脱口秀",
            "zuian": "罪案",
            "guzhuang": "古装",
            "oumeiju": "欧美剧",
            "dushi": "都市",
            "yingju": "英剧",
            "gangtaiju": "港台剧",
            "qingchun": "青春",
            "hanju": "韩剧",
            "xinwen": "新闻",
            "chuanyue": "穿越",
            "junlv": "军旅",
            "xuanhuan": "玄幻",
            "jilu": "纪录",
            "yanqing": "言情",
            "jingfei": "警匪",
            "yinyueju": "音乐剧",
            "shangzhan": "商战",
            "guochanju": "国产剧",
            "xinmataiju": "新马泰",
            "wuxia": "武侠",
            # 綜藝特有
            "wanhui": "晚会",
            "jilupian": "纪录片",
            # 動漫特有
            "mohuan": "魔幻",
            "rexue": "热血",
            "lianaiju": "恋爱",
            "baoxiao": "爆笑",
            "xiaoyuan": "校园",
            "jingji": "竞技",
            "shaonv": "少女",
            "paomian": "泡面",
            "gedou": "格斗",
            "zhiyu": "治愈",
            "jizhan": "机战",
            "tuili": "推理",
            "danmei": "耽美",
            "juchangban": "剧场版",
            "qita": "其它"
        }

        # 地區分類映射
        country_map = {
            "cn": "中国大陆",
            "us": "美国",
            "kr": "韩国",
            "hk": "香港",
            "tw": "台湾",
            "jp": "日本",
            "gb": "英国",
            "th": "泰国",
            "sp": "西班牙",
            "ca": "加拿大",
            "fr": "法国",
            "in": "印度",
            "au": "澳大利亚",
            "others": "其他地区"
        }
        
        # 設置請求體
        pageSize = 12 if cid == "children" else 24
        payload = {
            "chName": chName_map.get(cid, "电影"),
            "startTime": int(_year) if _year != 'all' and _year.isdigit() else 0,
            "endTime": int(_year) if _year != 'all' and _year.isdigit() else 0,
            "label": label_map.get(_class, _class) if _class != 'all' else "",
            "country": country_map.get(_area, _area) if _area != 'all' else "",
            "pageSize": pageSize,
            "page": int(page)
        }
        
        d = []
        try:
            print(f"Requesting API: {self.api_url} with payload {json.dumps(payload, ensure_ascii=False)}")
            res = self.session.post(self.api_url, headers=self.headers, json=payload, timeout=20)
            res.raise_for_status()
            data = res.json()
            
            # 打印原始響應以便調試
            print(f"API Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 檢查響應狀態
            if data.get('code') != 0:
                raise Exception(f"API error: code={data.get('code')}, message={data.get('message', 'Unknown error')}")
            
            # 檢查數據結構
            if 'data' not in data:
                raise Exception("Invalid API response: 'data' field missing")
            
            # 提取數據
            total = data['data'].get('total', 0)
            items = data['data'].get('list', [])
            
            for item in items:
                vod_id = f"/vod/detail/{item.get('id', '')}"
                vod_name = item.get('name', '')
                vod_pic = item.get('img', self.default_pic)
                if not vod_pic or vod_pic.startswith('/api/images/init'):
                    vod_pic = self.default_pic
                
                # 處理 countStr，截斷過長的更新信息，並處理 "更新至0集"
                vod_remarks = item.get('countStr', '')
                if vod_remarks == "更新至0集":
                    vod_remarks = "尚未更新"
                elif vod_remarks and len(vod_remarks) > 15:
                    vod_remarks = vod_remarks[:15] + "..."
                
                if not vod_id or not vod_name:
                    continue
                    
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            
            # 調整 pagecount 計算邏輯
            pagecount = (total + pageSize - 1) // pageSize if total > 0 else 0
            return {
                'list': d,
                'page': int(page),
                'pagecount': pagecount,
                'limit': pageSize,
                'total': total
            }
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {
                'list': d,
                'page': int(page),
                'pagecount': 0,
                'limit': pageSize,
                'total': 0
            }

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        if not ids.startswith('/vod/detail/'):
            ids = f"/vod/detail/{ids.lstrip('/')}"
        detail_url = f"{self.home_url}{ids}"
        print(f"請求的 detail_url: {detail_url}")
        try:
            res = self.session.get(detail_url, headers=self.headers, timeout=20)
            print(f"HTTP 狀態碼: {res.status_code}")
            if res.status_code != 200:
                print(f"頁面不存在，URL: {detail_url}")
                return {'list': [], 'msg': f'頁面不存在 (狀態碼: {res.status_code})'}

            res.encoding = 'utf-8'
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            
            if not next_data:
                print(f"未找到 __NEXT_DATA__，URL: {detail_url}, 響應片段: {res.text[:200]}")
                return {'list': [], 'msg': '未找到影片數據'}

            next_json = json.loads(next_data.group(1))
            page_props = next_json.get('props', {}).get('pageProps', {})
            if 'collectionInfo' not in page_props:
                print(f"collectionInfo 未找到，URL: {detail_url}, pageProps: {json.dumps(page_props, ensure_ascii=False)}")
                return {'list': [], 'msg': '影片數據缺少 collectionInfo'}

            collection_info = page_props['collectionInfo']
            print(f"collectionInfo: {json.dumps(collection_info, ensure_ascii=False, indent=2)}")
            
            vod_name = collection_info.get('name', '')
            vod_year = collection_info.get('time', '')
            vod_area = collection_info.get('country', '')
            vod_content = collection_info.get('desc', '')
            vod_remarks = collection_info.get('countStr', '')
            vod_actor = ', '.join([actor['name'] for actor in collection_info.get('actor', [])])
            vod_director = ', '.join([director['name'] for director in collection_info.get('director', [])])
            vod_pic = collection_info.get('imgUrl', self.default_pic)
            is_movie = collection_info.get('isMovie', False)
            
            play_from = []
            play_url = []
            videos_group = collection_info.get('videosGroup', [])
            if not videos_group:
                print(f"videosGroup 為空，URL: {detail_url}")
                # 嘗試從其他字段中提取播放 URL（如果有）
                fallback_url = collection_info.get('url', '')  # 假設有 url 字段
                if fallback_url:
                    play_from.append('備用線路')
                    play_url.append(f"{vod_name}${fallback_url}")
                else:
                    return {
                        'list': [{
                            'vod_id': ids,
                            'vod_name': vod_name,
                            'vod_pic': vod_pic,
                            'vod_remarks': vod_remarks,
                            'vod_year': vod_year,
                            'vod_area': vod_area,
                            'vod_actor': vod_actor,
                            'vod_director': vod_director,
                            'vod_content': vod_content,
                            'vod_play_from': '',
                            'vod_play_url': ''
                        }],
                        'msg': '無可用播放線路'
                    }

            for group in videos_group:
                if not group.get('videos'):
                    continue
                line_name = group.get('name', '线路1')
                if is_movie:
                    video = group['videos'][0]
                    play_from.append(line_name)
                    play_url.append(f"{vod_name}${video['purl']}")
                else:
                    episodes = []
                    for video in group['videos']:
                        ep_name = f"第{video['eporder']}集"
                        ep_url = video['purl']
                        episodes.append(f"{ep_name}${ep_url}")
                    play_from.append(line_name)
                    play_url.append('#'.join(episodes))
            
            video_list.append({
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_pic': vod_pic,
                'vod_remarks': vod_remarks,
                'vod_year': vod_year,
                'vod_area': vod_area,
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_play_from': '$$$'.join(play_from),
                'vod_play_url': '$$$'.join(play_url)
            })
            print(f"成功解析影片: {vod_name}, URL: {detail_url}")
            return {"list": video_list}
        except Exception as e:
            print(f"Error in detailContent: {str(e)}, URL: {detail_url}")
            return {'list': [], 'msg': f'解析錯誤: {str(e)}'}

    def searchContent(self, key, quick):
        try:
            search_url = f"{self.home_url}/search?q={key}"
            res = self.session.get(search_url, headers=self.headers, timeout=20)
            res.encoding = 'utf-8'
            print(f"搜索 URL: {search_url}, 響應片段: {res.text[:200]}")
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "h-film-listall_cardList___IXsY")]/a')
            
            result = []
            for item in data_list:
                vod_name = item.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')
                vod_name = vod_name[0].strip() if vod_name else ''
                vod_id = item.get('href', '')
                vod_pic = item.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')
                vod_pic = vod_pic[0] if vod_pic else self.default_pic
                if vod_pic == '/api/images/init':
                    vod_pic = self.default_pic
                if vod_name and vod_id:
                    result.append({
                        'vod_id': vod_id,
                        'vod_name': vod_name,
                        'vod_pic': vod_pic,
                        'vod_remarks': ''
                    })
            print(f"搜索結果: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return {'list': result}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': []}

    def playerContent(self, flag, pid, vipFlags):
        try:
            play_url = pid.split('$')[1]  # 從 pid 中提取播放 URL
            headers = self.headers.copy()
            headers['Referer'] = 'https://hlove.tv/'  # 添加 Referer 以確保播放鏈接有效
            return {
                'url': play_url,
                'header': json.dumps(headers),
                'parse': 0,
                'jx': 0
            }
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': '', 'parse': 0, 'jx': 0}

    def generate_children_html(self, vod_id):
        detail = self.detailContent([vod_id])
        if not detail['list']:
            return "<h1>無法加載內容</h1>"
        
        vod = detail['list'][0]
        vod_name = vod['vod_name']
        
        # 檢查是否有播放線路
        if not vod['vod_play_from'] or not vod['vod_play_url']:
            return f"<h1>{vod_name} - 無可用播放線路</h1>"
        
        play_from = vod['vod_play_from'].split('$$$')
        play_url = vod['vod_play_url'].split('$$$')
        lines = list(zip(play_from, play_url))
        sorted_lines = sorted(lines, key=lambda x: x[0] != 'heimuer')
        
        # 確保 sorted_lines 不為空
        if not sorted_lines:
            return f"<h1>{vod_name} - 無可用播放線路</h1>"
        
        selected_play_url = sorted_lines[0][1].split('#')[0].split('$')[1] if sorted_lines else ''
        
        # 檢查播放 URL 是否為 HLS 格式
        is_hls = selected_play_url.endswith('.m3u8')
        
        html = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{vod_name} - 兒童播放</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f8ff; text-align: center; }}
                h1 {{ color: #ff4500; }}
                video {{ width: 100%; max-width: 600px; margin: 20px auto; }}
            </style>
        </head>
        <body>
            <h1>{vod_name}</h1>
            <video controls controlsList="nodownload" oncontextmenu="return false;">
                <source src="{selected_play_url}" type="{ 'application/x-mpegURL' if is_hls else 'video/mp4' }">
                您的瀏覽器不支持視頻播放。
            </video>
            {'<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>' if is_hls else ''}
            <script>
                var video = document.querySelector('video');
                var videoSrc = '{selected_play_url}';
                {'if (Hls.isSupported()) { var hls = new Hls(); hls.loadSource(videoSrc); hls.attachMedia(video); } else if (video.canPlayType("application/vnd.apple.mpegurl")) { video.src = videoSrc; }' if is_hls else 'video.src = videoSrc;'}
            </script>
        </body>
        </html>
        """
        return html

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

# 測試代碼
if __name__ == "__main__":
    spider = Spider()
    # 測試 homeContent
    print("=== 測試 homeContent ===")
    result = spider.homeContent(True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試 homeVideoContent
    print("\n=== 測試 homeVideoContent ===")
    result = spider.homeVideoContent()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試 categoryContent（兒童）
    print("\n=== 測試 categoryContent（儿童，中國大陸，無年份限制） ===")
    result = spider.categoryContent("children", "1", True, {"class": "ertong", "area": "cn"})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試 detailContent（使用其他 vod_id）
    print("\n=== 測試 detailContent（故宫里的大怪兽） ===")
    result = spider.detailContent(["/vod/detail/LX89vyQfIj"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試 searchContent
    print("\n=== 測試 searchContent ===")
    result = spider.searchContent("猪猪侠", True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試 playerContent
    print("\n=== 測試 playerContent ===")
    result = spider.playerContent("线路1", "猪猪侠$https://example.com/video.m3u8", [])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試 generate_children_html（使用其他 vod_id）
    print("\n=== 測試 generate_children_html（故宫里的大怪兽） ===")
    result = spider.generate_children_html("/vod/detail/LX89vyQfIj")
    print(result)