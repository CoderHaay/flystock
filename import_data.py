# -*- coding: utf-8 -*-
# @Time : 2023/2/15 16:47
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : import_data.py
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

    now_date = Tools.get_current_date()

    db = Database(host=host, user=user, db_password=password, db_name=db_name)

    # file_path = result["capital_day"]  ## 文件
    # info_data = db.load_excel(file_path, 2)
    # db.many_insert_capital_day(info_data)

    zgyy_column = 4
    file_path = result["ZGYY1m80"]  ## 文件
    info_data, date = Tools.load_excel(file_path, zgyy_column)
    folder_path = None
    if date == now_date:
        folder_path = Tools.create_folder()
    Tools.copy_file(file_path, folder_path)

    if date == now_date and info_data is not False:
        db.executemany_replace_zgyy_model(info_data, 1)
    else:
        print("1号错误")

    file_path = result["ZGYY2m80"]  ## 文件
    Tools.copy_file(file_path, folder_path)

    info_data, date = Tools.load_excel(file_path, zgyy_column)
    if date == now_date and info_data is not False:
        db.executemany_replace_zgyy_model(info_data, 2)
    else:
        print("2号错误")

    file_path = result["ZGYY3m80"]  ## 文件
    Tools.copy_file(file_path, folder_path)

    info_data, date = Tools.load_excel(file_path, zgyy_column)
    if date == now_date and info_data is not False:
        db.executemany_replace_zgyy_model(info_data, 3)
    else:
        print("3号错误")

    # file_path = result["quotation_day"]  ## 文件
    info_data = Tools.load_excel(file_path)
    # db.many_insert_quotation_day(info_data)

    # data = db.check_data_exists("hm_capital_day", 'date="{}"'.format(db.get_current_date()))
    # print(data)
    # file_path = result["ZGYY1L80"]  ## 文件
    # info_data = Tools.load_excel(file_path, 3)
    # db.many_insert_zgyy_model(info_data, 1)

    # date = '2023-02-24'
    # from datetime import datetime
    # date_string = date
    # date_format = datetime.strptime(date_string, '%Y-%m-%d')
    # # date_format = datetime.strptime(date_string, "%Y/%m/%d")
    # value = date_format.strftime("%Y-%m-%d")
    # print(value)

    # code = "000099"
    # ddy = 0.0
    # ddz = 0.0
    #
    # insert_sql = "INSERT INTO hm_bad_data_record (CODE, DDY, DDZ, DATE) VALUES ('%s', %s, %s, '%s')" % (
    #     code, ddy, ddz, date)
    # print("sql = {}".format(insert_sql))
    # db.insert_by_sql(insert_sql)
    db.close()


if __name__ == '__main__':
    # global db, date
    main()
