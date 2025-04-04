# -*- coding: utf-8 -*-
# @Author  : Adapted for 華視頻
# @Time    : 2025/04/05

import sys
import requests
from lxml import etree
import re
import json
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "華視頻"

    def init(self, extend):
        self.home_url = 'https://hlove.tv'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://hlove.tv/",
        }
        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {
            'class': [
                {'type_id': 'movie', 'type_name': '电影'},
                {'type_id': 'drama', 'type_name': '连续剧'},
                {'type_id': 'animation', 'type_name': '动漫'},
                {'type_id': 'variety', 'type_name': '综艺'},
                {'type_id': 'children', 'type_name': '儿童'},
                {'type_id': 'documentary', 'type_name': '纪录片'},
                {'type_id': 'sports', 'type_name': '体育'},
                {'type_id': 'live', 'type_name': '电视直播'}
            ],
            'filters': {
                'children': [
                    {
                        'name': '分类',
                        'key': 'tag',
                        'value': [
                            {'n': '全部', 'v': 'all'},
                            {'n': '儿童', 'v': 'ertong'},
                            {'n': '动画', 'v': 'donghua'},
                            {'n': '喜剧', 'v': 'xiju'},
                            {'n': '动作冒险', 'v': 'dongzuomaoxian'},
                            {'n': '科幻&奇幻', 'v': 'kehuanqihuan'},
                            {'n': '家庭', 'v': 'jiating'},
                            {'n': '动作&冒险', 'v': 'dongzuomaoxian'},
                            {'n': '剧情', 'v': 'juqing'},
                            {'n': '悬疑', 'v': 'xuanyi'},
                            {'n': '犯罪', 'v': 'fanzui'},
                            {'n': '冒险', 'v': 'maoxian'},
                            {'n': '科幻', 'v': 'kehuan'},
                            {'n': '动作', 'v': 'dongzuo'},
                            {'n': '动漫', 'v': 'dongman'},
                            {'n': '历史', 'v': 'lishi'},
                            {'n': '奇幻', 'v': 'qihuan'}
                        ]
                    },
                    {
                        'name': '地区',
                        'key': 'area',
                        'value': [
                            {'n': '全部', 'v': 'all'},
                            {'n': '中国大陆', 'v': 'cn'},
                            {'n': '美国', 'v': 'us'},
                            {'n': '韩国', 'v': 'kr'},
                            {'n': '香港', 'v': 'hk'},
                            {'n': '台湾', 'v': 'tw'},
                            {'n': '日本', 'v': 'jp'},
                            {'n': '英国', 'v': 'gb'},
                            {'n': '泰国', 'v': 'th'},
                            {'n': '西班牙', 'v': 'sp'},
                            {'n': '加拿大', 'v': 'ca'},
                            {'n': '法国', 'v': 'fr'},
                            {'n': '印度', 'v': 'in'},
                            {'n': '澳大利亚', 'v': 'au'},
                            {'n': '其他地区', 'v': 'others'}
                        ]
                    },
                    {
                        'name': '年份',
                        'key': 'year',
                        'value': [
                            {'n': '全部', 'v': 'all'},
                            {'n': '2025', 'v': '2025'},
                            {'n': '2024', 'v': '2024'},
                            {'n': '2023', 'v': '2023'},
                            {'n': '2022', 'v': '2022'},
                            {'n': '2021', 'v': '2021'},
                            {'n': '2020', 'v': '2020'},
                            {'n': '2019-2010', 'v': '2010'},
                            {'n': '2009-2000', 'v': '2000'},
                            {'n': '90年代', 'v': '1990'},
                            {'n': '80年代', 'v': '1980'},
                            {'n': '更早', 'v': '1970'}
                        ]
                    }
                ]
            }
        }
        return result

    def homeVideoContent(self):
        d = []
        try:
            res = requests.get(self.home_url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "h-film-listall_cardList___IXsY")]/a')
            for i in data_list:
                vod_name = i.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                vod_id = i.get('href', '')
                vod_pic = i.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')[0]
                if vod_pic == '/api/images/init':  # 初始圖片替換為占位符
                    vod_pic = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg'
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': ''
                })
            return {'list': d[:10], 'parse': 0, 'jx': 0}  # 限制首頁顯示數量
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        _tag = ext.get('tag', 'all')
        _area = ext.get('area', 'all')
        _year = ext.get('year', 'all')
        url = f"{self.home_url}/{cid}/{_year}/{_tag}/{_area}"
        if page != '1':
            url += f"?page={page}"
        d = []
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "h-film-listall_cardList___IXsY")]/a')
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            total = 0
            if next_data:
                next_json = json.loads(next_data.group(1))
                init_cards = next_json['props']['pageProps']['initCard']
                total = next_json['props']['pageProps']['total']
                for i, card in enumerate(data_list):
                    vod_name = card.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                    vod_id = card.get('href', '')
                    vod_pic = init_cards[i]['img'] if i < len(init_cards) and init_cards[i]['img'] else 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg'
                    vod_remarks = init_cards[i]['countStr'] if i < len(init_cards) else ''
                    d.append({
                        'vod_id': vod_id,
                        'vod_name': vod_name,
                        'vod_pic': vod_pic,
                        'vod_remarks': vod_remarks
                    })
            pagecount = (total + 23) // 24 if total > 0 else 999  # 每頁24個，計算總頁數
            return {'list': d, 'page': int(page), 'pagecount': pagecount, 'limit': 24, 'total': total}
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {'list': d, 'page': int(page), 'pagecount': 999, 'limit': 24, 'total': 0}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        url = f"{self.home_url}{ids}"
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            
            # 假設詳情頁結構（需根據實際頁面調整）
            vod_name = root.xpath('//h1/text()')[0].strip() if root.xpath('//h1/text()') else ''
            vod_play_from = '華視頻'
            vod_play_url = f"播放${url}"  # 假設播放鏈接需要嗅探
            
            video_list.append({
                'type_name': '',
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_remarks': '',
                'vod_year': '',
                'vod_area': '',
                'vod_actor': '',
                'vod_director': '',
                'vod_content': '',
                'vod_play_from': vod_play_from,
                'vod_play_url': vod_play_url
            })
            return {"list": video_list, 'parse': 1, 'jx': 0}  # 需要嗅探
        except Exception as e:
            print(f"Error in detailContent: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        url = f"{self.home_url}/search?q={key}&page={page}"
        d = []
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "h-film-listall_cardList___IXsY")]/a')
            for i in data_list:
                vod_name = i.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                vod_id = i.get('href', '')
                vod_pic = i.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')[0]
                if vod_pic == '/api/images/init':
                    vod_pic = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg'
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': ''
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        url = f"{self.home_url}{pid}"
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            # 假設播放鏈接提取（需根據實際頁面調整）
            play_url = re.findall(r'var videoUrl = "(.*?)"', res.text)
            if not play_url:
                return {'url': url, 'parse': 1, 'jx': 0}  # 需要嗅探
            return {
                'url': play_url[0],
                'parse': 0,
                'jx': 0,
                'header': {"User-Agent": "okhttp/5.0.0"}
            }
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': self.default_play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

if __name__ == '__main__':
    pass