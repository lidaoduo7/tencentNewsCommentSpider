# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentnewscommentspiderItem(scrapy.Item):
    hot_subject = scrapy.Field() #热点的主题
    source = scrapy.Field()  #来源
    second_source = scrapy.Field()  # 二级来源
    title = scrapy.Field()  #标题
    content = scrapy.Field()  #内容
    link = scrapy.Field()  #链接
    pubtime = scrapy.Field()  #发布时间
    date = scrapy.Field()  #发布日期
    comments = scrapy.Field() #评论，包含评论内容和评论时间字段

    # comment = scrapy.Field()  #评论内容
    # comment_time = scrapy.Field()  # 评论时间

    terminal = scrapy.Field()  #终端





