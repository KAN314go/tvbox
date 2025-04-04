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
    def __init__(self):
        self.home_url = 'https://hlove.tv'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://hlove.tv/",
        }
        self.placeholder_pic = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg'

    def init(self, extend):
        pass

    def getName(self):
        return "華視頻"

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
                'movie': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '动作', 'v': 'dongzuo'}, {'n': '喜剧', 'v': 'xiju'},
                        {'n': '爱情', 'v': 'aiqing'}, {'n': '科幻', 'v': 'kehuan'}, {'n': '恐怖', 'v': 'kongbu'},
                        {'n': '剧情', 'v': 'juqing'}, {'n': '战争', 'v': 'zhanzheng'}, {'n': '罪案', 'v': 'zuian'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '中国大陆', 'v': 'cn'}, {'n': '美国', 'v': 'us'},
                        {'n': '韩国', 'v': 'kr'}, {'n': '香港', 'v': 'hk'}, {'n': '台湾', 'v': 'tw'},
                        {'n': '日本', 'v': 'jp'}, {'n': '英国', 'v': 'gb'}, {'n': '泰国', 'v': 'th'}]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, {'n': '2019-2010', 'v': '2010'}]}
                ],
                'drama': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '古装', 'v': 'guzhuang'}, {'n': '偶像', 'v': 'ouxiang'},
                        {'n': '家庭', 'v': 'jiating'}, {'n': '悬疑', 'v': 'xuanyi'}, {'n': '都市', 'v': 'dushi'},
                        {'n': '罪案', 'v': 'zuian'}]},
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
                ],
                'documentary': [
                    {'name': '分类', 'key': 'tag', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '历史', 'v': 'lishi'}, {'n': '自然', 'v': 'ziran'},
                        {'n': '科学', 'v': 'kexue'}, {'n': '传记', 'v': 'zhuanji'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': 'all'}, {'n': '中国大陆', 'v': 'cn'}, {'n': '美国', 'v': 'us'},
                        {'n': '英国', 'v': 'gb'}]},
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
                if vod_pic == '/api/images/init' or not vod_pic:
                    vod_pic = self.placeholder_pic
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
        # 修復篩選參數名稱（假設網站使用 'category' 而非 'tag'，需根據實際情況調整）
        url = f"{self.home_url}/{cid}"
        params = []
        if _year != 'all':
            params.append(f"year={_year}")
        if _tag != 'all':
            params.append(f"category={_tag}")  # 改用 'category'，若不正確請調整
        if _area != 'all':
            params.append(f"area={_area}")
        if page != '1':
            params.append(f"page={page}")
        if params:
            url += '?' + '&'.join(params)
        
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
                init_cards = next_json['props']['pageProps'].get('initCard', [])
                total = next_json['props']['pageProps'].get('total', 0)
                for i, card in enumerate(data_list):
                    vod_name = card.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                    vod_id = card.get('href', '')
                    # 優先從 init_cards 提取圖片，否則從 HTML 提取
                    vod_pic = init_cards[i]['img'] if i < len(init_cards) and 'img' in init_cards[i] else \
                              card.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')[0] if card.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src') else self.placeholder_pic
                    if vod_pic == '/api/images/init' or not vod_pic:
                        vod_pic = self.placeholder_pic
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
        detail_url = f"{self.home_url}{ids}"
        try:
            res = requests.get(detail_url, headers=self.headers)
            res.encoding = 'utf-8'
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
                vod_pic = collection_info.get('imgUrl', self.placeholder_pic)
                is_movie = collection_info.get('isMovie', False)
                
                play_from = []
                play_url = []
                for group in collection_info['videosGroup']:
                    if not group.get('videos'):
                        continue
                    line_name = group.get('name', '线路1')
                    if is_movie:
                        video = group['videos'][0]
                        play_from.append(line_name)
                        play_url.append(f"{vod_name}${video['purl']}")
                        break
                    else:
                        episodes = []
                        for video in group['videos']:
                            ep_name = f"第{video['eporder']}集"
                            ep_url = video['purl']
                            episodes.append(f"{ep_name}${ep_url}")
                        play_from.append(line_name)
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
                if vod_pic == '/api/images/init' or not vod_pic:
                    vod_pic = self.placeholder_pic
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
        try:
            play_url = pid
            return {
                'url': play_url,
                'header': json.dumps(self.headers),
                'parse': 0,
                'jx': 0
            }
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': '', 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

if __name__ == '__main__':
    spider = Spider()
    # 測試連續劇詳情
    result = spider.detailContent(['/vod/play-thrid/9b1169e9b7c04/1'])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # 測試篩選功能
    result = spider.categoryContent('drama', '1', True, {'tag': 'xuanyi', 'area': 'us', 'year': '2025'})
    print(json.dumps(result, ensure_ascii=False, indent=2))