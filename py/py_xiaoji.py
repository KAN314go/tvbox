# -*- coding: utf-8 -*-
# by @嗷呜
import json
import sys
from base64 import b64decode, b64encode
from pyquery import PyQuery as pq
from requests import Session
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def init(self, extend=""):
        self.host = self.gethost()
        self.headers['referer'] = f'{self.host}/'
        self.session = Session()
        self.session.headers.update(self.headers)
        pass

    def getName(self):
        return "minijj"

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-full-version': '"133.0.6943.98"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Google Chrome";v="133.0.6943.98", "Chromium";v="133.0.6943.98"',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'priority': 'u=0, i'
    }

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "電影": "1",
            "電視劇": "2",
            "經典動漫": "3",
            "綜藝娛樂": "4",
            "2022最新": "2022new"
        }
        classes = []
        filters = {}
        
        # 主分類
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })

        # 篩選條件
        filters = {
            '1': [  # 電影
                {
                    'key': 'type',
                    'name': '類型',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '動作片', 'v': '8'},
                        {'n': '喜劇片', 'v': '9'},
                        {'n': '愛情片', 'v': '10'},
                        {'n': '科幻片', 'v': '11'},
                        {'n': '恐怖片', 'v': '12'},
                        {'n': '戰爭片', 'v': '13'},
                        {'n': '劇情片', 'v': '14'}
                    ]
                },
                {
                    'key': 'year',
                    'name': '時間',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'},
                        {'n': '2016', 'v': '2016'},
                        {'n': '2015', 'v': '2015'}
                    ]
                },
                {
                    'key': 'by',
                    'name': '排序',
                    'value': [
                        {'n': '按時間', 'v': 'time'},
                        {'n': '按人氣', 'v': 'hits'},
                        {'n': '按評分', 'v': 'score'}
                    ]
                }
            ],
            '2': [  # 電視劇
                {
                    'key': 'type',
                    'name': '類型',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '大陸劇', 'v': '15'},
                        {'n': '香港劇', 'v': '16'},
                        {'n': '台灣劇', 'v': '918'},
                        {'n': '日劇', 'v': '18'},
                        {'n': '韓劇', 'v': '915'},
                        {'n': '美劇', 'v': '916'},
                        {'n': '英劇', 'v': '923'},
                        {'n': '歐美劇', 'v': '17'},
                        {'n': '泰劇', 'v': '922'},
                        {'n': '亞洲劇', 'v': '19'}
                    ]
                },
                {
                    'key': 'year',
                    'name': '時間',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'},
                        {'n': '2016', 'v': '2016'},
                        {'n': '2015', 'v': '2015'}
                    ]
                },
                {
                    'key': 'by',
                    'name': '排序',
                    'value': [
                        {'n': '按時間', 'v': 'time'},
                        {'n': '按人氣', 'v': 'hits'},
                        {'n': '按評分', 'v': 'score'}
                    ]
                }
            ],
            '3': [  # 經典動漫
                {
                    'key': 'type',
                    'name': '類型',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '國漫', 'v': '906'},
                        {'n': '日漫', 'v': '904'},
                        {'n': '美漫', 'v': '905'},
                        {'n': '其他動漫', 'v': '903'}
                    ]
                },
                {
                    'key': 'year',
                    'name': '時間',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'},
                        {'n': '2016', 'v': '2016'},
                        {'n': '2015', 'v': '2015'}
                    ]
                },
                {
                    'key': 'by',
                    'name': '排序',
                    'value': [
                        {'n': '按時間', 'v': 'time'},
                        {'n': '按人氣', 'v': 'hits'},
                        {'n': '按評分', 'v': 'score'}
                    ]
                }
            ],
            '4': [  # 綜藝娛樂
                {
                    'key': 'type',
                    'name': '類型',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '大陸綜藝', 'v': '911'},
                        {'n': '港台綜藝', 'v': '907'},
                        {'n': '韓綜', 'v': '908'},
                        {'n': '日綜', 'v': '912'},
                        {'n': '泰綜', 'v': '913'},
                        {'n': '歐美綜藝', 'v': '909'}
                    ]
                },
                {
                    'key': 'year',
                    'name': '時間',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'},
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'},
                        {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'},
                        {'n': '2016', 'v': '2016'},
                        {'n': '2015', 'v': '2015'}
                    ]
                },
                {
                    'key': 'by',
                    'name': '排序',
                    'value': [
                        {'n': '按時間', 'v': 'time'},
                        {'n': '按人氣', 'v': 'hits'},
                        {'n': '按評分', 'v': 'score'}
                    ]
                }
            ],
            '2022new': [  # 2022最新
                {
                    'key': 'year',
                    'name': '時間',
                    'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '2022', 'v': '2022'}
                    ]
                },
                {
                    'key': 'by',
                    'name': '排序',
                    'value': [
                        {'n': '按時間', 'v': 'time'},
                        {'n': '按人氣', 'v': 'hits'},
                        {'n': '按評分', 'v': 'score'}
                    ]
                }
            ]
        }

        result['class'] = classes
        result['filters'] = filters
        return result

    def homeVideoContent(self):
        data = self.getpq()
        return {'list': self.getlist(data(".update_area_lists .i_list"))}

    def categoryContent(self, tid, pg, filter, extend):
        result = {}
        _type = extend.get('type', '')  # 子分類
        _year = extend.get('year', '')  # 年份
        _by = extend.get('by', '')      # 排序
        
        # 如果有子分類，使用子分類 ID；否則使用主分類 ID
        type_id = _type if _type else tid
        
        # 構建 URL
        if tid == '2022new':
            url = f'{self.host}/ym/{tid}.html'
        else:
            url = f'{self.host}/lm/{type_id}/{pg}.html'
        
        # 如果有篩選條件，附加查詢參數（假設網站支持，需驗證）
        if _year or _by:
            url += f'?year={_year}&by={_by}'
        
        data = self.getpq(url)
        vdata = self.getlist(data(".update_area_lists .i_list"))
        
        result['list'] = vdata
        result['page'] = pg
        result['pagecount'] = 9999  # 假設總頁數未知
        result['limit'] = 20        # 每頁顯示數量（根據 HTML 推測）
        result['total'] = 999999    # 總數未知
        return result

    def detailContent(self, ids):
        data = self.getpq(ids[0])
        djs = self.getjsdata(data)
        vn = data('meta[property="og:title"]').attr('content')
        dtext = data('#video-tags-list-container')
        href = dtext('a').attr('href')
        title = dtext('span[class*="body-bold-"]').eq(0).text()
        pdtitle = ''
        if href:
            pdtitle = '[a=cr:' + json.dumps({'id': 'two_click_' + href, 'name': title}) + '/]' + title + '[/a]'
        vod = {
            'vod_name': vn,
            'vod_director': pdtitle,
            'vod_remarks': data('.rb-new__info').text(),
            'vod_play_from': 'Minijj',
            'vod_play_url': ''
        }
        try:
            plist = []
            d = djs['xplayerSettings']['sources']
            f = d.get('standard')
            def custom_sort_key(url):
                quality = url.split('$')[0]
                number = ''.join(filter(str.isdigit, quality))
                number = int(number) if number else 0
                return -number, quality
                
            if f:
                for key, value in f.items():
                    if isinstance(value, list):
                        for info in value:
                            id = self.e64(f'{0}@@@@{info.get("url") or info.get("fallback")}')
                            plist.append(f"{info.get('label') or info.get('quality')}${id}")
            plist.sort(key=custom_sort_key)
            if d.get('hls'):
                for format_type, info in d['hls'].items():
                    if url := info.get('url'):
                        encoded = self.e64(f'{0}@@@@{url}')
                        plist.append(f"{format_type}${encoded}")
                        
        except Exception as e:
            plist = [f"{vn}${self.e64(f'{1}@@@@{ids[0]}')}"]
            print(f"獲取視頻信息失敗: {str(e)}")
        vod['vod_play_url'] = '#'.join(plist)
        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        data = self.getpq(f'/ss.html?wd={key}&page={pg}')
        return {'list': self.getlist(data(".update_area_lists .i_list")), 'page': pg}

    def playerContent(self, flag, id, vipFlags):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5410.0 Safari/537.36',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'origin': self.host,
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'{self.host}/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'priority': 'u=1, i',
        }
        ids = self.d64(id).split('@@@@')
        return {'parse': int(ids[0]), 'url': ids[1], 'header': headers}

    def localProxy(self, param):
        pass

    def gethost(self):
        try:
            response = self.fetch('https://www.minijj.com', headers=self.headers, allow_redirects=False)
            return response.headers.get('Location', 'https://www.minijj.com')
        except Exception as e:
            print(f"獲取主頁失敗: {str(e)}")
            return "https://www.minijj.com"

    def e64(self, text):
        try:
            text_bytes = text.encode('utf-8')
            encoded_bytes = b64encode(text_bytes)
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64編碼錯誤: {str(e)}")
            return ""

    def d64(self, encoded_text):
        try:
            encoded_bytes = encoded_text.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64解碼錯誤: {str(e)}")
            return ""

    def getlist(self, data):
        vlist = []
        for i in data.items():
            vlist.append({
                'vod_id': i('a').attr('href'),
                'vod_name': i('.meta-title').text(),
                'vod_pic': i('img').attr('data-original'),
                'vod_remarks': i('.meta-post').text().replace('', '').strip(),
                'style': {'ratio': 1.33, 'type': 'rect'}
            })
        return vlist

    def getpq(self, path=''):
        h = '' if path.startswith('http') else self.host
        response = self.session.get(f'{h}{path}').text
        try:
            return pq(response)
        except Exception as e:
            print(f"{str(e)}")
            return pq(response.encode('utf-8'))

    def getjsdata(self, data):
        vhtml = data("script[id='initials-script']").text()
        jst = json.loads(vhtml.split('initials=')[-1][:-1])
        return jst