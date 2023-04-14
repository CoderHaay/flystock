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
    symbol = Column(Text)
    NAME = Column(Text)
    area = Column(Text)
    industry = Column(Text)
    fullname = Column(Text)
    enname = Column(Text)
    cnspell = Column(Text)
    market = Column(Text)
    exchange = Column(Text)
    curr_type = Column(Text)
    list_status = Column(Text)
    list_date = Column(Text)
    delist_date = Column(Text)
    is_hs = Column(Text)
    update_time = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
