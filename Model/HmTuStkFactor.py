# -*- coding: utf-8 -*-
# @Time : 2023/4/7 16:36
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuStkFactor.py
# @Project : 东方财富OCR

from sqlalchemy import Column, Float, Integer, String, Date, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel

Base = declarative_base()


class HmTuStkFactor(BaseModel):
    __tablename__ = 'hm_tu_stk_factor'

    CODE = Column(String(10), nullable=False, comment='股票代码')
    DATE = Column(String(255), comment='交易日期')
    dif = Column(Float(10, 4), nullable=False, comment='MACD_DIF')
    dea = Column(Float(10, 4), nullable=False, comment='MACD_DEA')
    macd = Column(Float(10, 4), nullable=False, comment='MACD')
    kdj_k = Column(Float(10, 4), nullable=False, comment='KDJ_K')
    kdj_d = Column(Float(10, 4), nullable=False, comment='KDJ_D')
    kdj_j = Column(Float(10, 4), nullable=False, comment='KDJ_J')
    rsi_6 = Column(Float(10, 4), nullable=False, comment='RSI_6')
    rsi_12 = Column(Float(10, 4), nullable=False, comment='RSI_12')
    rsi_24 = Column(Float(10, 4), nullable=False, comment='RSI_24')
    boll_upper = Column(Float(10, 4), nullable=False, comment='BOLL_UPPER')
    boll_mid = Column(Float(10, 4), nullable=False, comment='BOLL_MID')
    boll_lower = Column(Float(10, 4), nullable=False, comment='BOLL_LOWER')
    cci = Column(Float(10, 4), nullable=False, comment='CCI')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')
