# -*- coding: utf-8 -*-
# @Time : 2023/3/29 17:01
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : ticker.py
# @Project : 东方财富OCR

from Database import Database
import json
import time
import os
from Tools import Tools
from utils.CNCalendar import Calendar
import datetime

from utils.DateUtils import DateUtils
from utils.StockTools import StockTools
from utils.TushareApi import TushareAPI


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


# 拉取当前所有的股票数据
def insert_basic(ts_code=None):
    df = StockTools.get_stock_basic(ts_code)
    for index, row in df.iterrows():
        # val = (row['ts_code'], row['name'], row['area'])
        code = row['ts_code']
        val = db.select_one("hm_ticker", "code='{}'".format(code))
        if val is None:
            db.insert("hm_ticker", {"CODE": row['ts_code'], "NAME": row['name']})
        else:
            continue
            # print(val)
            # val = db.update("hm_ticker", {"NAME": row['name'], "PROVINCE": "哈哈12"}, "code='{}'".format(code))
            # print(val)

            # last_id = db.replace("hm_ticker", {"CODE": row['ts_code'], "NAME": row['name'], "PROVINCE": row['area']})
            # print(last_id)


def update_company(ts_code=None):
    df_company = tushareApi.get_stock_company(ts_code)
    for index, row in df_company.iterrows():
        print(row)
        code = row['ts_code']
        province = row['province']
        city = row['city']

        val = db.select_one("hm_ticker", "code='{}'".format(code))
        if val:
            db.update("hm_ticker", {"EMCODE": code, "PROVINCE": province, "CITY": city}, "code='{}'".format(code))
        else:
            print("************ 不用更新 {} *************".format(code))


# 更新到指定日期
def update_daily_basic(ts_code=None, trade_date=None):
    df_daily = tushareApi.get_daily_basic(ts_code, trade_date=trade_date)
    if len(df_daily) == 0:
        print("*********** 数据为空 *************")
        return False
    for index, row in df_daily.iterrows():
        # val = (row['ts_code'], row['name'], row['area'])
        # print(row)
        code = row['ts_code']
        totalshare = row['total_share'] * 10000  # 总股本
        liqshare = row['float_share'] * 10000  # 流通股本
        freeliqshare = row['free_share'] * 10000  # 自由流通股本
        close = row['close']  # 收盘价
        mv = row['total_mv'] * 10000  # 总市值
        freefloatmv = row['circ_mv'] * 10000  # 自由流通市值
        pe = row['pe']  # 市盈率

        val = db.select_one("hm_ticker", "code='{}'".format(code))
        if val:
            sql = 'UPDATE hm_ticker set totalshare = {}, liqshare = {} , freeliqshare = {} , close = {} ,  mv = {} ,  freefloatmv = {} ,  pe = {}  , last = "{}" WHERE CODE = "{}"'.format(
                totalshare, liqshare, freeliqshare, close, mv, freefloatmv, pe, DateUtils.str_to_date2(trade_date),
                code)
            sql = sql.replace("None", "NULL")
            db.insert_by_sql(sql)


@calculate_time
def main():
    ts_code = None
    # ts_code = "000004.SZ"
    trade_date = "20230331"
    insert_basic(ts_code)
    # update_company(ts_code)
    # update_daily_basic(ts_code, trade_date)


"""
股票列表
日线行情 get_stock_daily
个股资金流向 *** 
沪深港通资金流向 *** 
融资融券交易明细
指数基本信息
指数日线行情
"""

if __name__ == '__main__':
    with open('config_pre.json', encoding='utf-8') as f:
        # 读取文件
        result = json.load(f)
    host = result["host"]
    user = result["user"]
    password = result["password"]
    db_name = result["db_name"]
    db = Database(host=host, user=user, db_password=password, db_name=db_name)
    tushareApi = TushareAPI()
    main()
    # update_date = "2023/03/31"
    # print(DateUtils.str_to_date(update_date))

    db.close()
