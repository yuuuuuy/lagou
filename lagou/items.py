# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    position_name = scrapy.Field()  # 职位名称
    city = scrapy.Field()  # 城市
    business_zones = scrapy.Field()  # 工作区域
    company_full_name = scrapy.Field()  # 公司全称
    company_short_name = scrapy.Field()  # 公司简称
    company_lable_list = scrapy.Field()  # 公司福利
    company_size = scrapy.Field()  # 公司规模
    education = scrapy.Field()  # 要求学历
    finance_stage = scrapy.Field()  # 财务情况
    first_type = scrapy.Field()  # 一级分类 如后端、前端
    industry_field = scrapy.Field()  # 领域
    job_nature = scrapy.Field()  # 工作性质
    position_lables = scrapy.Field()  # 职位标签
    salary = scrapy.Field()  # 薪资范围
    salary_max = scrapy.Field()  # 最高薪资
    salary_min = scrapy.Field()  # 最低薪资
    salary_avg = scrapy.Field()  # 平均薪资
    second_type = scrapy.Field()  # 二级分类 如Java、Python、C++
    work_year = scrapy.Field()  # 工作年限

