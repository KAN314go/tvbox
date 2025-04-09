import requests
from lxml import etree
import json
import hashlib
import time

class Spider:
    def __init__(self):
        self.home_url = "https://www.xiaohys.com"
        self.api_url = "https://xiaohys.com/index.php/api/vod"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Origin": "https://xiaohys.com",
            "Referer": "https://xiaohys.com"
        }

    def getName(self):
        return "XiaoHongYingShi"

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        return url.endswith((".mp4", ".m3u8", ".flv"))

    def manualVideoCheck(self):
        return False

    def generate_key(self, t):
        string_to_hash = f"DS{t}DCC147D11943AF75"
        return hashlib.md5(string_to_hash.encode()).hexdigest()

    def homeContent(self, filter):
        categories = [
            {"type_id": "movie", "type_name": "电影"},
            {"type_id": "tv", "type_name": "电视剧"},
            {"type_id": "variety", "type_name": "综艺"},
            {"type_id": "anime", "type_name": "动漫"}
        ]
        filters = {
            "movie": [
                {"key": "class", "name": "類型", "value": [{"n": "全部", "v": ""}, {"n": "喜剧", "v": "喜剧"}, {"n": "爱情", "v": "爱情"}, {"n": "恐怖", "v": "恐怖"}, {"n": "动作", "v": "动作"}, {"n": "科幻", "v": "科幻"}, {"n": "剧情", "v": "剧情"}, {"n": "战争", "v": "战争"}, {"n": "警匪", "v": "警匪"}, {"n": "犯罪", "v": "犯罪"}, {"n": "动画", "v": "动画"}, {"n": "奇幻", "v": "奇幻"}, {"n": "武侠", "v": "武侠"}, {"n": "冒险", "v": "冒险"}, {"n": "枪战", "v": "枪战"}, {"n": "悬疑", "v": "悬疑"}, {"n": "惊悚", "v": "惊悚"}, {"n": "经典", "v": "经典"}, {"n": "青春", "v": "青春"}, {"n": "文艺", "v": "文艺"}, {"n": "微电影", "v": "微电影"}, {"n": "古装", "v": "古装"}, {"n": "历史", "v": "历史"}, {"n": "运动", "v": "运动"}, {"n": "农村", "v": "农村"}, {"n": "儿童", "v": "儿童"}, {"n": "网络电影", "v": "网络电影"}]},
                {"key": "area", "name": "地區", "value": [{"n": "全部", "v": ""}, {"n": "大陆", "v": "大陆"}, {"n": "香港", "v": "香港"}, {"n": "台湾", "v": "台湾"}, {"n": "美国", "v": "美国"}, {"n": "法国", "v": "法国"}, {"n": "英国", "v": "英国"}, {"n": "日本", "v": "日本"}, {"n": "韩国", "v": "韩国"}, {"n": "德国", "v": "德国"}, {"n": "泰国", "v": "泰国"}, {"n": "印度", "v": "印度"}, {"n": "意大利", "v": "意大利"}, {"n": "西班牙", "v": "西班牙"}, {"n": "加拿大", "v": "加拿大"}, {"n": "其他", "v": "其他"}]},
                {"key": "year", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}] + [{"n": str(y), "v": str(y)} for y in range(2024, 1997, -1)]},
                {"key": "lang", "name": "語言", "value": [{"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"}, {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "法语", "v": "法语"}, {"n": "德语", "v": "德语"}, {"n": "其它", "v": "其它"}]},
                {"key": "order", "name": "排序", "value": [{"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}]}
            ],
            "tv": [
                {"key": "class", "name": "類型", "value": [{"n": "全部", "v": ""}, {"n": "古装", "v": "古装"}, {"n": "战争", "v": "战争"}, {"n": "青春偶像", "v": "青春偶像"}, {"n": "喜剧", "v": "喜剧"}, {"n": "家庭", "v": "家庭"}, {"n": "犯罪", "v": "犯罪"}, {"n": "动作", "v": "动作"}, {"n": "奇幻", "v": "奇幻"}, {"n": "剧情", "v": "剧情"}, {"n": "历史", "v": "历史"}, {"n": "经典", "v": "经典"}, {"n": "乡村", "v": "乡村"}, {"n": "情景", "v": "情景"}, {"n": "商战", "v": "商战"}, {"n": "网剧", "v": "网剧"}, {"n": "其他", "v": "其他"}]},
                {"key": "area", "name": "地區", "value": [{"n": "全部", "v": ""}, {"n": "内地", "v": "内地"}, {"n": "韩国", "v": "韩国"}, {"n": "香港", "v": "香港"}, {"n": "台湾", "v": "台湾"}, {"n": "日本", "v": "日本"}, {"n": "美国", "v": "美国"}, {"n": "泰国", "v": "泰国"}, {"n": "英国", "v": "英国"}, {"n": "新加坡", "v": "新加坡"}, {"n": "其他", "v": "其他"}]},
                {"key": "year", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}] + [{"n": str(y), "v": str(y)} for y in range(2024, 2009, -1)]},
                {"key": "lang", "name": "語言", "value": [{"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"}, {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}]},
                {"key": "order", "name": "排序", "value": [{"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}]}
            ],
            "variety": [
                {"key": "class", "name": "類型", "value": [{"n": "全部", "v": ""}, {"n": "选秀", "v": "选秀"}, {"n": "情感", "v": "情感"}, {"n": "访谈", "v": "访谈"}, {"n": "播报", "v": "播报"}, {"n": "旅游", "v": "旅游"}, {"n": "音乐", "v": "音乐"}, {"n": "美食", "v": "美食"}, {"n": "纪实", "v": "纪实"}, {"n": "曲艺", "v": "曲艺"}, {"n": "生活", "v": "生活"}, {"n": "游戏互动", "v": "游戏互动"}, {"n": "财经", "v": "财经"}, {"n": "求职", "v": "求职"}]},
                {"key": "area", "name": "地區", "value": [{"n": "全部", "v": ""}, {"n": "内地", "v": "内地"}, {"n": "港台", "v": "港台"}, {"n": "日韩", "v": "日韩"}, {"n": "欧美", "v": "欧美"}]},
                {"key": "year", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}] + [{"n": str(y), "v": str(y)} for y in range(2024, 2009, -1)]},
                {"key": "lang", "name": "語言", "value": [{"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"}, {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}]},
                {"key": "order", "name": "排序", "value": [{"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}]}
            ],
            "anime": [
                {"key": "class", "name": "類型", "value": [{"n": "全部", "v": ""}, {"n": "情感", "v": "情感"}, {"n": "科幻", "v": "科幻"}, {"n": "热血", "v": "热血"}, {"n": "推理", "v": "推理"}, {"n": "搞笑", "v": "搞笑"}, {"n": "冒险", "v": "冒险"}, {"n": "萝莉", "v": "萝莉"}, {"n": "校园", "v": "校园"}, {"n": "动作", "v": "动作"}, {"n": "机战", "v": "机战"}, {"n": "运动", "v": "运动"}, {"n": "战争", "v": "战争"}, {"n": "少年", "v": "少年"}, {"n": "少女", "v": "少女"}, {"n": "社会", "v": "社会"}, {"n": "原创", "v": "原创"}, {"n": "亲子", "v": "亲子"}, {"n": "益智", "v": "益智"}, {"n": "励志", "v": "励志"}, {"n": "其他", "v": "其他"}]},
                {"key": "area", "name": "地區", "value": [{"n": "全部", "v": ""}, {"n": "国产", "v": "国产"}, {"n": "日本", "v": "日本"}, {"n": "欧美", "v": "欧美"}, {"n": "其他", "v": "其他"}]},
                {"key": "year", "name": "年份", "value": [{"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}] + [{"n": str(y), "v": str(y)} for y in range(2024, 2009, -1)]},
                {"key": "lang", "name": "語言", "value": [{"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"}, {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}]},
                {"key": "order", "name": "排序", "value": [{"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}]}
            ]
        }
        result = {"class": categories, "filters": filters if filter else {}}
        return json.dumps(result, ensure_ascii=False)

    def homeVideoContent(self):
        t = int(time.time())
        key = self.generate_key(t)
        params = {"page": "1", "limit": "5", "time": str(t), "key": key}
        try:
            response = requests.post(self.api_url, data=params, headers=self.headers)
            data = response.json()
            vod_list = [
                {
                    "vod_id": str(item.get("vod_id", "")),
                    "vod_name": item.get("vod_name", "未知"),
                    "vod_pic": item.get("vod_pic", ""),
                    "vod_remarks": item.get("vod_remarks", "")
                }
                for item in data.get("list", [])[:5] if data.get("code") == 1
            ]
        except Exception as e:
            print(f"Home Video Error: {e}")
            vod_list = []
        return json.dumps({"list": vod_list}, ensure_ascii=False)

    def categoryContent(self, tid, pg, filter, extend):
        t = int(time.time())
        key = self.generate_key(t)
        type_map = {"movie": "1", "tv": "2", "variety": "3", "anime": "4"}
        params = {
            "ac": "videolist",
            "t": type_map.get(tid, tid),
            "class": extend.get("class", ""),
            "area": extend.get("area", ""),
            "year": extend.get("year", ""),
            "lang": extend.get("lang", ""),
            "by": extend.get("order", "time"),
            "page": pg,
            "limit": "20",
            "time": str(t),
            "key": key
        }
        try:
            response = requests.post(self.api_url, data=params, headers=self.headers)
            print(f"Category API Raw Response: {response.text}")
            data = response.json()
            vod_list = [
                {
                    "vod_id": str(item.get("vod_id", "")),
                    "vod_name": item.get("vod_name", "未知"),
                    "vod_pic": item.get("vod_pic", ""),
                    "vod_remarks": item.get("vod_remarks", "")
                }
                for item in data.get("list", []) if data.get("code") == 1
            ]
            result = {
                "page": int(data.get("page", pg)),
                "pagecount": data.get("pagecount", 999),
                "limit": int(data.get("limit", 20)),
                "total": data.get("total", 9999),
                "list": vod_list
            }
        except Exception as e:
            print(f"Category Error: {e}")
            result = {"page": int(pg), "pagecount": 999, "limit": 20, "total": 9999, "list": []}
        return json.dumps(result, ensure_ascii=False)

    def detailContent(self, ids):
        vod_id = ids[0]
        detail_url = f"{self.home_url}/detail/{vod_id}/"

        try:
            print(f"Fetching detail page: {detail_url}")
            response = requests.get(detail_url, headers=self.headers)
            print(f"Detail Page HTML (first 500 chars): {response.text[:500]}")

            if response.status_code != 200:
                print(f"Failed to fetch detail page, status code: {response.status_code}")
                return json.dumps({"list": []}, ensure_ascii=False)

            html = etree.HTML(response.text)

            # 提取基本信息
            vod_name = html.xpath('//h3[@class="slide-info-title hide"]/text()')[0] if html.xpath('//h3[@class="slide-info-title hide"]/text()') else "未知"
            vod_pic = html.xpath('//div[@class="detail-pic"]/img/@data-src')[0] if html.xpath('//div[@class="detail-pic"]/img/@data-src') else ""
            vod_year = html.xpath('//div[@class="slide-info hide" and strong/text()="年代 :"]/text()')[0].strip() if html.xpath('//div[@class="slide-info hide" and strong/text()="年代 :"]/text()') else ""
            vod_remarks = html.xpath('//div[@class="slide-info hide" and strong/text()="备注 :"]/text()')[0].strip() if html.xpath('//div[@class="slide-info hide" and strong/text()="备注 :"]/text()') else ""
            vod_actor = ", ".join(html.xpath('//div[@class="slide-info hide" and strong/text()="演员 :"]/a/text()')) if html.xpath('//div[@class="slide-info hide" and strong/text()="演员 :"]/a/text()') else ""
            vod_director = ", ".join(html.xpath('//div[@class="slide-info hide" and strong/text()="导演 :"]/a/text()')) if html.xpath('//div[@class="slide-info hide" and strong/text()="导演 :"]/a/text()') else ""
            vod_content = html.xpath('//div[@class="datail-profile-text"]/p/text()')[0].strip() if html.xpath('//div[@class="datail-profile-text"]/p/text()') else html.xpath('//meta[@name="description"]/@content')[0] if html.xpath('//meta[@name="description"]/@content') else ""

            # 提取播放源和播放鏈接
            play_from_list = html.xpath('//div[@class="anthology-tab nav-swiper b-b br"]//a/text()')
            play_from_list = [name.strip().split()[0] for name in play_from_list]
            vod_play_from = "#".join(play_from_list) if play_from_list else "XiaoHongYingShi"

            play_urls = html.xpath('//ul[@class="anthology-list-play size"]/li/a/@href')
            play_names = html.xpath('//ul[@class="anthology-list-play size"]/li/a/text()')

            vod_play_url = ""
            if play_urls and play_names:
                play_url_dict = {}
                for i, url in enumerate(play_urls):
                    source_idx = url.split('-')[1]
                    if source_idx not in play_url_dict:
                        play_url_dict[source_idx] = []
                    episode_num = play_names[i].replace("第", "").replace("集", "").zfill(2)
                    play_url_dict[source_idx].append(f"第{episode_num}集${self.home_url}{url}")

                vod_play_url_parts = []
                for idx, source in enumerate(play_from_list, 1):
                    source_idx = str(idx)
                    if source_idx in play_url_dict:
                        vod_play_url_parts.append("#".join(play_url_dict[source_idx]))
                vod_play_url = "#".join(vod_play_url_parts)

            result = {
                "list": [{
                    "vod_id": vod_id,
                    "vod_name": vod_name,
                    "vod_pic": vod_pic,
                    "vod_year": vod_year,
                    "vod_remarks": vod_remarks,
                    "vod_actor": vod_actor,
                    "vod_director": vod_director,
                    "vod_content": vod_content,
                    "vod_play_from": vod_play_from,
                    "vod_play_url": vod_play_url
                }]
            }
        except Exception as e:
            print(f"Detail Error: {e}")
            result = {"list": []}
        return json.dumps(result, ensure_ascii=False)

    def searchContent(self, key, quick):
        t = int(time.time())
        key_hash = self.generate_key(t)
        params = {
            "ac": "videolist",
            "wd": key,
            "t": "",  # 移除限制，搜索所有類型
            "page": "1",
            "limit": "20",
            "time": str(t),
            "key": key_hash
        }
        try:
            response = requests.post(self.api_url, data=params, headers=self.headers)
            print(f"Search API Raw Response: {response.text}")
            data = response.json()
            print(f"Search API Parsed List: {[item['vod_name'] for item in data.get('list', [])]}")  # 添加診斷
            vod_list = [
                {
                    "vod_id": str(item.get("vod_id", "")),
                    "vod_name": item.get("vod_name", "未知"),
                    "vod_pic": item.get("vod_pic", ""),
                    "vod_remarks": item.get("vod_remarks", "")
                }
                for item in data.get("list", []) if data.get("code") == 1 and key in item.get("vod_name", "")
            ]
            if not vod_list:  # 若無精確匹配，返回所有結果
                vod_list = [
                    {
                        "vod_id": str(item.get("vod_id", "")),
                        "vod_name": item.get("vod_name", "未知"),
                        "vod_pic": item.get("vod_pic", ""),
                        "vod_remarks": item.get("vod_remarks", "")
                    }
                    for item in data.get("list", []) if data.get("code") == 1
                ]
        except Exception as e:
            print(f"Search Error: {e}")
            vod_list = []
        return json.dumps({"list": vod_list}, ensure_ascii=False)

    def playerContent(self, flag, id, vipFlags):
        try:
            response = requests.get(f"{self.home_url}{id}", headers=self.headers)
            html = etree.HTML(response.text)
            play_url = html.xpath('//video/@src') or html.xpath('//iframe/@src') or [id]
            play_url = play_url[0] if play_url else id

            result = {
                "parse": 1 if not self.isVideoFormat(play_url) else 0,
                "playUrl": "",
                "url": play_url,
                "header": json.dumps(self.headers)
            }
        except Exception as e:
            print(f"Player Error: {e}")
            result = {"parse": 1, "playUrl": "", "url": id, "header": json.dumps(self.headers)}
        return json.dumps(result, ensure_ascii=False)

    def localProxy(self, param):
        return json.dumps({"code": 0, "msg": "暂不支持本地代理"})


if __name__ == "__main__":
    spider = Spider()
    print("Home Content:", spider.homeContent(filter=True))
    print("Home Video Content:", spider.homeVideoContent())
    print("Category Content (Anime):", spider.categoryContent("anime", "1", True, {"class": "热血", "area": "日本", "year": "2024", "lang": "日语", "order": "time"}))
    print("Detail Content:", spider.detailContent(["46112"]))
    print("Search Content:", spider.searchContent("乌云之上", quick=False))