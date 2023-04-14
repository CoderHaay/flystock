# -*- coding: utf-8 -*-
# @Time : 2023/2/15 16:47
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : import_data.py
# @Project : 东方财富OCR

from Database import Database
import json
import time
import os
from Tools import Tools


# "host": "59.110.162.95",
# "user": "flystock",
# "password": "JyHCwfXKpY0e5RZq",
# "db_name": "flystock"

# 定义一个装饰器，用于计算函数执行的时间
def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} 运行耗时: {end_time - start_time:.4f} seconds to execute.")
        return result

    return wrapper


@calculate_time
def main():
    with open('config.json', encoding='utf-8') as f:
        # 读取文件
        result = json.load(f)

    # print(result)
    host = result["host"]
    user = result["user"]
    password = result["password"]
    db_name = result["db_name"]

    now_date = Tools.get_current_date()

    db = Database(host=host, user=user, db_password=password, db_name=db_name)
    # db.connect_check()

    # 定义文件夹路径
    folder_path = result["folder_path"]
    file_names = ["ZGYY1m80.xlsx", "ZGYY2m80.xlsx", "ZGYY3m80.xlsx", "全部A股日行情.xlsx", "全部A股资金流向.xlsx"]
    # print(os.listdir(folder_path))
    # 遍历年月日文件夹
    for year in os.listdir(folder_path):
        year_path = os.path.join(folder_path, year)
        if not os.path.isdir(year_path):
            continue
        for month in os.listdir(year_path):
            month_path = os.path.join(year_path, month)
            if not os.path.isdir(month_path):
                continue
            for day in os.listdir(month_path):
                day_path = os.path.join(month_path, day)
                if not os.path.isdir(day_path):
                    continue
                print("************  文件夹日期: {}-{}-{} ************ ".format(year, month, day))
                current_folder_date = Tools.date_format("{}-{}-{}".format(year, month, day))
                for file_name in os.listdir(day_path):
                    if file_name in file_names:
                        file_path = os.path.join(day_path, file_name)
                        print("************ 当前入库文件路径为:{} ************".format(file_path))
                        if file_name == "全部A股资金流向.xlsx":
                            info_data, file_date = Tools.load_excel(file_path, 2)
                            if current_folder_date == file_date:
                                db.executemany_replace_capital_day(info_data, file_date)
                            else:
                                print("{} {} 数据日期和 文件夹日期不匹配".format(file_name, current_folder_date))
                        elif file_name == "全部A股日行情.xlsx":
                            info_data, file_date = Tools.load_excel(file_path, 2)
                            if current_folder_date == file_date:
                                db.executemany_replace_quotation_day(info_data, file_date)
                            else:
                                print("{} {} 数据日期和 文件夹日期不匹配".format(file_name, current_folder_date))
                        elif file_name == "ZGYY1m80.xlsx":
                            info_data, file_date = Tools.load_excel(file_path, 4)
                            if current_folder_date == file_date:
                                db.executemany_replace_zgyy_model(info_data, 1, file_date)
                            else:
                                print("{} {} 数据日期和 文件夹日期不匹配".format(file_name, current_folder_date))
                        elif file_name == "ZGYY2m80.xlsx":
                            info_data, file_date = Tools.load_excel(file_path, 4)
                            if current_folder_date == file_date:
                                db.executemany_replace_zgyy_model(info_data, 2, file_date)
                            else:
                                print("{} {} 数据日期和 文件夹日期不匹配".format(file_name, current_folder_date))
                        elif file_name == "ZGYY3m80.xlsx":
                            info_data, file_date = Tools.load_excel(file_path, 4)
                            if current_folder_date == file_date:
                                db.executemany_replace_zgyy_model(info_data, 3, file_date)
                            else:
                                print("{} {} 数据日期和 文件夹日期不匹配".format(file_name, current_folder_date))
                        else:
                            value = False
                        print(file_path)

    db.close()


if __name__ == '__main__':
    # global db, date
    main()
