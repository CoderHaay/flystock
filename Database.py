# -*- coding: utf-8 -*-
# @Time : 2023/2/9 14:17
# @Author : 郝毅
# @Email : haoyi@harmight.com
# @File : Datebase.py
# @Project : 东方财富OCR
import datetime
import re

import pymysql
import pymysql.cursors
import numpy as np
import time
import pandas


class Database:
    connected = False
    db = None

    # 构造函数，初始化时直接连接数据库
    def __init__(self, host=None, user=None, db_password=None, db_name=None, port=3306):
        if host is not None:
            import pymysql
            import pymysql.cursors
            conf = {
                "host": host,
                "user": user,
                "password": db_password,
                "database": db_name,
                "port": port,
                "charset": "utf8"
            }
            if type(conf) is not dict:
                print('错误: 参数不是字典类型！')
            else:
                for key in ['host', 'port', 'user', 'password', 'database']:
                    if key not in conf.keys():
                        print('错误: 参数字典缺少 %s' % key)
                if 'charset' not in conf.keys():
                    conf['charset'] = 'utf8'
            try:
                self.db = pymysql.connect(
                    host=conf['host'],
                    port=conf['port'],
                    user=conf['user'],
                    passwd=conf['password'],
                    db=conf['database'],
                    charset=conf['charset'],
                    cursorclass=pymysql.cursors.DictCursor)
                self.connected = True

            except pymysql.Error as e:
                print('数据库连接失败:', end='')
        else:
            pass

    def connect_check(self):
        # 使用 cursor() 方法创建一个游标对象
        cursor = self.db.cursor()

        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT VERSION()")

        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchone()

        print("Database version : %s " % data)
        self.close()

    # 插入数据到数据表
    def insert(self, table, val_obj):
        import pymysql
        sql_top = 'INSERT INTO ' + table + ' ('
        sql_tail = ') VALUES ('
        for key, val in val_obj.items():
            sql_top += '`' + key + '`' + ','
            val = "'" + val + "'" if type(val) == str else val
            sql_tail += val + ','
        sql = sql_top[:-1] + sql_tail[:-1] + ')'
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            self.db.rollback()
            return {e, sql}

    # 插入数据到数据表
    def replace(self, table, val_obj):
        import pymysql
        sql_top = 'REPLACE INTO ' + table + ' ('
        sql_tail = ') VALUES ('
        for key, val in val_obj.items():
            sql_top += '`' + key + '`' + ','
            val = "'" + val + "'" if type(val) == str else val
            sql_tail += val + ','
        sql = sql_top[:-1] + sql_tail[:-1] + ')'
        print("sql = {}".format(sql))
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.lastrowid
        except pymysql.Error as e:
            self.db.rollback()
            return {e, sql}

    def insert_many(self, table, params, all_data):
        import pymysql
        sql_top = 'INSERT INTO ' + str(table) + ' ('
        sql_tail = ') VALUES ('
        for val in params:
            sql_top += '`' + str(val) + '`' + ','
            # val = "'" + val + "'" if type(val) == str else val
            sql_tail += str('%s') + ','
        sql = sql_top[:-1] + sql_tail[:-1] + ')'
        try:
            # return {sql, all_data}
            with self.db.cursor() as cursor:
                flag = cursor.executemany(sql, all_data)
            self.db.commit()
            return flag
        except pymysql.Error as e:
            self.db.rollback()
            print({e, sql})
            return {e, sql}

    # 更新数据到数据表
    def update(self, table, val_obj, range_str):
        import pymysql
        sql = 'UPDATE ' + table + ' SET '
        for key, val in val_obj.items():
            if val is None:
                val = ''
            val = "'" + val + "'" if type(val) == str else val
            sql += key + '=' + val + ','
        sql = sql[:-1] + ' WHERE ' + range_str
        print("sql = {}".format(sql))
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            self.db.rollback()
            return False

    # 删除数据在数据表中
    def delete(self, table, range_str):
        import pymysql
        sql = 'DELETE FROM ' + table + ' WHERE ' + range_str
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.rowcount
        except pymysql.Error as e:
            self.db.rollback()
            return False

    # 查询唯一数据在数据表中
    def select_one(self, table, factor_str, field='*'):
        import pymysql
        sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + factor_str
        print("sql = {}".format(sql))
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.fetchone()
        except pymysql.Error as e:
            return False

    # 查询多条数据在数据表中
    def select_more(self, table, range_str, field='*'):
        import pymysql
        sql = 'SELECT ' + field + ' FROM ' + table + ' WHERE ' + range_str
        print("sql = {}".format(sql))
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            return False

    # 统计某表某条件下的总行数
    def count(self, table, range_str='1'):
        import pymysql
        sql = 'SELECT count(*)res FROM ' + table + ' WHERE ' + range_str
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            return False

    # 统计某字段（或字段计算公式）的合计值
    def sum(self, table, field, range_str='1'):
        import pymysql
        sql = 'SELECT SUM(' + field + ') AS res FROM ' + table + ' WHERE ' + range_str
        try:
            with self.db.cursor() as cursor:
                cursor.execute(sql)
            self.db.commit()
            return cursor.fetchall()[0]['res']
        except pymysql.Error as e:
            return False

    def query(self, sql):
        import pymysql
        try:
            with self.db.cursor() as cursor:
                cursor.execute(str(sql))
            self.db.commit()
            return cursor.fetchall()
        except pymysql.Error as e:
            print(str(e))
            return False

    # 纯 sql 封装
    def ping(self, value=True):
        self.db.ping(value)

    def insert_by_sql(self, sql):
        ''' 插入数据库操作 '''
        print(sql)
        cursor = self.db.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

    def execute_many_by_sql(self, sql, data_list):
        import pymysql
        ''' 批量插入数据库操作 '''
        print(sql)
        cursor = self.db.cursor()
        # start = time.clock()
        try:
            cursor.executemany(sql, data_list)
            self.db.commit()
            cursor.close()
        except pymysql.Error as e:
            print(e)
            self.db.rollback()
        # end = time.clock()

    def delete_by_sql(self, sql):
        ''' 操作数据库数据删除 '''
        cursor = self.db.cursor()

        try:
            # 执行sql
            cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

    def update_by_sql(self, sql):
        ''' 更新数据库操作 '''

        cursor = self.db.cursor()

        try:
            # 执行sql
            cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()

    def select_by_sql(self, sql):
        ''' 数据库查询 '''
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果

            data = cursor.fetchall()  # 返回所有记录列表

            print(data)

            # 结果遍历
            for row in data:
                sid = row[0]
                name = row[1]
                # 遍历打印结果
                print('sid = %s,  name = %s' % (sid, name))
        except:
            print('Error: unable to fecth data')

    def data_clear(self, data, file_date):
        import numpy as np
        data_each = np.insert(data, 2, file_date)

        for d in range(len(data_each)):
            if data_each[d] == "——":
                data_each[d] = None
            if data_each[d] == "否":
                data_each[d] = 0
            elif data_each[d] == "是":
                data_each[d] = 1
        return data_each

    def insert_capital_day(self, info_data,
                           sql='insert into hm_capital_day (CODE, NAME, DATE, INFLOW, OUTFLOW, NETINFLOW, INFLOWRATE, BUYVOLUME , SELLVOLUME, NETINVOLUME, SUPINFLOW, SUPOUTFLOW, SUPNETINFLOW, SUPBUYVOLUME, SUPSELLVOLUME, SUPNETINVOLUME, BIGINFLOW, BIGOUTFLOW, BIGNETINFLOW, BIGBUYVOLUME, BIGSELLVOLUME, BIGNETINVOLUME, MIDINFLOW, MIDOUTFLOW, MIDNETINFLOW, MIDBUYVOLUME, MIDSELLVOLUME, SMINFLOW, SMOUTFLOW, SMNETINFLOW, SMBUYVOLUME, SMSELLVOLUME) values {}'):

        self.batch_insert(info_data, sql)

    def insert_quotation_day(self, info_data,
                             sql='insert into hm_quotation_day (CODE, NAME, DATE, OPEN, CLOSE, HIGH, LOW, PRECLOSE, AVERAGE, `CHANGE`, PCTCHANGE, VOLUME, HIGHLIMIT, AMOUNT, TURN, LOWLIMIT, AMPLITUDE, TNUM, TAFACTOR, FRONTTAFACTOR, ISSTSTOCK,ISXSTSTOCK) values {}'):
        self.batch_insert(info_data, sql)

    def batch_insert(self, info_data, sql):
        for i in range(0, len(info_data)):
            print("*" * 5, i, "*" * 5)
            if i > 1:
                self.ping()
            data_each = info_data[i]
            data_each = self.data_clear(data_each)
            insert_sql = sql.format(tuple(data_each))
            self.insert_by_sql(insert_sql)

    def many_insert_data(self, info_data, file_date):
        list = []
        for i in range(0, len(info_data)):
            # print("*" * 5, i, "*" * 5)
            data_each = info_data[i]
            data_each = self.data_clear(data_each, file_date)
            # print(data_each)
            list.append(tuple(data_each))

        return list

    def check_data_exists(self, table_name, factor_str):
        data = self.select_one(table_name, factor_str)
        if data is not None:
            return True
        return False

    def executemany_replace_capital_day(self, data, file_date):
        sql = 'replace  into hm_capital_day (CODE, NAME, DATE, INFLOW, OUTFLOW, NETINFLOW, INFLOWRATE, BUYVOLUME , SELLVOLUME, NETINVOLUME, SUPINFLOW, SUPOUTFLOW, SUPNETINFLOW, SUPBUYVOLUME, SUPSELLVOLUME, SUPNETINVOLUME, BIGINFLOW, BIGOUTFLOW, BIGNETINFLOW, BIGBUYVOLUME, BIGSELLVOLUME, BIGNETINVOLUME, MIDINFLOW, MIDOUTFLOW, MIDNETINFLOW, MIDBUYVOLUME, MIDSELLVOLUME, SMINFLOW, SMOUTFLOW, SMNETINFLOW, SMBUYVOLUME, SMSELLVOLUME, DDX) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data = self.many_insert_data(data, file_date)
        self.execute_many_by_sql(sql, data)

    # 22 个字段
    def executemany_replace_quotation_day(self, data, file_date):
        sql = 'replace  into hm_quotation_day (CODE, NAME, DATE, OPEN, CLOSE, HIGH, LOW, PRECLOSE, AVERAGE, `CHANGE`, PCTCHANGE, VOLUME, HIGHLIMIT, AMOUNT, TURN, LOWLIMIT, AMPLITUDE, TNUM, PE, TAFACTOR, FRONTTAFACTOR, ISSTSTOCK,ISXSTSTOCK) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data = self.many_insert_data(data, file_date)
        self.execute_many_by_sql(sql, data)

    def executemany_replace_zgyy_model(self, info_data, model, file_date):
        sql = 'replace  into hm_zgyy_{} (CODE ,NAME ,DATE ,c1 ,c2 ,c3 ,C4 ,C5 ,C6 ,C7 ,C8 ,C9 ,C10 ,C11 ,C12 ,C13 ,C14 ,C15 ,C16 ,C17 ,C18 ,C19 ,C20 ,C21 ,C22 ,C23 ,C24 ,C25 ,C26 ,C27 ,C28 ,C29 ,C30 ,C31 ,C32 ,C33 ,C34 ,C35 ,C36 ,C37 ,C38 ,C39 ,C40 ,C41 ,C42 ,C43 ,C44 ,C45 ,C46 ,C47 ,C48 ,C49 ,C50 ,C51 ,C52 ,C53 ,C54 ,C55 ,C56 ,C57 ,C58 ,C59 ,C60 ,C61 ,C62 ,C63 ,C64 ,C65 ,C66 ,C67 ,C68 ,C69 ,C70 ,C71 ,C72 ,C73 ,C74 ,C75 ,C76 ,C77 ,C78 ,C79 ,C80 ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(
            model)
        list = self.many_insert_data(info_data, file_date)
        self.execute_many_by_sql(sql, list)

    # 销毁对象时关闭数据库连接

    # 关闭数据库连接
    def close(self):
        import pymysql
        try:
            self.db.cursor().close()
            self.db.close()
        except pymysql.Error as e:
            pass
