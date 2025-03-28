# coding=utf-8
# !/usr/bin/python

import sys
import requests
from lxml import etree
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "GimyCC"

    def init(self, extend):
        self.home_url = 'https://gimy.cc'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        # 同之前的 homeContent 實現，略
        pass

    def homeVideoContent(self):
        data = self.get_data(self.home_url)
        return {'list': data, 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        _area = ext.get('area') if ext.get('area') else ''
        _year = ext.get('year') if ext.get('year') else ''
        _by = ext.get('by') if ext.get('by') else ''
        url = f'{self.home_url}/filter/{cid}-{_area}-{_year}-{_by}/page/{page}.html'
        data = self.get_data(url)
        return {'list': data, 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        try:
            res = requests.get(f'{self.home_url}/vod/{ids}.html', headers=self.headers)
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join(root.xpath('//a[@class="vod-playerUrl"]/text()'))
            play_list = root.xpath('//div[@class="anthology-list-box"]')
            vod_play_url = []
            for i in play_list:
                name_list = i.xpath('./ul/li/a/span/text()')
                url_list = i.xpath('./ul/li/a/@href')
                vod_play_url.append(
                    '#'.join([_name + '$' + _url for _name, _url in zip(name_list, url_list)])
                )
            video_list.append({
                'type_name': '',
                'vod_id': ids,
                'vod_name': root.xpath('//h1/text()')[0] if root.xpath('//h1/text()') else '',
                'vod_remarks': '',
                'vod_year': '',
                'vod_area': '',
                'vod_actor': '',
                'vod_director': '',
                'vod_content': '',
                'vod_play_from': vod_play_from,
                'vod_play_url': '$$$'.join(vod_play_url)
            })
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except requests.RequestException as e:
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        url = f'{self.home_url}/search.html?wd={key}&page={page}'
        data = self.get_data(url)
        return {'list': data, 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        try:
            # pid 是從 detailContent 中傳來的播放 URL，如 /play/261378-2-1.html
            res = requests.get(f'{self.home_url}{pid}', headers=self.headers)
            root = etree.HTML(res.text)
            # 提取 Artplayer 中的播放 URL
            script_content = ''.join(root.xpath('//script/text()'))
            import re
            m3u8_url = re.search(r"url:\s*['\"](https?://[^'\"]+?\.m3u8)['\"]", script_content)
            if m3u8_url:
                return {
                    'url': m3u8_url.group(1),
                    'parse': 0,  # 直接返回 M3U8 鏈接，無需解析
                    'jx': 0
                }
            return {'url': '', 'parse': 0, 'jx': 0, 'msg': '未找到播放鏈接'}
        except requests.RequestException as e:
            return {'url': '', 'parse': 0, 'jx': 0, 'msg': str(e)}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

    def get_data(self, url):
        data = []
        try:
            res = requests.get(url, headers=self.headers)
            root = etree.HTML(res.text)
            data_list = root.xpath('//li[contains(@class, "box border")]')
            for i in data_list:
                vod_id = i.xpath('./a/@href')[0].split('/')[-1].split('.')[0] if i.xpath('./a/@href') else ''
                vod_name = i.xpath('./a/@title')[0] if i.xpath('./a/@title') else ''
                vod_pic = i.xpath('./a/img/@src')[0] if i.xpath('./a/img/@src') else ''
                vod_remarks = i.xpath('./span/text()')[0] if i.xpath('./span/text()') else ''
                data.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
        except requests.RequestException as e:
            return data
        return data