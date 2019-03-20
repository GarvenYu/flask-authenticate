#! usr/bin/env python3
# -*-coding:utf-8-*-

from flask import Flask, request, jsonify
import pymysql
from model.model import User, Guest
from flask_login import login_user
from decorators import check_role
from flask_login import LoginManager

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='test_user_role',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask('app')
app.secret_key = 'secret'
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.anonymous_user = Guest


@login_manager.user_loader
def load_user(user_id):
    cursor = connection.cursor()
    sql1 = "select role_id from user where id = %s" % (user_id,)
    cursor.execute(sql1)
    role_id = cursor.fetchone()
    sql2 = "select a.code from sys a left join sys_role_mid b on a.id = b.func_id where b.role_id = %d" \
           % role_id.get('role_id')
    cursor.execute(sql2)
    sys_codes = cursor.fetchall()
    return User(user_id, name='admin', funcs=[i.get('code') for i in sys_codes])


@app.route('/index', methods=['GET'])
def index():
    account = request.args.get('account')
    password = request.args.get('password')
    # 假设账号密码无误
    # 获取用户信息
    cursor = connection.cursor()
    sql1 = "select role_id from user where account = '%s' and password = '%s'" % (account, password)
    cursor.execute(sql1)
    role_id = cursor.fetchone()
    sql2 = "select a.code from sys a left join sys_role_mid b on a.id = b.func_id where b.role_id = %d " \
           % role_id.get('role_id')
    cursor.execute(sql2)
    sys_codes = cursor.fetchall()
    user = User(2, name='admin', funcs=[i.get('code') for i in sys_codes])
    login_user(user)
    return jsonify(msg="success")


@app.route('/admin')
@check_role('read')
def check():
    return jsonify(msg="admin")
