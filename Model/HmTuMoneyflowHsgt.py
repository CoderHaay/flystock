# -*- coding: utf-8 -*-
# @Time : 2023/4/4 15:51
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : TuMoneyflowHsgt.py
# @Project : 东方财富OCR

from sqlalchemy import Column, Integer, Date, Numeric, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel


class HmTuMoneyflowHsgt(BaseModel):
    __tablename__ = 'hm_tu_moneyflow_hsgt'

    # date = Column(Date, comment='交易日期')
    DATE = Column(String(255), comment='交易日期')
    ggt_ss = Column(Numeric(16, 2), comment='港股通（上海）')
    ggt_sz = Column(Numeric(16, 2), comment='港股通（深圳）')
    hgt = Column(Numeric(16, 2), comment='沪股通(元) 原值为百万，转换为元')
    sgt = Column(Numeric(16, 2), comment='深股通(元) 原值为百万，转换为元')
    north_money = Column(Numeric(16, 2), comment='北向资金(元) 原值为百万，转换为元')
    south_money = Column(Numeric(16, 2), comment='南向资金(元) 原值为百万，转换为元')
    update_time = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')
