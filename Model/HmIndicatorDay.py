# -*- coding: utf-8 -*-
# @Time : 2023/4/4 18:07
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmIndicatorDay.py
# @Project : 东方财富OCR

from sqlalchemy import Column, Integer, String, Date, Numeric, Float, DateTime, UniqueConstraint, Index
from Model.BaseModel import BaseModel


class HmIndicatorDay(BaseModel):
    __tablename__ = 'hm_indicator_day'

    CODE = Column(String(20), nullable=False, comment='股票代码')
    NAME = Column(String(155), comment='名称')
    # DATE = Column(Date, nullable=False, comment='日期')
    DATE = Column(String(255), comment='交易日期')
    DDX = Column(Numeric(11, 2), comment='ddx')
    DDY = Column(Numeric(11, 3), comment='ddy')
    DDZ = Column(Numeric(11, 3), comment='ddz')
    DIF = Column(Numeric(11, 3), comment='macd_dif')
    DEA = Column(Numeric(11, 3), comment='macd_dea')
    MACD = Column(Numeric(11, 3), comment='macd')
    DKX = Column(Numeric(11, 3), comment='dkx')
    MADKX = Column(Numeric(11, 3), comment='madkx')
    KDJ_K = Column(Float, comment='KDJ_K')
    KDJ_D = Column(Float, comment='kdj_d')
    KDJ_J = Column(Float, comment='kdj_j')
    RSI_6 = Column(Float, comment='rsi_6')
    RSI_12 = Column(Float, comment='rsi_12')
    RSI_24 = Column(Float, comment='rsi_24')
    BOLL_UPPER = Column(Float, comment='BOLL_UPPER')
    BOLL_MID = Column(Float, comment='BOLL_MID')
    BOLL_LOWER = Column(Float, comment='BOLL_LOWER')
    CCI = Column(Float, comment='CCI')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')

    __table_args__ = (
        UniqueConstraint('CODE', 'DATE', name='唯一'),
        Index('CODE', 'NAME')
    )
