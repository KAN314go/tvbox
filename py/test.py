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
import time
import random
from fake_useragent import UserAgent
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "GimyCC_Test"

    def init(self, extend):
        self.home_url = 'https://gimy.la'
        ua = UserAgent()
        self.headers = {
            "User-Agent": ua.random
        }
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        try:
            # 如果需要指定 ChromeDriver 路徑，取消註釋並修改
            # self.driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=chrome_options)
            self.driver = webdriver.Chrome(options=chrome_options)
            print("WebDriver 初始化成功")
        except Exception as e:
            print(f"WebDriver 初始化失敗: {str(e)}")
            raise

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        print("調用 homeContent")
        return {'list': [], 'parse': 0, 'jx': 0}

    def homeVideoContent(self):
        print("調用 homeVideoContent")
        return {'list': [], 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        print(f"調用 categoryContent: cid={cid}, page={page}")
        return {'list': [], 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0] if isinstance(did, list) else did
        print(f"調用 detailContent: ids={ids}")
        try:
            url = f'{self.home_url}/detail/{ids}.html'
            print(f"正在訪問: {url}")
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "slide-info")]'))
            )
            html = self.driver.page_source
            with open('detail_debug.html', 'w', encoding='utf-8') as f:
                f.write(html)
            root = etree.HTML(html)

            vod_name = root.xpath('//h3[@class="slide-info-title"]/text()')
            vod_name = vod_name[0].strip() if vod_name else "測試影片"

            # 模擬返回簡單數據
            video_item = {
                'type_name': '',
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_remarks': '測試備註',
                'vod_year': '2025',
                'vod_area': '中國',
                'vod_actor': '測試演員',
                'vod_director': '測試導演',
                'vod_content': '這是一個測試描述',
                'vod_play_from': '測試線路1$$$測試線路2',
                'vod_play_url': '第1集$/play/{}-1-1.html#第2集$/play/{}-1-2.html$$$第1集$/play/{}-2-1.html#第2集$/play/{}-2-2.html'.format(ids, ids, ids, ids)
            }
            print(f"detailContent 成功返回: {vod_name}")
            return {"list": [video_item], 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"detailContent 錯誤: {str(e)}")
            # 返回模擬數據作為後備
            video_item = {
                'vod_id': ids,
                'vod_name': '模擬影片',
                'vod_play_from': '模擬線路',
                'vod_play_url': '第1集$/play/{}-1-1.html'.format(ids)
            }
            return {'list': [video_item], 'parse': 0, 'jx': 0, 'msg': f"Error: {str(e)}"}
        finally:
            self.driver.quit()

    def searchContent(self, key, quick, page='1'):
        print(f"調用 searchContent: key={key}, page={page}")
        return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        print(f"調用 playerContent: flag={flag}, pid={pid}")
        try:
            play_url = f'{self.home_url}{pid}'
            print(f"正在解析播放地址: {play_url}")
            res = requests.get(play_url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)
            script_content = ''.join(root.xpath('//script/text()'))
            with open('player_debug.html', 'w', encoding='utf-8') as f:
                f.write(res.text)
            m3u8_url = re.search(r"url:\s*['\"](https?://[^'\"]+?\.m3u8)['\"]", script_content)
            if m3u8_url:
                print(f"找到 m3u8 地址: {m3u8_url.group(1)}")
                return {'url': m3u8_url.group(1), 'parse': 0, 'jx': 0}
            print("未找到 m3u8 地址，檢查 player_debug.html")
            # 模擬返回測試播放地址
            return {'url': 'https://example.com/test.m3u8', 'parse': 0, 'jx': 0, 'msg': '模擬播放地址'}
        except Exception as e:
            print(f"playerContent 錯誤: {str(e)}")
            # 返回模擬播放地址作為後備
            return {'url': 'https://example.com/test.m3u8', 'parse': 0, 'jx': 0, 'msg': f"Error: {str(e)}"}

    def localProxy(self, params):
        print(f"調用 localProxy: params={params}")
        pass

    def destroy(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        print("Spider 已銷毀")
        return '正在Destroy'

    def get_data(self, url):
        print(f"調用 get_data: url={url}")
        return []

if __name__ == "__main__":
    # 測試運行
    spider = Spider()
    spider.init({})

    # 測試 detailContent
    print("測試 detailContent:")
    result = spider.detailContent(['260933'])
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 測試 playerContent
    print("\n測試 playerContent:")
    play_result = spider.playerContent("測試線路1", "/play/260933-1-1.html", [])
    print(json.dumps(play_result, ensure_ascii=False, indent=2))

    spider.destroy()