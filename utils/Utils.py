# -*- coding: utf-8 -*-
# @Time : 2023/4/3 18:12
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : Utils.py
# @Project : 东方财富OCR
import datetime


def log(msg):
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {msg}")


class Utils(object):
    def __int__(self):
        pass

    @staticmethod
    def convert_value(value, times=10000):
        return value * times if value is not None else None
