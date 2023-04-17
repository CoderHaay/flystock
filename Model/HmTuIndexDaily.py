# -*- coding: utf-8 -*-
# @Time : 2023/4/11 11:30
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuIndexDaily.py
# @Project : 东方财富OCR
from sqlalchemy import create_engine, Column, String, Float, DateTime
from Model.BaseModel import BaseModel


# 创建HmTuIndexDaily模型
class HmTuIndexDaily(BaseModel):
    __tablename__ = 'hm_tu_index_daily'

    CODE = Column(String(10), comment='TS指数代码')
    DATE = Column(String(10), comment='交易日')
    CLOSE = Column(Float, comment='收盘点位')
    OPEN = Column(Float, comment='开盘点位')
    HIGH = Column(Float, comment='最高点位')
    LOW = Column(Float, comment='最低点位')
    PRE_CLOSE = Column(Float, comment='昨日收盘点')
    CHANGE = Column(Float, comment='涨跌点')
    PCT_CHG = Column(Float, comment='涨跌幅（%）')
    VOL = Column(Float, comment='成交量（手）')
    AMOUNT = Column(Float, comment='成交额（千元）')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')
