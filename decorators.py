#! usr/bin/env python3
# -*-coding:utf-8-*-

from functools import wraps
from flask_login import current_user
from flask import abort


def check_role(code):
    """
    检查用户权限
    :param code: 权限代码
    :return: Function
    """

    def decorator(func):
        @wraps(func)
        def f(*args, **kwargs):
            if not current_user.can(code):
                abort(403)
            return func(*args, **kwargs)

        return f

    return decorator
