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
    fullname = Column(String(255), comment='指数全称')
    market = Column(String(255), comment='市场')
    publisher = Column(String(255), comment='发布方')
    index_type = Column(String(255), comment='指数风格')
    category = Column(String(255), comment='指数类别')
    base_date = Column(String(255), comment='基期')
    base_point = Column(Float, comment='基点')
    list_date = Column(String(255), comment='发布日期')
    weight_rule = Column(String(255), comment='加权方式')
    desc = Column(String(255), comment='描述')
    exp_date = Column(String(255), comment='终止日期')
    update_time = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                         comment='更新时间')
