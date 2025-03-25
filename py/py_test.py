# -*- coding: utf-8 -*-
# @Author  : Doubebly (Modified by Grok 3 for 壹影視)
# @Time    : 2025/3/26
import json
import sys
import requests
from lxml import etree
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):
    def getName(self):
        return "壹影視"

    def init(self, extend=""):
        self.home_url = 'https://yiyiyi.tv'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://yiyiyi.tv/",
        }
        self.image_domain = "https://img.bfzypic.com"
        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'
        self.play_map = {
            '臻享蓝光': 'y1', '臻享(备)': 'z1', '臻享4K': 'bb', '蓝光': 'abc', '蓝光1': 'c1',
            '蓝光2': 'g1', '蓝光3': 'f1', '蓝光4': 't1', '极速蓝光': 'j12', '高清': 'a1',
            '极速蓝光1': 'e', '极速': 'd', '极速1': 'n', '极速2': 'v', '极速4': 'x', '优质1': 'l'
        }

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {
            'class': [
                {'type_id': '1', 'type_name': '电影'},
                {'type_id': '2', 'type_name': '电视剧'},
                {'type_id': '3', 'type_name': '综艺'},
                {'type_id': '4', 'type_name': '动漫'},
                {'type_id': '22', 'type_name': '短剧'}  # 修正為 22，與篩選頁面一致
            ],
            'filters': {
                '1': [
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '最新', 'v': 'time'}, {'n': '熱播榜', 'v': 'hits_day'}, {'n': '好評榜', 'v': 'score'}]},
                    {'key': 'class', 'name': '類型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '喜劇', 'v': '喜劇'}, {'n': '冒險', 'v': '冒險'}, {'n': '愛情', 'v': '愛情'},
                        {'n': '動畫', 'v': '動畫'}, {'n': '戰爭', 'v': '戰爭'}, {'n': '劇情', 'v': '劇情'}, {'n': '動作', 'v': '動作'},
                        {'n': '恐怖', 'v': '恐怖'}, {'n': '懸疑', 'v': '懸疑'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '災難', 'v': '災難'},
                        {'n': '同性', 'v': '同性'}, {'n': '驚悚', 'v': '驚悚'}, {'n': '歌舞', 'v': '歌舞'}, {'n': '犯罪', 'v': '犯罪'},
                        {'n': '科幻', 'v': '科幻'}, {'n': '經典', 'v': '經典'}, {'n': '網絡電影', 'v': '網絡電影'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': '大陸'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'},
                        {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}, {'n': '歐美', 'v': '歐美'}, {'n': '泰國', 'v': '泰國'},
                        {'n': '新馬', 'v': '新馬'}, {'n': '印度', 'v': '印度'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'lang', 'name': '語言', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '國語', 'v': '國語'}, {'n': '粵語', 'v': '粵語'}, {'n': '英語', 'v': '英語'},
                        {'n': '韓語', 'v': '韓語'}, {'n': '日語', 'v': '日語'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '法語', 'v': '法語'},
                        {'n': '德語', 'v': '德語'}, {'n': '泰語', 'v': '泰語'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'},
                        {'n': '2014-2011', 'v': '2014-2011'}, {'n': '2010-2000', 'v': '2010-2000'}, {'n': '90年代', 'v': '90年代'},
                        {'n': '80年代', 'v': '80年代'}, {'n': '更早', 'v': '更早'}]}
                ],
                '2': [
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '最新', 'v': 'time'}, {'n': '熱播榜', 'v': 'hits_day'}, {'n': '好評榜', 'v': 'score'}]},
                    {'key': 'class', 'name': '類型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '古裝', 'v': '古裝'}, {'n': '偶像', 'v': '偶像'}, {'n': '愛情', 'v': '愛情'},
                        {'n': '都市', 'v': '都市'}, {'n': '懸疑', 'v': '懸疑'}, {'n': '劇情', 'v': '劇情'}, {'n': '武俠', 'v': '武俠'}]},
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': '大陸'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'},
                        {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}, {'n': '歐美', 'v': '歐美'}, {'n': '泰國', 'v': '泰國'},
                        {'n': '新馬', 'v': '新馬'}, {'n': '印度', 'v': '印度'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'lang', 'name': '語言', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '國語', 'v': '國語'}, {'n': '粵語', 'v': '粵語'}, {'n': '英語', 'v': '英語'},
                        {'n': '韓語', 'v': '韓語'}, {'n': '日語', 'v': '日語'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '法語', 'v': '法語'},
                        {'n': '德語', 'v': '德語'}, {'n': '泰語', 'v': '泰語'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'},
                        {'n': '2014-2011', 'v': '2014-2011'}, {'n': '2010-2000', 'v': '2010-2000'}, {'n': '90年代', 'v': '90年代'},
                        {'n': '80年代', 'v': '80年代'}, {'n': '更早', 'v': '更早'}]}
                ],
                '3': [
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '最新', 'v': 'time'}, {'n': '熱播榜', 'v': 'hits_day'}, {'n': '好評榜', 'v': 'score'}]},
                    {'key': 'class', 'name': '類型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '真人秀', 'v': '真人秀'}, {'n': '脫口秀', 'v': '脫口秀'}, {'n': '選秀', 'v': '選秀'}]},
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': '大陸'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'},
                        {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}, {'n': '歐美', 'v': '歐美'}, {'n': '泰國', 'v': '泰國'},
                        {'n': '新馬', 'v': '新馬'}, {'n': '印度', 'v': '印度'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'lang', 'name': '語言', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '國語', 'v': '國語'}, {'n': '粵語', 'v': '粵語'}, {'n': '英語', 'v': '英語'},
                        {'n': '韓語', 'v': '韓語'}, {'n': '日語', 'v': '日語'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '法語', 'v': '法語'},
                        {'n': '德語', 'v': '德語'}, {'n': '泰語', 'v': '泰語'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'},
                        {'n': '2014-2011', 'v': '2014-2011'}, {'n': '2010-2000', 'v': '2010-2000'}, {'n': '90年代', 'v': '90年代'},
                        {'n': '80年代', 'v': '80年代'}, {'n': '更早', 'v': '更早'}]}
                ],
                '4': [
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '最新', 'v': 'time'}, {'n': '熱播榜', 'v': 'hits_day'}, {'n': '好評榜', 'v': 'score'}]},
                    {'key': 'class', 'name': '類型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '熱血', 'v': '熱血'}, {'n': '冒險', 'v': '冒險'}, {'n': '科幻', 'v': '科幻'},
                        {'n': '戀愛', 'v': '戀愛'}]},
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': '大陸'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'},
                        {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}, {'n': '歐美', 'v': '歐美'}, {'n': '泰國', 'v': '泰國'},
                        {'n': '新馬', 'v': '新馬'}, {'n': '印度', 'v': '印度'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'lang', 'name': '語言', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '國語', 'v': '國語'}, {'n': '粵語', 'v': '粵語'}, {'n': '英語', 'v': '英語'},
                        {'n': '韓語', 'v': '韓語'}, {'n': '日語', 'v': '日語'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '法語', 'v': '法語'},
                        {'n': '德語', 'v': '德語'}, {'n': '泰語', 'v': '泰語'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'},
                        {'n': '2014-2011', 'v': '2014-2011'}, {'n': '2010-2000', 'v': '2010-2000'}, {'n': '90年代', 'v': '90年代'},
                        {'n': '80年代', 'v': '80年代'}, {'n': '更早', 'v': '更早'}]}
                ],
                '22': [
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '最新', 'v': 'time'}, {'n': '熱播榜', 'v': 'hits_day'}, {'n': '好評榜', 'v': 'score'}]},
                    {'key': 'class', 'name': '類型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '劇情', 'v': '劇情'}, {'n': '愛情', 'v': '愛情'}]},
                    {'key': 'area', 'name': '地區', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': '大陸'}, {'n': '香港', 'v': '香港'}, {'n': '台灣', 'v': '台灣'},
                        {'n': '日本', 'v': '日本'}, {'n': '韓國', 'v': '韓國'}, {'n': '歐美', 'v': '歐美'}, {'n': '泰國', 'v': '泰國'},
                        {'n': '新馬', 'v': '新馬'}, {'n': '印度', 'v': '印度'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'lang', 'name': '語言', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '國語', 'v': '國語'}, {'n': '粵語', 'v': '粵語'}, {'n': '英語', 'v': '英語'},
                        {'n': '韓語', 'v': '韓語'}, {'n': '日語', 'v': '日語'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '法語', 'v': '法語'},
                        {'n': '德語', 'v': '德語'}, {'n': '泰語', 'v': '泰語'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'},
                        {'n': '2014-2011', 'v': '2014-2011'}, {'n': '2010-2000', 'v': '2010-2000'}, {'n': '90年代', 'v': '90年代'},
                        {'n': '80年代', 'v': '80年代'}, {'n': '更早', 'v': '更早'}]}
                ]
            }
        }
        return result

    def homeVideoContent(self):
        d = []
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "swiper-slide")]')
            for item in data_list[:10]:
                vod_id = item.xpath('.//a/@href')[0].split('/')[-1].split('.')[0]
                vod_name = item.xpath('.//div[contains(@class, "text-white")]/text()')[0].strip()
                vod_pic = item.xpath('.//img/@src')[0]
                vod_remarks = item.xpath('.//span[contains(@class, "rounded-sm")]/text()')[0].strip()
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        by = ext.get('by', 'time')
        class_filter = ext.get('class', '')
        area = ext.get('area', '')
        lang = ext.get('lang', '')
        year = ext.get('year', '')
        
        url = f'{self.home_url}/api/vod/v1/vod/list?pageNum={page}&pageSize=12&tid={cid}&by={by}&class={class_filter}&area={area}&lang={lang}&year={year}'
        d = []
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            response = res.json()
            data = response['data']['List']
            for item in data:
                d.append({
                    'vod_id': str(item['vod_id']),
                    'vod_name': item['vod_name'],
                    'vod_pic': item['vod_pic'],
                    'vod_remarks': item['vod_remarks']
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}

    def detailContent(self, ids):
        d = []
        for vod_id in ids:
            try:
                url = f"{self.home_url}/vod/play/id/{vod_id}/nid/1"
                res = requests.get(url, headers=self.headers, timeout=5)
                res.encoding = 'utf-8'
                doc = etree.HTML(res.text)
                
                detail = {'vod_id': vod_id}
                detail['vod_name'] = doc.xpath('//div[contains(@class, "vod-episode-list")]//span[contains(@class, "text-lg")]/text()')[0].strip()
                year_genres = doc.xpath('//div[contains(@class, "vod-episode-list")]//div[contains(@class, "text-sm") and contains(@class, "py-1")][1]/text()')[0].strip()
                detail['vod_year'] = year_genres.split()[0]
                detail['type_name'] = ', '.join(year_genres.split()[1:])
                detail['vod_remarks'] = doc.xpath('//div[contains(@class, "vod-episode-list")]//div[contains(@class, "text-sm") and contains(@class, "py-1")]/text()')[0].split()[0]
                
                play_sources = [x.strip() for x in doc.xpath('//div[contains(@class, "whitespace-nowrap") and contains(@class, "text-sm")]/text()')]
                detail['vod_play_from'] = '$$$'.join(play_sources)
                
                episodes = []
                for a in doc.xpath('//div[contains(@class, "vod-episode-list")]//ul//div//a'):
                    name = a.xpath('.//li//label//div/text()')[0].strip()
                    href = a.xpath('./@href')[0]
                    episodes.append({'name': name, 'href': href})
                
                play_urls = []
                for source in play_sources:
                    key = self.play_map.get(source, '')
                    line_episodes = ['%s$%s%s' % (ep['name'], self.home_url, ep['href'].replace(ep['href'].split('/')[-1], key)) for ep in episodes]
                    play_urls.append('#'.join(line_episodes))
                detail['vod_play_url'] = '$$$'.join(play_urls)
                
                detail['vod_barrage'] = 'https://v.qq.com/x/cover/mzc00200gtvxu1j/n4100tc9165.html'
                
                d.append(detail)
            except Exception as e:
                print(f"Error in detailContent: {e}")
        return {'list': d, 'parse': 0, 'jx': 0}

    def searchContent(self, key, quick, page='1'):
        d = []
        url = f'{self.home_url}/api/vod/v1/vod/search?pageNum={page}&pageSize=12&keyword={key}'
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            res.encoding = 'utf-8'
            response = res.json()
            data = response['data']['List']
            for item in data:
                d.append({
                    'vod_id': str(item['vod_id']),
                    'vod_name': item['vod_name'],
                    'vod_pic': item['vod_pic'],
                    'vod_remarks': item['vod_remarks']
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        try:
            if not pid.startswith('http'):
                url = f"{self.home_url}/api/playurl"
                data = {'urlEncode': pid, 'sourceCode': self.play_map.get(flag, '')}
                res = requests.post(url, json=data, headers=self.headers, timeout=5)
                response = res.json()
                real_url = response.get('data', {}).get('url', self.default_play_url)
            else:
                real_url = pid
            
            if '.m3u8' in real_url or '.mp4' in real_url:
                return {'parse': 0, 'playUrl': '', 'url': real_url, 'header': json.dumps(self.headers)}
            return {'parse': 1, 'playUrl': '', 'url': real_url, 'header': json.dumps(self.headers)}
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'parse': 0, 'playUrl': '', 'url': self.default_play_url, 'header': json.dumps(self.headers)}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

    def get_data(self):
        pass

if __name__ == '__main__':
    spider = Spider()
    spider.init()  # 確保調用 init
    print(json.dumps(spider.homeContent(True), ensure_ascii=False, indent=2))
    print(json.dumps(spider.homeVideoContent(), ensure_ascii=False, indent=2))
    print(json.dumps(spider.categoryContent('1', '1', True, {'by': 'hits_day', 'area': '大陸', 'year': '2024'}), ensure_ascii=False, indent=2))
    print(json.dumps(spider.searchContent('骗骗喜欢你', True), ensure_ascii=False, indent=2))