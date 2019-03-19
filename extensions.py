#! usr/bin/env python3
# -*-coding:utf-8-*-

from flask_login import LoginManager
from model.model import User
from app import connection

login_manager = None


def register_login(app):
    global login_manager
    login_manager = LoginManager(app)
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user WHERE id = %s" % (user_id,)
            cursor.execute(sql)
            result = cursor.fetchone()
            return User(result[0], name=result[1], group_id=result[2])
    finally:
        connection.close()
