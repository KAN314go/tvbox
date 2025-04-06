import requests
import json

class Spider:
    def __init__(self):
        self.home_url = "https://hlove.tv"
        self.api_url = "https://app.ymedium.top/v3/web/api/filter"
        self.default_pic = "https://pic.rmb.bdstatic.com/bjh/default/8f948e47e8e73a7bfd7c2f548a492e6e.png"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": self.home_url,
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Sec-Ch-Ua": '"Chromium";v="134", "Not-A.Brand";v="24", "Google Chrome";v="134"'
        }

    def categoryContent(self, cid, page, filter, ext):
        _year = ext.get('year', 'all')
        _class = ext.get('class', 'all')
        _area = ext.get('area', 'all')
        
        # 映射字段值為中文
        chName_map = {
            "movie": "电影",
            "tv": "电视剧",
            "anime": "动漫",
            "variety": "综艺",
            "kids": "动画片"  # 更新為 "动画片"
        }

        # 劇情分類映射
        label_map = {
            # 通用分類
            "juqing": "剧情",
            "xiju": "喜剧",
            "dongzuo": "动作",
            "jingsong": "惊悚",
            "aiqing": "爱情",
            "kongbu": "恐怖",
            "fanzui": "犯罪",
            "maoxian": "冒险",
            "qihuan": "奇幻",
            "xuanyi": "悬疑",
            "kehuan": "科幻",
            "jiating": "家庭",
            "donghua": "动画",
            "lishi": "历史",
            "zhanzheng": "战争",
            "yinyue": "音乐",
            "dongman": "动漫",
            "dianshidianying": "电视电影",
            "xibu": "西部",
            "wangluodianying": "网络电影",
            "jilu": "纪录",
            "tongxing": "同性",
            "gewu": "歌舞",
            "zainan": "灾难",
            "dongzuomaoxian": "动作冒险",
            "dongzuoandmaoxian": "动作&冒险",
            "zhanzhengandzhengzhi": "战争&政治",
            # 電視劇特有
            "feizaoju": "肥皂剧",
            "duanju": "短剧",
            "ertong": "儿童",
            "zhenshixiu": "真人秀",
            "tuokouxiu": "脱口秀",
            "zuian": "罪案",
            "guzhuang": "古装",
            "oumeiju": "欧美剧",
            "dushi": "都市",
            "yingju": "英剧",
            "gangtaiju": "港台剧",
            "qingchun": "青春",
            "hanju": "韩剧",
            "xinwen": "新闻",
            "chuanyue": "穿越",
            "junlv": "军旅",
            "xuanhuan": "玄幻",
            "jilu": "纪录",
            "yanqing": "言情",
            "jingfei": "警匪",
            "yinyueju": "音乐剧",
            "shangzhan": "商战",
            "guochanju": "国产剧",
            "xinmataiju": "新马泰",
            "wuxia": "武侠",
            # 綜藝特有
            "wanhui": "晚会",
            "jilupian": "纪录片",
            # 動漫特有
            "mohuan": "魔幻",
            "rexue": "热血",
            "lianaiju": "恋爱",
            "baoxiao": "爆笑",
            "xiaoyuan": "校园",
            "jingji": "竞技",
            "shaonv": "少女",
            "paomian": "泡面",
            "gedou": "格斗",
            "zhiyu": "治愈",
            "jizhan": "机战",
            "tuili": "推理",
            "danmei": "耽美",
            "juchangban": "剧场版",
            "qita": "其它"
        }

        # 地區分類映射
        country_map = {
            "cn": "中国大陆",
            "us": "美国",
            "kr": "韩国",
            "hk": "香港",
            "tw": "台湾",
            "jp": "日本",
            "uk": "英国",
            "th": "泰国",
            "es": "西班牙",
            "ca": "加拿大",
            "fr": "法国",
            "in": "印度",
            "au": "澳大利亚",
            "other": "其他地区"
        }
        
        # 設置請求體
        payload = {
            "chName": chName_map.get(cid, "电影"),
            "startTime": int(_year) if _year != 'all' else 0,
            "endTime": int(_year) if _year != 'all' else 0,
            "label": label_map.get(_class, _class) if _class != 'all' else "",
            "country": country_map.get(_area, _area) if _area != 'all' else "",
            "pageSize": 12,  # 調整為 12，與新請求一致
            "page": int(page)
        }
        
        d = []
        try:
            print(f"Requesting API: {self.api_url} with payload {json.dumps(payload, ensure_ascii=False)}")
            res = self.session.post(self.api_url, headers=self.headers, json=payload, timeout=20)
            res.raise_for_status()
            data = res.json()
            
            # 打印原始響應以便調試
            print(f"API Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            # 檢查響應狀態
            if data.get('code') != 0:
                raise Exception(f"API error: code={data.get('code')}, message={data.get('message', 'Unknown error')}")
            
            # 檢查數據結構
            if 'data' not in data:
                raise Exception("Invalid API response: 'data' field missing")
            
            # 提取數據
            total = data['data'].get('total', 0)
            items = data['data'].get('list', [])
            
            for item in items:
                vod_id = f"/vod/detail/{item.get('id', '')}"
                vod_name = item.get('name', '')
                vod_pic = item.get('img', self.default_pic)
                if not vod_pic or vod_pic.startswith('/api/images/init'):
                    vod_pic = self.default_pic
                
                # 處理 countStr，截斷過長的更新信息，並處理 "更新至0集"
                vod_remarks = item.get('countStr', '')
                if vod_remarks == "更新至0集":
                    vod_remarks = "尚未更新"
                elif vod_remarks and len(vod_remarks) > 15:
                    vod_remarks = vod_remarks[:15] + "..."
                
                if not vod_id or not vod_name:
                    continue
                    
                d.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name,
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            
            # 調整 pagecount 計算邏輯
            pagecount = (total + 11) // 12 if total > 0 else 0  # 調整為每頁 12 條
            return {
                'list': d,
                'page': int(page),
                'pagecount': pagecount,
                'limit': 12,
                'total': total
            }
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {
                'list': d,
                'page': int(page),
                'pagecount': 0,
                'limit': 12,
                'total': 0
            }

# 測試代碼
if __name__ == "__main__":
    spider = Spider()
    # 測試電影（動作，美國）
    print("=== 測試電影（動作，美國） ===")
    result = spider.categoryContent("movie", "1", True, {"year": "2024", "class": "dongzuo", "area": "us"})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試電視劇（古装，中國大陸，無年份限制）
    print("\n=== 測試電視劇（古装，中國大陸，無年份限制） ===")
    result = spider.categoryContent("tv", "1", True, {"class": "guzhuang", "area": "cn"})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試綜藝（真人秀，中國大陸）
    print("\n=== 測試綜藝（真人秀，中國大陸） ===")
    result = spider.categoryContent("variety", "1", True, {"year": "2024", "class": "zhenshixiu", "area": "cn"})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試動漫（热血，日本）
    print("\n=== 測試動漫（热血，日本） ===")
    result = spider.categoryContent("anime", "1", True, {"year": "2024", "class": "rexue", "area": "jp"})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 測試兒童（儿童，中國大陸，無年份限制）
    print("\n=== 測試兒童（儿童，中國大陸，無年份限制） ===")
    result = spider.categoryContent("kids", "4", True, {"class": "ertong", "area": "cn"})
    print(json.dumps(result, ensure_ascii=False, indent=2))