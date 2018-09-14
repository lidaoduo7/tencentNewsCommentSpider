# -*- coding: utf-8 -*-

from scrapy import cmdline


'''

scrapy crawl comment_spider
scrapy crawl comment_spider -o test.json
scrapy crawl comment_spider -o test.csv
'''



cmdline.execute("scrapy crawl comment_spider".split())