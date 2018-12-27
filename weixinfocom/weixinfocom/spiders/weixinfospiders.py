# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from weixinfocom.items import WeixinfocomItem
from weixinfocom.conversion import Conversion
class Weixinfo(CrawlSpider):
    name = "weixinfo.com"
    allowed_domains = ["www.weixinfo.com"]
    start_urls = [
        "https://www.weixinfo.com/huazhuangpin/index_0.html",
        "https://www.weixinfo.com/shechipin/index_0.html"
    ]
    def parse(self, response):
        infos = response.xpath('//div[@class="nl_wxc"]/dl')
        for info in infos:
            item = WeixinfocomItem()
            # 标题
            item["title"] = info.xpath('dd/h3/a/text()').extract()[0].strip()
            # 分类
            classify = response.url.split("/")[-2]
            item["classify"] = Conversion().conversion(str(classify))
            # 简介
            item["introduction"] = info.xpath('dd/span/text()').extract()[0].strip()
            # 发布时间
            item["release_time"] = info.xpath('dd/h6/text()').extract()[0][5:].strip()
            # 缩略图
            thumbnail = info.xpath('dt/a/img/@src').extract()
            if thumbnail:
                item["thumbnail"] = thumbnail[0]
            else:
                item["thumbnail"] = ""
            # 详情页url
            detail_url = r"https://www.weixinfo.com" + info.xpath('dd/h3/a/@href').extract()[0]
            yield Request(url=detail_url,callback=self.parse_details,meta={"item":item})
        # 下一页链接
        pages = int(response.xpath('//div[@class="page_list"]/a/b/text()').extract()[0])
        if pages % 10 == 0:
            page = pages // 10
        else:
            page = pages // 10 + 1
        urls = ["https://www.weixinfo.com" + "/" + response.url.split("/")[-2] + "/index_{}.html".format(str(i)) for i in range(1,page)]
        for url in urls:
            yield Request(url=url, callback=self.parse, dont_filter=False)
    def parse_details(self,response):
        item = response.meta["item"]
        # 详情页，联系方式
        contact = ""
        # 详情页的内容
        details = ""
        # 详情页的图片
        detail_image = []
        detail_image.append(item["thumbnail"])
        # 联系方式
        infos = response.xpath('//ul[@class="soft2"]/li')
        for info in infos[:4]:
            contact1 = info.xpath('text()').extract()[0].strip()
            contact2 = info.xpath('span/text()').extract()
            if contact2:
                contact2 = contact2[0].strip()
            else:
                contact2 = ""
            contact = contact + contact1 + contact2 + ","
        item["contact"] = contact[:-1]
        # 详情页内容
        detail = response.xpath('//div[@class="content"]//text()').extract()
        for deta in detail:
            details = details + deta.strip()
        item["details"] = details
        # 图片
        detail_images = response.xpath('//div[@class="content"]//img/@src').extract()
        if detail_images:
            for img in detail_images:
                if img[0] == "/":
                    detail_image.append(r"https://www.weixinfo.com" + img)
                else:
                    detail_image.append(img)
        else:
            detail_image.append("")
        item["details_image"] = detail_image
        yield item