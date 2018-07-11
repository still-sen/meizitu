# -*- coding: utf-8 -*-
# @Time             :  2018/6/30 16:52
# @Author           :  lenovo;
# @project_name     :  work_space
# @File             :  meizitu_spider.py
# @Software         :  PyCharm
# @belong to file   :  妹子图爬虫


#为了深度爬虫采集使用crawlspider
from scrapy.spider import CrawlSpider,Rule

#爬虫请求
from scrapy import Request

#获取定义的item
from meizitu_scrapy.items import MeizituScrapyItem

#深度爬取提取链接
from scrapy.linkextractors import LinkExtractor

import copy

#scrapy.Spider 是普通的爬虫开发，当使用深度采集时要换crawlspider类
#CrawlSpider类定义了一些规则(rule)来提供跟进link的方便的机制，
# 从爬取的网页中获取link并继续爬取的工作更适合。

class MeiZiTu(CrawlSpider):
    '''
    定义开发爬虫
    '''
    #启动名称
    name = 'meizitu'
    allowed_domains=['meizitu.com']
    start_urls=['http://www.meizitu.com/a/more_1.html',]

    #定义链接提取规则
    link_extractor=LinkExtractor(
        #正则匹配，还有其他操作
        allow=(r'http://www.meizitu.com/a/more_\d+.html')
    )
    #定义链接操作规则
    rules = [
        Rule(link_extractor,follow=True,callback='parse_item'),
    ]


    def parse_item(self,response):

        #获得定义的item函数，封装数据
        item = MeizituScrapyItem()

        #处理响应得到的数据
        img_list=response.xpath("//div[@class='con']/h3[@class='tit']/a")

        #将得到的土图片专辑列表for循环得到每一个图集
        for i in img_list:

            #图集的名字和图集的链接
            name=i.xpath("string(.)").extract()[0]
            url=i.xpath('@href').extract()[0]

            # 封装
            item['name'] = name
            item['url'] = url

            #获取每个图集的具体页面图片
            yield Request(url,meta={'item':copy.deepcopy(item)},callback=self.img_url)

            # print(item)

            yield item

    def img_url(self,response):

        '''
        取出每张图片的URL放在URLS里
        :param response:
        :return:
        '''

        item = response.meta['item']
        #获取图集的每张图片链接
        img_list=response.xpath("//div[@id='picture']/p/img/@src").extract()

        #将链接传递使用
        item['image_urls'] = img_list
        return item



 
 


