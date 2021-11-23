import scrapy
import requests
import logging
from lxml import html
from liepinSpider.items import LiepinspiderItem
from liepinSpider.settings import DEFAULT_REQUEST_HEADERS


class LiepincrawlerSpider(scrapy.Spider):
    name = 'liepinCrawler'
    # allowed_domains = ['web']
    start_urls_tags = ['java', '数据挖掘']
    start_urls = 'https://www.liepin.com/zhaopin/?headId=1919df6b67b0269654c84bb99a40dd53&ckId=1919df6b67b0269654c84bb99a40dd53&key={i}&currentPage={j}'
    fake_url = 'http://quotes.toscrape.com/'

    def start_requests(self):
        yield scrapy.Request(url=self.fake_url, callback=self.parse)

    def parse(self, response):
        proxy = self.get_proxy
        logging.info('receive proxy ip：', proxy, ' ...crawler start')
        for i in range(len(self.start_urls_tags)):
            for j in range(0, 10):
                item = LiepinspiderItem()
                real_url = self.start_urls.format(i=self.start_urls_tags[i], j=j)
                res = requests.get(url=real_url, proxies={'http': proxy.text}, headers=DEFAULT_REQUEST_HEADERS)
                res.encoding = 'utf-8'
                etree = html.etree.HTML(res.content)
                item['position_name'] = etree.xpath("//div[@class='job-title-box']/div[1]/text()")
                item['place'] = etree.xpath("//div[@class='job-title-box']/div[2]/span[2]/text()")
                item['wage'] = etree.xpath("//span[@class='job-salary']/text()")
                item['employment_time'] = etree.xpath("//span[@class='labels-tag'][1]/text()")
                item['academic_qualification'] = etree.xpath("//span[@class='labels-tag'][2]/text()")
                item['company_name'] = etree.xpath("//div[@class='job-company-info-box']/span/text()")
                item['company_tag'] = etree.xpath("//div[@class='job-company-info-box']/div[2]/span[1]/text()")
                item['company_Financing'] = etree.xpath("//div[@class='job-title-box']/div[2]/span[2]/text()")
                item['company_staff_number'] = etree.xpath("//div[@class='job-title-box']/div[2]/span[2]/text()")

    @property
    def get_proxy(self):
        proxy = requests.get('http://127.0.0.1:5000/get')
        return proxy






