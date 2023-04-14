# -*- coding: utf-8 -*-
# @Time : 2023/3/31 9:56
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : TushareApi.py
# @Project : 东方财富OCR

import tushare as ts


class TushareAPI:
    def __init__(self, token="e2fe3e1d78d8f7baa97af3887c26eb37aa62ab505f424c091b5468e5"):
        ts.set_token(token)
        self.pro = ts.pro_api()

    ################################## 沪深股票 - 基础数据  ##################################
    def get_stock_basic(self, ts_code='', exchange='', list_status='', fields=None):
        """
        获取股票基本信息

        :param ts_code:
        :param exchange: str, 交易所代码，例如：SSE 上交所，SZSE 深交所
        :param list_status: str, 上市状态，例如：L 上市，D 退市，P 暂停上市
        :param fields:
        :return: pandas.DataFrame
        """
        if fields is None:
            fields = ["ts_code", "symbol", "name", "area", "industry", "fullname",
                      "enname", "cnspell", "market", "exchange", "curr_type",
                      "list_status", "list_date", "delist_date", "is_hs"
                      ]
        return self.pro.stock_basic(ts_code=ts_code, exchange=exchange, list_status=list_status, fields=fields)

    def check_trade_date(self, now_date, fields=None):
        if fields is None:
            fields = ["exchange", "cal_date", "is_open", "pretrade_date"]
        return self.pro.trade_cal(cal_date=now_date, fields=fields)

    def get_bak_basic(self, ts_code='', trade_date='', limit='', offset='', fields=None):
        """
        备用列表  24小时重置
        """
        if fields is None:
            fields = ["ts_code", "trade_date", "total_share", "float_share"]
        return self.pro.bak_basic(ts_code=ts_code, trade_date=trade_date, limit=limit, offset=offset, fields=fields)

    def get_daily_basic(self, ts_code='', trade_date='', start_date='', end_date='', limit='', offset='', fields=None):
        """
        每日指标
        """
        if fields is None:
            # fields = ["ts_code", "trade_date", "close", "turnover_rate", "turnover_rate_f", "volume_ratio", "pe",
            #           "pe_ttm", "pb", "ps", "ps_ttm", "dv_ratio", "dv_ttm", "total_share", "float_share", "free_share",
            #           "total_mv", "circ_mv"]
            fields = ["ts_code", "trade_date", "close", "pe", "total_share", "float_share", "free_share",
                      "total_mv", "circ_mv"]
        return self.pro.daily_basic(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date,
                                    limit=limit, offset=offset, fields=fields)

    def get_moneyflow_hsgt(self, trade_date='', start_date='', end_date='', limit='', offset='', fields=None):
        """
        沪深港通资金流向
        获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。每天18~20点之间完成当日更新
        积分要求：2000积分起，5000积分每分钟可提取500次
        """
        if fields is None:
            fields = ['trade_date', 'ggt_ss', 'ggt_sz', 'hgt', 'sgt', 'north_money', 'south_money']
        return self.pro.moneyflow_hsgt(trade_date=trade_date, start_date=start_date, end_date=end_date,
                                       limit=limit, offset=offset, fields=fields)

    # 每分钟内最多调取500次，每次6000条数据
    def get_stock_daily(self, ts_code='', trade_date='', start_date='', end_date='', fields=None):
        """
        获取股票每日交易数据  -- 日线行情
        :param ts_code: str, 股票代码，例如：'000001.SZ'，'600000.SH'
        :param trade_date:
        :param start_date: str, 开始日期，例如：'20210101'
        :param end_date: str, 结束日期，例如：'20210331'
        :param fields: str, 字段列表，多个字段用逗号分隔，例如：'ts_code,trade_date,open,close'
        :return: pandas.DataFrame
        """
        if fields is None:
            fields = ["ts_code", "trade_date", "open", "high", "low", "close",
                      "pre_close", "change", "pct_chg", "vol", "amount"]
        return self.pro.daily(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date,
                              fields=fields)

    def get_stock_company(self, ts_code='', exchange='', status='', limit='', offset='', fields=None):
        if fields is None:
            fields = ["ts_code", "exchange", "chairman", "manager", "secretary", "reg_capital", "setup_date",
                      "province", "city", "website", "email", "employees"]
        return self.pro.stock_company(ts_code=ts_code, exchange=exchange, status=status, limit=limit, offset=offset,
                                      fields=fields)

    ################################## 沪深股票 - 特色数据 - 股票技术因子（量化因子）  ##################################
    def get_stk_factor(self, ts_code='', trade_date='', start_date='', end_date='', fields=None):
        """
        沪深股票 - 特色数据 -  股票技术面因子
        :param ts_code: str, 股票代码，例如：'000001.SZ'，'600000.SH'
        :param trade_date:
        :param start_date: str, 开始日期，例如：'20210101'
        :param end_date: str, 结束日期，例如：'20210331'
        :param fields: str, 字段列表，多个字段用逗号分隔，例如：'ts_code,trade_date,open,close'
        :return: pandas.DataFrame
        """
        if fields is None:
            fields = ["ts_code", "trade_date", "macd", "kdj_k", "kdj_d", "kdj_j", "rsi_6", "rsi_12", "rsi_24",
                      "boll_upper", "boll_mid", "boll_lower", "cci", "macd_dea", "macd_dif"]
        return self.pro.stk_factor(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date,
                                   fields=fields)

    def get_moneyflow(self, ts_code='', trade_date='', start_date='', end_date='', limit='', offset='', fields=None):
        """
        个股资金流向
        :param ts_code: 股票代码
        :param trade_date: 交易日期
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param limit: 单次返回数据长度
        :param offset: 请求数据的开始位移量
        :param fields:
        :return:
        """
        if fields is None:
            fields = ["ts_code", "trade_date", "buy_sm_vol", "buy_sm_amount", "sell_sm_vol", "sell_sm_amount",
                      "buy_md_vol", "buy_md_amount", "sell_md_vol", "sell_md_amount", "buy_lg_vol", "buy_lg_amount",
                      "sell_lg_vol", "sell_lg_amount", "buy_elg_vol", "buy_elg_amount", "sell_elg_vol",
                      "sell_elg_amount", "net_mf_vol", "net_mf_amount", "trade_count"]
        return self.pro.moneyflow(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date,
                                  limit=limit, offset=offset, fields=fields)

    ################################## 沪深股票 - 市场参考数据  ##################################

    def get_margin_detail(self, ts_code='', trade_date='', start_date='', end_date='', limit='', offset='',
                          fields=None):
        """
        融资融券交易明细
        :param ts_code: 股票代码
        :param trade_date: 交易日期
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param limit: 单次返回数据长度
        :param offset: 请求数据的开始位移量
        :param fields:
        :return:
        """
        if fields is None:
            fields = ["trade_date", "ts_code", "rzye", "rqye", "rzmre", "rqyl", "rzche", "rqchl", "rqmcl", "rzrqye",
                      "name"]
        return self.pro.margin_detail(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date,
                                      limit=limit, offset=offset, fields=fields)

    ################################## 指数 - 指数基本信息  ##################################
    def get_index_basic(self, ts_code="", market="", publisher="", category="", name="", limit="", offset="",
                        fields=None):
        """
        获取指数基本信息
        :param ts_code: 指数代码
        :param market: 交易所或服务商
        :param publisher: 发布商
        :param category: 指数类别
        :param name: 指数名称
        :param limit: 单次返回数据长度
        :param offset: 请求数据的开始位移量
        :param fields: 返回的字段
        :return:
        """
        if fields is None:
            fields = ["ts_code", "name", "market", "publisher", "category", "base_date", "base_point", "list_date",
                      "fullname", "index_type", "weight_rule", "desc", "exp_date"]

        return self.pro.index_basic(ts_code=ts_code, market=market, publisher=publisher, category=category, name=name,
                                    limit=limit, offset=offset, fields=fields)

    def get_index_daily(self, ts_code, trade_date='', start_date='', end_date='', limit='', offset='',
                        fields=None):
        """
        指数日线行情 每分钟最多访问该接口300次
        :param ts_code: 指数代码
        :param trade_date:
        :param start_date:
        :param end_date:
        :param limit:
        :param offset:
        :param fields:
        :return:
        """

        if fields is None:
            fields = ["ts_code", "trade_date", "close", "open", "high", "low", "pre_close", "change", "pct_chg", "vol",
                      "amount"
                      ]
        return self.pro.index_daily(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date,
                                    limit=limit, offset=offset, fields=fields)

# 在实例化 TushareAPI 类时需要传入 tushare 的 token，例如：

# api = TushareAPI()
# 然后就可以调用类中定义的方法获取股票数据和基本信息，例如：

# 获取 A 股股票的基本信息
# stock_info = api.get_stock_basic(exchange='SSE', fields='ts_code,symbol,name,area')
# print(stock_info)

# # 获取某只股票的每日交易数据和复权因子数据
# daily_data = api.get_stock_daily(ts_code='000001.SZ', start_date='20210101', end_date='20210331',
#                                  fields='ts_code,trade_date,open,close')
# adj_factor = api.get_stock_adj_factor(ts_code='000001.SZ', start_date='20210101', end_date='20210331',
#                                       fields='ts_code,trade_date,adj_factor')

# daily_data = api.get_stock_daily()
# print(daily_data)
