# -*- coding: utf-8 -*-
# @Time : 2023/3/29 14:35
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : trade_date.py
# @Project : 东方财富OCR

from Database import Database
import json
import time
import os
from Tools import Tools
from utils.CNCalendar import Calendar
import datetime

# "host": "59.110.162.95",
# "user": "flystock",
# "password": "JyHCwfXKpY0e5RZq",
# "db_name": "flystock"


# 定义一个装饰器，用于计算函数执行的时间
def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} 运行耗时: {end_time - start_time:.4f} seconds to execute.")
        return result

    return wrapper


@calculate_time
def main():
    with open('config_pre.json', encoding='utf-8') as f:
        # 读取文件
        result = json.load(f)

    # print(result)
    host = result["host"]
    user = result["user"]
    password = result["password"]
    db_name = result["db_name"]

    now_date = Tools.get_current_date()

    db = Database(host=host, user=user, db_password=password, db_name=db_name)
    # 判断全年日期是否为交易日
    start_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2023, 12, 31)
    delta = datetime.timedelta(days=1)

    current_date = start_date
    while current_date <= end_date:
        if Calendar.is_trade_day(current_date):
            print('{} 是交易日'.format(current_date))
            db.insert("hm_trade_date", {"date": current_date.strftime('%Y-%m-%d')})
        else:
            print('{} 不是交易日'.format(current_date))
        current_date += delta
    db.close()


if __name__ == '__main__':
    main()
