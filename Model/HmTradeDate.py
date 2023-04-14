# -*- coding: utf-8 -*-
# @Time : 2023/4/10 16:00
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTradeDate.py
# @Project : 东方财富OCR

from sqlalchemy import create_engine, Column, Integer, Date, String
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel


# 定义hm_trade_date表的ORM映射类
class HmTradeDate(BaseModel):
    __tablename__ = 'hm_trade_date'
    # date = Column(Date, unique=True, nullable=False)
    DATE = Column(String(255), comment='交易日期')
    # is_open = Column(String(2), comment='是否交易 0休市 1交易')
