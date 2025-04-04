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
                {'type_id': 'children', 'type_name': '儿童'}
            ],
            'filters': {
                'movie': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '动作', 'v': 'dongzuo'}, {'n': '喜剧', 'v': 'xiju'},
                        {'n': '爱情', 'v': 'aiqing'}, {'n': '科幻', 'v': 'kehuan'}, {'n': '恐怖', 'v': 'kongbu'},
                        {'n': '剧情', 'v': 'juqing'}, {'n': '战争', 'v': 'zhanzheng'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '中国大陆', 'v': 'cn'}, {'n': '美国', 'v': 'us'},
                        {'n': '韩国', 'v': 'kr'}, {'n': '香港', 'v': 'hk'}, {'n': '台湾', 'v': 'tw'},
                        {'n': '日本', 'v': 'jp'}, {'n': '英国', 'v': 'gb'}]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, {'n': '2019-2010', 'v': '2010'}]}
                ],
                'drama': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '古装', 'v': 'guzhuang'}, {'n': '偶像', 'v': 'ouxiang'},
                        {'n': '家庭', 'v': 'jiating'}, {'n': '悬疑', 'v': 'xuanyi'}, {'n': '都市', 'v': 'dushi'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '中国大陆', 'v': 'cn'}, {'n': '美国', 'v': 'us'},
                        {'n': '韩国', 'v': 'kr'}, {'n': '香港', 'v': 'hk'}, {'n': '台湾', 'v': 'tw'},
                        {'n': '日本', 'v': 'jp'}]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}]}
                ],
                'animation': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '热血', 'v': 'rexue'}, {'n': '冒险', 'v': 'maoxian'},
                        {'n': '搞笑', 'v': 'gaoxiao'}, {'n': '奇幻', 'v': 'qihuan'}, {'n': '科幻', 'v': 'kehuan'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '中国大陆', 'v': 'cn'}, {'n': '日本', 'v': 'jp'},
                        {'n': '美国', 'v': 'us'}]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}]}
                ],
                'variety': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '真人秀', 'v': 'zhenrenxiu'}, {'n': '脱口秀', 'v': 'tuokouxiu'},
                        {'n': '访谈', 'v': 'fangtan'}, {'n': '美食', 'v': 'meishi'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '中国大陆', 'v': 'cn'}, {'n': '韩国', 'v': 'kr'},
                        {'n': '台湾', 'v': 'tw'}]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}]}
                ],
                'children': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '儿童', 'v': 'ertong'}, {'n': '动画', 'v': 'donghua'},
                        {'n': '喜剧', 'v': 'xiju'}, {'n': '动作冒险', 'v': 'dongzuomaoxian'}, {'n': '科幻&奇幻', 'v': 'kehuanqihuan'},
                        {'n': '家庭', 'v': 'jiating'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '中国大陆', 'v': 'cn'}, {'n': '美国', 'v': 'us'},
                        {'n': '日本', 'v': 'jp'}]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}]}
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
                if vod_pic == '/api/images/init':
                    vod_pic = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg'
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': ''
                })
            return {'list': d[:10], 'parse': 0, 'jx': 0}
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
            pagecount = (total + 23) // 24 if total > 0 else 999
            return {'list': d, 'page': int(page), 'pagecount': pagecount, 'limit': 24, 'total': total}
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {'list': d, 'page': int(page), 'pagecount': 999, 'limit': 24, 'total': 0}

    def detailContent(self, did):
        ids = did[0]  # 假設傳入的是 /vod/detail/se4pnjL1IF6D
        video_list = []
        detail_url = f"{self.home_url}{ids}"
        play_url_base = f"{self.home_url}/vod/play-thrid{ids.split('/detail')[1]}"  # 轉換為播放頁基礎 URL
        try:
            res = requests.get(detail_url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            
            if next_data:
                next_json = json.loads(next_data.group(1))
                collection_info = next_json['props']['pageProps']['collectionInfo']
                
                vod_name = collection_info.get('name', '')
                vod_year = collection_info.get('time', '')
                vod_area = collection_info.get('country', '')
                vod_content = collection_info.get('desc', '')
                vod_remarks = collection_info.get('countStr', '')
                vod_actor = ', '.join([actor['name'] for actor in collection_info.get('actor', [])])
                vod_director = ', '.join([director['name'] for director in collection_info.get('director', [])])
                vod_pic = collection_info.get('imgUrl', 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg')
                
                # 提取播放列表
                play_from = []
                play_url = []
                for group in collection_info['videosGroup']:
                    if group['name'] == '线路1':  # 僅使用线路1
                        episodes = []
                        for video in group['videos']:
                            ep_name = f"第{video['eporder']}集"
                            ep_url = f"{play_url_base}/{video['eporder']}"
                            episodes.append(f"{ep_name}${ep_url}")
                        play_from.append('華視頻')
                        play_url.append('#'.join(episodes))
                        break
                
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
            return {"list": video_list}
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
        url = f"{self.home_url}{pid}"  # pid 為 /vod/play-thrid/se4pnjL1IF6D/1
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            
            if next_data:
                next_json = json.loads(next_data.group(1))
                videos_group = next_json['props']['pageProps']['collectionInfo']['videosGroup']
                ep = int(pid.split('/')[-1])  # 提取集數
                for group in videos_group:
                    if group['name'] == '线路1':  # 僅使用线路1
                        for video in group['videos']:
                            if video['eporder'] == ep:
                                return {
                                    'url': video['purl'],
                                    'header': json.dumps(self.headers),
                                    'parse': 0,
                                    'jx': 0
                                }
            # 如果未找到，直接從 video 標籤提取
            play_url = root.xpath('//video[@id="hlove-player"]/@src')
            if play_url:
                return {
                    'url': play_url[0],
                    'header': json.dumps(self.headers),
                    'parse': 0,
                    'jx': 0
                }
            return {'url': '', 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': '', 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

if __name__ == '__main__':
    pass