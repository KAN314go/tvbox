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
        return "華視界"

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        # 從 ext 中動態生成分類和篩選選項
        categories = "电影$movie#电视剧$drama#动漫$animation#综艺$variety#儿童$children"
        classes = "全部$all#劇情$juqing#喜劇$xiju#懸疑$xuanyi#都市$dushi#罪案$zuian"  # 根據需求擴展
        areas = "全部$all#大陸$cn#美國$us#韓國$kr#日本$jp#臺灣$tw#香港$hk#英國$gb"
        years = "all&2025&2024&2023&2022&2021&2020&2010&2000&1990&1980&1970"

        class_list = [{'type_id': v.split('$')[1], 'type_name': v.split('$')[0]} for v in categories.split('#')]
        filters = {
            'movie': [
                {'name': '剧情', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v, 'v': v} for v in years.split('&')]}
            ],
            'drama': [
                {'name': '剧情', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v, 'v': v} for v in years.split('&')]}
            ],
            'animation': [
                {'name': '剧情', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v, 'v': v} for v in years.split('&')]}
            ],
            'variety': [
                {'name': '剧情', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v, 'v': v} for v in years.split('&')]}
            ],
            'children': [
                {'name': '剧情', 'key': 'class', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in classes.split('#')]},
                {'name': '地区', 'key': 'area', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in areas.split('#')]},
                {'name': '年份', 'key': 'year', 'value': [{'n': v, 'v': v} for v in years.split('&')]}
            ]
        }
        return {'class': class_list, 'filters': filters}

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
                vod_pic = i.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')[0] if i.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src') else self.placeholder_pic
                if vod_pic == '/api/images/init':
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
        _year = ext.get('year', 'all')
        _class = ext.get('class', 'all')  # 使用 'class' 代替 'tag'，與配置一致
        _area = ext.get('area', 'all')
        # 使用分段 URL 格式
        url = f"{self.home_url}/{cid}/{_year}/{_class}/{_area}"
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
            init_cards = []
            if next_data:
                next_json = json.loads(next_data.group(1))
                init_cards = next_json['props']['pageProps'].get('initCard', [])
                total = next_json['props']['pageProps'].get('total', len(data_list))
            
            for i, card in enumerate(data_list):
                vod_name = card.xpath('.//div[contains(@class, "h-film-listall_name__Gyb9x")]/text()')[0].strip()
                vod_id = card.get('href', '')
                # 優先從 HTML 提取圖片
                vod_pic_list = card.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')
                vod_pic = vod_pic_list[0] if vod_pic_list else None
                if not vod_pic or vod_pic == '/api/images/init':
                    # 若 HTML 失敗，從 init_cards 提取
                    vod_pic = init_cards[i]['img'] if i < len(init_cards) and 'img' in init_cards[i] else self.placeholder_pic
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
                vod_pic = i.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src')[0] if i.xpath('.//img[contains(@class, "h-film-listall_img__jiamS")]/@src') else self.placeholder_pic
                if vod_pic == '/api/images/init':
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
    result = spider.categoryContent('drama', '1', True, {'year': '2025', 'class': 'xuanyi', 'area': 'us'})
    print(json.dumps(result, ensure_ascii=False, indent=2))