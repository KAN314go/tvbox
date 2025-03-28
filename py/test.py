# -*- coding: utf-8 -*-
# @Author  : Adapted from Doubebly's LreeOk by Grok
# @Time    : 2025/3/28
# @Purpose : Spider for gimy.la to use in CatVod

import sys
import requests
import hashlib
import time
import json
import re
from lxml import etree

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
        return []

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
                '1': [  # 電影
                    {'key': 'class', 'name': '類型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '動作', 'v': '動作'}, {'n': '喜劇', 'v': '喜劇'}, 
                        {'n': '愛情', 'v': '愛情'}, {'n': '科幻', 'v': '科幻'}, {'n': '恐怖', 'v': '恐怖'}]},
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, 
                        {'n': '台灣', 'v': '台灣'}, {'n': '美國', 'v': '美國'}, {'n': '日本', 'v': '日本'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, 
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}
                ],
                '2': [  # 劇集
                    {'key': 'class', 'name': '類型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '古裝', 'v': '古裝'}, {'n': '偶像', 'v': '偶像'}, 
                        {'n': '家庭', 'v': '家庭'}, {'n': '懸疑', 'v': '懸疑'}, {'n': '奇幻', 'v': '奇幻'}]},
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, 
                        {'n': '台灣', 'v': '台灣'}, {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, 
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}
                ],
                '3': [  # 綜藝
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, 
                        {'n': '台灣', 'v': '台灣'}, {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, 
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}
                ],
                '4': [  # 動漫
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中國', 'v': '中國'}, {'n': '日本', 'v': '日本'}, 
                        {'n': '美國', 'v': '美國'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, 
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '按最新', 'v': 'time'}, {'n': '按最熱', 'v': 'hits'}]}
                ]
            }
        }
        return result

    def homeVideoContent(self):
        d = []
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=10)
            res.encoding = 'utf-8'
            res.raise_for_status()
            root = etree.HTML(res.text)
            # gimy.la 的首頁推薦結構
            data_list = root.xpath('//div[contains(@class, "public-list-exp")]')
            if not data_list:
                # 嘗試備用路徑
                data_list = root.xpath('//div[contains(@class, "fed-list-item")]') or root.xpath('//ul[contains(@class, "vodlist")]/li')
                if not data_list:
                    print("未找到首頁推薦內容，網站結構可能已改變")
                    print("前 500 字元 HTML:", res.text[:500])
            for i in data_list:
                vod_id = i.xpath('.//a/@href')[0].split('/')[-1].split('.')[0] if i.xpath('.//a/@href') else ''
                vod_name = i.xpath('.//a/@title')[0] if i.xpath('.//a/@title') else i.xpath('.//a/text()')[0] if i.xpath('.//a/text()') else ''
                vod_pic = i.xpath('.//img/@data-src')[0] if i.xpath('.//img/@data-src') else i.xpath('.//img/@src')[0] if i.xpath('.//img/@src') else ''
                vod_remarks = i.xpath('.//span[contains(@class, "ft2")]/text()')[0] if i.xpath('.//span[contains(@class, "ft2")]/text()') else ''
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
        d = []
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "public-list-exp")]')
            for i in data_list:
                vod_id = i.xpath('.//a/@href')[0].split('/')[-1].split('.')[0] if i.xpath('.//a/@href') else ''
                vod_name = i.xpath('.//a/@title')[0] if i.xpath('.//a/@title') else i.xpath('.//a/text()')[0] if i.xpath('.//a/text()') else ''
                vod_pic = i.xpath('.//img/@data-src')[0] if i.xpath('.//img/@data-src') else i.xpath('.//img/@src')[0] if i.xpath('.//img/@src') else ''
                vod_remarks = i.xpath('.//span[contains(@class, "ft2")]/text()')[0] if i.xpath('.//span[contains(@class, "ft2")]/text()') else ''
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
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join([name.strip() for name in root.xpath('//div[contains(@class, "anthology-tab")]//a/text()') if name.strip()]) or '量子雲$$$索尼雲$$$快捷雲'
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
            
            vod_name = root.xpath('//h1[@class="fed-part-eone"]/text()')[0] if root.xpath('//h1[@class="fed-part-eone"]/text()') else '未知名稱'
            video_list.append({
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_pic': root.xpath('//img[@class="fed-part-thumb fed-lazy"]/@data-original')[0] if root.xpath('//img[@class="fed-part-thumb fed-lazy"]/@data-original') else '',
                'vod_remarks': root.xpath('//span[contains(@class, "fed-text-orange")]/text()')[0] if root.xpath('//span[contains(@class, "fed-text-orange")]/text()') else '',
                'vod_year': root.xpath('//li[contains(text(), "年份")]/a/text()')[0] if root.xpath('//li[contains(text(), "年份")]/a/text()') else '',
                'vod_area': root.xpath('//li[contains(text(), "地區")]/a/text()')[0] if root.xpath('//li[contains(text(), "地區")]/a/text()') else '',
                'vod_actor': root.xpath('//li[contains(text(), "主演")]/a/text()')[0] if root.xpath('//li[contains(text(), "主演")]/a/text()') else '',
                'vod_director': root.xpath('//li[contains(text(), "導演")]/a/text()')[0] if root.xpath('//li[contains(text(), "導演")]/a/text()') else '',
                'vod_content': root.xpath('//span[contains(@class, "sketch")]/text()')[0] if root.xpath('//span[contains(@class, "sketch")]/text()') else '',
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
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "public-list-box")]')
            for i in data_list:
                vod_id = i.xpath('.//a/@href')[0].split('/')[-1].split('.')[0] if i.xpath('.//a/@href') else ''
                vod_name = i.xpath('.//a/@title')[0] if i.xpath('.//a/@title') else i.xpath('.//a/text()')[0] if i.xpath('.//a/text()') else ''
                vod_pic = i.xpath('.//img/@data-src')[0] if i.xpath('.//img/@data-src') else i.xpath('.//img/@src')[0] if i.xpath('.//img/@src') else ''
                vod_remarks = i.xpath('.//span[contains(@class, "ft2")]/text()')[0] if i.xpath('.//span[contains(@class, "ft2")]/text()') else ''
                if vod_id and vod_name:
                    d.append({
                        'vod_id': vod_id,
                        'vod_name': vod_name,
                        'vod_pic': vod_pic,
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
        # gimy.la 不使用 API，直接留空
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