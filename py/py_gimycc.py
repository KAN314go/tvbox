# coding=utf-8
# !/usr/bin/python

import sys
import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "GimyCC"

    def init(self, extend):
        self.home_url = 'https://gimy.la'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
        self.driver = webdriver.Chrome(options=chrome_options)

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        return {'list': [], 'parse': 0, 'jx': 0}

    def homeVideoContent(self):
        data = self.get_data(self.home_url)
        return {'list': data, 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        _area = ext.get('area', '')
        _year = ext.get('year', '')
        _by = ext.get('by', '')
        url = f'{self.home_url}/filter/{cid}-{_area}-{_year}-{_by}/page/{page}.html'
        data = self.get_data(url)
        return {'list': data, 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0] if isinstance(did, list) else did
        video_list = []
        try:
            url = f'{self.home_url}/detail/{ids}.html'
            self.driver.get(url)
            # 等待播放線路和詳情內容加載
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "anthology-tab")]//a | //div[contains(@class, "slide-info")]'))
            )
            html = self.driver.page_source
            root = etree.HTML(html)

            # 調試：輸出原始 HTML 以確認結構
            with open('debug.html', 'w', encoding='utf-8') as f:
                f.write(html)

            # 提取影片名稱
            vod_name = root.xpath('//h3[@class="slide-info-title"]/text()')
            if not vod_name:
                vod_name = root.xpath('//title/text()')
                vod_name = vod_name[0].split(' - ')[0].strip() if vod_name else '未知名稱'

            # 提取年份
            vod_year = root.xpath('//div[@class="slide-info"]//a[contains(@href, "/search/year/")]/text()')
            vod_year = vod_year[0].strip() if vod_year else '2025'

            # 提取地區
            vod_area = root.xpath('//div[@class="slide-info"]//a[contains(@href, "/search/area/")]/text()')
            vod_area = vod_area[0].strip() if vod_area else '中國'

            # 提取導演（更靈活的匹配）
            vod_director = root.xpath('//div[contains(@class, "slide-info") and contains(., "導演")]//a/text()')
            if not vod_director:
                vod_director = root.xpath('//strong[contains(text(), "導演")]/following-sibling::a/text()')
            vod_director = ','.join([director.strip() for director in vod_director if director.strip()]) if vod_director else '未知'

            # 提取演員（更靈活的匹配）
            vod_actor = root.xpath('//div[contains(@class, "slide-info") and contains(., "演員")]//a/text()')
            if not vod_actor:
                vod_actor = root.xpath('//strong[contains(text(), "演員")]/following-sibling::a/text()')
            vod_actor = ','.join([actor.strip() for actor in vod_actor if actor.strip()]) if vod_actor else '未知'

            # 提取劇情
            vod_content = root.xpath('//meta[@name="description"]/@content')
            vod_content = vod_content[0].strip() if vod_content else ''.join(root.xpath('//div[@id="height_limit"]/text()'))

            # 提取播放線路名稱
            play_from_list = root.xpath('//div[contains(@class, "anthology-tab")]//a/text()')
            vod_play_from = '$$$'.join([name.strip().replace('\xa0', '') for name in play_from_list if name.strip()]) if play_from_list else '默認線路'

            # 提取每個線路的選集
            play_list_boxes = root.xpath('//div[contains(@class, "anthology-list-box")]')
            vod_play_url = []
            for box in play_list_boxes:
                name_list = box.xpath('.//ul[contains(@class, "anthology-list-play")]/li/a/text()')
                url_list = box.xpath('.//ul[contains(@class, "anthology-list-play")]/li/a/@href')
                if len(name_list) != len(url_list):
                    min_length = min(len(name_list), len(url_list))
                    name_list = name_list[:min_length]
                    url_list = url_list[:min_length]
                play_url = '#'.join([f"{name}${self.home_url}{url}" for name, url in zip(name_list, url_list)])
                if play_url:
                    vod_play_url.append(play_url)

            # 組合數據
            video_item = {
                'type_name': '',
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_remarks': '',
                'vod_year': vod_year,
                'vod_area': vod_area,
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_play_from': vod_play_from,
                'vod_play_url': '$$$'.join(vod_play_url) if vod_play_url else ''
            }
            video_list.append(video_item)
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in detailContent: {str(e)}")
            return {'list': [], 'msg': f"Error in detailContent: {str(e)}"}
        finally:
            self.driver.quit()

    def searchContent(self, key, quick, page='1'):
        url = f'{self.home_url}/search.html?wd={key}&page={page}'
        data = self.get_data(url)
        return {'list': data, 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        try:
            res = requests.get(f'{self.home_url}{pid}', headers=self.headers)
            root = etree.HTML(res.text)
            script_content = ''.join(root.xpath('//script/text()'))
            m3u8_url = re.search(r"url:\s*['\"](https?://[^'\"]+?\.m3u8)['\"]", script_content)
            if m3u8_url:
                return {'url': m3u8_url.group(1), 'parse': 0, 'jx': 0}
            return {'url': '', 'parse': 0, 'jx': 0, 'msg': '未找到播放鏈接'}
        except requests.RequestException as e:
            return {'url': '', 'parse': 0, 'jx': 0, 'msg': str(e)}

    def localProxy(self, params):
        pass

    def destroy(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
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
        except requests.RequestException:
            return data
        return data

if __name__ == "__main__":
    spider = Spider()
    spider.init({})
    result = spider.detailContent(['260933'])
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))