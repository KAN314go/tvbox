# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2025/3/22 21:03
import json
import sys
import requests
from lxml import etree
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "爱瓜TV"

    def init(self, extend=""):
        self.home_url = extend if extend else 'https://aigua1.com'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": self.home_url,
        }
        self.image_domain = "https://vres.wbadl.cn"
        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        return False

    def manualVideoCheck(self):
        return False

    def homeContent(self, filter):
        result = {
            'class': [
                {'type_id': '2', 'type_name': '电视剧'},
                {'type_id': '1', 'type_name': '电影'},
                {'type_id': '3', 'type_name': '综艺'},
                {'type_id': '4', 'type_name': '动漫'},
                {'type_id': '32', 'type_name': '纪录片'}
            ],
            'filters': {
                '1': [
                    {'key': 'class', 'name': '剧情', 'value': [
                        {'n': '全部', 'v': '0'}, {'n': '魔幻', 'v': '179'}, {'n': '动作', 'v': '154'},
                        {'n': '科幻', 'v': '159'}, {'n': '惊悚', 'v': '156'}, {'n': '犯罪', 'v': '157'},
                        {'n': '剧情', 'v': '161'}, {'n': '悬疑', 'v': '160'}, {'n': '奇幻', 'v': '226'},
                        {'n': '爱情', 'v': '155'}, {'n': '战争', 'v': '164'}, {'n': '恐怖', 'v': '169'},
                        {'n': '喜剧', 'v': '153'}, {'n': '冒险', 'v': '280'}, {'n': '灾难', 'v': '281'},
                        {'n': '歌舞', 'v': '282'}, {'n': '动画', 'v': '283'}, {'n': '经典', 'v': '284'},
                        {'n': '同性', 'v': '285'}, {'n': '网络电影', 'v': '286'}, {'n': '其他', 'v': '178'}
                    ]},
                    {'key': 'area', 'name': '地区', 'value': [
                        {'n': '全部', 'v': '0'}, {'n': '大陆', 'v': '18'}, {'n': '日本', 'v': '24'},
                        {'n': '香港', 'v': '20'}, {'n': '韩国', 'v': '21'}, {'n': '台湾', 'v': '23'},
                        {'n': '英国', 'v': '22'}, {'n': '东南亚', 'v': '29'}, {'n': '欧美', 'v': '19'},
                        {'n': '其它', 'v': '30'}
                    ]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': '0'}, {'n': '2025', 'v': '131'}, {'n': '2024', 'v': '130'},
                        {'n': '2023', 'v': '129'}, {'n': '2022', 'v': '21'}, {'n': '2021', 'v': '22'},
                        {'n': '2020', 'v': '23'}, {'n': '2019', 'v': '24'}, {'n': '2018', 'v': '25'},
                        {'n': '2017', 'v': '26'}, {'n': '2016', 'v': '27'}, {'n': '2015', 'v': '28'},
                        {'n': '2014', 'v': '29'}, {'n': '2013', 'v': '30'}, {'n': '2012', 'v': '31'},
                        {'n': '2011', 'v': '32'}, {'n': '2010', 'v': '33'}, {'n': '2009', 'v': '34'},
                        {'n': '2008', 'v': '35'}, {'n': '更早', 'v': '127'}
                    ]},
                    {'key': 'status', 'name': '状态', 'value': [
                        {'n': '全部', 'v': '0'}, {'n': '完结', 'v': '1'}, {'n': '更新中', 'v': '2'}
                    ]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '添加时间', 'v': 'new'}, {'n': '人气高低', 'v': 'hot'}, {'n': '评分高低', 'v': 'score'}
                    ]}
                ],
                # 其他分類（2, 3, 4, 32）的 filters 這裡省略，可直接從原代碼複製
            }
        }
        return result

    def homeVideoContent(self):
        d = []
        try:
            res = requests.get(self.home_url, headers=self.headers, timeout=10)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text.encode('utf-8'))
            data_list = root.xpath('//div[@class="video-box-new"]/div[@class="Movie-list"]')
            for i in data_list:
                d.append({
                    'vod_id': i.xpath('./a[@class="Movie movie-height"]/@href')[0].split('=')[-1],
                    'vod_name': i.xpath('./a[2]/text()')[0].strip(),
                    'vod_pic': i.xpath('./a[1]/img/@originalsrc')[0],
                    'vod_remarks': i.xpath('./div[@class="Movie-type02"]/div[2]/text()')[0].strip()
                })
            return {'list': d}
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': []}

    def categoryContent(self, tid, pg, filter, ext):
        d = []
        _class = ext.get('class', '0')
        _area = ext.get('area', '0')
        _year = ext.get('year', '0')
        _status = ext.get('status', '0')
        _by = ext.get('by', 'new')
        url = f"{self.home_url}/video/refresh-cate?page_num={pg}&sorttype=desc&channel_id={tid}&tag={_class}&area={_area}&year={_year}&status={_status}&sort={_by}&page_size=28"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            data_list = res.json()['data']['list']
            for i in data_list:
                d.append({
                    'vod_id': i['video_id'],
                    'vod_name': i['video_name'],
                    'vod_pic': i['cover'],
                    'vod_remarks': i['flag']
                })
            return {'list': d}
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {'list': []}

    def detailContent(self, ids):
        ids = ids[0]
        url = f"{self.home_url}/video/detail?video_id={ids}"
        video_list = []
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            root = etree.HTML(res.text.encode('utf-8'))
            vod_play_from = '$$$'.join(['线路一', '线路二', '线路三'])
            play_list1 = root.xpath('//ul[contains(@class, "qy-episode-num")]')
            play_list2 = root.xpath('//ul[@id="srctab-1"]')
            vod_play_url_list = []
            if len(play_list1) > 0:
                play_list = play_list1[:-1]
            elif len(play_list2) > 0:
                play_list = play_list2
            else:
                play_list = []

            for i in play_list:
                name_list = i.xpath('.//div[@class="select-link"]/text()') + \
                           i.xpath('.//span[@class="title-link"]/text()') + \
                           i.xpath('./li/text()')
                url_list = i.xpath('./li/@data-chapter-id')
                vod_play_url_list.append(
                    '#'.join([_name.strip() + '$' + f'{ids}-{_url}' for _name, _url in zip(name_list, url_list)])
                )

            vod_play_url = '$$$'.join(vod_play_url_list * 3)
            video_list.append({
                'vod_id': ids,
                'vod_name': '',
                'vod_pic': '',
                'type_name': '',
                'vod_year': '',
                'vod_area': '',
                'vod_remarks': '',
                'vod_actor': '',
                'vod_director': '',
                'vod_content': '',
                'vod_play_from': vod_play_from,
                'vod_play_url': vod_play_url
            })
            return {"list": video_list}
        except Exception as e:
            print(f"Error in detailContent: {e}")
            return {'list': []}

    def searchContent(self, key, quick):
        d = []
        url = f"{self.home_url}/video/refresh-video?page_num=1&sorttype=desc&page_size=28&tvNum=7&sort=new&keyword={key}"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[@class="SSbox"]')
            for i in data_list:
                d.append({
                    'vod_id': i.xpath('./a/@href')[0].split('=')[-1],
                    'vod_name': ''.join(i.xpath('.//span/text()')),
                    'vod_pic': i.xpath('./a/img/@originalsrc')[0],
                    'vod_remarks': i.xpath('.//div[@class="SSjgTitle"]/text()')[0]
                })
            return {'list': d}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': []}

    def playerContent(self, flag, id, vipFlags):
        a = id.split('-')
        videoId = a[0]
        chapterId = a[1]
        url = f"{self.home_url}/video/play-url?videoId={videoId}&sourceId=0&citycode=HKG&chapterId={chapterId}"
        try:
            res = requests.get(url, headers=self.headers, timeout=10)
            play_url_list = res.json()['data']['urlinfo']['resource_url']
            if flag == '线路一':
                play_url = play_url_list['1']
            elif flag == '线路二':
                play_url = play_url_list['16']
            else:
                play_url = play_url_list['21']
            return {'url': play_url, 'header': json.dumps(self.headers), 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': self.default_play_url, 'header': json.dumps(self.headers), 'parse': 0, 'jx': 0}

    def localProxy(self, param):
        return None

    def destroy(self):
        pass

if __name__ == "__main__":
    spider = Spider()
    spider.init("https://aigua1.com")
    print("測試首頁內容:")
    home_content = spider.homeVideoContent()
    for item in home_content['list'][:3]:
        print(f"影片: {item['vod_name']}, ID: {item['vod_id']}")