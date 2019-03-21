#! usr/bin/env python3
# -*-coding:utf-8-*-

from flask import Flask, request, jsonify
from model.model import User, Guest
from flask_login import login_user
from decorators import check_role
from flask_login import LoginManager
from config import MysqlConfig


app = Flask('app')
app.secret_key = 'secret'
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.anonymous_user = Guest
config = MysqlConfig('Test')


@login_manager.user_loader
def load_user(user_id):
    sql1 = "select role_id from user where id = %s" % (user_id,)
    role_id = config.execute_sql(sql1)
    sql2 = "select a.code from sys a left join sys_role_mid b on a.id = b.func_id where b.role_id = %d" \
           % role_id[0].get('role_id')
    sys_codes = config.execute_sql(sql2)
    return User(user_id, name='admin', funcs=[i.get('code') for i in sys_codes])


@app.route('/index', methods=['GET'])
def index():
    account = request.args.get('account')
    password = request.args.get('password')
    # 假设账号密码无误
    # 获取用户信息
    sql1 = "select role_id from user where account = '%s' and password = '%s'" % (account, password)
    role_id = config.execute_sql(sql1)
    sql2 = "select a.code from sys a left join sys_role_mid b on a.id = b.func_id where b.role_id = %d " \
           % role_id[0].get('role_id')
    sys_codes = config.execute_sql(sql2)
    user = User(2, name='admin', funcs=[i.get('code') for i in sys_codes])
    login_user(user)
    return jsonify(msg="success")


@app.route('/admin')
@check_role('read')
def check():
    return jsonify(msg="admin")
