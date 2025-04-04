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
        # 同前略
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
            # filters 略
        }
        return result

    def homeVideoContent(self):
        # 同前略
        pass

    def categoryContent(self, cid, page, filter, ext):
        # 同前略
        pass

    def detailContent(self, did):
        ids = did[0]  # 假設傳入的是 /vod/detail/se4pnjL1IF6D
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
                vod_pic = collection_info.get('imgUrl', 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg')
                is_movie = collection_info.get('isMovie', False)
                
                # 提取播放線路和集數
                play_from = []
                play_url = []
                for group in collection_info['videosGroup']:
                    if not group.get('videos'):  # 跳過無視頻的線路
                        continue
                    print(f"Debug: group['name'] = {group.get('name', 'N/A')}, videos count = {len(group['videos'])}")
                    if is_movie:
                        # 電影只取第一個有效線路的第一個視頻
                        video = group['videos'][0]
                        play_from.append("线路1")
                        play_url.append(f"{vod_name}${video['purl']}")
                        break
                    else:
                        # 連續劇處理多集
                        episodes = []
                        for video in group['videos']:
                            ep_name = f"第{video['eporder']}集" if video.get('eporder') else vod_name
                            ep_url = video['purl']
                            episodes.append(f"{ep_name}${ep_url}")
                        play_from.append("线路1")
                        play_url.append('#'.join(episodes))
                        break  # 只取第一個有效線路
                
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
        # 同前略
        pass

    def playerContent(self, flag, pid, vipFlags):
        # pid 格式為 "第X集$https://m3u8.heimuertv.com/play/xxx.m3u8"
        try:
            if '$' in pid:
                play_url = pid.split('$')[1]  # 提取 URL 部分
            else:
                play_url = pid  # 若無 $ 分隔，直接使用 pid
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
    # 測試連續劇 detailContent
    result = spider.detailContent(['/vod/detail/se4pnjL1IF6D'])
    print(json.dumps(result, ensure_ascii=False, indent=2))