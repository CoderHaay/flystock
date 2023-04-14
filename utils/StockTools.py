# -*- coding: utf-8 -*-
# @Time : 2023/3/14 17:51
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : StockTools.py
# @Project : src

import tushare as ts
import datetime

# 初始化pro接口
pro = ts.pro_api('e2fe3e1d78d8f7baa97af3887c26eb37aa62ab505f424c091b5468e5')


class StockTools:
    def __init__(self):
        pass

    @staticmethod
    def get_stock_exchange(stock_code):
        if stock_code.startswith("6"):
            return "SH"
        elif stock_code.startswith("0") or stock_code.startswith("3") or stock_code.startswith("002"):
            return "SZ"
        else:
            return None

    # 与发行日期比较，如果发行日期晚于目标日期，则只采集到发行日
    @staticmethod
    def get_issue_date(code):
        stock_exchange_code = StockTools.get_stock_exchange(code)
        if stock_exchange_code is None:
            return None
        stock_code = code + ".{}".format(stock_exchange_code)

        # 设置 token
        ts.set_token("e2fe3e1d78d8f7baa97af3887c26eb37aa62ab505f424c091b5468e5")
        # 初始化 tushare
        local_pro = ts.pro_api()
        try:
            company_info = local_pro.stock_basic(exchange='', list_status='L', fields='ts_code, name, list_date')
            issue_date = company_info[company_info['ts_code'] == stock_code]['list_date'].values[0]
            issue_date = datetime.datetime.strptime(issue_date, "%Y%m%d").date()
            return issue_date
        except Exception as err:
            return None

    # 获取股票列表
    @staticmethod
    def get_stock_basic(code=None):
        df = pro.stock_basic(**{
            "ts_code": code
        }, fields=[
            "name",
            "area",  # 地域
            "industry",  # 所属行业
            "market",  # 市场类型 主板
            "list_date",
            "ts_code"
        ])

        return df

    # 获取上市公司基本信息
    @staticmethod
    def get_stock_company(code=None):
        # 拉取数据
        df = pro.stock_company(**{
            "ts_code": code
        }, fields=[
            "ts_code",
            "province",
            "city"
        ])

        return df
