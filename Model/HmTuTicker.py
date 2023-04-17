# -*- coding: utf-8 -*-
# @Time : 2023/3/31 14:56
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuTicker.py
# @Project : 东方财富OCR
from sqlalchemy import create_engine, Column, Integer, DateTime, Text, text

from Model.BaseModel import BaseModel


class HmTuTicker(BaseModel):
    __tablename__ = 'hm_tu_ticker'

    CODE = Column(Text)
    SYMBOL = Column(Text)
    NAME = Column(Text)
    AREA = Column(Text)
    INDUSTRY = Column(Text)
    FULLNAME = Column(Text)
    ENNAME = Column(Text)
    CNSPELL = Column(Text)
    MARKET = Column(Text)
    EXCHANGE = Column(Text)
    CURR_TYPE = Column(Text)
    LIST_STATUS = Column(Text)
    LIST_DATE = Column(Text)
    DELIST_DATE = Column(Text)
    IS_HS = Column(Text)
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')

