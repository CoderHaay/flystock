# -*- coding: utf-8 -*-
# @Time : 2023/3/31 15:52
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuQuotationDay.py
# @Project : 东方财富OCR

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

from Model.BaseModel import BaseModel


class HmTuQuotationDay(BaseModel):
    __tablename__ = 'hm_tu_quotation_day'

    CODE = Column(String(11), nullable=True, comment='股票代码')
    DATE = Column(String(255), nullable=True, comment='交易日期')
    OPEN = Column(Float, nullable=True, comment='开盘价')
    HIGH = Column(Float, nullable=True, comment='最高价')
    LOW = Column(Float, nullable=True, comment='最低价')
    CLOSE = Column(Float, nullable=True, comment='收盘价')
    PRE_CLOSE = Column(Float, nullable=True, comment='昨收价')
    CHANGE = Column(Float, nullable=True, comment='涨跌额')
    PCT_CHG = Column(Float, nullable=True, comment='涨跌幅')
    VOL = Column(Float, nullable=True, comment='成交量')
    AMOUNT = Column(Float, nullable=True, comment='成交额')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')
