# -*- coding: utf-8 -*-
# @Time : 2023/3/24 14:55
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : update_data.py
# @Project : 东方财富OCR
from Database import Database
import json

from Tools import Tools


def main():
    with open('config.json', encoding='utf-8') as f:
        # 读取文件
        result = json.load(f)

    # print(result)
    host = result["host"]
    user = result["user"]
    password = result["password"]
    db_name = result["db_name"]

    db = Database(host=host, user=user, db_password=password, db_name=db_name)

    now_date = Tools.get_current_date()
    # file_path = result["capital_day"]  ## 文件
    # info_data = db.load_excel(file_path, 2)
    # db.many_insert_capital_day(info_data)

    zgyy_column = 4
    file_path = result["ZGYY1m80"]  ## 文件
    info_data, date = Tools.load_excel(file_path, zgyy_column)

    folder_path = Tools.create_folder()
    Tools.copy_file(file_path, folder_path)
