#! usr/bin/env python3
# -*-coding:utf-8-*-
import pymysql


class MysqlConfig:
    CONFIG = {
        'Test': {'host': 'localhost',
                 'port': 3306,
                 'user': 'root',
                 'password': '123456',
                 'db': 'test_user_role',
                 'cursorclass': pymysql.cursors.DictCursor
                 },
        'Production': {}
    }

    def __init__(self, env):
        self._config = self.CONFIG.get(env)

    def handle_error(self, err):
        print("Error!", err)

    def execute_sql(self, sql) -> "list[dict]":
        connection = pymysql.connect(**self._config)
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            rs = cursor.fetchall()
            return rs
        except Exception as e:
            self.handle_error(e)
        finally:
            connection.close()
