# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class WeixinfocomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题
    title = Field()
    # 分类
    classify = Field()
    # 简介
    introduction = Field()
    # 缩略图
    thumbnail = Field()
    # 详情图
    details_image = Field()
    # 发布时间
    release_time = Field()
    # 联系方式
    contact = Field()
    # 详情内容
    details = Field()
