# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import re,json
class WeixinfocomPipeline(object):
    def __init__(self):
        self.title_set = set()
    def process_item(self, item, spider):
        # 去重
        if item["title"] in self.title_set:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.title_set.add(item["title"])
        path = r"D:\desktop\python actual\python spider\weixinfocom\weixinfoimags\weixinfo.json"
        with open(path,"a+",encoding="utf-8") as f:
            f.write(json.dumps(dict(item),ensure_ascii=False) + "\n")
        return item
# 写存储图片的piplines管道，继承自ImagesPipeline类，存图片是，获取的url最好是放在列表里面
class ImagePipeline(ImagesPipeline):
    # 写存储图片的函数
    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for image_url in item['details_image']:
            if image_url:
                yield Request(image_url, meta={"data": item["title"],"classify":item["classify"]})
    # 重写图片存放的目录名及文件名的函数
    def file_path(self, request, response=None, info=None):
        # 接收传递过来的title作为图片的存放目录
        name = re.sub(r'[?\\*|“<>:/]',"",request.meta["data"])
        classify = request.meta["classify"]
        # 提取url后面的图片名称
        if "www." in request.url:
            image_guid = request.url.split("/")[-1]
        else:
            image_guid = item["details_image"].index(request.url)
        # 分文件存储的关键，{0}对应着name,对应着目录名，{1}对应着image_guid，对应着文件名
        filename = u'{0}/{1}/{2}'.format(classify,name, image_guid)
        return filename
    # 将图片的地址从网址变成本地的路径
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if item["details_image"][0] == "":
            item['details_image'] = image_paths
        else:
            if image_paths:
                item["thumbnail"] = image_paths[0]
                item["details_image"] = image_paths[1:]
            else:
                item["thumbnail"] = ""
                item["details_image"] = ""
        return item
