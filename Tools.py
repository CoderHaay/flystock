# -*- coding: utf-8 -*-
# @Time : 2023/3/23 18:52
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : Tools.py
# @Project : 东方财富OCR

from datetime import date
import datetime
import os
import shutil
from datetime import datetime


class Tools:
    def __int__(self):
        pass

    def create_folder(self):
        # 获取当前日期
        today = datetime.date.today()
        folder_path = r'D:\choice_excel_files'

        # 创建年月日文件夹
        year_folder = r"{}\{}".format(folder_path, today.year)
        month_folder = os.path.join(year_folder, str(today.month))
        day_folder = os.path.join(month_folder, str(today.day))

        if not os.path.exists(year_folder):
            os.mkdir(year_folder)
        if not os.path.exists(month_folder):
            os.mkdir(month_folder)
        if not os.path.exists(day_folder):
            os.mkdir(day_folder)

        self.copy_file(r'C:\Users\HaoYi\Downloads\LANDrop\ZGYY1m80.xlsx', day_folder)

    @staticmethod
    def copy_file(source_file, target_folder):
        # 指定源文件路径和目标文件夹路径
        # source_file = "example.txt"
        # source_file = source_file
        target_folder = target_folder

        # 将源文件复制到目标文件夹中
        shutil.copy(source_file, target_folder)

        # # 获取源文件的文件名和扩展名
        # file_name, file_extension = os.path.splitext(source_file)
        #
        # # 定义新文件名并重命名文件
        # new_file_name = "renamed" + file_extension
        # new_file_path = os.path.join(target_folder, new_file_name)
        # os.rename(os.path.join(target_folder, source_file), new_file_path)

    @staticmethod
    def load_excel(file_path, column_num):
        import pandas
        import datetime
        import re
        df = pandas.read_excel(file_path)  ## 读文件
        df = df.dropna()
        # print(df)

        date_string = list(df.columns)[column_num]
        match = re.search('\d{4}-\d{2}-\d{2}', date_string)
        excel_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()

        excel_data = pandas.DataFrame(df).values
        return excel_data, excel_date

    @staticmethod
    def get_current_date():
        from datetime import date
        return date.today()

    @staticmethod
    def date_format(string_time):
        date_time = datetime.strptime(string_time, "%Y-%m-%d").date()
        print(date_time)
        return date_time
