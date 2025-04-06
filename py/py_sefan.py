# -*- coding: utf-8 -*-
# @Author  : Adapted for 華視頻
# @Time    : 2025/04/06

import sys
import requests
from lxml import etree
import re
import json
from flask import Flask, jsonify

sys.path.append('..')
from base.spider import Spider

app = Flask(__name__)

class Spider(Spider):
    def __init__(self):
        self.home_url = 'https://hlove.tv'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://hlove.tv/",
        }
        self.default_pic = 'https://hlove.tv/api/images/default'

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
        categories = [
            {"type_id": "movie", "type_name": "电影"},
            {"type_id": "drama", "type_name": "电视剧"},
            {"type_id": "animation", "type_name": "动漫"},
            {"type_id": "variety", "type_name": "综艺"},
            {"type_id": "children", "type_name": "儿童"}
        ]
        return {'class': categories, 'filters': {}}

    def fetch_home_page(self):
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            return res.text
        except Exception as e:
            print(f"Error fetching home page: {e}")
            return None

    def homeVideoContent(self):
        d = []
        try:
            home_html = self.fetch_home_page()
            if not home_html:
                print("首頁 HTML 為空")
                return {'list': []}

            next_data = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', home_html)
            if next_data:
                next_json = json.loads(next_data.group(1))
                cards = next_json['props']['pageProps'].get('cards', [])
                print(f"找到 {len(cards)} 個分類區塊")
                for section in cards:
                    section_title = section.get('name', '未知分類')
                    section_cards = section.get('cards', [])
                    for card in section_cards:
                        vod_id = card.get('id', '')
                        vod_name = card.get('name', '')
                        vod_pic = card.get('img', self.default_pic)
                        vod_remarks = card.get('countStr', section_title)

                        if not vod_id or not vod_name:
                            continue

                        if vod_pic == '/api/images/init':
                            vod_pic = self.default_pic

                        # 增加 type_id 和其他可能需要的字段
                        d.append({
                            'vod_id': vod_id,
                            'vod_name': vod_name,
                            'vod_pic': vod_pic,
                            'vod_remarks': vod_remarks,
                            'type_id': self.infer_type_id(section_title),  # 推斷分類 ID
                            'vod_tag': self.infer_tag(vod_remarks)  # 推斷標籤
                        })

            unique_d = {item['vod_id']: item for item in d if item['vod_id']}.values()
            print(f"最終返回 {len(unique_d)} 個影片")
            return {'list': list(unique_d)}
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': []}

    def infer_type_id(self, section_title):
        """根據分類名稱推斷 type_id"""
        type_mapping = {
            '電影': 'movie',
            '电视剧': 'drama',
            '动漫': 'animation',
            '综艺': 'variety',
            '儿童': 'children'
        }
        for key, value in type_mapping.items():
            if key in section_title:
                return value
        return 'movie'  # 默認為電影

    def infer_tag(self, remarks):
        """根據備註推斷標籤"""
        if '更新至' in remarks:
            return 'series'
        elif '完结' in remarks:
            return 'finished'
        else:
            return 'movie'

    @app.route('/api/home', methods=['GET'])
    def api_home():
        spider = Spider()
        result = spider.homeVideoContent()
        return jsonify(result)

    @app.route('/api/detail', methods=['GET'])
    def api_detail():
        return jsonify({'list': []})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)