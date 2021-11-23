# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position_name = scrapy.Field()              # 职位
    place = scrapy.Field()                      # 地址
    wage = scrapy.Field()                       # 薪资
    employment_time = scrapy.Field()            # 就业时间
    academic_qualification = scrapy.Field()     # 学历
    company_name = scrapy.Field()               # 招聘公司
    company_tag = scrapy.Field()                # 公司类型
    company_staff_number = scrapy.Field()       # 公司人数
    company_Financing = scrapy.Field()          # 公司融资情况

