# -*- coding: utf-8 -*-
# @Author  : Adapted for 華視頻
# @Time    : 2025/04/06

import sys
import requests
from lxml import etree
import re
import json
from flask import Flask, jsonify  # 新增 Flask 支持
sys.path.append('..')
from base.spider import Spider

app = Flask(__name__)  # 初始化 Flask 應用

class Spider(Spider):
    def __init__(self):
        self.home_url = 'https://hlove.tv'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://hlove.tv/",
        }
        self.default_pic = 'https://hlove.tv/api/images/default'  # 使用網站默認圖片

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
        # 主類別（頂部導航）
        categories = "电影$movie#电视剧$drama#动漫$animation#综艺$variety#儿童$children"
        class_list = [{'type_id': v.split('$')[1], 'type_name': v.split('$')[0]} for v in categories.split('#')]
        filters = {}  # 簡化測試，實際應保留原篩選條件
        return {'class': class_list, 'filters': filters}

    def fetch_home_page(self):
        """獲取首頁數據（無緩存，簡化測試）"""
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
                return {'list': d, 'parse': 0, 'jx': 0}

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
                        vod_pic = card.get('img', self.default_pic)  # 直接使用網站默認圖片
                        vod_remarks = card.get('countStr', section_title)  # 若無 countStr，使用分類名稱

                        if not vod_id or not vod_name:
                            continue

                        if vod_pic == '/api/images/init':
                            vod_pic = self.default_pic

                        d.append({
                            'vod_id': vod_id,
                            'vod_name': vod_name,
                            'vod_pic': vod_pic,
                            'vod_remarks': vod_remarks
                        })

            # 去重並返回
            unique_d = {item['vod_id']: item for item in d if item['vod_id']}.values()
            print(f"最終返回 {len(unique_d)} 個影片")
            return {'list': list(unique_d), 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}

    # Flask 接口
    @app.route('/api/home', methods=['GET'])
    def api_home():
        spider = Spider()
        result = spider.homeVideoContent()
        return jsonify(result)

    @app.route('/api/detail', methods=['GET'])
    def api_detail():
        # 簡單示例，實際應實現 detailContent
        return jsonify({'list': []})

if __name__ == "__main__":
    # 運行 Flask 服務器
    app.run(host='0.0.0.0', port=5000, debug=True)
    # 單獨測試時可取消註釋以下行
    # spider = Spider()
    # result = spider.homeVideoContent()
    # print(result)