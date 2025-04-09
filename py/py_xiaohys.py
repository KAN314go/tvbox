import requests
from lxml import etree
import json
import hashlib
import time

class Spider:
    def getName(self):
        return "XiaoHYS"

    def init(self, extend=""):
        self.home_url = "https://www.xiaohys.com"
        self.api_url = "https://xiaohys.com/index.php/api/vod"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Origin": "https://xiaohys.com",
            "Referer": "https://xiaohys.com"
        }

    def generate_key(self, t):
        return hashlib.md5(f"DS{t}DCC147D11943AF75".encode()).hexdigest()

    def homeContent(self, filter):
        categories = [
            {"type_id": "movie", "type_name": "电影"},
            {"type_id": "tv", "type_name": "电视剧"},
            {"type_id": "variety", "type_name": "综艺"},
            {"type_id": "anime", "type_name": "动漫"}
        ]
        filters = {
            "movie": [
                {"key": "class", "name": "类型", "value": [
                    {"n": "全部", "v": ""}, {"n": "喜剧", "v": "喜剧"}, {"n": "爱情", "v": "爱情"}, {"n": "恐怖", "v": "恐怖"},
                    {"n": "动作", "v": "动作"}, {"n": "科幻", "v": "科幻"}, {"n": "剧情", "v": "剧情"}, {"n": "战争", "v": "战争"},
                    {"n": "警匪", "v": "警匪"}, {"n": "犯罪", "v": "犯罪"}, {"n": "动画", "v": "动画"}, {"n": "奇幻", "v": "奇幻"},
                    {"n": "武侠", "v": "武侠"}, {"n": "冒险", "v": "冒险"}, {"n": "枪战", "v": "枪战"}, {"n": "悬疑", "v": "悬疑"},
                    {"n": "惊悚", "v": "惊悚"}, {"n": "经典", "v": "经典"}, {"n": "青春", "v": "青春"}, {"n": "文艺", "v": "文艺"},
                    {"n": "微电影", "v": "微电影"}, {"n": "古装", "v": "古装"}, {"n": "历史", "v": "历史"}, {"n": "运动", "v": "运动"},
                    {"n": "农村", "v": "农村"}, {"n": "儿童", "v": "儿童"}, {"n": "网络电影", "v": "网络电影"}
                ]},
                {"key": "area", "name": "地区", "value": [
                    {"n": "全部", "v": ""}, {"n": "大陆", "v": "大陆"}, {"n": "香港", "v": "香港"}, {"n": "台湾", "v": "台湾"},
                    {"n": "美国", "v": "美国"}, {"n": "法国", "v": "法国"}, {"n": "英国", "v": "英国"}, {"n": "日本", "v": "日本"},
                    {"n": "韩国", "v": "韩国"}, {"n": "德国", "v": "德国"}, {"n": "泰国", "v": "泰国"}, {"n": "印度", "v": "印度"},
                    {"n": "意大利", "v": "意大利"}, {"n": "西班牙", "v": "西班牙"}, {"n": "加拿大", "v": "加拿大"}, {"n": "其他", "v": "其他"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"},
                    {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"},
                    {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"},
                    {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"},
                    {"n": "2010", "v": "2010"}
                ]},
                {"key": "lang", "name": "语言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最热", "v": "hits"}, {"n": "按评分", "v": "score"}
                ]}
            ],
            "tv": [
                {"key": "class", "name": "类型", "value": [
                    {"n": "全部", "v": ""}, {"n": "古装", "v": "古装"}, {"n": "战争", "v": "战争"}, {"n": "青春偶像", "v": "青春偶像"},
                    {"n": "喜剧", "v": "喜剧"}, {"n": "家庭", "v": "家庭"}, {"n": "犯罪", "v": "犯罪"}, {"n": "动作", "v": "动作"},
                    {"n": "奇幻", "v": "奇幻"}, {"n": "剧情", "v": "剧情"}, {"n": "历史", "v": "历史"}, {"n": "经典", "v": "经典"},
                    {"n": "乡村", "v": "乡村"}, {"n": "情景", "v": "情景"}, {"n": "商战", "v": "商战"}, {"n": "网剧", "v": "网剧"}
                ]},
                {"key": "area", "name": "地区", "value": [
                    {"n": "全部", "v": ""}, {"n": "内地", "v": "内地"}, {"n": "韩国", "v": "韩国"}, {"n": "香港", "v": "香港"},
                    {"n": "台湾", "v": "台湾"}, {"n": "日本", "v": "日本"}, {"n": "美国", "v": "美国"}, {"n": "泰国", "v": "泰国"},
                    {"n": "英国", "v": "英国"}, {"n": "新加坡", "v": "新加坡"}, {"n": "其他", "v": "其他"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"},
                    {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"},
                    {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"},
                    {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"},
                    {"n": "2010", "v": "2010"}
                ]},
                {"key": "lang", "name": "语言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最热", "v": "hits"}, {"n": "按评分", "v": "score"}
                ]}
            ],
            "variety": [
                {"key": "class", "name": "类型", "value": [
                    {"n": "全部", "v": ""}, {"n": "选秀", "v": "选秀"}, {"n": "情感", "v": "情感"}, {"n": "访谈", "v": "访谈"},
                    {"n": "播报", "v": "播报"}, {"n": "旅游", "v": "旅游"}, {"n": "音乐", "v": "音乐"}, {"n": "美食", "v": "美食"},
                    {"n": "纪实", "v": "纪实"}, {"n": "曲艺", "v": "曲艺"}, {"n": "生活", "v": "生活"}, {"n": "游戏互动", "v": "游戏互动"}
                ]},
                {"key": "area", "name": "地区", "value": [
                    {"n": "全部", "v": ""}, {"n": "内地", "v": "内地"}, {"n": "港台", "v": "港台"}, {"n": "日韩", "v": "日韩"}, {"n": "欧美", "v": "欧美"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"},
                    {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"},
                    {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"},
                    {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"},
                    {"n": "2010", "v": "2010"}
                ]},
                {"key": "lang", "name": "语言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最热", "v": "hits"}, {"n": "按评分", "v": "score"}
                ]}
            ],
            "anime": [
                {"key": "class", "name": "类型", "value": [
                    {"n": "全部", "v": ""}, {"n": "情感", "v": "情感"}, {"n": "科幻", "v": "科幻"}, {"n": "热血", "v": "热血"},
                    {"n": "推理", "v": "推理"}, {"n": "搞笑", "v": "搞笑"}, {"n": "冒险", "v": "冒险"}, {"n": "校园", "v": "校园"},
                    {"n": "动作", "v": "动作"}, {"n": "机战", "v": "机战"}, {"n": "运动", "v": "运动"}, {"n": "战争", "v": "战争"},
                    {"n": "少年", "v": "少年"}, {"n": "少女", "v": "少女"}, {"n": "原创", "v": "原创"}, {"n": "励志", "v": "励志"}
                ]},
                {"key": "area", "name": "地区", "value": [
                    {"n": "全部", "v": ""}, {"n": "国产", "v": "国产"}, {"n": "日本", "v": "日本"}, {"n": "欧美", "v": "欧美"}, {"n": "其他", "v": "其他"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"},
                    {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"},
                    {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"},
                    {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"},
                    {"n": "2010", "v": "2010"}
                ]},
                {"key": "lang", "name": "语言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最热", "v": "hits"}, {"n": "按评分", "v": "score"}
                ]}
            ]
        }
        return {"class": categories, "filters": filters if filter else {}, "parse": 0, "jx": 0}

    def homeVideoContent(self):
        try:
            response = requests.get(self.home_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = etree.HTML(response.text)
            items = html.xpath('//div[@class="slide-time-bj swiper-slide"]/a')
            vod_list = []
            for item in items[:10]:  # 限制为前10个轮播推荐
                vod_id = item.xpath('./@href')[0].split('/')[-2]
                vod_name = item.xpath('.//h3[@class="slide-info-title hide"]/text()')[0]
                vod_pic = item.xpath('.//div[contains(@class, "slide-time-img3")]/@style')[0].split("url('")[1].rstrip("');")
                remarks = item.xpath('.//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/text()')
                vod_remarks = " ".join(remarks) if remarks else ""
                vod_list.append({
                    "vod_id": vod_id,
                    "vod_name": vod_name,
                    "vod_pic": vod_pic,
                    "vod_remarks": vod_remarks
                })
            print(f"Home Video Content: {json.dumps(vod_list, ensure_ascii=False)}")
            return {"list": vod_list, "parse": 0, "jx": 0}
        except Exception as e:
            print(f"Home Video Error: {e}")
            return {"list": [], "parse": 0, "jx": 0}

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
            "pg": str(pg),
            "limit": "20",
            "time": str(t),
            "key": key
        }
        print(f"API Params: {params}")
        try:
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=10)
            data = response.json()
            print(f"API Response: {json.dumps(data, ensure_ascii=False)}")
            vod_list = [
                {
                    "vod_id": str(item.get("vod_id", "")),
                    "vod_name": item.get("vod_name", "未知"),
                    "vod_pic": item.get("vod_pic", ""),
                    "vod_remarks": item.get("vod_remarks", "")
                }
                for item in data.get("list", []) 
                if data.get("code") == 1
            ]
            return {
                "page": int(data.get("page", pg)),
                "pagecount": data.get("pagecount", 999),
                "limit": int(data.get("limit", 20)),
                "total": data.get("total", 9999),
                "list": vod_list,
                "parse": 0,
                "jx": 0
            }
        except Exception as e:
            print(f"Category Error: {e}")
            return {"page": int(pg), "pagecount": 999, "limit": 20, "total": 9999, "list": [], "parse": 0, "jx": 0}

    def detailContent(self, ids):
        try:
            vod_id = ids[0]
            url = f"https://www.xiaohys.com/detail/{vod_id}/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = etree.HTML(response.text)
            vod_item = {"vod_id": vod_id}

            vod_item["vod_name"] = html.xpath('//h1[@class="title"]/text()')[0] if html.xpath('//h1[@class="title"]/text()') else ""
            year = html.xpath('//div[contains(@class, "slide-info")]/span[@class="slide-info-remarks"]/text()')
            vod_item["vod_year"] = next((y for y in year if y.isdigit() and len(y) == 4), "")
            vod_item["vod_content"] = html.xpath('//div[@class="slide-info hide2"]/text()')[0].strip() if html.xpath('//div[@class="slide-info hide2"]/text()') else ""
            vod_item["vod_director"] = ""
            vod_item["vod_actor"] = ""
            vod_item["vod_area"] = ""
            vod_item["vod_type"] = html.xpath('//div[@class="slide-info-type"]/span/text()')[0] if html.xpath('//div[@class="slide-info-type"]/span/text()') else ""
            remarks = html.xpath('//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/text()')
            vod_item["vod_remarks"] = " ".join(remarks) if remarks else ""
            vod_item["vod_pic"] = html.xpath('//div[contains(@class, "slide-time-img3")]/@style')[0].split("url('")[1].rstrip("');") if html.xpath('//div[contains(@class, "slide-time-img3")]/@style') else ""

            play_from_list = html.xpath('//div[@class="play_source_tab"]/a/text()')
            play_url_list = []
            for i in range(len(play_from_list)):
                episodes = html.xpath(f'(//ul[@class="content_playlist"])[{i+1}]/li/a/text()')
                urls = html.xpath(f'(//ul[@class="content_playlist"])[{i+1}]/li/a/@href')
                if episodes and urls:
                    play_url = "#".join([f"{ep}${self.home_url}{url}" for ep, url in zip(episodes, urls)])
                    play_url_list.append(play_url)
                else:
                    play_url_list.append("")

            vod_item["vod_play_from"] = "$$$".join(play_from_list) if play_from_list else "默认线路"
            vod_item["vod_play_url"] = "$$$".join(play_url_list) if play_url_list else ""
            return {"list": [vod_item], "parse": 0, "jx": 0}
        except Exception as e:
            print(f"Detail Error: {e}")
            return {"list": [], "parse": 0, "jx": 0}

    def searchContent(self, key, quick, page='1'):
        t = int(time.time())
        key_hash = self.generate_key(t)
        params = {
            "ac": "videolist",
            "wd": key,
            "pg": page,
            "time": str(t),
            "key": key_hash
        }
        try:
            response = requests.get(self.api_url, params=params, headers=self.headers, timeout=10)
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
            return {"list": vod_list, "parse": 0, "jx": 0}
        except Exception as e:
            print(f"Search Error: {e}")
            return {"list": [], "parse": 0, "jx": 0}

    def playerContent(self, flag, pid, vipFlags):
        try:
            url = f"https://www.xiaohys.com{pid}"
            return {
                "url": url,
                "header": json.dumps(self.headers),
                "parse": 0,
                "jx": 0
            }
        except Exception as e:
            print(f"Player Error: {e}")
            return {"url": "", "header": "", "parse": 0, "jx": 0}

    def isVideoFormat(self, url):
        return False

    def manualVideoCheck(self):
        return False

    def localProxy(self, params):
        return None

    def destroy(self):
        pass

if __name__ == "__main__":
    spider = Spider()
    spider.init()
    print(spider.homeContent(filter=True))
    print(spider.homeVideoContent())
    print(spider.categoryContent("tv", "1", True, {"class": "古装", "area": "内地", "year": "2024", "lang": "国语", "order": "score"}))
    print(spider.detailContent(["49864"]))  # 测试《乌云之上》
    print(spider.searchContent("假面骑士", True))