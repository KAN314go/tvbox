# -*- coding: utf-8 -*-
# @Author  : Adapted for 華視頻
# @Time    : 2025/04/05

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
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://hlove.tv/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
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
        movie_classes = "全部$all#剧情$juqing#喜剧$xiju#动作$dongzuo#惊悚$jingsong#爱情$aiqing#恐怖$kongbu#犯罪$fanzui#冒险$maoxian#奇幻$qihuan#悬疑$xuanyi#科幻$kehuan#家庭$jiating#动画$donghua#历史$lishi#战争$zhanzheng#音乐$yinle#动漫$dongman#电视电影$dianshidianying#西部$xibu#网络电影$wangluodianying#纪录$jilu#同性$tongxing#歌舞$gewu#灾难$zainan#动作冒险$dongzuomaoxian#战争政治$zhanzhengzhengzhi"
        movie_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        movie_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 電視劇篩選條件
        drama_classes = "全部$all#国产剧$guocanju#韩剧$hanju#欧美剧$oumeiju#港台剧$gangtaiju#英剧$yingju#新马泰$xinmata#剧情$juqing#喜剧$xiju#悬疑$xuanyi#犯罪$fanzui#科幻&奇幻$kehuanqihuan#动作冒险$dongzuomaoxian#动作&冒险$dongzuojiemaoxian#家庭$jiating#战争&政治$zhanzhengzhengzhi#爱情$aiqing#肥皂剧$feizaoju#短剧$duanju#同性$tongxing#西部$xibu#儿童$ertong#真人秀$zhenrenxiu#动画$donghua#惊悚$jingsong#脱口秀$tuokouxiu#动作$dongzuo#罪案$zuian#古装$guzhuang#都市$dushi#奇幻$qihuan#科幻$kehuan#历史$lishi#青春$qinchun#新闻$xinwen#穿越$chuanyue#军旅$junlv#歌舞$gewu#玄幻$xuanhuan#纪录$jilu#言情$yanqing#警匪$jingfei#音乐剧$yinleju#商战$shangzhan#武侠$wuxia#电视电影$dianshidianying"
        drama_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#其他地区$others"
        drama_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2015$2015#2014-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 綜藝篩選條件
        variety_classes = "全部$all#真人秀$zhenrenxiu#喜剧$xiju#脱口秀$tuokouxiu#家庭$jiating#剧情$juqing#动作冒险$dongzuomaoxian#悬疑$xuanyi#动作&冒险$dongzuojiemaoxian#犯罪$fanzui#儿童$ertong#晚会$wanhui#音乐$yinle#动画$donghua#纪录$jilu#纪录片$jilupian"
        variety_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        variety_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2015$2015#2014-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 動漫篩選條件
        animation_classes = "全部$all#动画$donghua#喜剧$xiju#科幻&奇幻$kehuanqihuan#动作冒险$dongzuomaoxian#动作&冒险$dongzuojiemaoxian#剧情$juqing#悬疑$xuanyi#家庭$jiating#魔幻$mohuan#热血$rexue#犯罪$fanzui#战争&政治$zhanzhengzhengzhi#冒险$maoxian#剧场版$juchangban#其它$qita#恋爱$lianai#科幻$kehuan#爆笑$baoxiao#儿童$ertong#校园$xiaoyuan#竞技$jingji#少女$shaonv#爱情$aiqing#泡面$paomian#西部$xibu#穿越$chuanyue#格斗$gedou#治愈$zhiyu#机战$jizhan#推理$tuili#耽美$danmei#肥皂剧$feizaoju"
        animation_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        animation_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2015$2015#2014-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"

        # 兒童篩選條件
        children_classes = "全部$all#儿童$ertong#动画$donghua#喜剧$xiju#动作冒险$dongzuomaoxian#科幻&奇幻$kehuanqihuan#家庭$jiating#动作&冒险$dongzuojiemaoxian#剧情$juqing#悬疑$xuanyi#犯罪$fanzui#冒险$maoxian#科幻$kehuan#动作$dongzuo#动漫$dongman#历史$lishi#奇幻$qihuan"
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
        url = f"{self.home_url}/{cid}/{_year}/{_class}/{_area}"
        if page != '1':
            url += f"?page={page}"
        
        d = []
        try:
            res = self.session.get(url, headers=self.headers, timeout=20)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "h-film-listall_cardList___IXsY")]/a')
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            total = 0
            init_cards = []
            if next_data:
                next_json = json.loads(next_data.group(1))
                init_cards = next_json['props']['pageProps'].get('initCard', [])
                total = next_json['props']['pageProps'].get('total', len(data_list))
            
            for i, card in enumerate(data_list):
                vod_name = card.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                vod_id = card.get('href', '')
                vod_pic_list = card.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')
                vod_pic = vod_pic_list[0] if vod_pic_list else None
                if not vod_pic or vod_pic == '/api/images/init':
                    vod_pic = init_cards[i]['img'] if i < len(init_cards) and 'img' in init_cards[i] else self.default_pic
                vod_remarks = init_cards[i]['countStr'] if i < len(init_cards) and 'countStr' in init_cards[i] else ''
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            
            pagecount = (total + 23) // 24 if total > 0 else 999
            return {'list': d, 'page': int(page), 'pagecount': pagecount, 'limit': 24, 'total': total}
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {'list': d, 'page': int(page), 'pagecount': 999, 'limit': 24, 'total': 0}

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
            for group in collection_info.get('videosGroup', []):
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
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "h-film-listall_cardList___IXsY")]/a')
            
            result = []
            for item in data_list:
                vod_name = item.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                vod_id = item.get('href', '')
                vod_pic = item.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')[0] if item.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src') else self.default_pic
                if vod_pic == '/api/images/init':
                    vod_pic = self.default_pic
                result.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': ''
                })
            return {'list': result}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': []}

    def playerContent(self, flag, pid, vipFlags):
        try:
            play_url = pid
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
        
        play_from = vod['vod_play_from'].split('$$$')
        play_url = vod['vod_play_url'].split('$$$')
        lines = list(zip(play_from, play_url))
        sorted_lines = sorted(lines, key=lambda x: x[0] != 'heimuer')
        
        selected_play_url = sorted_lines[0][1].split('#')[0].split('$')[1] if sorted_lines else ''
        
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
                <source src="{selected_play_url}" type="application/x-mpegURL">
                您的瀏覽器不支持視頻播放。
            </video>
            <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            <script>
                var video = document.querySelector('video');
                var videoSrc = '{selected_play_url}';
                if (Hls.isSupported()) {{
                    var hls = new Hls();
                    hls.loadSource(videoSrc);
                    hls.attachMedia(video);
                }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                    video.src = videoSrc;
                }}
            </script>
        </body>
        </html>
        """
        return html

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

if __name__ == "__main__":
    spider = Spider()
    # 測試主頁
    result = spider.homeVideoContent()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # 測試詳情頁
    result = spider.detailContent(["/vod/detail/se4pnjL1IF6D"])
    print(json.dumps(result, ensure_ascii=False, indent=2))