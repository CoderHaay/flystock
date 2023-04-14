# -*- coding: utf-8 -*-
# @Time : 2023/4/3 18:13
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : DateUtils.py
# @Project : 东方财富OCR
from datetime import datetime, timedelta


class DateUtils(object):

    @staticmethod
    def get_current_time():
        return datetime.now()

    @staticmethod
    def get_current_date():
        return datetime.date.today()

    @staticmethod
    def str_to_date(date_str, fmt="%Y/%m/%d"):
        if isinstance(date_str, str):
            return datetime.strptime(date_str, fmt).date()
        else:
            return date_str

    @staticmethod
    def str_to_date2(date_str, fmt="%Y%m%d"):
        if isinstance(date_str, str):
            return datetime.strptime(date_str, fmt).date()
        else:
            return date_str

    @staticmethod
    def date_to_str(date_obj, fmt="%Y-%m-%d"):
        if isinstance(date_obj, str):
            return date_obj
        return datetime.strftime(date_obj, fmt)

    @staticmethod
    def date_to_str2(date_obj, fmt="%Y%m%d"):
        if isinstance(date_obj, str):
            return date_obj

        return datetime.strftime(date_obj, fmt)

    @staticmethod
    def get_back_day_str(trade_date):
        """
        倒退一天，返回字符串日期
        :param trade_date:
        :return:
        """
        trade_date = DateUtils.str_to_date2(trade_date)
        trade_date -= timedelta(days=1)
        trade_date = DateUtils.date_to_str2(trade_date)
        return trade_date

