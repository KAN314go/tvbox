# coding=utf-8
# !/usr/bin/python

import sys
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        print("調用 getName")
        return "GimyCC_SimpleTest"

    def init(self, extend):
        print("調用 init: extend={}".format(extend))

    def getDependence(self):
        print("調用 getDependence")
        return []

    def homeContent(self, filter):
        print("調用 homeContent: filter={}".format(filter))
        return {'list': [], 'parse': 0, 'jx': 0}

    def homeVideoContent(self):
        print("調用 homeVideoContent")
        return {'list': [], 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        print("調用 categoryContent: cid={}, page={}, filter={}, ext={}".format(cid, page, filter, ext))
        return {'list': [], 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0] if isinstance(did, list) else did
        print("調用 detailContent: ids={}".format(ids))
        video_item = {
            'vod_id': ids,
            'vod_name': '測試影片',
            'vod_remarks': '測試備註',
            'vod_year': '2025',
            'vod_area': '測試地區',
            'vod_actor': '測試演員',
            'vod_director': '測試導演',
            'vod_content': '這是一個測試影片描述',
            'vod_play_from': '測試線路',
            'vod_play_url': '第1集$/test/{}-1-1.m3u8'.format(ids)  # 模擬播放地址
        }
        print("detailContent 返回測試數據")
        return {"list": [video_item], 'parse': 0, 'jx': 0}

    def searchContent(self, key, quick, page='1'):
        print("調用 searchContent: key={}, quick={}, page={}".format(key, quick, page))
        return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        print("調用 playerContent: flag={}, pid={}, vipFlags={}".format(flag, pid, vipFlags))
        play_url = 'https://example.com/test.m3u8'  # 模擬真實播放地址
        print("playerContent 返回模擬播放地址: {}".format(play_url))
        return {'url': play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        print("調用 localProxy: params={}".format(params))
        pass

    def destroy(self):
        print("調用 destroy")
        return '正在Destroy'

if __name__ == "__main__":
    spider = Spider()
    spider.init({})

    # 測試 detailContent
    print("測試 detailContent:")
    result = spider.detailContent(['260933'])
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 測試 playerContent
    print("\n測試 playerContent:")
    play_result = spider.playerContent("測試線路", "/test/260933-1-1.m3u8", [])
    print(json.dumps(play_result, ensure_ascii=False, indent=2))

    spider.destroy()