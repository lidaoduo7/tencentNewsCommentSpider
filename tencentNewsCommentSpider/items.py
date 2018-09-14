# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentnewscommentspiderItem(scrapy.Item):
    # define the fields for your item here like:
    time = scrapy.Field()
    comment = scrapy.Field()
    news_title = scrapy.Field()
    news_pubtime = scrapy.Field()
    # news_link = scrapy.Field()
    # hot_event = scrapy.Field()


