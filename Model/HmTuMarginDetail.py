# -*- coding: utf-8 -*-
# @Time : 2023/4/6 18:44
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuMarginDetail.py
# @Project : 东方财富OCR

from sqlalchemy import Column, String, Float, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel

Base = declarative_base()


class HmTuMarginDetail(BaseModel):
    __tablename__ = 'hm_tu_margin_detail'
    DATE = Column(String(255), comment='交易日期')
    CODE = Column(String(255), comment='TS股票代码')
    NAME = Column(String(255), comment='股票名称')
    RZYE = Column(Float, comment='融资余额(元)')
    RQYE = Column(Float, comment='融券余额(元)')
    RZMRE = Column(Float, comment='融资买入额(元)')
    RQYL = Column(Float, comment='融券余量（手）')
    RZCHE = Column(Float, comment='融资偿还额(元)')
    RQCHL = Column(Float, comment='融券偿还量(手)')
    RQMCL = Column(Float, comment='融券卖出量(股,份,手)')
    RZRQYE = Column(Float, comment='融资融券余额(元)')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')
