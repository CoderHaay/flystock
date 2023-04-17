# -*- coding: utf-8 -*-
# @Time : 2023/4/6 14:32
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : HmTuIndexBasic.py
# @Project : 东方财富OCR


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

from Model.BaseModel import BaseModel

Base = declarative_base()


class HmTuIndexBasic(BaseModel):
    __tablename__ = 'hm_tu_index_basic'

    CODE = Column(String(255), comment='TS代码')
    NAME = Column(String(255), comment='简称')
    FULLNAME = Column(String(255), comment='指数全称')
    MARKET = Column(String(255), comment='市场')
    PUBLISHER = Column(String(255), comment='发布方')
    INDEX_TYPE = Column(String(255), comment='指数风格')
    CATEGORY = Column(String(255), comment='指数类别')
    BASE_DATE = Column(String(255), comment='基期')
    BASE_POINT = Column(Float, comment='基点')
    LIST_DATE = Column(String(255), comment='发布日期')
    WEIGHT_RULE = Column(String(255), comment='加权方式')
    DESC = Column(String(255), comment='描述')
    EXP_DATE = Column(String(255), comment='终止日期')
    UPDATE_TIME = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')
