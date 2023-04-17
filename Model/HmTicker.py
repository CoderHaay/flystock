# -*- coding: utf-8 -*-
# @Time : 2023/4/14 16:56
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTicker.py
# @Project : flystock

from sqlalchemy import Column, Integer, String, BigInteger, Date, DateTime, DECIMAL, text
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel


class HmTicker(BaseModel):
    __tablename__ = 'hm_ticker'

    id = Column(Integer, primary_key=True, autoincrement=True)
    CODE = Column(String(100), nullable=False, comment='股票代码')
    NAME = Column(String(100), comment='股票简称')
    EMCODE = Column(String(100), comment='东财代码')
    MARKET = Column(String(100), nullable=False, server_default=text("'001004'"))
    PROVINCE = Column(String(100), comment='省份')
    CITY = Column(String(100), comment='城市')
    TOTALSHARE = Column(BigInteger, comment='总股本')
    LIQASHARE = Column(BigInteger, comment='流通A股')
    LIQSHARE = Column(BigInteger, comment='流通股本')
    FREELIQSHARE = Column(BigInteger, comment='自由流通股本')
    CLOSE = Column(DECIMAL(6, 2), comment='收盘价')
    MV = Column(DECIMAL(16, 2), comment='总市值')
    FREEFLOATMV = Column(DECIMAL(16, 2), comment='自由流通市值')
    PE = Column(DECIMAL(6, 2), comment='市盈率(PE)')
    LIST_STATUS = Column(String(1, 'utf8mb4'), comment='上市状态 L上市 D退市 P暂停上市')
    LAST = Column(Date, comment='最后交易日')
    RZRQ = Column(Integer, comment='融资融券')
    ST = Column(Integer, comment='ST')
    XST = Column(Integer, comment='*ST')
    GT = Column(Integer, comment='沪深港通')
    UPDATE_TIME = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False, comment='更新时间')