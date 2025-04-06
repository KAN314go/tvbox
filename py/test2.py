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
from urllib.parse import urljoin
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        self.home_url = 'https://hlove.tv'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Referer": "https://hlove.tv/",
            "Origin": "https://hlove.tv",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Sec-Ch-Ua": '"Chromium";v="123", "Not-A.Brand";v="24", "Google Chrome";v="123"'
        }
        self.default_pic = 'https://hlove.tv/api/images/default'
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
        movie_classes = "全部$all#剧情$juqing#喜剧$xiju#动作$dongzuo#惊悚$jingsong#爱情$aiqing#恐怖$kongbu#犯罪$fanzui#冒险$maoxian#奇幻$qihuan#悬疑$xuanyi#科幻$kehuan#家庭$jiating#动画$donghua#历史$lishi#战争$zhanzheng#音乐$yinyue#动漫$dongman#电视电影$dianshidianying#西部$xibu#网络电影$wangluodianying#纪录$jilu#同性$tongxing#歌舞$gewu#灾难$zainan#动作冒险$dongzuomaoxian#战争政治$zhanzhengzhengzhi"
        movie_areas = "全部$all#中国大陆$cn#美国$us#韩国$kr#香港$hk#台湾$tw#日本$jp#英国$gb#泰国$th#西班牙$sp#加拿大$ca#法国$fr#印度$in#澳大利亚$au#其他地区$others"
        movie_years = "全部$all#2025$2025#2024$2024#2023$2023#2022$2022#2021$2021#2020$2020#2019-2010$2010#2009-2000$2000#90年代$1990#80年代$1980#更早$1970"
        filters = {
            'movie': [
                {'name': '分类', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in movie_classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in movie_areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in movie_years.split('#')]}
            ],
            # 其他分類略
        }
        return {'class': class_list, 'filters': filters}

    def homeVideoContent(self):
        d = []
        try:
            res = self.session.get(self.home_url, headers=self.headers, timeout=20)
            res.encoding = 'utf-8'
            html_text = res.text
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html_text)
            if not next_data:
                print("未找到 __NEXT_DATA__")
                return {'list': [], 'parse': 0, 'jx': 0}
            next_json = json.loads(next_data.group(1))
            cards = next_json['props']['pageProps'].get('cards', [])
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
        
        # 動態渲染假設：網站通過 API 加載分頁數據
        # 這裡假設 API 端點為 /api/vod/list，實際需通過瀏覽器檢查確認
        api_url = f"{self.home_url}/api/vod/list"  # 需替換為實際 API 端點
        params = {
            'category': cid,
            'year': _year,
            'class': _class,
            'area': _area,
            'page': page,
            'limit': 24
        }

        d = []
        try:
            print(f"請求的初始 URL: {url}")
            # 首次請求初始頁面以獲取分頁信息
            res = self.session.get(url, headers=self.headers, timeout=20)
            res.encoding = 'utf-8'
            print(f"初始頁面 HTTP 狀態碼: {res.status_code}")
            root = etree.HTML(res.text)
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            total = 0
            if next_data:
                next_json = json.loads(next_data.group(1))
                page_props = next_json.get('props', {}).get('pageProps', {})
                total = page_props.get('total', 0)
                print(f"初始 pageProps: {json.dumps(page_props, ensure_ascii=False, indent=2)}")
            else:
                print("未找到 __NEXT_DATA__，嘗試從頁面提取總數")
                total_elem = root.xpath('//div[contains(@class, "pagination")]//text()')
                for elem in total_elem:
                    if elem.strip().isdigit():
                        total = int(elem) * 24
                        break

            # 模擬動態渲染的 API 請求
            print(f"模擬 API 請求: {api_url}, 參數: {params}")
            api_res = self.session.get(api_url, headers=self.headers, params=params, timeout=20)
            api_res.encoding = 'utf-8'
            print(f"API 響應: {api_res.text[:200]}")
            try:
                api_data = json.loads(api_res.text)
                data_list = api_data.get('list', [])  # 假設 API 返回的數據結構
                total = api_data.get('total', total)  # 更新總數
            except json.JSONDecodeError:
                print("API 未返回 JSON，嘗試從初始頁面提取數據")
                data_list = root.xpath('//div[contains(@class, "h-film-listall_cardList___IXsY")]/a')

            for item in data_list:
                if isinstance(item, dict):  # API 返回的 JSON 數據
                    vod_name = item.get('name', '')
                    vod_id = item.get('href', f"/vod/detail/{item.get('id', '')}")
                    vod_pic = item.get('img', self.default_pic)
                    vod_remarks = item.get('countStr', '')
                else:  # HTML 提取的數據
                    vod_name = item.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                    vod_id = item.get('href', '')
                    vod_pic_list = item.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')
                    vod_pic = vod_pic_list[0] if vod_pic_list else self.default_pic
                    vod_remarks = ''
                if not vod_id or not vod_name:
                    continue
                if vod_pic == '/api/images/init':
                    vod_pic = self.default_pic
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })

            pagecount = (total + 23) // 24 if total > 0 else 999
            print(f"總影片數: {total}, 計算出的總頁數: {pagecount}, 返回影片數: {len(d)}")
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
                    index_url = video['purl']
                    mixed_url = self.get_mixed_m3u8_url(index_url) or index_url
                    play_from.append(line_name)
                    play_url.append(f"{vod_name}${mixed_url}")
                else:
                    episodes = []
                    for video in group['videos']:
                        ep_name = f"第{video['eporder']}集"
                        index_url = video['purl']
                        mixed_url = self.get_mixed_m3u8_url(index_url) or index_url
                        episodes.append(f"{ep_name}${mixed_url}")
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
            print(f"成功解析影片: {vod_name}, URL: {detail_url}, 播放URL示例: {play_url[0] if play_url else '無'}")
            return {"list": video_list}
        except Exception as e:
            print(f"Error in detailContent: {str(e)}, URL: {detail_url}")
            return {'list': [], 'msg': f'解析錯誤: {str(e)}'}

    def get_mixed_m3u8_url(self, index_url):
        try:
            headers = self.headers.copy()
            headers['Referer'] = 'https://hlove.tv/'
            response = self.session.get(index_url, headers=headers, timeout=10)
            response.raise_for_status()
            m3u8_content = response.text
            mixed_path = re.search(r'(\S*/mixed\.m3u8)', m3u8_content)
            if mixed_path:
                mixed_relative_url = mixed_path.group(1)
                mixed_url = urljoin(index_url, mixed_relative_url)
                print(f"提取到 mixed.m3u8 URL: {mixed_url}")
                return mixed_url
            print(f"未在 {index_url} 中找到 mixed.m3u8")
            return None
        except Exception as e:
            print(f"無法提取 mixed.m3u8 URL: {str(e)}")
            return None

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
            play_url = pid.split('$')[1]
            headers = self.headers.copy()
            headers['Referer'] = 'https://hlove.tv/'
            headers['Origin'] = 'https://hlove.tv'
            print(f"播放 URL: {play_url}")
            return {
                'url': play_url,
                'header': json.dumps(headers),
                'parse': 1,  # 動態解析 HLS
                'jx': 1
            }
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': play_url, 'parse': 1, 'jx': 1}

    def generate_children_html(self, vod_id):
        detail = self.detailContent([vod_id])
        if not detail['list']:
            return "<h1>無法加載內容</h1>"
        
        vod = detail['list'][0]
        vod_name = vod['vod_name']
        if not vod['vod_play_from'] or not vod['vod_play_url']:
            return f"<h1>{vod_name} - 無可用播放線路</h1>"
        
        play_from = vod['vod_play_from'].split('$$$')
        play_url = vod['vod_play_url'].split('$$$')
        lines = list(zip(play_from, play_url))
        sorted_lines = sorted(lines, key=lambda x: x[0] != 'heimuer')
        if not sorted_lines:
            return f"<h1>{vod_name} - 無可用播放線路</h1>"

        html = """
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
                select {{ margin: 10px; padding: 5px; }}
                .episode-list {{ margin: 10px; }}
                .episode-list button {{ margin: 5px; padding: 5px 10px; }}
            </style>
        </head>
        <body>
            <h1>{vod_name}</h1>
            <div>
                <label for="lineSelect">選擇線路：</label>
                <select id="lineSelect" onchange="changeLine()">
        """.format(vod_name=vod_name)

        for i, (line_name, _) in enumerate(sorted_lines):
            html += f'<option value="{i}">{line_name}</option>'

        html += """
                </select>
            </div>
            <div id="episodeContainer" class="episode-list">
        """

        for i, (line_name, line_url) in enumerate(sorted_lines):
            episodes = line_url.split('#')
            html += f'<div id="line-{i}" class="episodes" style="display: { "block" if i == 0 else "none" };">'
            for episode in episodes:
                ep_name, ep_url = episode.split('$')
                html += f'<button onclick="playVideo(\'{ep_url}\')">{ep_name}</button>'
            html += '</div>'

        html += """
            </div>
            <video id="videoPlayer" controls controlsList="nodownload" oncontextmenu="return false;">
                <source id="videoSource" src="" type="application/x-mpegURL">
                您的瀏覽器不支持視頻播放。
            </video>
            <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            <script>
                var video = document.getElementById('videoPlayer');
                var videoSource = document.getElementById('videoSource');
                var hls = null;

                function changeLine() {{
                    var lineIndex = document.getElementById('lineSelect').value;
                    document.querySelectorAll('.episodes').forEach(function(el) {{
                        el.style.display = 'none';
                    }});
                    document.getElementById('line-' + lineIndex).style.display = 'block';
                    video.pause();
                    videoSource.src = '';
                    video.load();
                }}

                function playVideo(url) {{
                    if (hls) {{
                        hls.destroy();
                        hls = null;
                    }}
                    videoSource.src = url;
                    if (Hls.isSupported()) {{
                        hls = new Hls();
                        hls.loadSource(url);
                        hls.attachMedia(video);
                    }} else if (video.canPlayType("application/vnd.apple.mpegurl")) {{
                        video.src = url;
                    }}
                    video.load();
                    video.play();
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