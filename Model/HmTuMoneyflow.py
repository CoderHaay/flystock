# -*- coding: utf-8 -*-
# @Time : 2023/4/6 16:02
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuMoneyflow.py
# @Project : 东方财富OCR

from sqlalchemy import Column, Integer, String, Date, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel

Base = declarative_base()


class HmTuMoneyflow(BaseModel):
    __tablename__ = 'hm_tu_moneyflow'

    CODE = Column(String(10), nullable=False, comment='TS代码')
    # date = Column(Date, nullable=False, comment='交易日期')
    DATE = Column(String(255), nullable=True, comment='交易日期')
    buy_sm_vol = Column(Integer, comment='小单买入量（手）')
    buy_sm_amount = Column(Float, comment='小单买入金额（元）')
    sell_sm_vol = Column(Integer, comment='小单卖出量（手）')
    sell_sm_amount = Column(Float, comment='小单卖出金额（元）')
    buy_md_vol = Column(Integer, comment='中单买入量（手）')
    buy_md_amount = Column(Float, comment='中单买入金额（元）')
    sell_md_vol = Column(Integer, comment='中单卖出量（手）')
    sell_md_amount = Column(Float, comment='中单卖出金额（元）')
    buy_lg_vol = Column(Integer, comment='大单买入量（手）')
    buy_lg_amount = Column(Float, comment='大单买入金额（元）')
    sell_lg_vol = Column(Integer, comment='大单卖出量（手）')
    sell_lg_amount = Column(Float, comment='大单卖出金额（元）')
    buy_elg_vol = Column(Integer, comment='特大单买入量（手）')
    buy_elg_amount = Column(Float, comment='特大单买入金额（元）')
    sell_elg_vol = Column(Integer, comment='特大单卖出量（手）')
    sell_elg_amount = Column(Float, comment='特大单卖出金额（元）')
    net_mf_vol = Column(Integer, comment='净流入量（手）')
    net_mf_amount = Column(Float, comment='净流入额（元）')

    __table_args__ = (
        UniqueConstraint('CODE', 'DATE', name='唯一'),
        {'comment': '股票资金流向数据'}
    )
