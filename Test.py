import datetime

from Model.BaseModel import Base, User
from Model.HmIndicatorDay import HmIndicatorDay
from Model.HmTuIndexBasic import HmTuIndexBasic
from Model.HmTuMarginDetail import HmTuMarginDetail
from Model.HmTuQuotationDay import HmTuQuotationDay
from Model.HmTuMoneyflowHsgt import HmTuMoneyflowHsgt
from Model.HmTuTicker import HmTuTicker
from utils.DateUtils import DateUtils
from utils.TushareApi import TushareAPI
from Database import Database
import json
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import numpy as np

from utils.Utils import log


def init_db():
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
    engine = create_engine('mysql+pymysql://{}:{}@{}:3306/{}'.format(user, password, host, db_name), echo=False,
                           pool_size=8, pool_recycle=3600)

    return engine


def query_null_data():
    # 查询空值数据
    results = session.query(HmIndicatorDay).filter(
        HmIndicatorDay.DDX.is_(None) | HmIndicatorDay.DDY.is_(None) | HmIndicatorDay.DDZ.is_(None)).all()

    # 打印结果
    for result in results:
        print(result.id, result.CODE, result.NAME, result.DATE, result.DDX, result.DDY, result.DDZ)


# start_date 为最新交易日，然后往前开始
def get_trade_date(start_date, end_date):
    """打印从当前日期开始到指定日期结束的每一天"""
    # end_date = datetime.datetime.strptime(str(end_date), '%Y%m%d').date()
    today = start_date
    delta = today - end_date
    for i in range(delta.days + 1):
        current_date = today - datetime.timedelta(days=i)
        print(current_date.strftime("%Y-%m-%d"))
        return current_date
    return None


def get_hsgt_money_flow(start_date, end_date):
    # 获取 沪深港通资金流向
    if start_date is None:
        start_date = DateUtils.get_current_date()
    else:
        start_date = DateUtils.str_to_date2(start_date)
    # log(start_date)
    end_date = DateUtils.str_to_date2(end_date)
    delta = start_date - end_date
    for i in range(delta.days + 1):
        current_date = start_date - datetime.timedelta(days=i)
        log(current_date.strftime("%Y-%m-%d"))







    # count = 0
    # while start_date <= end_date:
    #     log("************ {} ************".format(start_date))
    #     trade_date = start_date
    #     count += 1
    #     if count > 295:
    #         log("************* 开始等待... *************")
    #         time.sleep(61)
    #         count = 0
    #
    #     data = tushareApi.get_moneyflow_hsgt(trade_date, start_date, end_date)
    #     # 将数据转换为 DataFrame 格式
    #     df = pd.DataFrame(data)
    #     if df.empty:
    #         start_date = (datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=1)).strftime(
    #             '%Y%m%d')
    #         continue
    #     df = df.rename(columns={'trade_date': 'date'})
    #     print(df.head(1))
    #     hsgt_list = []
    #     for index, row in df.iterrows():
    #         model = HmTuMoneyflowHsgt(date=row['date'],
    #                                   ggt_ss=Utils.convert_value(row['ggt_ss'], 1000000),
    #                                   ggt_sz=Utils.convert_value(row['ggt_sz'], 1000000),
    #                                   hgt=Utils.convert_value(row['hgt'], 1000000),
    #                                   sgt=Utils.convert_value(row['sgt'], 1000000),
    #                                   north_money=Utils.convert_value(row['north_money'], 1000000),
    #                                   south_money=Utils.convert_value(row['south_money'], 1000000))
    #         hsgt_list.append(model)
    #
    #     session.add_all(hsgt_list)
    #     try:
    #         session.commit()
    #     except Exception as e:
    #         # 处理异常的代码
    #         log(f"发生了异常：{e}")
    #
    #     start_date = (datetime.datetime.strptime(start_date, '%Y%m%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')

tushareApi = TushareAPI()
engine = init_db()
session = sessionmaker(bind=engine)()

get_hsgt_money_flow("20230410", "20230401")



