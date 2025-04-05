# -*- coding: utf-8 -*-
# @Author  : Adapted for 泥視頻.CC as CatVod Interface
# @Time    : 2025/04/05

import sys
import requests
from lxml import etree
import json
from urllib.parse import urlparse
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        self.home_url = 'https://www.nivod.cc'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Referer": "https://www.nivod.cc/",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        }
        self.placeholder_pic = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/placeholder.jpg'

    def init(self, extend=""):
        pass

    def getName(self):
        return "泥視頻.CC"

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        return url.endswith('.m3u8') or url.endswith('.mp4')

    def manualVideoCheck(self):
        return False

    def homeContent(self, filter):
        categories = "電影$movie#電視劇$tv#綜藝$show#動漫$anime"
        class_list = [{'type_id': v.split('$')[1], 'type_name': v.split('$')[0]} for v in categories.split('#')]
        filters = {
            'movie': [
                {'key': 'class', 'name': '剧情', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "冒险$mao-xian#剧情$ju-qing#动作$dong-zuo#同性$tong-xing#喜剧$xi-ju#奇幻$qi-huan#恐怖$kong-bu#悬疑$xuan-yi#惊悚$jing-song#战争$zhan-zheng#歌舞$ge-wu#灾难$zai-nan#爱情$ai-qing#犯罪$fan-zui#科幻$ke-huan".split('#')]},
                {'key': 'area', 'name': '地区', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "大陆$cn#香港$hk#台湾$tw#欧美$west#泰国$th#新马$sg-my#其他$other".split('#')]},
                {'key': 'year', 'name': '年份', 'value': [{'n': v, 'v': v} for v in ["2025", "2024", "2023", "2022", "2021", "2020", "2019-2010", "2009-2000", "90年代", "80年代", "更早"]]}
            ],
            'tv': [
                {'key': 'class', 'name': '剧情', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "剧情$ju-qing#动作$dong-zuo#历史$li-shi#历险$mao-xian#古装$gu-zhuang#同性$tong-xing#喜剧$xi-ju#奇幻$qi-huan#家庭$jia-ting#悬疑$xuan-yi#惊悚$zhan-zheng#战争$zhan-zheng#武侠$wu-xia#爱情$ai-qing#科幻$ke-huan#罪案$zui-an".split('#')]},
                {'key': 'area', 'name': '地区', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "大陆$cn#香港$hk#台湾$tw#日本$jp#韩国$kr#欧美$west#泰国$th#新马$sg-my".split('#')]},
                {'key': 'year', 'name': '年份', 'value': [{'n': v, 'v': v} for v in ["2025", "2024", "2023", "2022", "2021", "2020", "2019-2015", "2014-2010", "2009-2000", "90年代", "80年代", "更早"]]}
            ],
            'show': [
                {'key': 'class', 'name': '剧情', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "搞笑$gao-xiao#音乐$yin-yue#真人秀$zhen-ren-xiu#脱口秀$tuo-kou-xiu".split('#')]},
                {'key': 'area', 'name': '地区', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "大陆$cn#韩国$kr#欧美$west#其它$other".split('#')]},
                {'key': 'year', 'name': '年份', 'value': [{'n': v, 'v': v} for v in ["2025", "2024", "2023", "2022", "2021", "2020", "2019-2015", "2014-2010", "2009-2000", "90年代", "80年代", "更早"]]}
            ],
            'anime': [
                {'key': 'class', 'name': '剧情', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "冒险$mao-xian#动画电影$movie#推理$tui-li#校园$xiao-yuan#治愈$zhi-yu#泡面$pao-mian#热血$re-xue#科幻$ke-huan#魔幻$mo-huan".split('#')]},
                {'key': 'area', 'name': '地区', 'value': [{'n': v.split('$')[0], 'v': v.split('$')[1]} for v in "大陆$cn#日本$jp#欧美$west".split('#')]},
                {'key': 'year', 'name': '年份', 'value': [{'n': v, 'v': v} for v in ["2025", "2024", "2023", "2022", "2021", "2020", "2019-2015", "2014-2010", "2009-2000", "90年代", "80年代", "更早"]]}
            ]
        }
        result = {
            'class': class_list,
            'filters': filters if filter else {}
        }
        return result

    def homeVideoContent(self):
        result = {'list': []}
        try:
            res = requests.get(self.home_url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "qy-mod-link-wrap")]/a')
            for i in data_list:
                vod_name = i.xpath('.//text()')[0].strip() if i.xpath('.//text()') else "未知"
                vod_id = i.get('href', '')
                vod_pic = self.placeholder_pic
                result['list'].append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': ''
                })
            result['list'] = result['list'][:10]
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
        return result

    def categoryContent(self, tid, pg, filter, ext):
        result = {'list': []}
        _year = ext.get('year', '')
        _class = ext.get('class', '')
        _area = ext.get('area', '')
        url = f"{self.home_url}/filter.html?channel={tid}&region={_area}&showtype={_class}&year={_year}&page={pg}"
        
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//a[contains(@class, "qy-mod-link")]')
            for i in data_list:
                vod_name = i.xpath('.//span[contains(@class, "qy-mod-text")]/text()')[0].strip() if i.xpath('.//span[contains(@class, "qy-mod-text")]') else "未知"
                vod_id = i.get('href', '')
                vod_pic = i.xpath('.//img/@src')[0] if i.xpath('.//img/@src') else self.placeholder_pic
                vod_remarks = i.xpath('.//span[contains(@class, "qy-mod-label")]/text()')[0] if i.xpath('.//span[contains(@class, "qy-mod-label")]') else ''
                result['list'].append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            result['page'] = int(pg)
            result['pagecount'] = 999  # 假設最大頁數，實際可根據網站調整
            result['limit'] = 24
            result['total'] = len(data_list)
        except Exception as e:
            print(f"Error in categoryContent: {e}")
        return result

    def detailContent(self, array):
        result = {'list': []}
        ids = array[0]
        detail_url = f"{self.home_url}{ids}"
        try:
            res = requests.get(detail_url, headers=self.headers)
            res.encoding = 'utf-8'
            if not res.ok:
                raise Exception(f"HTTP 請求失敗，狀態碼: {res.status_code}")
            
            root = etree.HTML(res.text)
            
            vod_name = root.xpath('//div[@class="right-title"]/text()')[0].strip() if root.xpath('//div[@class="right-title"]') else "未知"
            vod_year = root.xpath('//div[@id="postYear"]/text()')[0].strip() if root.xpath('//div[@id="postYear"]') else ""
            vod_area = root.xpath('//div[@id="region"]/text()')[0].strip() if root.xpath('//div[@id="region"]') else ""
            vod_content = root.xpath('//div[@id="show-desc"]/text()')[0].strip() if root.xpath('//div[@id="show-desc"]') else ""
            vod_remarks = root.xpath('//div[@id="updateTxt"]/text()')[0].strip() if root.xpath('//div[@id="updateTxt"]') else ""
            vod_actor = root.xpath('//div[@id="actors"]/text()')[0].strip() if root.xpath('//div[@id="actors"]') else ""
            vod_director = root.xpath('//div[@id="director"]/text()')[0].strip() if root.xpath('//div[@id="director"]') else ""
            vod_pic = root.xpath('//img[@class="left-img"]/@src')[0] if root.xpath('//img[@class="left-img"]') else self.placeholder_pic
            
            # 提取播放列表
            play_from = ["泥視頻"]
            play_url = []
            episodes = root.xpath('//div[@id="list-jj"]/a')
            if not episodes:
                print("未找到播放列表，可能頁面結構不匹配")
            for ep in episodes[::-1]:
                ep_name = ep.xpath('.//div[@class="item"]/text()')[0].strip() if ep.xpath('.//div[@class="item"]') else "未知"
                ep_url = self.home_url + ep.get('href', '')
                play_url.append(f"{ep_name}${ep_url}")
            
            vod = {
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_pic': vod_pic,
                'type_name': '',  # 可根據實際分類填充
                'vod_year': vod_year,
                'vod_area': vod_area,
                'vod_remarks': vod_remarks,
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_play_from': '$$$'.join(play_from),
                'vod_play_url': '$$$'.join(play_url) if play_url else ""
            }
            result['list'].append(vod)
        except Exception as e:
            print(f"Error in detailContent: {e}")
            result['list'].append({
                'vod_id': ids,
                'vod_name': '未知',
                'vod_pic': self.placeholder_pic,
                'vod_play_from': '泥視頻',
                'vod_play_url': ''
            })
        return result

    def searchContent(self, key, quick, pg='1'):
        result = {'list': []}
        try:
            search_url = f"{self.home_url}/search_x.html?keyword={key}&page={pg}"
            res = requests.get(search_url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//a[contains(@class, "qy-mod-link")]')
            
            for item in data_list:
                vod_name = item.xpath('.//span[contains(@class, "qy-mod-text")]/text()')[0].strip() if item.xpath('.//span[contains(@class, "qy-mod-text")]') else "未知"
                vod_id = item.get('href', '')
                vod_pic = item.xpath('.//img/@src')[0] if item.xpath('.//img/@src') else self.placeholder_pic
                vod_remarks = ''
                result['list'].append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
        except Exception as e:
            print(f"Error in searchContent: {e}")
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        try:
            if '/vodplay' not in id:
                raise Exception("無效的播放 URL")
            
            parsed_url = urlparse(id)
            path_parts = parsed_url.path.split('/')
            vod_id = path_parts[2]  # "202552243"
            ep_id = path_parts[3]   # "ep15"
            xhr_url = f"{self.home_url}/xhr_playinfo/{vod_id}-{ep_id}"
            
            print(f"正在請求播放信息: {xhr_url}")
            res = requests.get(xhr_url, headers=self.headers)
            res.encoding = 'utf-8'
            if not res.ok:
                print(f"響應內容: {res.text}")
                raise Exception(f"播放信息請求失敗，狀態碼: {res.status_code}")
            
            data = res.json()
            print(f"播放信息返回數據: {json.dumps(data, ensure_ascii=False)}")
            if 'pdatas' not in data or not data['pdatas']:
                raise Exception("未找到播放數據")
            
            # 返回第一條線路的播放地址
            play_url = data['pdatas'][0]['playurl']
            result = {
                'url': play_url,
                'header': json.dumps(self.headers),
                'parse': 0,  # 直接播放 .m3u8，不需解析
                'playUrl': ''  # 若需要代理播放，可在此設置
            }
        except Exception as e:
            print(f"Error in playerContent: {e}")
            result = {'url': '', 'parse': 0}
        return result

    def localProxy(self, param):
        return [200, "video/MP2T", {}, b""]

    def destroy(self):
        pass

if __name__ == '__main__':
    spider = Spider()
    # 測試 homeContent
    home = spider.homeContent(True)
    print("homeContent:", json.dumps(home, ensure_ascii=False, indent=2))
    
    # 測試 detailContent
    detail = spider.detailContent(['/voddetail/202552243'])
    print("detailContent:", json.dumps(detail, ensure_ascii=False, indent=2))
    
    # 測試 playerContent
    player = spider.playerContent("泥視頻", "https://www.nivod.cc/vodplay/202552243/ep15", None)
    print("playerContent:", json.dumps(player, ensure_ascii=False, indent=2))