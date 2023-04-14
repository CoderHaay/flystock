# -*- coding: utf-8 -*-
# @Time : 2023/3/31 11:20
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : Model.py
# @Project : 东方财富OCR

import enum
from typing import Any
from sqlalchemy import Column, String, Integer, SMALLINT, FLOAT, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp, current_time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(BaseModel):
    __tablename__ = 'hm_test_user'

    mobile = Column(String(11))
    nickname = Column(String(50))
    status = Column(SMALLINT, default=1)
    appid = Column(String(50), nullable=True)
    created_time = Column(DateTime, default=datetime.now)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 设置默认值为当前时间，并且在更新时自动更新时间

    def __init__(self, nickname, mobile, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.nickname = nickname
        self.mobile = mobile

# Base.metadata.create_all()  # 将模型映射到数据库中
