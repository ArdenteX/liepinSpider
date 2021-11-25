import random
import time
import scrapy
import requests
from lxml import html
from liepinSpider.items import LiepinspiderItem
from liepinSpider.settings import HEADERS


class LiepincrawlerSpider(scrapy.Spider):
    name = 'liepinCrawler'
    # allowed_domains = ['web']
    start_urls_tags = ['java', '数据挖掘', 'php', 'python', 'Docker', 'Hadoop', 'ios', 'Html5', 'C', 'Go', '推荐系统',
                       'Spark', 'HBase', 'Ruby', 'Javascript', 'ASP', 'C++', 'U3D', 'web前端', '全栈工程师', 'Android', 'ui设计师', '视觉设计师'
                       , '原画师', '数据分析师', '平面设计师', '运营经理', '测试工程师']
    start_urls = 'https://www.liepin.com/zhaopin/?key={i}&currentPage={j}'
    fake_url = 'https://quotes.toscrape.com/'

    def start_requests(self):

        yield scrapy.Request(url=self.fake_url, callback=self.parse)

    def parse(self, response):
        proxy = self.get_proxy
        error_count = 0
        self.logger.info(proxy.text, ' ...crawler start')
        for i in range(len(self.start_urls_tags)):
            for j in range(0, 10):
                real_url = self.start_urls.format(i=self.start_urls_tags[i], j=j)

                if error_count == 15:
                    proxy = self.get_proxy
                    error_count = 0
                    time.sleep(30)

                time.sleep(random.randint(20, 26))
                res = requests.get(real_url, proxies={"http": proxy.text}, timeout=15, headers=HEADERS)
                print(res.url)
                res.encoding = 'utf-8'
                etree = html.etree.HTML(res.content)
                self.logger.info("to_item method is working")
                position_names = etree.xpath("//div[@class='job-title-box']/div[1]/text()")
                places = etree.xpath("//div[@class='job-title-box']/div[2]/span[2]/text()")
                wages = etree.xpath("//span[@class='job-salary']/text()")
                employment_times = etree.xpath("//span[@class='labels-tag'][1]/text()")
                academic_qualifications = etree.xpath("//span[@class='labels-tag'][2]/text()")
                company_names = etree.xpath("//div[@class='job-company-info-box']/span/text()")
                company_tag1 = etree.xpath("//div[@class='job-company-info-box']/div[2]/span[1]/text()")
                company_tags = etree.xpath("//div[@class='job-company-info-box']/div[2]/span/text()")
                suit_tags = self.suit_tags(tag1=company_tag1, tag_all=company_tags)
                for position_name, place, wage, times, qualification, company_name, tags in zip(position_names, places,
                                                                                                wages,
                                                                                                employment_times,
                                                                                                academic_qualifications,
                                                                                                company_names,
                                                                                                suit_tags):
                    item = LiepinspiderItem()
                    item['position_name'] = position_name
                    item['place'] = place
                    item['wage'] = wage
                    item['employment_time'] = times
                    item['academic_qualification'] = qualification
                    item['company_name'] = company_name
                    item['company_tag'] = tags[0]
                    if len(tags) == 1:
                        continue

                    if len(tags) == 2:
                        if '人' in tags[1]:
                            item['company_staff_number'] = tags[1]
                            item['company_Financing'] = 'null'
                        else:
                            item['company_Financing'] = tags[1]
                            item['company_staff_number'] = 'null'

                    if len(tags) == 3:
                        item['company_Financing'] = tags[1]
                        item['company_staff_number'] = tags[2]
                    yield item

                if 'safe' in res.url:
                    proxy = self.get_proxy
                    continue
                error_count += 1

    def to_item(self, etree):
        self.logger.info("to_item method is working")
        position_names = etree.xpath("//div[@class='job-title-box']/div[1]/text()")
        places = etree.xpath("//div[@class='job-title-box']/div[2]/span[2]/text()")
        wages = etree.xpath("//span[@class='job-salary']/text()")
        employment_times = etree.xpath("//span[@class='labels-tag'][1]/text()")
        academic_qualifications = etree.xpath("//span[@class='labels-tag'][2]/text()")
        company_names = etree.xpath("//div[@class='job-company-info-box']/span/text()")
        company_tag1 = etree.xpath("//div[@class='job-company-info-box']/div[2]/span[1]/text()")
        company_tags = etree.xpath("//div[@class='job-company-info-box']/div[2]/span/text()")
        suit_tags = self.suit_tags(tag1=company_tag1, tag_all=company_tags)
        for position_name, place, wage, times, qualification, company_name, tags in zip(position_names, places, wages,
                                                                                        employment_times,
                                                                                        academic_qualifications,
                                                                                        company_names, suit_tags):
            item = LiepinspiderItem()
            item['position_name'] = position_name
            item['place'] = place
            item['wage'] = wage
            item['employment_time'] = times
            item['academic_qualification'] = qualification
            item['company_name'] = company_name
            item['company_tag'] = suit_tags[0]
            if len(suit_tags) == 1:
                continue

            if len(suit_tags) == 2:
                if '人' in suit_tags[1]:
                    item['company_staff_number'] = suit_tags[1]
                else:
                    item['company_Financing'] = suit_tags[1]

            if len(suit_tags) == 3:
                item['company_Financing'] = suit_tags[1]
                item['company_staff_number'] = suit_tags[2]
            yield item

    def suit_tags(self, tag1, tag_all):
        marker = [0] * len(tag_all)
        index = 0

        for i in range(0, len(tag_all)):
            if index == len(tag1):
                break
            if tag_all[i] == tag1[index]:
                marker[i] = 1
                index += 1

        a = []
        b = []
        for i in range(len(tag_all)):
            if i == len(tag_all):
                break

            a.append(tag_all[i])
            if i == len(tag_all) - 1:
                break
            i += 1

            if marker[i] == 1:
                b.append(a)
                a = []
                continue

        return b

    @property
    def get_proxy(self):
        proxy = requests.get('http://127.0.0.1:5000/get')
        return proxy
