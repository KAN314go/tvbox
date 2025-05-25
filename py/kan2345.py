import time
from urllib import request
import re
import random
from fake_useragent import UserAgent
import pymysql
from hashlib import md5
class DianYing2345Spider(object):
    # 初始化以及连接数据库
    def __init__(self):
        self.url='https://kan.2345.com/vip/list/--movie--0---{}.html'
        self.db=pymysql.connect(host='localhost',user='root',password='123456',database='filmskydb',charset='utf8')
        self.cursor=self.db.cursor()

    # 发起请求
    def get_html(self,url):
        headers={
            'User-Agent': UserAgent().random
        }
        req=request.Request(url=url,headers=headers)
        res=request.urlopen(req)
        # 得到响应
        html=res.read().decode('gb2312','ignore')#ignore忽略解析不了的字符串
        return html

    # 解析一级页面得到个电影url
    def parse_html(self,one_url):
        #得到一级页面
        one_html=self.get_html(one_url)
        #正则匹配
        re_dbs='<a class="aPlayBtn" href="(.*?)" target="_blank"'
        link_list=self.re_func(re_dbs,one_html)
        # print(link_list)
        for link in link_list:
            # 得到二级页面的链接
            two_url=link
            # self.save_html(two_url)
            # time.sleep(random.randint(1,3))
            # 增量爬取，md5加密
            s=md5()
            s.update(two_url.encode())
            finger=s.hexdigest()
            if self.is_go_on(finger):
                self.save_html(two_url)
                time.sleep(random.randint(1,3))

                # 保存指纹
                self.save_finger(finger)
            else:
                print("已经下载过")
    # 正则解析方法
    def re_func(self, re_dbs, html):
        pattern = re.compile(re_dbs, re.S)
        r_list = pattern.findall(html)
        return r_list

# 保存二级页面内容
    def save_html(self,two_url):
        two_html=self.get_html(two_url)
        re_dbs='<a class="aPlayBtn_show" href="(.*?)" target="_blank".*?<div class="tit">.*?<h1>(.*?)<em class="emScore">(.*?)</em>.*?</h1>'
        film_list=self.re_func(re_dbs,two_html)
        # print(film_list)
        #得到的数据存到数据库
        ins = 'insert into films values(%s,%s,%s)'
        for film in film_list:
            L = [
                film[0].strip(),
                film[1].strip(),
                film[2].strip()
            ]
            print(L)
        self.cursor.execute(ins, L)
        # 千万别忘了提交到数据库执行
        self.db.commit()


    def run(self):
        for offset in range(1,2):
            url=self.url.format(offset)
            self.parse_html(url)
            time.sleep(random.randint(1,3))


    # 增量爬取，判断指纹是否继续
    def is_go_on(self,finger):
        sql='select finger from request_finger where finger=%s'
        r=self.cursor.execute(sql,[finger])
        if not r:
            return True

    # 保存指纹
    def save_finger(self,finger):
        sql = 'insert into request_finger values(%s)'
        self.cursor.execute(sql, [finger])
        self.db.commit()
if __name__ == '__main__':
    spider=DianYing2345Spider()
    spider.run()