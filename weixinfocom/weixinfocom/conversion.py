# -*- coding: utf-8 -*-
class Conversion(object):
    def conversion(self,string):
        if string == "huazhuangpin":
            return "化妆品"
        elif string == "shechipin":
            return "奢侈品"
        elif string == "nannvbao":
            return "男女包"
        elif string == "nvzhuang":
            return "女装"
        elif string == "nanzhuang":
            return "男装"
        elif string == "nvxie":
            return "女鞋"
        elif string == "nanxie":
            return "男鞋"
        elif string == "tongzhuang":
            return "童装"
        elif string == "meishi":
            return "美食"
        elif string == "qita":
            return "其他"
        else:
            return False