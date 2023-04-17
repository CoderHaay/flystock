# -*- coding: utf-8 -*-
# @Time : 2023/4/6 16:02
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuMoneyflow.py
# @Project : 东方财富OCR

from sqlalchemy import Column, Integer, String, Date, Float, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base

from Model.BaseModel import BaseModel

Base = declarative_base()


class HmTuMoneyflow(BaseModel):
    __tablename__ = 'hm_tu_moneyflow'

    CODE = Column(String(10), nullable=False, comment='TS代码')
    # date = Column(Date, nullable=False, comment='交易日期')
    DATE = Column(String(255), nullable=True, comment='交易日期')
    BUY_SM_VOL = Column(Integer, comment='小单买入量（手）')
    BUY_SM_AMOUNT = Column(Float, comment='小单买入金额（元）')
    SELL_SM_VOL = Column(Integer, comment='小单卖出量（手）')
    SELL_SM_AMOUNT = Column(Float, comment='小单卖出金额（元）')
    BUY_MD_VOL = Column(Integer, comment='中单买入量（手）')
    BUY_MD_AMOUNT = Column(Float, comment='中单买入金额（元）')
    SELL_MD_VOL = Column(Integer, comment='中单卖出量（手）')
    SELL_MD_AMOUNT = Column(Float, comment='中单卖出金额（元）')
    BUY_LG_VOL = Column(Integer, comment='大单买入量（手）')
    BUY_LG_AMOUNT = Column(Float, comment='大单买入金额（元）')
    SELL_LG_VOL = Column(Integer, comment='大单卖出量（手）')
    SELL_LG_AMOUNT = Column(Float, comment='大单卖出金额（元）')
    BUY_ELG_VOL = Column(Integer, comment='特大单买入量（手）')
    BUY_ELG_AMOUNT = Column(Float, comment='特大单买入金额（元）')
    SELL_ELG_VOL = Column(Integer, comment='特大单卖出量（手）')
    SELL_ELG_AMOUNT = Column(Float, comment='特大单卖出金额（元）')
    NET_MF_VOL = Column(Integer, comment='净流入量（手）')
    NET_MF_AMOUNT = Column(Float, comment='净流入额（元）')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')

    __table_args__ = (
        UniqueConstraint('CODE', 'DATE', name='唯一'),
        {'comment': '股票资金流向数据'}
    )
