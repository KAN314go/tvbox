# -*- coding: utf-8 -*-
# @Author  : Adapted from Doubebly's LreeOk by Grok, optimized with XBPQ and Selenium logic
# @Time    : 2025/3/28
# @Purpose : Spider for gimy.la to use in CatVod

import sys
import requests
import json
import re
from lxml import etree
try:
    from requests_html import HTMLSession
except ImportError:
    HTMLSession = None

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):
    def getName(self):
        return "GimyCC"

    def init(self, extend):
        self.home_url = 'https://gimy.la/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Referer": "https://gimy.la/"
        }

    def getDependence(self):
        return ['requests_html'] if HTMLSession else []

    def isVideoFormat(self, url):
        video_extensions = ['.mp4', '.m3u8', '.flv', '.avi', '.mkv']
        return any(url.lower().endswith(ext) for ext in video_extensions)

    def manualVideoCheck(self):
        return False

    def homeContent(self, filter):
        result = {
            'class': [
                {'type_id': '1', 'type_name': '電影'},
                {'type_id': '2', 'type_name': '劇集'},
                {'type_id': '3', 'type_name': '綜藝'},
                {'type_id': '4', 'type_name': '動漫'}
            ],
            'filters': {
                '1': [{'key': 'area', 'name': '地區', 'value': [{'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'}, {'n': '美国', 'v': '美国'}, {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}]},
                      {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}]},
                      {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}],
                '2': [{'key': 'area', 'name': '地區', 'value': [{'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'}, {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}]},
                      {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}]},
                      {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}],
                '3': [{'key': 'area', 'name': '地區', 'value': [{'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'}, {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}]},
                      {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}]},
                      {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}],
                '4': [{'key': 'area', 'name': '地區', 'value': [{'n': '中國', 'v': '中國'}, {'n': '日本', 'v': '日本'}, {'n': '美国', 'v': '美国'}]},
                      {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}]},
                      {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}]
            }
        }
        return result

    def homeVideoContent(self):
        try:
            if HTMLSession:
                session = HTMLSession()
                res = session.get(self.home_url, headers=self.headers, timeout=10)
                res.html.render(timeout=20)
                root = etree.HTML(res.html.html)
            else:
                res = requests.get(self.home_url, headers=self.headers, timeout=10)
                res.encoding = 'utf-8'
                root = etree.HTML(res.text)
            data_list = root.xpath('//div[@class="public-list-exp"]')
            d = []
            for i in data_list:
                vod_id = i.xpath('.//a/@href')[0].split('/')[-1].split('.')[0] if i.xpath('.//a/@href') else ''
                vod_name = i.xpath('.//a/@title')[0].strip() if i.xpath('.//a/@title') else ''
                vod_pic = i.xpath('.//img/@data-src')[0] if i.xpath('.//img/@data-src') else ''
                vod_remarks = i.xpath('.//span[@class="ft2"]/text()')[0] if i.xpath('.//span[@class="ft2"]/text()') else ''
                if vod_id and vod_name:
                    d.append({
                        'vod_id': vod_id,
                        'vod_name': vod_name,
                        'vod_pic': vod_pic,
                        'vod_remarks': vod_remarks
                    })
            print(f"homeVideoContent 提取到 {len(d)} 個項目")
            return {'list': d}
        except Exception as e:
            print(f"homeVideoContent 錯誤: {str(e)}")
            return {'list': []}

    def categoryContent(self, cid, page, filter, ext):
        payload = {
            'type': cid,
            'area': ext.get('area', ''),
            'year': ext.get('year', ''),
            'by': ext.get('by', ''),
            'page': page
        }
        url = f'{self.home_url}filter/area/{payload["area"]}/by/{payload["by"]}/id/{cid}/page/{page}/year/{payload["year"]}.html'
        try:
            if HTMLSession:
                session = HTMLSession()
                res = session.get(url, headers=self.headers, timeout=10)
                res.html.render(timeout=20)
                root = etree.HTML(res.html.html)
            else:
                res = requests.get(url, headers=self.headers, timeout=10)
                res.encoding = 'utf-8'
                root = etree.HTML(res.text)
            data_list = root.xpath('//div[@class="public-list-exp"]')
            d = []
            for i in data_list:
                vod_id = i.xpath('.//a/@href')[0].split('/')[-1].split('.')[0] if i.xpath('.//a/@href') else ''
                vod_name = i.xpath('.//a/@title')[0].strip() if i.xpath('.//a/@title') else ''
                vod_pic = i.xpath('.//img/@data-src')[0] if i.xpath('.//img/@data-src') else ''
                vod_remarks = i.xpath('.//span[@class="ft2"]/text()')[0] if i.xpath('.//span[@class="ft2"]/text()') else ''
                if vod_id and vod_name:
                    d.append({
                        'vod_id': vod_id,
                        'vod_name': vod_name,
                        'vod_pic': vod_pic,
                        'vod_remarks': vod_remarks
                    })
            print(f"categoryContent 提取到 {len(d)} 個項目")
            return {'list': d}
        except Exception as e:
            print(f"categoryContent 錯誤: {str(e)}")
            return {'list': []}

    def detailContent(self, did):
        ids = did[0] if isinstance(did, list) else did
        video_list = []
        try:
            res = requests.get(f'{self.home_url}detail/{ids}.html', headers=self.headers, timeout=10)
            res.raise_for_status()
            res.encoding = 'utf-8'
            print("detailContent 前 3000 字元 HTML:", res.text[:3000])
            root = etree.HTML(res.text)

            # 提取播放線路
            vod_play_from_list = [name.strip().replace('\xa0', '') for name in root.xpath('//div[contains(@class, "anthology-tab")]//a/text()') if name.strip()]
            vod_play_from_order = ['量子雲', '索尼雲', '快捷雲', '無限雲', '閃電雲', '小牛雲', '速播雲', '優酷雲']
            vod_play_from_sorted = sorted(vod_play_from_list, key=lambda x: vod_play_from_order.index(x) if x in vod_play_from_order else len(vod_play_from_order))
            vod_play_from = '$$$'.join(vod_play_from_sorted) if vod_play_from_sorted else '量子雲$$$索尼雲$$$快捷雲'

            # 提取播放列表
            play_list = root.xpath('//div[contains(@class, "anthology-list-box")]//ul[contains(@class, "anthology-list-play")]')
            vod_play_url = []
            for i in play_list:
                name_list = i.xpath('./li/a/text()')
                url_list = i.xpath('./li/a/@href')
                if len(name_list) != len(url_list):
                    min_length = min(len(name_list), len(url_list))
                    name_list = name_list[:min_length]
                    url_list = url_list[:min_length]
                play_url = '#'.join([f"{name.strip()}${self.home_url.rstrip('/')}{url}" for name, url in zip(name_list, url_list) if name.strip()])
                if play_url:
                    vod_play_url.append(play_url)

            # 提取影片信息
            vod_name = (root.xpath('//h3[@class="slide-info-title"]/text()')[0] if root.xpath('//h3[@class="slide-info-title"]/text()') else 
                       root.xpath('//title/text()')[0].split(' - ')[0] if root.xpath('//title/text()') else '未知名稱').strip()
            vod_year_match = re.search(r'年份 :(\d{4})', res.text) or re.search(r'更新 :.*?(\d{4})', res.text)
            vod_area_match = re.search(r'地區 :([^<]+)', res.text) or ''.join(root.xpath('//div[contains(@class, "slide-info") and contains(., "地區")]//text()')).strip()
            vod_remarks_match = re.search(r'備注 :(.+?)</div>', res.text)
            vod_director = ','.join([d.strip() for d in root.xpath('//div[contains(@class, "slide-info") and contains(., "導演")]//a/text()') if d.strip()]) or ''
            vod_actor = ','.join([a.strip() for a in root.xpath('//div[contains(@class, "slide-info") and contains(., "演員")]//a/text()') if a.strip()]) or ''
            vod_content = root.xpath('//meta[@name="description"]/@content')[0].strip() if root.xpath('//meta[@name="description"]/@content') else ''.join(root.xpath('//div[@id="height_limit"]/text()')).strip()
            vod_pic_match = re.search(r'data-src="([^"]+)"', res.text)

            video_list.append({
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_pic': vod_pic_match.group(1) if vod_pic_match else '',
                'vod_remarks': re.sub(r'</?\w+[^>]*>', '', vod_remarks_match.group(1)).strip() if vod_remarks_match else '',
                'vod_year': vod_year_match.group(1).strip() if vod_year_match else '',
                'vod_area': vod_area_match if isinstance(vod_area_match, str) else vod_area_match.group(1).strip() if vod_area_match else '',
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_play_from': vod_play_from,
                'vod_play_url': '$$$'.join(vod_play_url) if vod_play_url else ''
            })
            print(f"detailContent 成功解析: {vod_name}")
            return {"list": video_list}
        except Exception as e:
            print(f"detailContent 錯誤: {str(e)}")
            return {'list': []}

    def searchContent(self, key, quick, page='1'):
        d = []
        url = f'{self.home_url}search.html?wd={key}&page={page}'
        try:
            if HTMLSession:
                session = HTMLSession()
                res = session.get(url, headers=self.headers, timeout=10)
                res.html.render(timeout=20)
                root = etree.HTML(res.html.html)
            else:
                res = requests.get(url, headers=self.headers, timeout=10)
                res.raise_for_status()
                res.encoding = 'utf-8'
                root = etree.HTML(res.text)
            print("searchContent 前 3000 字元 HTML:", res.text[:3000] if not HTMLSession else res.html.html[:3000])
            data_list = root.xpath('//div[@class="public-list-box"]') or root.xpath('//li[contains(@class, "box border")]') or root.xpath('//li[contains(@class, "search-item")]') or root.xpath('//div[contains(@class, "search-list")]')
            for i in data_list:
                vod_id_match = re.search(r'href="/detail/(\d+).html"', etree.tostring(i, encoding='unicode'))
                vod_id = vod_id_match.group(1) if vod_id_match else ''
                vod_name = i.xpath('.//a/@title')[0].strip() if i.xpath('.//a/@title') else i.xpath('.//a/text()')[0].strip() if i.xpath('.//a/text()') else '未知'
                vod_pic_match = re.search(r'(?:src|data-src)="([^"]+)"', etree.tostring(i, encoding='unicode'))
                vod_remarks = i.xpath('.//span/text()')[0].strip() if i.xpath('.//span/text()') else ''
                if vod_id and vod_name != '未知':
                    d.append({
                        'vod_id': vod_id,
                        'vod_name': vod_name,
                        'vod_pic': vod_pic_match.group(1) if vod_pic_match else '',
                        'vod_remarks': vod_remarks
                    })
            print(f"searchContent 提取到 {len(d)} 個結果")
            return {'list': d}
        except Exception as e:
            print(f"searchContent 錯誤: {str(e)}")
            return {'list': []}

    def playerContent(self, flag, pid, vipFlags):
        try:
            play_url = f'{self.home_url.rstrip("/")}{pid}'
            res = requests.get(play_url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)
            script_content = ''.join(root.xpath('//script/text()'))
            m3u8_url = re.search(r"url:\s*['\"](https?://[^'\"]+?\.m3u8)['\"]", script_content)
            if m3u8_url:
                print(f"playerContent 找到 m3u8 地址: {m3u8_url.group(1)}")
                return {
                    'url': m3u8_url.group(1),
                    'header': json.dumps(self.headers),
                    'parse': 0,
                    'jx': 0
                }
            iframe_urls = root.xpath('//iframe/@src')
            if iframe_urls:
                print(f"playerContent 找到 iframe 地址: {iframe_urls[0]}")
                return {
                    'url': iframe_urls[0],
                    'header': json.dumps(self.headers),
                    'parse': 1,
                    'jx': 0
                }
            print("playerContent 未找到有效播放地址")
            return {'url': '', 'header': json.dumps(self.headers), 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"playerContent 錯誤: {str(e)}")
            return {'url': '', 'header': json.dumps(self.headers), 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        return None

    def destroy(self):
        return '正在Destroy'

    def get_data(self, payload):
        return []

if __name__ == '__main__':
    spider = Spider()
    spider.init({})
    print("測試首頁推薦內容:")
    home_videos = spider.homeVideoContent()
    print(json.dumps(home_videos, ensure_ascii=False, indent=2))
    print("\n測試分類和篩選選項:")
    result = spider.homeContent(True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\n測試分類內容:")
    category = spider.categoryContent('1', '1', True, {'area': '中國', 'year': '2024', 'by': 'time'})
    print(json.dumps(category, ensure_ascii=False, indent=2))
    print("\n測試詳情內容:")
    detail = spider.detailContent(['260933'])
    print(json.dumps(detail, ensure_ascii=False, indent=2))
    print("\n測試播放內容:")
    play = spider.playerContent("測試線路", "/play/260933-1-1.html", [])
    print(json.dumps(play, ensure_ascii=False, indent=2))
    print("\n測試搜索內容:")
    search = spider.searchContent("海賊王", True, "1")
    print(json.dumps(search, ensure_ascii=False, indent=2))