#! usr/bin/env python3
# -*-coding:utf-8-*-

from uuid import uuid4
from flask_login import UserMixin, AnonymousUserMixin


class SystemFunction:

    def __init__(self, code=None, name=None):
        self.id = uuid4()
        self.func_code = code
        self.func_name = name


class Role:

    def __init__(self, name=None):
        self.id = uuid4()
        self.name = name


class User(UserMixin):

    def __init__(self, id, name=None, funcs=None):
        self.id = id
        self.name = name
        self.funcs = funcs

    def can(self, code):
        """检查是否有某项权限"""
        for a in self.funcs:
            if a == code:
                return True
        return False


class Guest(AnonymousUserMixin):

    def can(self, code):
        return False
