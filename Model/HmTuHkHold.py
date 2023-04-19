# -*- coding: utf-8 -*-
# @Time : 2023/4/18 17:29
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuHkHold.py
# @Project : flystock


from sqlalchemy import Column, Integer, String, Date, Float, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel


class HmTuHkHold(BaseModel):
    __tablename__ = 'hm_tu_hk_hold'

    CODE = Column(String(10), nullable=False, comment='股票代码')
    DATE = Column(Date, comment='交易日期')
    NAME = Column(String(50), comment='股票名称')
    VOL = Column(Integer, comment='持股数量(股)')
    RATIO = Column(Float, comment='持股占比（%），占已发行股份百分比')
    EXCHANGE = Column(String(10), comment='类型：SH沪股通SZ深股通HK港股通')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')

    __table_args__ = (UniqueConstraint('CODE', 'DATE', name='唯一'),)

    def __repr__(self):
        return f"<HmTuHkHold(CODE='{self.CODE}', DATE='{self.DATE}', NAME='{self.NAME}')>"
