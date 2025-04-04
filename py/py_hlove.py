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
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        }

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
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=10)
            res.encoding = 'utf-8'
            print(f"Debug: homeContent response status = {res.status_code}")
            # 這裡假設首頁有推薦分類，實際需根據網站結構調整
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
                ]
            }
            return result
        except Exception as e:
            print(f"Error in homeContent: {e}")
            return {'class': []}

    def homeVideoContent(self):
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=10)
            res.encoding = 'utf-8'
            print(f"Debug: homeVideoContent response status = {res.status_code}, length = {len(res.text)}")
            # 假設首頁有推薦影片，需根據實際結構解析
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            if next_data:
                next_json = json.loads(next_data.group(1))
                print(f"Debug: homeVideoContent __NEXT_DATA__ found, keys = {list(next_json.keys())}")
                # 這裡需根據實際數據結構提取推薦內容
                return {'list': []}  # 暫時返回空列表，需完善
            return {'list': []}
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': []}

    def categoryContent(self, cid, page, filter, ext):
        # 待實現，根據分類 ID 返回內容
        return {'list': []}

    def detailContent(self, did):
        ids = did[0]  # 如 /vod/detail/se4pnjL1IF6D
        video_list = []
        detail_url = f"{self.home_url}{ids}"
        try:
            res = requests.get(detail_url, headers=self.headers, timeout=10)
            res.encoding = 'utf-8'
            print(f"Debug: detailContent URL = {detail_url}, status = {res.status_code}, length = {len(res.text)}")
            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', res.text)
            
            if not next_data:
                print("Error: __NEXT_DATA__ not found in response")
                return {'list': [], 'msg': '__NEXT_DATA__ not found'}
            
            next_json = json.loads(next_data.group(1))
            print(f"Debug: detailContent __NEXT_DATA__ keys = {list(next_json.keys())}")
            collection_info = next_json['props']['pageProps'].get('collectionInfo', {})
            if not collection_info:
                print("Error: collectionInfo not found in __NEXT_DATA__")
                return {'list': [], 'msg': 'collectionInfo missing'}
            
            vod_name = collection_info.get('name', '')
            vod_year = collection_info.get('time', '')
            vod_area = collection_info.get('country', '')
            vod_content = collection_info.get('desc', '')
            vod_remarks = collection_info.get('countStr', '')
            vod_actor = ', '.join([actor['name'] for actor in collection_info.get('actor', [])])
            vod_director = ', '.join([director['name'] for director in collection_info.get('director', [])])
            vod_pic = collection_info.get('imgUrl', 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg')
            is_movie = collection_info.get('isMovie', False)
            
            play_from = []
            play_url = []
            for group in collection_info.get('videosGroup', []):
                if not group.get('videos'):
                    print(f"Debug: Skipping empty group['name'] = {group.get('name', 'N/A')}")
                    continue
                print(f"Debug: group['name'] = {group.get('name', 'N/A')}, videos count = {len(group['videos'])}")
                if is_movie:
                    video = group['videos'][0]
                    play_from.append(group.get('name', '线路1'))
                    play_url.append(f"{vod_name}${video['purl']}")
                    break
                else:
                    episodes = []
                    for video in group['videos']:
                        ep_name = f"第{video['eporder']}集" if video.get('eporder') else vod_name
                        ep_url = video['purl']
                        episodes.append(f"{ep_name}${ep_url}")
                    if episodes:
                        play_from.append(group.get('name', '线路1'))
                        play_url.append('#'.join(episodes))
            
            if not play_from:
                print("Error: No valid play sources found")
                return {'list': [], 'msg': 'No valid play sources found'}
            
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
        return {'list': []}

    def playerContent(self, flag, pid, vipFlags):
        try:
            if '$' in pid:
                play_url = pid.split('$')[1]
            else:
                play_url = pid
            print(f"Debug: Playing URL = {play_url}")
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
    print("Testing homeContent:")
    print(json.dumps(spider.homeContent(False), ensure_ascii=False, indent=2))
    print("Testing homeVideoContent:")
    print(json.dumps(spider.homeVideoContent(), ensure_ascii=False, indent=2))
    print("Testing detailContent:")
    result = spider.detailContent(['/vod/detail/se4pnjL1IF6D'])
    print(json.dumps(result, ensure_ascii=False, indent=2))