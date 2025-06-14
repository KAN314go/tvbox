# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2025/6/14 21:01
import re
import sys
import urllib.request
import urllib.parse
from lxml import etree
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def getName(self):
        return "MissAV"

    def init(self, extend):
        self.home_url = 'https://missav.ai'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        self.error_url = "https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4"

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        return {
            'class': [
                {'type_id': '/actresses', 'type_name': '女優一覽'},
                {'type_id': '/actresses/ranking', 'type_name': '女優排行 JUN 2025'},
                # {'type_id': '/genres', 'type_name': '類型'},
                # {'type_id': '/makers', 'type_name': '發行商'},
                {'type_id': '/genres/VR', 'type_name': 'VR'},
                {'type_id': '/dm265/chinese-subtitle', 'type_name': '中文字幕'},
                {'type_id': '/dm514/new', 'type_name': '最近更新'},
                {'type_id': '/dm588/release', 'type_name': '新作上市'},
                {'type_id': '/dm621/uncensored-leak', 'type_name': '無碼流出'},
                {'type_id': '/dm291/today-hot', 'type_name': '今日熱門'},
                {'type_id': '/dm169/weekly-hot', 'type_name': '本週熱門'},
                {'type_id': '/dm257/monthly-hot', 'type_name': '本月熱門'},
                {'type_id': '/dm23/siro', 'type_name': 'SIRO'},
                {'type_id': '/dm20/luxu', 'type_name': 'LUXU'},
                {'type_id': '/dm17/gana', 'type_name': 'GANA'},
                {'type_id': '/dm862/maan', 'type_name': 'PRESTIGE PREMIUM'},
                {'type_id': '/dm23/scute', 'type_name': 'S-CUTE'},
                {'type_id': '/dm19/ara', 'type_name': 'ARA'},
                {'type_id': '/dm621/uncensored-leak', 'type_name': '無碼流出'},
                {'type_id': '/dm99/fc2', 'type_name': 'FC2'},
                {'type_id': '/dm319995/heyzo', 'type_name': 'HEYZO'},
                {'type_id': '/dm29/tokyohot', 'type_name': '東京熱'},
                {'type_id': '/dm695579/1pondo', 'type_name': '一本道'},
                {'type_id': '/dm1271239/caribbeancom', 'type_name': 'Caribbeancom'},
                {'type_id': '/dm14081/caribbeancompr', 'type_name': 'Caribbeancompr'},
                {'type_id': '/dm1117248/10musume', 'type_name': '10musume'},
                {'type_id': '/dm370414/pacopacomama', 'type_name': 'pacopacomama'},
                {'type_id': '/dm135/gachinco', 'type_name': 'Gachinco'},
                {'type_id': '/dm29/xxxav', 'type_name': 'XXX-AV'},
                {'type_id': '/dm24/marriedslash', 'type_name': '人妻斬'},
                {'type_id': '/dm19/naughty4610', 'type_name': '頑皮 4610'},
                {'type_id': '/dm22/naughty0930', 'type_name': '頑皮 0930'},
                {'type_id': '/dm34/madou', 'type_name': '麻豆傳媒'},
                {'type_id': '/dm17/twav', 'type_name': 'TWAV'},
                {'type_id': '/dm15/furuke', 'type_name': 'Furuke'},
                {'type_id': '/klive', 'type_name': '韓國直播'},
                {'type_id': '/clive', 'type_name': '中國直播'},
            ],
            'filters': {}
        }

    def homeVideoContent(self):
        video_list = []
        res = self.api_req(f'{self.home_url}/dm45')
        # print(res)
        if res == 'False':
            return {'list': [],'parse': 0,'jx': 0}

        root = etree.HTML(res)
        data_list = root.xpath('//div[contains(@class,"thumbnail group")]')
        # print(len(data_list))
        for i in data_list:
            names = i.xpath('./div[2]/a/text()')
            # print(names)
            if len(names) > 0:
                name = names[0].strip()
                if len(name) > 0:
                    href = i.xpath('./div[2]/a/@href')[0].replace(self.home_url, '')
                    pic = i.xpath('./div[1]/a/img/@data-src')[0]
                    # print(pic)
                    video_list.append(
                        {
                            'vod_id': href,
                            'vod_name': name,
                            'vod_pic': pic,
                            'vod_remarks': '',
                            'style': {'type': 'rect','ratio': 1.5}
                        }
                    )

        return {
            'list': video_list,
            'parse': 0,
            'jx': 0
        }

    def categoryContent(self, cid, page, filter, ext):
        a = ['/actresses', '/actresses/ranking']
        b = ['/genres', '/makers']
        video_list = []
        res = self.api_req(f'{self.home_url}{cid}?page={page}')
        # print(res)
        if res == 'False':
            return {'list': [], 'parse': 0, 'jx': 0}
        root = etree.HTML(res)
        if cid in a:
            data_list = root.xpath('//div[contains(@class,"space-y-4")]')
            for i in data_list:
                names = i.xpath('./div/a/h4/text()')
                # print(names)
                if len(names) > 0:
                    name = names[0].strip()
                    href = i.xpath('./div/a/@href')[0].replace(self.home_url, '')
                    pics = i.xpath('./a/div/img/@src')
                    if len(pics) > 0:
                        pic = pics[0]
                    else:
                        pic = 'https://img.icons8.com/?size=256w&id=l24cyKyOwOjt&format=png'
                    # print(pic)
                    # remarks = i.xpath('./div/a/p[1]/text()')[0] + ' ' + i.xpath('./div/a/p[2]/text()')[0]
                    # print(remarks)
                    video_list.append(
                        {
                            'vod_id': href,
                            'vod_name': name,
                            'vod_pic': pic,
                            'vod_remarks': '',
                            'vod_tag': 'folder',
                            'style': {"type": "oval"}
                        }
                    )
        elif cid in b:
            pass
        else:
            data_list = root.xpath('//div[contains(@class,"thumbnail group")]')
            for i in data_list:
                names = i.xpath('./div[2]/a/text()')
                # print(names)
                if len(names) > 0:
                    name = names[0].strip()
                    if len(name) > 0:
                        href = i.xpath('./div[2]/a/@href')[0].replace(self.home_url, '')
                        pic = i.xpath('./div[1]/a/img/@data-src')[0]
                        # print(pic)
                        video_list.append(
                            {
                                'vod_id': href,
                                'vod_name': name,
                                'vod_pic': pic,
                                'vod_remarks': '',
                                'style': {'type': 'rect', 'ratio': 1.5}
                            }
                        )
        return {'list': video_list, 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        res = self.api_req(f'{self.home_url}{ids}')
        # print(res)
        if res == 'False':
            return {'list': [], 'parse': 0, 'jx': 0}

        datas = re.findall(r'm3u8(.*?)com', res)
        if len(datas) > 0:
            b = datas[0].split('|')[1:-1]
            b.reverse()
            b = '-'.join(b)
            # print(b)
            url = f"https://surrit.com/{b}/playlist.m3u8"

        else:
            url = self.error_url

        video_list.append(
            {
                'type_name': '',
                'vod_id': ids,
                'vod_name': '',
                'vod_remarks': '',
                'vod_year': '',
                'vod_area': '',
                'vod_actor': '',
                'vod_director': '',
                'vod_content': '',
                'vod_play_from': 'MissAV',
                'vod_play_url': f'01${url}'

            }
        )
        return {"list": video_list, 'parse': 0, 'jx': 0}

    def searchContent(self, key, quick, page='1'):
        wd = urllib.parse.quote(key)
        video_list = []
        res = self.api_req(f'{self.home_url}/search/{wd}?page={page}')
        if res == 'False':
            return {'list': [], 'parse': 0, 'jx': 0}
        root = etree.HTML(res)
        data_list = root.xpath('//div[contains(@class,"thumbnail group")]')
        # print(len(data_list))
        for i in data_list:
            names = i.xpath('./div[2]/a/text()')
            # print(names)
            if len(names) > 0:
                name = names[0].strip()
                if len(name) > 0:
                    href = i.xpath('./div[2]/a/@href')[0].replace(self.home_url, '')
                    pic = i.xpath('./div[1]/a/img/@data-src')[0]
                    # print(pic)
                    video_list.append(
                        {
                            'vod_id': href,
                            'vod_name': name,
                            'vod_pic': pic,
                            'vod_remarks': '',
                            'style': {'type': 'rect', 'ratio': 1.5}
                        }
                    )

        return {
            'list': video_list,
            'parse': 0,
            'jx': 0
        }

    def playerContent(self, flag, pid, vipFlags):
        h2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }

        return {"url": pid, "header": h2, "parse": 0, "jx": 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

    def api_req(self,url):
        # 创建请求对象
        request = urllib.request.Request(url, headers=self.headers)
        # 发起请求
        try:
            response = urllib.request.urlopen(request)
            data = response.read().decode('utf-8')
            return data
        except:
            return 'False'


if __name__ == '__main__':
    pass
