# -*- coding: utf-8 -*-
import scrapy
import re
import json
import datetime
import requests
from tencentNewsCommentSpider.items import TencentnewscommentspiderItem
from scrapy.selector import Selector
import datetime
import socket

'''
简介：爬取腾讯新闻评论
解析参考 https://www.cnblogs.com/bigyang/p/8941672.html
20180914
1- 直接给出评论页面网址 http://coral.qq.com/3082500237
2- 浏览器审查元素，网络，刷新，找出真正的请求地址
http://coral.qq.com/article/3082500237/comment/v2?callback=_article3082500237commentv2&orinum=10&oriorder=o
&pageflag=1&cursor=0&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1536906868563
3- 浏览器审查元素，网络，【点击查看更多的评论】
http://coral.qq.com/article/3082500237/comment/v2?callback=_article3082500237commentv2&orinum=10&oriorder=o
&pageflag=1&cursor=6444817531328604004&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1&_=1536906868566
4- 【6444817531328604004】对应页面中的last值
5- 这个页面的解析，无法用xpath
6- 从新闻页面获取评论页面的cmt_id
'''


class CommentSpiderSpider(scrapy.Spider):
    name = 'comment_spider'
    allowed_domains = ['coral.qq.com']
    # start_urls = ['http://coral.qq.com/']
    # start_urls = ['http://hn.qq.com/a/20180910/029307.htm']
    start_urls = ['http://hn.qq.com/a/20180910/029307.htm',
                  'http://hn.qq.com/a/20180916/039002.htm',
                  'http://hn.qq.com/a/20180626/013102.htm',
                  'http://hn.qq.com/a/20180823/050027.htm',
                  'http://hn.qq.com/a/20161115/038479.htm',
                  'http://hn.qq.com/a/20160226/056722.htm',
                  'http://hn.qq.com/a/20180912/082456.htm',
                  'http://hn.qq.com/a/20161227/033389.htm',
                  'http://hn.qq.com/a/20171108/024211.htm',
                  'http://hn.qq.com/a/20180604/038348.htm',
                  'http://hn.qq.com/a/20180510/022456.htm',
                  'http://hn.qq.com/a/20180719/035934.htm',
                  'http://hn.qq.com/a/20171122/017869.htm',
                  'http://hn.qq.com/a/20160804/014680.htm',
                  'http://hn.qq.com/a/20171128/059455.htm',
                  'http://hn.qq.com/a/20180919/010893.htm',
                  'http://hn.qq.com/a/20180919/014495.htm',
                  'http://hn.qq.com/a/20170327/015273.htm',
                  'http://hn.qq.com/a/20161223/019175.htm',
                  'http://hn.qq.com/a/20171019/019442.htm',
                  'http://hn.qq.com/a/20170622/042305.htm'
                  ]

    hot_event_dict = {
        "http://hn.qq.com/a/20180910/029307.htm":"吉首非法拘禁案",
        "http://hn.qq.com/a/20180916/039002.htm":"吉首寻亲",
        "http://hn.qq.com/a/20180626/013102.htm":"吉首交通",
        "http://hn.qq.com/a/20180823/050027.htm":"吉首交通",
        "http://hn.qq.com/a/20161115/038479.htm":"吉首高铁",
        "http://hn.qq.com/a/20160226/056722.htm":"吉首高铁",
        "http://hn.qq.com/a/20180912/082456.htm":"吉首好人好事",
        "http://hn.qq.com/a/20161227/033389.htm":"吉首PPP项目",
        "http://hn.qq.com/a/20171108/024211.htm":"吉首PPP项目",
        "http://hn.qq.com/a/20180604/038348.htm":"吉首治安",
        "http://hn.qq.com/a/20180510/022456.htm":"吉首治安",
        "http://hn.qq.com/a/20180719/035934.htm":"吉首治安",
        "http://hn.qq.com/a/20171122/017869.htm":"吉首治安",
        "http://hn.qq.com/a/20160804/014680.htm":"吉首智慧城市",
        "http://hn.qq.com/a/20171128/059455.htm":"吉首治安",
        "http://hn.qq.com/a/20180919/010893.htm":"霸座",
        "http://hn.qq.com/a/20180919/014495.htm":"霸座",
        "http://hn.qq.com/a/20170327/015273.htm":"吉首高铁",
        "http://hn.qq.com/a/20161223/019175.htm":"吉首高铁",
        "http://hn.qq.com/a/20171019/019442.htm":"湘西特色文化",
        "http://hn.qq.com/a/20170622/042305.htm":"吉首建设"
    }

    def get_hot_subject(self,url):
        return self.hot_event_dict[str(url)]

    def parse(self, response):
        item = TencentnewscommentspiderItem()
        selector = Selector(response)
        print("网页信息")
        print(response.url)

        pubtime = re.findall(re.compile(r"pubtime:'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})'"),str(response.text))
        cmtid = re.findall(re.compile(r'cmt_id = (\d+)'), str(response.text))
        # print(pubtime[0])
        item['pubtime'] = pubtime[0]


        date = re.findall(re.compile(r"(\d{4}-\d{1,2}-\d{1,2})"),str(pubtime[0]))
        item['date'] = date[0]


        news_title = re.findall(re.compile(r"title:(.*)"), str(response.text))
        item['title'] = news_title[0]
        # results = self.parse_coral("3082500237")
        results,commentnum = self.parse_coral(str(cmtid[0])) #从新闻页面获取评论页面的cmt_id
        # item['comments'] = results

        # comment_time = results[0][0]
        # comment = results[0][1]
        # item['comments'] = {'comment_time':comment_time,'comment':comment}

        comments_list = []
        for i in range(len(results)):
            comment_time = results[i][0]
            comment = results[i][1]
            comments_dict = {'comment_time':comment_time,'comment':comment}
            comments_list.append(comments_dict)
        item['comments'] = comments_list

        passage = selector.xpath('//div[@class="qq_article"]//div[@class="bd"]//div[@class="Cnt-Main-Article-QQ"]/p/text()').extract()
        res_str = ''
        for every_pas in passage:
            res_str += every_pas
        item['content'] = res_str

        # item['comments'] = {'comment':u'','comment_time':''}

        # item['hot_subject'] = "吉首非法拘禁案"
        # item['hot_subject'] = "吉首寻亲"
        hot_subject = self.get_hot_subject(response.url)
        item['hot_subject'] = hot_subject

        item['source'] = "news"
        item['second_source'] = "tencentNews"
        item['link'] = response.url
        item['terminal'] = ""
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # item['crawl_time'] = now_time
        machine_node = socket.gethostname()
        # item['machine_node'] = machine_node
        IP = socket.gethostbyname(machine_node)
        # item['IP'] = IP
        item['comments_num'] = commentnum

        yield item
        # for i in range(len(results)):
        #     print(results[i])
        #     item['comment_time'] = results[i][0]
        #     item['comment']  = results[i][1]
        #     yield item

    def parse_coral(self, commentid):
        '''
        获取腾讯新闻评论内容、时间、评论数
        :param cmtid: 评论网址http://coral.qq.com/3082500237中的3082500237
        :return: （[时间，评论内容]，评论数）
        '''
        url1 = 'http://coral.qq.com/article/' + commentid + '/comment/v2?callback=_article' + commentid + 'commentv2&orinum=10&oriorder=o&pageflag=1&cursor='
        url2 = '&orirepnum=10&_=1536906868563'
        # 一定要加头要不然无法访问,orinum=10表示返回评论的数目为10，最大为30
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        response = self.getHTMLText(url1 + '0' + url2, headers)     # 查看更多评论，不断更改cursor的值

        result = []
        commentnum = 0
        while 1:
            pattern = "_article" + commentid + "commentv2\\((.+)\\)"
            g = re.search(pattern, response)
            out = json.loads(g.group(1))
            print("评论数：")
            print(out["data"]["targetInfo"]["commentnum"])
            commentnum = out["data"]["targetInfo"]["commentnum"]
            if not out["data"]["last"]:
                print("finish！")
                break;
            for i in out["data"]["oriCommList"]:
                time = str(datetime.datetime.fromtimestamp(int(i["time"])))  # 将unix时间戳转化为正常时间
                # line = json.dumps(time + ':' + i["content"], ensure_ascii=False) + '\n'
                # print(i["content"])
                # print("评论时间")
                # print(time)
                # result.append(i["content"])
                # result.append({time:i["content"]})
                result.append((time, i["content"]))

            url = url1 + out["data"]["last"] + url2  # 得到下一个评论页面链接
            # print("下一个评论页面链接")
            # print(url)
            response = self.getHTMLText(url, headers)
        return result,commentnum

    def getHTMLText(self, url, headers):
        try:
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return "产生异常 "