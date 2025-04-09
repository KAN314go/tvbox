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
                {"key": "class", "name": "類型", "value": [
                    {"n": "全部", "v": ""}, {"n": "喜剧", "v": "喜剧"}, {"n": "爱情", "v": "爱情"}, {"n": "恐怖", "v": "恐怖"},
                    {"n": "动作", "v": "动作"}, {"n": "科幻", "v": "科幻"}, {"n": "剧情", "v": "剧情"}, {"n": "战争", "v": "战争"},
                    {"n": "警匪", "v": "警匪"}, {"n": "犯罪", "v": "犯罪"}, {"n": "动画", "v": "动画"}, {"n": "奇幻", "v": "奇幻"},
                    {"n": "武侠", "v": "武侠"}, {"n": "冒险", "v": "冒险"}, {"n": "枪战", "v": "枪战"}, {"n": "悬疑", "v": "悬疑"},
                    {"n": "惊悚", "v": "惊悚"}, {"n": "经典", "v": "经典"}, {"n": "青春", "v": "青春"}, {"n": "文艺", "v": "文艺"},
                    {"n": "微电影", "v": "微电影"}, {"n": "古装", "v": "古装"}, {"n": "历史", "v": "历史"}, {"n": "运动", "v": "运动"},
                    {"n": "农村", "v": "农村"}, {"n": "儿童", "v": "儿童"}, {"n": "网络电影", "v": "网络电影"}
                ]},
                {"key": "area", "name": "地區", "value": [
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
                    {"n": "2010", "v": "2010"}, {"n": "2009", "v": "2009"}, {"n": "2008", "v": "2008"}, {"n": "2007", "v": "2007"},
                    {"n": "2006", "v": "2006"}, {"n": "2005", "v": "2005"}, {"n": "2004", "v": "2004"}, {"n": "2003", "v": "2003"},
                    {"n": "2002", "v": "2002"}, {"n": "2001", "v": "2001"}, {"n": "2000", "v": "2000"}, {"n": "1999", "v": "1999"},
                    {"n": "1998", "v": "1998"}
                ]},
                {"key": "lang", "name": "語言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "法语", "v": "法语"},
                    {"n": "德语", "v": "德语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}
                ]}
            ],
            "tv": [
                {"key": "class", "name": "類型", "value": [
                    {"n": "全部", "v": ""}, {"n": "古装", "v": "古装"}, {"n": "战争", "v": "战争"}, {"n": "青春偶像", "v": "青春偶像"},
                    {"n": "喜剧", "v": "喜剧"}, {"n": "家庭", "v": "家庭"}, {"n": "犯罪", "v": "犯罪"}, {"n": "动作", "v": "动作"},
                    {"n": "奇幻", "v": "奇幻"}, {"n": "剧情", "v": "剧情"}, {"n": "历史", "v": "历史"}, {"n": "经典", "v": "经典"},
                    {"n": "乡村", "v": "乡村"}, {"n": "情景", "v": "情景"}, {"n": "商战", "v": "商战"}, {"n": "网剧", "v": "网剧"},
                    {"n": "其他", "v": "其他"}
                ]},
                {"key": "area", "name": "地區", "value": [
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
                {"key": "lang", "name": "語言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}
                ]}
            ],
            "variety": [
                {"key": "class", "name": "類型", "value": [
                    {"n": "全部", "v": ""}, {"n": "选秀", "v": "选秀"}, {"n": "情感", "v": "情感"}, {"n": "访谈", "v": "访谈"},
                    {"n": "播报", "v": "播报"}, {"n": "旅游", "v": "旅游"}, {"n": "音乐", "v": "音乐"}, {"n": "美食", "v": "美食"},
                    {"n": "纪实", "v": "纪实"}, {"n": "曲艺", "v": "曲艺"}, {"n": "生活", "v": "生活"}, {"n": "游戏互动", "v": "游戏互动"},
                    {"n": "财经", "v": "财经"}, {"n": "求职", "v": "求职"}
                ]},
                {"key": "area", "name": "地區", "value": [
                    {"n": "全部", "v": ""}, {"n": "内地", "v": "内地"}, {"n": "港台", "v": "港台"}, {"n": "日韩", "v": "日韩"}, {"n": "欧美", "v": "欧美"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"},
                    {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"},
                    {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"},
                    {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"},
                    {"n": "2010", "v": "2010"}
                ]},
                {"key": "lang", "name": "語言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}
                ]}
            ],
            "anime": [
                {"key": "class", "name": "類型", "value": [
                    {"n": "全部", "v": ""}, {"n": "情感", "v": "情感"}, {"n": "科幻", "v": "科幻"}, {"n": "热血", "v": "热血"},
                    {"n": "推理", "v": "推理"}, {"n": "搞笑", "v": "搞笑"}, {"n": "冒险", "v": "冒险"}, {"n": "萝莉", "v": "萝莉"},
                    {"n": "校园", "v": "校园"}, {"n": "动作", "v": "动作"}, {"n": "机战", "v": "机战"}, {"n": "运动", "v": "运动"},
                    {"n": "战争", "v": "战争"}, {"n": "少年", "v": "少年"}, {"n": "少女", "v": "少女"}, {"n": "社会", "v": "社会"},
                    {"n": "原创", "v": "原创"}, {"n": "亲子", "v": "亲子"}, {"n": "益智", "v": "益智"}, {"n": "励志", "v": "励志"},
                    {"n": "其他", "v": "其他"}
                ]},
                {"key": "area", "name": "地區", "value": [
                    {"n": "全部", "v": ""}, {"n": "国产", "v": "国产"}, {"n": "日本", "v": "日本"}, {"n": "欧美", "v": "欧美"}, {"n": "其他", "v": "其他"}
                ]},
                {"key": "year", "name": "年份", "value": [
                    {"n": "全部", "v": ""}, {"n": "2025", "v": "2025"}, {"n": "2024", "v": "2024"}, {"n": "2023", "v": "2023"},
                    {"n": "2022", "v": "2022"}, {"n": "2021", "v": "2021"}, {"n": "2020", "v": "2020"}, {"n": "2019", "v": "2019"},
                    {"n": "2018", "v": "2018"}, {"n": "2017", "v": "2017"}, {"n": "2016", "v": "2016"}, {"n": "2015", "v": "2015"},
                    {"n": "2014", "v": "2014"}, {"n": "2013", "v": "2013"}, {"n": "2012", "v": "2012"}, {"n": "2011", "v": "2011"},
                    {"n": "2010", "v": "2010"}
                ]},
                {"key": "lang", "name": "語言", "value": [
                    {"n": "全部", "v": ""}, {"n": "国语", "v": "国语"}, {"n": "英语", "v": "英语"}, {"n": "粤语", "v": "粤语"},
                    {"n": "闽南语", "v": "闽南语"}, {"n": "韩语", "v": "韩语"}, {"n": "日语", "v": "日语"}, {"n": "其它", "v": "其它"}
                ]},
                {"key": "order", "name": "排序", "value": [
                    {"n": "按最新", "v": "time"}, {"n": "按最熱", "v": "hits"}, {"n": "按評分", "v": "score"}
                ]}
            ]
        }
        return json.dumps({"class": categories, "filters": filters if filter else {}}, ensure_ascii=False)

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
        print(f"API Params: {params}")
        try:
            response = requests.post(self.api_url, data=params, headers=self.headers)
            data = response.json()
            print(f"API Response: {json.dumps(data, ensure_ascii=False)}")  # 打印完整響應
            vod_list = [
                {
                    "vod_id": str(item.get("vod_id", "")),
                    "vod_name": item.get("vod_name", "未知"),
                    "vod_pic": item.get("vod_pic", ""),
                    "vod_remarks": item.get("vod_remarks", "")
                }
                for item in data.get("list", []) 
                if data.get("code") == 1 and ("集" not in item.get("vod_remarks", "") or tid != "movie")
            ]
            return json.dumps({
                "page": int(data.get("page", pg)),
                "pagecount": data.get("pagecount", 999),
                "limit": int(data.get("limit", 20)),
                "total": data.get("total", 9999),
                "list": vod_list
            }, ensure_ascii=False)
        except Exception as e:
            print(f"Category Error: {e}")
            return json.dumps({"page": int(pg), "pagecount": 999, "limit": 20, "total": 9999, "list": []}, ensure_ascii=False)

    def detailContent(self, ids):
        try:
            vod_id = ids[0]
            base_url = "https://www.xiaohys.com"
            url = f"{base_url}/detail/{vod_id}/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = etree.HTML(response.text)
            vod_item = {"vod_id": vod_id}

            vod_item["vod_name"] = html.xpath('//h3[@class="slide-info-title hide"]/text()')[0] if html.xpath('//h3[@class="slide-info-title hide"]/text()') else ""
            # 放寬年份提取條件，避免正則表達式依賴
            year_candidates = html.xpath('//span[@class="slide-info-remarks"]/a/text()')
            vod_item["vod_year"] = next((y for y in year_candidates if y.isdigit() and len(y) == 4), "")
            vod_content = "".join(html.xpath('//div[@id="height_limit"]/text()')).strip()
            vod_item["vod_content"] = vod_content.replace("\xa0", " ").replace("\u3000", " ").strip()
            directors = html.xpath('//div[contains(@class, "slide-info hide")]/strong[contains(text(), "导演")]/following-sibling::a/text()')
            vod_item["vod_director"] = " / ".join(directors) if directors else ""
            actors = html.xpath('//div[contains(@class, "slide-info hide")]/strong[contains(text(), "演员")]/following-sibling::a/text()')
            vod_item["vod_actor"] = " / ".join(actors) if actors else ""
            vod_item["vod_area"] = html.xpath('//span[@class="slide-info-remarks"]/a[contains(@href, "area")]/text()')[0] if html.xpath('//span[@class="slide-info-remarks"]/a[contains(@href, "area")]') else ""
            types = html.xpath('//span[@class="slide-info-remarks"]/a[contains(@href, "show/")]/text()')
            vod_item["vod_type"] = " ".join(types) if types else ""
            vod_item["vod_remarks"] = html.xpath('//div[contains(@class, "slide-info hide")]/strong[contains(text(), "备注")]/following-sibling::text()')[0].strip() if html.xpath('//div[contains(@class, "slide-info hide")]/strong[contains(text(), "备注")]/following-sibling::text()') else ""
            vod_item["vod_pic"] = html.xpath('//div[@class="detail-pic"]/img/@data-src')[0] if html.xpath('//div[@class="detail-pic"]/img/@data-src') else ""

            play_from_list = [name.replace("\xa0", "").strip() for name in html.xpath('//div[@class="anthology-tab nav-swiper b-b br"]/div[@class="swiper-wrapper"]/a/text()')]
            play_url_list = []
            for i in range(len(play_from_list)):
                episodes = html.xpath(f'(//div[contains(@class, "anthology-list-box")])[{i+1}]//ul[@class="anthology-list-play size"]/li/a/text()')
                urls = html.xpath(f'(//div[contains(@class, "anthology-list-box")])[{i+1}]//ul[@class="anthology-list-play size"]/li/a/@href')
                if episodes and urls:
                    play_url = "#".join([f"{ep}${base_url}{url}" for ep, url in zip(episodes, urls)])
                    play_url_list.append(play_url)
                else:
                    play_url_list.append("")

            vod_item["vod_play_from"] = "$$$".join(play_from_list)
            vod_item["vod_play_url"] = "$$$".join(play_url_list)
            return json.dumps({"list": [vod_item]}, ensure_ascii=False)
        except Exception as e:
            print(f"Detail Error: {e}")
            return json.dumps({"list": []}, ensure_ascii=False)

if __name__ == "__main__":
    spider = Spider()
    print(spider.homeContent(filter=True))
    print(spider.categoryContent("tv", "1", True, {"class": "古装", "area": "内地", "year": "2024", "lang": "国语", "order": "score"}))
    print(spider.detailContent(["49751"]))