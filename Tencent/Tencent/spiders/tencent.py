# -*- coding: utf-8 -*-
''' 爬虫文件 '''
import scrapy
from Tencent.items import TencentItem


class TencentSpider(scrapy.Spider):
    ''' 处理请求和响应 '''
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = 'http://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        nodes = response.xpath("//tr[@class='even'] | //tr[@class='odd']")
        for node in nodes:
            item = TencentItem()
            item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0]
            item['positionLink'] = node.xpath("./td[1]/a/@href").extract()[0]
            if len(node.xpath("./td[2]/text()").extract()) > 0:
                item['positionType'] = node.xpath(
                    "./td[2]/text()").extract()[0]
            item['recruitNumber'] = node.xpath("./td[3]/text()").extract()[0]
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0]
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0]
            print(item)
            yield item

        # 直接拼接url,页数无法确定
        # if self.offset < 20:
        #     self.offset += 10
        #     url = self.baseURL + str(self.offset)
        #     yield scrapy.Request(url, callback=self.parse)

        if len(response.xpath("//a[@class='noactive' and @id='next']")) < 1:
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("http://hr.tencent.com/" + url, callback=self.parse)
