#! usr/bin/env python3
# -*-coding:utf-8-*-

from uuid import uuid4
from flask_login import UserMixin
from app import connection


class SystemFunction:

    def __init__(self, code=None):
        id = uuid4()
        func_code = code


class Role:

    def __init__(self, name=None, func_id=None):
        id = uuid4()
        name = name
        func_id = func_id


class UserGroup:

    def __init__(self, name=None, role_id=None):
        id = uuid4()
        name = name
        role_id = role_id


class User(UserMixin):

    def __init__(self, id, name=None, group_id=None):
        id = id
        name = name
        group_id = group_id

    def can(self, code):
        """检查是否有某项权限"""
        try:
            with connection.cursor() as cursor:
                sql = """
                        SELECT a.id
                        from sys a
                        inner join role b
                        on a.id = b.func_id
                        inner join user_group c
                        on b.id = c.role_id
                        inner join user d
                        on d.group_id = c.id
                        where d.id = %s and a.code = %s
                        """ % (self.id, code)
                cursor.execute(sql)
                result = cursor.fetchone()
                return True if result else False
        finally:
            connection.close()
