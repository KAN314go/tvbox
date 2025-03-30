# coding = utf-8
# !/usr/bin/python

"""

作者 丢丢喵 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================Diudiumiao====================

"""

from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from bs4 import BeautifulSoup
from base64 import b64decode
import urllib.request
import urllib.parse
import binascii
import requests
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "https://freevideo.zqqds.cn"

headerx = {
    'Host': 'freevideo.zqqds.cn',
    'alg': 'HG45LKBS',
    'datas': 'phM9hgPlRJYhe1CnGhmAXAGxykuiUzMzDg9O6gim3BYyV82hDVoeHMMzRimC6OhW7BLsDRmEnSa5Tv/yZHZ2+Q3hypMQTA6hentuuRFdFSRnRqGF0aeskqdImcXPXZOKfNWw8w2syoAxXUCYd+8H5fX+hF34F5UQidB8DN8KHWmNn79AAEb2xTXFsB4mcn5YYDGm1iIDRaosixoS5pFySNGOLtkMgjIbRSrN1cxPq/BNE/7isNe/25z+svVABRWfFFM1ehaWgLSnsAn96c8Ptc3TwLjx7kDCWnNx2MP9f04T6qA8mP/SworDn4Hhoo0Tsrjmg5enoPwLs3V1HHazSMPxC+pIC6bW3GrQ0Ar0uhIVXXmX+zYQGcyI4bXphY9iFObo81h6d9LIxR47RbNHfGZ2NJUHJmF5lFHXCInleDrNjw+gf91VG6EjPaBNmN60ka7/nVpYmGK3GC8cw6iEi52jCn+AgRbeygGPH2CdMLcunIOgEIT+aL4YnVxP13peX//bi1+gfeItPB0rsL5YPh3XWas/73dLYTtTYZVVYQspAnYwj2BTvlCfnjGcKNgPa7YfB21xLLuCCAnrrmy7zgkKmyTr2zGVPgaCv5IhiNtrbw8XQMODjgEhijC+arxig3wPaXkHbSkHFwlpO4UaWgLxz8gUYxKDSFXa+5Z8988z7EcDtsOepH1EwyV277SV+McDi/4QDNhC4UV8hA0bDQ==',
    'x-request-id': '267871ed-5d33-469d-b349-d0a4df6730cc',
    'x-request-id': '05af6be8-b7c3-4ba4-9402-6a40b388626a',
    'content-type': 'application/json; charset=utf-8',
    'content-length': '216',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/4.10.0'
          }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
          }

pm = ''

class Spider(Spider):
    global xurl
    global headerx
    global headers

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "434@推荐", "type_name": "好剧🌠"},
                            {"type_id": "441@新剧", "type_name": "新剧🌠"},
                            {"type_id": "179@排行榜", "type_name": "排行榜🌠"},
                            {"type_id": "183@VIP抢先", "type_name": "VIP抢先🌠"},
                            {"type_id": "431@经典好剧", "type_name": "经典好剧🌠"},
                            {"type_id": "416@微短剧大赛", "type_name": "微短剧大赛🌠"}],
                }

        return result

    def decrypt(self, encrypted_data):
        key = "ZHpramdmeXhnc2h5bGd6bQ=="
        iv = "YXBpdXBkb3duZWRjcnlwdA=="
        key_bytes = base64.b64decode(key)
        iv_bytes = base64.b64decode(iv)
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted_padded_bytes = cipher.decrypt(encrypted_bytes)
        decrypted_bytes = unpad(decrypted_padded_bytes, AES.block_size)
        return decrypted_bytes.decode('utf-8')

    def decrypt_wb(self, encrypted_data):
        key_base64 = "ZHpramdmeXhnc2h5bGd6bQ=="
        key_bytes = base64.b64decode(key_base64)
        iv_base64 = "YXBpdXBkb3duZWRjcnlwdA=="
        iv_bytes = base64.b64decode(iv_base64)
        plaintext = encrypted_data
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        ciphertext_bytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        ciphertext_base64 = base64.b64encode(ciphertext_bytes).decode('utf-8')
        return ciphertext_base64

    def homeVideoContent(self):
        videos = []
        di = '{"recSwitch":true,"storePageId":141,"channelGroupId":"434","channelId":1768,"channelName":"精选","pageFlag":"1","theaterSubscriptSwitch":true}'
        detail = self.decrypt_wb(di)

        url = f"{xurl}/free-video-portal/portal/1125"
        response = requests.post(url=url, headers=headerx, data=detail)

        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get('data')
            detail = self.decrypt(data)
            detail = json.loads(detail)

            js = detail['columnData'][0]['videoData']

            for vod in js:

                name = vod['bookName']

                id = vod['bookId']

                pic = vod['coverWap']

                remark = vod['finishStatusCn']

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result = {'list': videos}
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        fenge = cid.split("@")

        di = f'{{"recSwitch":true,"storePageId":141,"channelGroupId":"434","channelId":"{fenge[0]}","channelName":"{fenge[1]}","lastColumnStyle":3,"fromColumnId":"1","pageFlag":{pg},"theaterSubscriptSwitch":true}}'
        detail = self.decrypt_wb(di)
        url = f"{xurl}/free-video-portal/portal/1125"
        response = requests.post(url=url, headers=headerx, data=detail)

        if response.status_code == 200:
            response_data = response.json()

            data = response_data.get('data')
            detail = self.decrypt(data)
            detail = json.loads(detail)

            js = detail['columnData'][0]['videoData']

            for vod in js:

                name = vod['bookName']

                id = vod['bookId']

                pic = vod['coverWap']

                remark = vod['finishStatusCn']

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        global pm
        did = ids[0]
        result = {}
        videos = []
        xianlu = ''
        purl = ''

        di = f'{{"bookId":"{did}","needNextChapter":0,"isNeedAlias":"","bookAlias":"","resolutionRate":"720P"}}'
        detail = self.decrypt_wb(di)

        url = f"{xurl}/free-video-portal/portal/1131"
        response = requests.post(url=url, headers=headerx, data=detail)
        if response.status_code == 200:
            response_data = response.json()

            data = response_data.get('data')
            detail = self.decrypt(data)
            detail = json.loads(detail)

            vod_content = detail['videoInfo']['introduction']

            vod_actor = detail['videoInfo']['protagonist']
            vod_actor = ', '.join(vod_actor)
            vod_actor = vod_actor.replace('[', '').replace(']', '').replace("'", "").replace(",", "")

            vod_director = detail['videoInfo']['protagonist'][0]

            bookTags = detail['videoInfo']['bookTags']
            bookTags = ', '.join(bookTags)
            bookTags = bookTags.replace(',', '')
            vod_remarks = detail['videoInfo']['finishStatusCn']
            vod_remarks = vod_remarks + " " + bookTags

            year = detail['videoInfo']['utime']

            area = "中国"

            sz = len(detail['chapterList']) - 1
            zhyj = detail['chapterList'][sz]['chapterId']

            soups = detail['chapterList']

            for vods in soups:

                name = vods['chapterName']

                parse = vods['chapterId']

                parse = did + '@' + parse + '@' + zhyj

                purl = purl + name + '$' + parse + '#'

            purl = purl[:-1] + '$$$'

        purl = purl[:-3]

        xianlu = '短剧专线'

        videos.append({
            "vod_id": did,
            "vod_actor": vod_actor,
            "vod_director": vod_director,
            "vod_content": vod_content,
            "vod_remarks": vod_remarks,
            "vod_year": year,
            "vod_area": area,
            "vod_play_from": xianlu,
            "vod_play_url": purl
                      })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):

        fenge = id.split("@")

        di = '{"bookId":"","chapterIds":[""],"unClockType":"load","chapterId":"","resolutionRate":"720P"}'
        data = json.loads(di)
        data['bookId'] = fenge[0]
        data['chapterIds'][0] = fenge[1]
        data['chapterId'] = fenge[2]
        new_di = json.dumps(data, ensure_ascii=False, indent=4)

        detail2 = self.decrypt_wb(new_di)
        url = f"{xurl}/free-video-portal/portal/1139"
        res2 = requests.post(url=url, headers=headerx,data=detail2)

        js = json.loads(res2.text)
        data = js['data']

        detail2 = self.decrypt(data)
        detail = json.loads(detail2)
        url = detail['chapterInfo'][0]['content']['mp4SwitchUrl'][0]

        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = url
        result["header"] = headers
        return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []

        di = f'{{"keyword":"{key}","page":{page},"size":15,"searchSource":"搜索按钮","hotWordType":2,"tagIds":"","reservationSwitch":true}}'
        detail = self.decrypt_wb(di)

        url = f"{xurl}/free-video-portal/portal/1803"
        response = requests.post(url=url, headers=headerx, data=detail)

        if response.status_code == 200:
            response_data = response.json()
            data = response_data.get('data')
            detail = self.decrypt(data)
            detail = json.loads(detail)

            js = detail['searchVos']

            for vod in js:

                name = vod['bookName']

                id = vod['bookId']

                pic = vod['coverWap']

                remark = vod['finishStatusCn']

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result = {'list': videos}
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None







