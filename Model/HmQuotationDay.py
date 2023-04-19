# -*- coding: utf-8 -*-
# @Time : 2023/4/17 15:58
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmQuotationDay.py
# @Project : flystock

from sqlalchemy import Column, Date, DateTime, DECIMAL, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel


class HmQuotationDay(BaseModel):
    __tablename__ = 'hm_quotation_day'

    CODE = Column(String(20), nullable=False, comment='证券代码')
    NAME = Column(String(155), comment='名称')
    DATE = Column(Date, nullable=False, comment='交易日期')
    OPEN = Column(DECIMAL(6, 2), comment='开盘价')
    CLOSE = Column(DECIMAL(6, 2), comment='收盘价')
    HIGH = Column(DECIMAL(6, 2), comment='最高价')
    LOW = Column(DECIMAL(6, 2), comment='最低价')
    PRECLOSE = Column(DECIMAL(6, 2), comment='前收盘价')
    AVERAGE = Column(DECIMAL(6, 2), comment='均价')
    CHANGE = Column(DECIMAL(6, 2), comment='涨跌')
    PCTCHANGE = Column(DECIMAL(6, 2), comment='涨跌幅')
    VOLUME = Column(Integer, comment='成交量')
    HIGHLIMIT = Column(String(10), comment='是否涨停')
    AMOUNT = Column(DECIMAL(14, 2), comment='成交金额')
    TURN = Column(DECIMAL(11, 2), comment='换手率')
    LOWLIMIT = Column(String(10), comment='是否跌停')
    AMPLITUDE = Column(DECIMAL(6, 2), comment='振幅')
    TNUM = Column(Integer, comment='成交笔数')
    PE = Column(DECIMAL(14, 2), comment='市盈率(PE)')
    MV = Column(DECIMAL(16, 2), comment='总市值')
    FREEFLOATMV = Column(DECIMAL(16, 2), comment='自由流通市值')
    TRADESTATUS = Column(String(10), comment='交易状态')
    TAFACTOR = Column(DECIMAL(18, 15), comment='复权因子(后)')
    FRONTTAFACTOR = Column(DECIMAL(18, 15), comment='前复权因子（定点复权）')
    ISSTSTOCK = Column(String(10), comment='是否为ST股票')
    ISXSTSTOCK = Column(String(10), comment='是否为*ST股票')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', comment='更新时间')