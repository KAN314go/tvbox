# coding=utf-8
#!/usr/bin/python

import sys
import requests
from lxml import etree
import re
import json
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        print("調用 getName")
        return "GimyCC"

    def init(self, extend):
        print("調用 init: extend={}".format(extend))
        self.home_url = 'https://gimy.la/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Referer": "https://gimy.la/"
        }
        # 可選：添加代理
        self.proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}

    def getDependence(self):
        print("調用 getDependence")
        return []

    def isVideoFormat(self, url):
        print(f"調用 isVideoFormat: url={url}")
        video_extensions = ['.mp4', '.m3u8', '.flv', '.avi', '.mkv']
        return any(url.lower().endswith(ext) for ext in video_extensions)

    def manualVideoCheck(self):
        print("調用 manualVideoCheck")
        return False

    def homeContent(self, filter):
        print("調用 homeContent: filter={}".format(filter))
        result = {
            'class': [
                {'type_id': '1', 'type_name': '電影'},
                {'type_id': '2', 'type_name': '劇集'},
                {'type_id': '3', 'type_name': '綜藝'},
                {'type_id': '4', 'type_name': '動漫'}
            ],
            'filters': {
                '1': [
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, 
                        {'n': '台灣', 'v': '台灣'}, {'n': '美国', 'v': '美国'}]},
                    {'key': 'year', 'name': '時間', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, 
                        {'n': '2023', 'v': '2023'}]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '按時間', 'v': 'time'}, {'n': '按熱度', 'v': 'hits'}]}
                ],
                '2': [
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中國', 'v': '中國'}, {'n': '香港', 'v': '香港'}, 
                        {'n': '台灣', 'v': '台灣'}, {'n': '日本', 'v': '日本'}]},
                    {'key': 'year', 'name': '時間', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, 
                        {'n': '2023', 'v': '2023'}]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '按時間', 'v': 'time'}, {'n': '按熱度', 'v': 'hits'}]}
                ]
            }
        }
        print(f"homeContent 返回: {json.dumps(result, ensure_ascii=False)}")
        return result

    def homeVideoContent(self):
        print("調用 homeVideoContent")
        return self.get_data(self.home_url)

    def categoryContent(self, cid, page, filter, ext):
        print("調用 categoryContent: cid={}, page={}, filter={}, ext={}".format(cid, page, filter, ext))
        _area = ext.get('area', '')
        _year = ext.get('year', '')
        _by = ext.get('by', '')
        url = f'{self.home_url}filter/area/{_area}/by/{_by}/id/{cid}/page/{page}/year/{_year}.html'
        return self.get_data(url)

    def detailContent(self, did):
        ids = did[0] if isinstance(did, list) else did
        print("調用 detailContent: ids={}".format(ids))
        try:
            url = f'{self.home_url}detail/{ids}.html'
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)

            vod_name = root.xpath('//a[@class="fed-play-btn fed-btns-info fed-rims-info"]/@title')
            vod_name = vod_name[0].strip() if vod_name else '未知名稱'

            play_from_list = root.xpath('//div[contains(@class, "anthology-tab")]//a/text()')
            vod_play_from = '$$$'.join([name.strip().replace('\xa0', '') for name in play_from_list if name.strip()]) or '量子雲$$$索尼雲$$$快捷雲'

            play_list_boxes = root.xpath('//div[contains(@class, "anthology-list-box")]')
            vod_play_url = []
            for box in play_list_boxes:
                name_list = box.xpath('.//ul[contains(@class, "anthology-list-play")]/li/a/text()')
                url_list = box.xpath('.//ul[contains(@class, "anthology-list-play")]/li/a/@href')
                if len(name_list) != len(url_list):
                    min_length = min(len(name_list), len(url_list))
                    name_list = name_list[:min_length]
                    url_list = url_list[:min_length]
                play_url = '#'.join([f"{name.strip()}${self.home_url}{url}" for name, url in zip(name_list, url_list) if name.strip()])
                if play_url:
                    vod_play_url.append(play_url)

            video_item = {
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_play_from': vod_play_from,
                'vod_play_url': '$$$'.join(vod_play_url) if vod_play_url else ''
            }
            print("detailContent 成功返回: {}".format(vod_name))
            return {"list": [video_item], 'parse': 0, 'jx': 0}
        except requests.RequestException as e:
            print(f"detailContent 錯誤: {str(e)}")
            return {'list': [], 'parse': 0, 'jx': 0, 'msg': f"Error: {str(e)}"}

    def searchContent(self, key, quick, page='1'):
        print("調用 searchContent: key={}, quick={}, page={}".format(key, quick, page))
        url = f'{self.home_url}search.html?wd={key}'
        return self.get_data(url, is_search=True)

    def playerContent(self, flag, pid, vipFlags):
        print("調用 playerContent: flag={}, pid={}, vipFlags={}".format(flag, pid, vipFlags))
        try:
            play_url = f'{self.home_url}{pid}'
            print(f"正在請求播放頁面: {play_url}")
            res = requests.get(play_url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)

            iframe_urls = root.xpath('//iframe/@src')
            if iframe_urls:
                iframe_url = iframe_urls[0]
                print(f"找到 iframe 地址: {iframe_url}")
                return {
                    'url': iframe_url,
                    'header': json.dumps(self.headers),
                    'parse': 1,
                    'jx': 0
                }

            script_content = ''.join(root.xpath('//script/text()'))
            m3u8_url = re.search(r"url:\s*['\"](https?://[^'\"]+?\.m3u8)['\"]", script_content)
            if m3u8_url:
                print(f"找到 m3u8 地址: {m3u8_url.group(1)}")
                return {
                    'url': m3u8_url.group(1),
                    'header': json.dumps(self.headers),
                    'parse': 0,
                    'jx': 0
                }

            test_url = 'https://gitee.com/dobebly/my_img/raw/c1977fa6134aefb8e5a34dabd731a4d186c84a4d/x.mp4'
            print("未找到播放地址，使用測試鏈接")
            return {
                'url': test_url,
                'header': json.dumps(self.headers),
                'parse': 0,
                'jx': 0,
                'msg': '未找到播放地址，使用測試鏈接'
            }
        except requests.RequestException as e:
            print(f"playerContent 錯誤: {str(e)}")
            return {
                'url': 'https://gitee.com/dobebly/my_img/raw/c1977fa6134aefb8e5a34dabd731a4d186c84a4d/x.mp4',
                'header': json.dumps(self.headers),
                'parse': 0,
                'jx': 0,
                'msg': f"Error: {str(e)}"
            }

    def localProxy(self, params):
        print("調用 localProxy: params={}".format(params))
        return None

    def destroy(self):
        print("調用 destroy")
        return '正在Destroy'

    def get_data(self, url, is_search=False):
        print("調用 get_data: url={}".format(url))
        data = []
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)
            if is_search:
                data_list = root.xpath('//div[contains(@class, "public-list-box")]')
            else:
                data_list = root.xpath('//div[contains(@class, "public-list-exp")]')
            for item in data_list:
                vod_id = item.xpath('.//a/@href')[0].split('/')[-1].split('.')[0] if item.xpath('.//a/@href') else ''
                vod_name = item.xpath('.//a/@title')[0] if item.xpath('.//a/@title') else ''
                vod_pic = item.xpath('.//img/@data-src')[0] if item.xpath('.//img/@data-src') else ''
                vod_remarks = item.xpath('.//span[contains(@class, "ft2")]/text()')[0] if item.xpath('.//span[contains(@class, "ft2")]/text()') else ''
                data.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
        except requests.RequestException as e:
            print(f"get_data 錯誤: {str(e)}")
        return {'list': data, 'parse': 0, 'jx': 0}

if __name__ == "__main__":
    spider = Spider()
    spider.init({})
    result = spider.homeContent(True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    detail = spider.detailContent(['260933'])
    print(json.dumps(detail, ensure_ascii=False, indent=2))
    play = spider.playerContent("測試線路", "/play/260933-1-1.html", [])
    print(json.dumps(play, ensure_ascii=False, indent=2))
    spider.destroy()