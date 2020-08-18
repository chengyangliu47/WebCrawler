# -*- coding: utf-8 -*-
from scrapy import Spider
import scrapy_gui
import scrapy
from indeed.items import IndeedItem


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    allowed_domains = ["ca.indeed.com"]
    Q = None
    start_url = None
    page = 0

    def start_requests(self):
        self.Q.put('Start Crawling')
        for result_num in range(0, self.page):
            page = '&start=%d' % (result_num*10)
            url = self.start_url + page
            if '%2C' in url:
                    url = url.replace('%2C', ',')
            #url = 'https://ca.indeed.com/jobs?q=java&l=Ottawa,+ON&start=%d' % (result_num*10)
            self.Q.put(url)
            yield scrapy.Request(url)

    def parse(self, response):
        for clickCard in response.xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result"]'):
            # 初始化Item
            items = IndeedItem()
            self.Q.put('Initialized......')

            # jobTitle
            items['jobTitle'] = clickCard.xpath(
                './/h2/a/@title').extract()[0]
            self.Q.put('title parsed......')

            # companyName
            if clickCard.xpath('.//div/span[@class="company"]/text()').extract()[0].strip() == '':
                items['companyName'] = clickCard.xpath(
                    './/div/span[@class="company"]/a/text()').extract()[0].strip()
            else:
                items['companyName'] = clickCard.xpath(
                    './/div/span[@class="company"]/text()').extract()[0].strip()
            self.Q.put('companyName parsed......')

            # url
            items['url'] = clickCard.xpath(
                './/h2/a/@href').extract()[0]
            self.Q.put('url parsed......')

            self.Q.put(f"\n{items['jobTitle']}\n{items['companyName']}\n{items['url']}\n")
            yield items

    def close(spider, reason):
        spider.Q.put('Crawling Finished')
