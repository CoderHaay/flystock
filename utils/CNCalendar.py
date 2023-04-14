# -*- coding: utf-8 -*-
# @Time : 2023/3/3 16:38
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : CNCalendar.py
# @Project : src

from chinese_calendar import is_workday
# from datetime import datetime


class Calendar:
    def __int__(self):
        pass

    @staticmethod
    # 得到当前日期是否为股票交易日
    def is_trade_day(date):
        if is_workday(date):
            if date.isoweekday() < 6:
                return True
        return False

# date = '2023-03-06'
# date = datetime.strptime(date, '%Y-%m-%d').date()
#
# print(Calendar.is_trade_day(date))
