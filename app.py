#! usr/bin/env python3
# -*-coding:utf-8-*-

from flask import Flask
import extensions as ex
import pymysql

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='test_user_role',
                             cursorclass=pymysql.cursors.DictCursor)


def create_app():
    app = Flask(__name__)
    ex.register_login(app)
    return app
