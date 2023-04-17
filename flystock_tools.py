# -*- coding: utf-8 -*-
# @Time : 2023/3/31 10:00
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : flystock_tools.py
# @Project : 东方财富OCR
import datetime

from Model.BaseModel import Base, User
from Model.HmIndicatorDay import HmIndicatorDay
from Model.HmTradeDate import HmTradeDate
from Model.HmTuIndexBasic import HmTuIndexBasic
from Model.HmTuIndexDaily import HmTuIndexDaily
from Model.HmTuMarginDetail import HmTuMarginDetail
from Model.HmTuMoneyflow import HmTuMoneyflow
from Model.HmTuQuotationDay import HmTuQuotationDay
from Model.HmTuMoneyflowHsgt import HmTuMoneyflowHsgt
from Model.HmTuStkFactor import HmTuStkFactor
from Model.HmTuTicker import HmTuTicker
from utils.DateUtils import DateUtils
from utils.TushareApi import TushareAPI
from Database import Database
import json
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import threading
from sqlalchemy.orm import scoped_session
import numpy as np
from utils.Utils import log
from utils.Utils import Utils


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        log(f"Function {func.__name__} 运行耗时: {end_time - start_time:.4f} seconds to execute.")
        return result

    return wrapper


def init_db_dev():
    log("***************** 本地开发环境 ***************")
    with open('config.json', encoding='utf-8') as f:
        # 读取文件
        result = json.load(f)
    host = result["host"]
    user = result["user"]
    password = result["password"]
    db_name = result["db_name"]
    # db = Database(host=host, user=user, db_password=password, db_name=db_name)
    # 建立数据库连接 https://www.jianshu.com/p/ad1d936951ea
    # echo：设置为True时会打印日志
    # pool_size：连接池的大小默认为5个，设置为0时表示连接无限制
    # pool_recycle：设置时间以限制数据库多久没连接自动断开
    return create_engine('mysql+pymysql://{}:{}@{}:3306/{}'.format(user, password, host, db_name), echo=False,
                         pool_size=8, pool_recycle=3600)


def init_db_pre():
    log("***************** 线上环境 ***************")
    with open('config_pre.json', encoding='utf-8') as f:
        # 读取文件
        result = json.load(f)
    host = result["host"]
    user = result["user"]
    password = result["password"]
    db_name = result["db_name"]
    # db = Database(host=host, user=user, db_password=password, db_name=db_name)
    # 建立数据库连接 https://www.jianshu.com/p/ad1d936951ea
    # echo：设置为True时会打印日志
    # pool_size：连接池的大小默认为5个，设置为0时表示连接无限制
    # pool_recycle：设置时间以限制数据库多久没连接自动断开
    return create_engine('mysql+pymysql://{}:{}@{}:3306/{}'.format(user, password, host, db_name), echo=False,
                         pool_size=8, pool_recycle=3600)


# 股票的基本信息 入库
def update_tu_ticker():
    code = None
    # code = "000001.SZ"
    # 获取 A 股股票的基本信息
    data = tushareApi.get_stock_basic(code)
    # 将数据转换为 DataFrame 格式
    df = pd.DataFrame(data)
    # 将第一行的 'code' 键改为 'code'
    df = df.rename(columns={'ts_code': 'code'})

    # 将数据写入数据库
    for _, row in df.iterrows():
        # 查询数据库中是否已经存在该记录
        query = global_session.query(HmTuTicker).filter_by(CODE=row['code'])
        record = query.first()

        # 根据记录是否存在来插入或更新数据
        if record:
            record.symbol = row['symbol']
            record.NAME = row['name']
            record.area = row['area']
            record.industry = row['industry']
            record.fullname = row['fullname']
            record.enname = row['enname']
            record.cnspell = row['cnspell']
            record.market = row['market']
            record.exchange = row['exchange']
            record.curr_type = row['curr_type']
            record.list_status = row['list_status']
            record.list_date = row['list_date']
            record.delist_date = row['delist_date']
            record.is_hs = row['is_hs']
            log("{}: 更新完成".format(row['name']))
        else:
            new_record = HmTuTicker(
                CODE=row['code'],
                symbol=row['symbol'],
                NAME=row['name'],
                area=row['area'],  # 地域
                industry=row['industry'],  # 所属行业
                fullname=row['fullname'],  # 股票全称
                enname=row['enname'],  # 英文全称
                cnspell=row['cnspell'],  # 拼音缩写
                market=row['market'],  # 市场类型
                exchange=row['exchange'],  # 交易所代码
                curr_type=row['curr_type'],  # 交易货币
                list_status=row['list_status'],  # 上市状态
                list_date=row['list_date'],  # 上市日期
                delist_date=row['delist_date'],  # 退市日期
                is_hs=row['is_hs'],  # 是否沪深港通标的
            )
            log("{}: 插入完成".format(row['name']))
            global_session.add(new_record)

    # 提交修改并关闭连接
    try:
        global_session.commit()
    except Exception as e:
        # 处理异常的代码
        log(f"发生了异常：{e}")
        global_session.rollback()


# 是否是交易日
def is_trade_day(now_date):
    result = global_session.query(HmTradeDate).filter(HmTradeDate.DATE == now_date).first()
    if result:
        return True
    return False


# 获取股票每日交易数据
def get_stock_daily(code=None, trade_date=None, start_date=None, end_date=None):
    if trade_date is None:
        trade_date = DateUtils.date_to_str2(DateUtils.get_current_time())
    if start_date is None:
        start_date = DateUtils.date_to_str2(DateUtils.get_current_time())
    if end_date is None:
        end_date = DateUtils.date_to_str2(DateUtils.get_current_time())

    count = 0
    log("trade_date = {}, start_date = {}, end_state = {}".format(trade_date, start_date, end_date))
    while start_date <= end_date:
        log("************ {} ************".format(start_date))
        trade_date = start_date
        result = is_trade_day(trade_date)
        if result is False:
            start_date = (datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=1)).strftime(
                '%Y%m%d')
            continue
        count += 1
        if count > 500:
            log("************* 开始等待... *************")
            time.sleep(2)
            count = 0
        # 获取股票每日交易数据
        data = tushareApi.get_stock_daily(code, trade_date)
        # 将数据转换为 DataFrame 格式
        df = pd.DataFrame(data)
        if df.empty:
            start_date = (datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=1)).strftime(
                '%Y%m%d')
            continue

        df = df.rename(columns={'trade_date': 'date'})
        df = df.rename(columns={'ts_code': 'code'})
        # 去掉时分秒
        df['date'] = pd.to_datetime(df['date']).dt.date
        # log("df = {}".format(df))
        daily_data_list = []
        for index, row in df.iterrows():
            model = HmTuQuotationDay(CODE=row['code'], DATE=row['date'], open=row["open"], high=row["high"],
                                     low=row["low"],
                                     close=row["close"], pre_close=row["pre_close"], change=row["change"],
                                     pct_chg=row["pct_chg"], vol=row["vol"], amount=row["amount"])
            daily_data_list.append(model)

        global_session.add_all(daily_data_list)
        try:
            global_session.commit()
        except Exception as e:
            # 处理异常的代码
            log(f"发生了异常：{e}")
            global_session.rollback()
        start_date = (datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')
        time.sleep(0.15)


def get_stock_daily_with_trade(trade_date=None):
    if trade_date is None:
        trade_date = DateUtils.date_to_str2(DateUtils.get_current_time())

    log("trade_date = {}".format(trade_date))
    result = is_trade_day(trade_date)
    if result is False:
        return False

    # 获取股票日交易数据
    data = tushareApi.get_stock_daily(trade_date=trade_date)
    # 将数据转换为 DataFrame 格式
    df = pd.DataFrame(data)
    if df.empty:
        log("数据为空")
        return False
    df = df.rename(columns={'trade_date': 'date'})
    df = df.rename(columns={'ts_code': 'code'})
    # 去掉时分秒
    df['date'] = pd.to_datetime(df['date']).dt.date
    # log("df = {}".format(df))
    daily_data_list = []
    for index, row in df.iterrows():
        model = HmTuQuotationDay(CODE=row['code'], DATE=row['date'], open=row["open"], high=row["high"],
                                 low=row["low"],
                                 close=row["close"], pre_close=row["pre_close"], change=row["change"],
                                 pct_chg=row["pct_chg"], vol=row["vol"], amount=row["amount"])
        daily_data_list.append(model)

    global_session.add_all(daily_data_list)
    try:
        global_session.commit()
    except Exception as e:
        # 处理异常的代码
        log(f"发生了异常：{e}")
        global_session.rollback()


def get_hsgt_money_flow(start_trade_date=None, end_trade_date=None):
    log("***************** 8 沪深港通资金流向入库 ***************")
    if start_trade_date is None:
        start_trade_date = DateUtils.date_to_str2(DateUtils.get_current_time())
    if end_trade_date is None:
        end_trade_date = DateUtils.date_to_str2(DateUtils.get_current_time())
    log("start_trade_date = {}, end_trade_date = {}".format(start_trade_date, end_trade_date))
    count = 0
    trade_date = end_trade_date
    while start_trade_date <= end_trade_date:
        result = is_trade_day(trade_date)
        if result is False:
            trade_date = DateUtils.get_back_day_str(trade_date)
            end_trade_date = trade_date
            continue
        existing_Hsgt = global_session.query(HmTuMoneyflowHsgt).filter_by(DATE=trade_date).first()
        if existing_Hsgt:
            trade_date = DateUtils.get_back_day_str(trade_date)
            end_trade_date = trade_date
            continue

        log("************ {} ***********".format(trade_date))
        count += 1
        if count > 295:
            log("************* 开始等待... *************")
            time.sleep(1)
            count = 0

        data = tushareApi.get_moneyflow_hsgt(trade_date=trade_date)
        # 将数据转换为 DataFrame 格式
        df = pd.DataFrame(data)
        if df.empty:
            log("沪深港通资金流向 {} 数据为空".format(trade_date))
            trade_date = DateUtils.get_back_day_str(trade_date)
            end_trade_date = trade_date
            continue
        df = df.rename(columns={'trade_date': 'date'})
        print(df.head(1))
        hsgt_list = []
        for index, row in df.iterrows():
            model = HmTuMoneyflowHsgt(DATE=row['date'],
                                      ggt_ss=Utils.convert_value(row['ggt_ss'], 1000000),
                                      ggt_sz=Utils.convert_value(row['ggt_sz'], 1000000),
                                      hgt=Utils.convert_value(row['hgt'], 1000000),
                                      sgt=Utils.convert_value(row['sgt'], 1000000),
                                      north_money=Utils.convert_value(row['north_money'], 1000000),
                                      south_money=Utils.convert_value(row['south_money'], 1000000))
            hsgt_list.append(model)

        global_session.add_all(hsgt_list)
        try:
            global_session.commit()
        except Exception as e:
            # 处理异常的代码
            # log(f"发生了异常：{e}")
            global_session.rollback()

        trade_date = DateUtils.get_back_day_str(trade_date)
        end_trade_date = trade_date
        time.sleep(0.22)

    log("***************** 8 沪深港通资金流向入库完成 ***************")
    global_session.close()


def update_index_basic():
    ts_code = None
    # ts_code = "000001.CZC"

    data = tushareApi.get_index_basic(ts_code=ts_code)
    # 将数据转换为 DataFrame 格式
    df = pd.DataFrame(data)
    df = df.replace(np.nan, None)
    df = df.rename(columns={'ts_code': 'code'})
    print(df.head(1))
    log("数据量：{}".format(len(df)))

    # 将数据写入数据库
    for _, row in df.iterrows():
        # 查询记录
        record = global_session.query(HmTuIndexBasic).filter_by(CODE=row['code']).first()
        # 更新记录或插入新记录
        if record:
            # 如果记录存在，则更新对应字段的值
            record.NAME = row['name']
            record.fullname = row['fullname']
            record.market = row['market']
            record.publisher = row['publisher']
            record.index_type = row['index_type']
            record.category = row['category']
            record.base_date = row['base_date']
            record.base_point = row['base_point']
            record.list_date = row['list_date']
            record.weight_rule = row['weight_rule']
            record.desc = row['desc']
            record.exp_date = row['exp_date']
        else:
            # 如果记录不存在，则插入新记录
            new_record = HmTuIndexBasic(
                CODE=row['code'],
                NAME=row['name'],
                fullname=row['fullname'],
                market=row['market'],
                publisher=row['publisher'],
                index_type=row['index_type'],
                category=row['category'],
                base_date=row['base_date'],
                base_point=row['base_point'],
                list_date=row['list_date'],
                weight_rule=row['weight_rule'],
                desc=row['desc'],
                exp_date=row['exp_date']
            )
            global_session.merge(new_record)

    # 提交事务
    try:
        global_session.commit()
    except Exception as e:
        # 处理异常的代码
        log(f"发生了异常：{e}")
        global_session.rollback()


# 更新当前日期是否为交易日
def update_trade_date(now_date=None):
    if now_date is None:
        now_date = DateUtils.date_to_str2(DateUtils.get_current_time())
    data = tushareApi.check_trade_date(now_date=now_date, fields=["cal_date", "is_open"])
    # print(data)
    for index, row in data.iterrows():
        if row["is_open"] == 1:
            record = global_session.query(HmTradeDate).filter_by(DATE=row['cal_date']).first()
            if record:
                # 如果记录存在，则更新对应字段的值
                record.DATE = row['cal_date']
            else:
                new_record = HmTradeDate(
                    DATE=row['cal_date']
                )
                global_session.add(new_record)
                # 提交事务
            try:
                global_session.commit()
            except Exception as e:
                # 处理异常的代码
                log(f"发生了异常：{e}")
                global_session.rollback()


# 个股资金流向
def get_moneyflow(trade_end_date=None):
    ts_code = None
    # ts_code = "000001.SZ"
    if trade_end_date is None:
        trade_end_date = DateUtils.date_to_str2(DateUtils.get_current_time())
        log("默认结束日为:{}".format(trade_end_date))
    count = 0
    wait_count = 0
    max_request = 1  # 每天天最多请求次数
    # 循环打印10天日期列表
    trade_date = DateUtils.str_to_date2(trade_end_date)
    # trade_date = trade_end_date
    while count < max_request:
        result = is_trade_day(trade_date)
        if result is False:
            log("{} 不是交易日".format(trade_date))
            trade_date = DateUtils.str_to_date2(trade_date)
            trade_date -= datetime.timedelta(days=1)
            # trade_date = DateUtils.date_to_str2(trade_date)
            continue

        if wait_count > 9:
            log("************* 开始等待... *************")
            time.sleep(2)
            wait_count = 0
        count += 1
        wait_count += 1
        trade_date = DateUtils.date_to_str2(trade_date)
        # 打印当前日期
        log(trade_date)

        data = tushareApi.get_moneyflow(trade_date=trade_date)
        # 将数据转换为 DataFrame 格式
        df = pd.DataFrame(data)
        if df.empty:
            # 减去一天得到前一天日期
            trade_date = DateUtils.str_to_date2(trade_date)
            trade_date -= datetime.timedelta(days=1)
            continue

        df = df.replace(np.nan, None)
        df = df.rename(columns={'ts_code': 'code'})
        df = df.rename(columns={'trade_date': 'date'})
        log(df.head(1))
        hsgt_list = []
        for index, row in df.iterrows():
            model = HmTuMoneyflow(CODE=row['code'], DATE=row['date'], buy_sm_vol=row['buy_sm_vol'],
                                  buy_sm_amount=Utils.convert_value(row['buy_sm_amount']),
                                  sell_sm_vol=row['sell_sm_vol'],
                                  sell_sm_amount=Utils.convert_value(row['sell_sm_amount']),
                                  buy_md_vol=row['buy_md_vol'],
                                  buy_md_amount=Utils.convert_value(row['buy_md_amount']),
                                  sell_md_vol=row['sell_md_vol'],
                                  sell_md_amount=Utils.convert_value(row['sell_md_amount']),
                                  buy_lg_vol=row['buy_lg_vol'],
                                  buy_lg_amount=Utils.convert_value(row['buy_lg_amount']),
                                  sell_lg_vol=row['sell_lg_vol'],
                                  sell_lg_amount=Utils.convert_value(row['sell_lg_amount']),
                                  buy_elg_vol=row['buy_elg_vol'],
                                  buy_elg_amount=Utils.convert_value(row['buy_elg_amount']),
                                  sell_elg_vol=row['sell_elg_vol'],
                                  sell_elg_amount=Utils.convert_value(row['sell_elg_amount']),
                                  net_mf_vol=row['net_mf_vol'],
                                  net_mf_amount=Utils.convert_value(row['net_mf_amount']))
            hsgt_list.append(model)

        global_session.add_all(hsgt_list)
        try:
            global_session.commit()
        except Exception as e:
            # 处理异常的代码
            log(f"发生了异常：{e}")
            global_session.rollback()
        trade_date = DateUtils.str_to_date2(trade_date)
        trade_date -= datetime.timedelta(days=1)
    # # 查询所有的HmTuTicker对象
    # tickers = session.query(HmTuTicker).all()
    # # 301167
    #
    # # 遍历所有的HmTuTicker对象并打印
    # for ticker in tickers:
    #     # log(f'TS代码: {ticker.code}, 股票名称: {ticker.name}, 所属行业: {ticker.industry}, 上市日期: {ticker.list_date}')
    #     ts_code = ticker.code
    #     # 查询数据
    #     result = session.query(HmTuMoneyflow).filter_by(CODE=ts_code, DATE=).first()
    #     # 判断是否存在
    #     if result:
    #         print('存在')
    #         continue
    #     else:
    #         print('不存在')
    #
    #     time.sleep(0.5)
    #     data = tushareApi.get_moneyflow(ts_code=ts_code)
    #     # 将数据转换为 DataFrame 格式
    #     df = pd.DataFrame(data)
    #     df = df.replace(np.nan, None)
    #     df = df.rename(columns={'ts_code': 'code'})
    #     df = df.rename(columns={'trade_date': 'date'})
    #     log(df.head(1))
    #     hsgt_list = []
    #     for index, row in df.iterrows():
    #         model = HmTuMoneyflow(CODE=row['code'], DATE=row['date'], buy_sm_vol=row['buy_sm_vol'],
    #                               buy_sm_amount=Utils.convert_value(row['buy_sm_amount']),
    #                               sell_sm_vol=row['sell_sm_vol'],
    #                               sell_sm_amount=Utils.convert_value(row['sell_sm_amount']),
    #                               buy_md_vol=row['buy_md_vol'],
    #                               buy_md_amount=Utils.convert_value(row['buy_md_amount']),
    #                               sell_md_vol=row['sell_md_vol'],
    #                               sell_md_amount=Utils.convert_value(row['sell_md_amount']),
    #                               buy_lg_vol=row['buy_lg_vol'],
    #                               buy_lg_amount=Utils.convert_value(row['buy_lg_amount']),
    #                               sell_lg_vol=row['sell_lg_vol'],
    #                               sell_lg_amount=Utils.convert_value(row['sell_lg_amount']),
    #                               buy_elg_vol=row['buy_elg_vol'],
    #                               buy_elg_amount=Utils.convert_value(row['buy_elg_amount']),
    #                               sell_elg_vol=row['sell_elg_vol'],
    #                               sell_elg_amount=Utils.convert_value(row['sell_elg_amount']),
    #                               net_mf_vol=row['net_mf_vol'],
    #                               net_mf_amount=Utils.convert_value(row['net_mf_amount']))
    #         hsgt_list.append(model)
    #
    #     session.add_all(hsgt_list)
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         # 处理异常的代码
    #         # log(f"发生了异常：{e}")
    #         continue

    return


def get_margin_detail(start_trade_date=None, end_trade_date=None):
    log("***************** 融资融券交易明细入库a ***************")
    # mult_session = Session()
    if start_trade_date is None:
        start_trade_date = DateUtils.date_to_str2(DateUtils.get_current_time())
    if end_trade_date is None:
        end_trade_date = DateUtils.date_to_str2(DateUtils.get_current_time())

    log("start_trade_date = {}, end_trade_date = {}".format(start_trade_date, end_trade_date))
    trade_date = end_trade_date
    while start_trade_date <= end_trade_date:
        log("************ {} ************".format(trade_date))
        result = is_trade_day(trade_date)
        if result is False:
            trade_date = DateUtils.get_back_day_str(trade_date)
            end_trade_date = trade_date
            continue

        result = global_session.query(HmTuMarginDetail).filter_by(DATE=trade_date).first()
        # 判断是否存在
        if result:
            log('{} 数据已存在存在'.format(trade_date))
            break

        data = tushareApi.get_margin_detail(trade_date=trade_date)
        # 将数据转换为 DataFrame 格式
        df = pd.DataFrame(data)
        if df.empty:
            log('融资融券交易明细 {}: 数据为空'.format(trade_date))
            trade_date = DateUtils.get_back_day_str(trade_date)
            end_trade_date = trade_date
            continue
        df = df.replace(np.nan, None)
        df = df.rename(columns={'ts_code': 'code'})
        df = df.rename(columns={'trade_date': 'date'})
        print(df.head(1))
        hsgt_list = []
        for index, row in df.iterrows():
            model = HmTuMarginDetail(CODE=row['code'], DATE=row['date'], NAME=row['name'],
                                     rzye=row['rzye'], rqye=row['rqye'], rzmre=row['rzmre'],
                                     rqyl=row['rqyl'], rzche=row['rzche'], rqchl=row['rqchl'],
                                     rqmcl=row['rqmcl'], rzrqye=row['rzrqye'], )
            hsgt_list.append(model)

        global_session.add_all(hsgt_list)
        try:
            global_session.commit()
        except Exception as e:
            # 处理异常的代码
            log(f"发生了异常：{e}")
            global_session.rollback()

        trade_date = DateUtils.get_back_day_str(trade_date)
        end_trade_date = trade_date

    global_session.close()
    log("***************** 融资融券交易明细入库 完成 ***************")


# 沪深股票 - 特色数据 -  股票技术面因子
def get_stock_stk_factor(code=None, trade_date=None, start_date=None, end_date=None):
    ts_code = None
    ts_code = "000001.SZ"
    # 获取 沪深港通资金流向
    if end_date is None:
        end_date = DateUtils.date_to_str2(DateUtils.get_current_time())
        log("默认结束日为:{}".format(end_date))
    count = 0
    wait_count = 0
    max_request = 100  # 明天最多请求次数
    # 循环打印10天日期列表
    # trade_date = DateUtils.str_to_date2(end_date)
    trade_date = end_date
    while count < max_request:
        result = is_trade_day(trade_date)
        if result is False:
            log("{} 不是交易日".format(trade_date))
            trade_date = DateUtils.get_back_day_str(trade_date)
            continue

        if wait_count > 9:
            log("************* 开始等待... *************")
            time.sleep(2)
            wait_count = 0
        wait_count += 1
        trade_date = DateUtils.date_to_str2(trade_date)
        # 打印当前日期
        # log(trade_date)

        data = tushareApi.get_stk_factor(ts_code=code, trade_date=trade_date)
        # 将数据转换为 DataFrame 格式
        df = pd.DataFrame(data)
        if df.empty:
            # 减去一天得到前一天日期
            trade_date = DateUtils.get_back_day_str(trade_date)
            continue
        df = df.replace(np.nan, None)
        df = df.rename(columns={'ts_code': 'code'})
        df = df.rename(columns={'trade_date': 'date'})
        df = df.rename(columns={'macd_dif': 'dif'})
        df = df.rename(columns={'macd_dea': 'dea'})
        print(df.head(5))
        log("数据长度为:{}".format(len(df)))
        for index, row in df.iterrows():
            indicator = HmIndicatorDay(CODE=row['code'], DATE=row['date'], DIF=row['dif'],
                                       DEA=row['dea'], MACD=row['macd'],
                                       KDJ_K=row['kdj_k'], KDJ_D=row['kdj_d'], KDJ_J=row['kdj_j'], RSI_6=row['rsi_6'],
                                       RSI_12=row['rsi_12'],
                                       RSI_24=row['rsi_24'], BOLL_UPPER=row['boll_upper'], BOLL_MID=row['boll_mid'],
                                       BOLL_LOWER=row['boll_lower'],
                                       CCI=row['cci'])
            try:
                # 查询数据库中是否已存在该条数据
                existing_indicator = global_session.query(HmIndicatorDay).filter_by(CODE=indicator.CODE,
                                                                                    DATE=indicator.DATE).one()
                # 如果已存在，则更新数据
                existing_indicator.DIF = row['dif']
                existing_indicator.DEA = row['dea']
                existing_indicator.MACD = row['macd']
                existing_indicator.KDJ_K = row['kdj_k']
                existing_indicator.KDJ_D = row['kdj_d']
                existing_indicator.KDJ_J = row['kdj_j']
                existing_indicator.RSI_6 = row['rsi_6']
                existing_indicator.RSI_12 = row['rsi_12']
                existing_indicator.RSI_24 = row['rsi_24']
                existing_indicator.BOLL_UPPER = row['boll_upper']
                existing_indicator.BOLL_MID = row['boll_mid']
                existing_indicator.BOLL_LOWER = row['boll_lower']
                existing_indicator.CCI = row['cci']
                global_session.merge(existing_indicator)
                global_session.commit()
                log('{} {} 数据已更新'.format(indicator.CODE, indicator.DATE))
            except Exception as e:
                # 如果不存在，则插入数据
                global_session.add(indicator)
                global_session.commit()
                log('{} {} 数据已插入'.format(indicator.CODE, DateUtils.date_to_str2(indicator.DATE)))

        # 减去一天得到前一天日期
        # trade_date = DateUtils.get_back_day_str(trade_date)
        trade_date = DateUtils.get_back_day_str(trade_date)
        count += 1
        log("等待6s ...")
        time.sleep(1)

    return


# 您每分钟最多访问该接口300次
def get_all_index_daily(trade_date=None, start_date=None, end_date=None):
    # 查询所有的HmTuTicker对象
    indexBasics = global_session.query(HmTuIndexBasic).all()
    # 301167

    # 遍历所有
    for indexBasic in indexBasics:
        # log(f'TS代码: {ticker.code}, 股票名称: {ticker.name}, 所属行业: {ticker.industry}, 上市日期: {ticker.list_date}')
        ts_code = indexBasic.CODE
        log("index code = {}".format(ts_code))

        data = tushareApi.get_index_daily(ts_code=ts_code, trade_date=trade_date, start_date=start_date,
                                          end_date=end_date)

        # 将数据转换为 DataFrame 格式
        df = pd.DataFrame(data)
        # log("{} 数据长度为:{}".format(ts_code, len(df)))
        if df.empty:
            # log('{}: 为空'.format(ts_code))
            time.sleep(0.22)
            continue
        df = df.replace(np.nan, None)
        df = df.rename(columns={'ts_code': 'code'})
        df = df.rename(columns={'trade_date': 'date'})
        print(df.head(3))
        index_daily = []
        for index, row in df.iterrows():
            model = HmTuIndexDaily(CODE=row['code'], DATE=row['date'], close=row['close'],
                                   open=row['open'], high=row['high'], low=row['low'], pre_close=row['pre_close'],
                                   change=row['change'], pct_chg=row['pct_chg'], vol=row['vol'],
                                   amount=Utils.convert_value(row['amount'], 1000))
            index_daily.append(model)

        global_session.add_all(index_daily)
        try:
            global_session.commit()
        except Exception as e:
            # 处理异常的代码
            log(f"发生了异常：{e}")
            global_session.rollback()
            # continue
        time.sleep(0.22)


@calculate_time
def main():
    # 特殊股票：兴华股份
    # log("***************** 1: 更新股票基本信息 ***************")
    # update_tu_ticker()
    # log("***************** 1: 更新股票基本信息 完成 ***************")
    #
    # log("***************** 2: 更新指数基本信息 入库 ***************")
    # update_index_basic()
    # log("***************** 2: 更新指数基本入库 完成 ***************")
    #
    # log("***************** 3: 检测交易日 ***************")
    # update_trade_date()
    # log("***************** 3: 检测交易日 完成 ***************")
    #
    # log("***************** 4: 日线行情 ***************")
    # # start_date = '20230412'
    # # end_date = '20230412'
    # # get_stock_daily(start_date=start_date, end_date=end_date)
    # # 默认更新当天的
    # get_stock_daily_with_trade()
    # log("***************** 4: 日线行情入库完成 ***************")

    # log("***************** 5: 指数日线行情入库 ***************")
    # start_date = "20230413"
    # # start_date = None
    # end_date = "20230413"
    # # end_date = None
    # get_all_index_daily(start_date=start_date, end_date=end_date)
    # log("***************** 5: 指数日线行情入库完成 ***************")

    # log("***************** 6: 个股资金流向入库 ***************")
    # # trade_end_date = "20230409"
    # trade_end_date = None
    # get_moneyflow(trade_end_date)
    # log("***************** 6: 个股资金流向完成 ***************")
    #
    # log("***************** 股票技术因子（量化因子）入库 ***************")
    # start_date = "20230412"
    # start_date = None
    # end_date = "20220511"
    # # end_date = None
    # code = None
    # get_stock_stk_factor(code=code, start_date=start_date, end_date=end_date)
    # log("***************** 股票技术因子（量化因子）入库完成 ***************")

    log("***************** 沪深港通资金流向 ***************")
    start_trade_date = "20230414"
    end_trade_date = "20230414"
    get_hsgt_money_flow(start_trade_date, end_trade_date)
    log("***************** 沪深港通资金流向入库完成 ***************")

    # log("***************** 融资融券交易明细入库 ***************")
    # start_trade_date = "20230414"
    # end_trade_date = "20230414"
    # get_margin_detail(start_trade_date, end_trade_date)
    # log("***************** 融资融券交易明细完成 ***************")

    pass


if __name__ == '__main__':
    tushareApi = TushareAPI()
    # engine = init_db_dev()
    engine = init_db_pre()
    global_session = sessionmaker(bind=engine)()

    main()
    # 关闭会话
    global_session.close()
