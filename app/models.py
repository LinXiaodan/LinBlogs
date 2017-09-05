#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask_login import UserMixin
from bson import ObjectId
from . import login_manager


def verify_password(user_password, password):
    return check_password_hash(user_password, password)


@login_manager.user_loader
def load_user(user_id):
    user = MongoClient().LinBlogsDB.User.find_one({'_id': ObjectId(user_id)})
    return temp(user_id=user_id, username=user.get('username'), email=user.get('email'), password=user.get('password'))


class User(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username', 'nameNone')
        self.email = kwargs.get('email', 'emailNone')
        self.password = generate_password_hash(kwargs.get('password', 'passwordNone'))
        self.db = MongoClient().LinBlogsDB.User

    def add_user(self):
        result = self.find_user()
        if result == 0:
            collection = {
                'username': self.username,
                'email': self.email,
                'password': self.password
            }
            self.db.insert(collection)

        return result

    def find_user(self):
        name_find = self.db.find_one({'username': self.username})
        if name_find:
            return 1
        email_find = self.db.find_one({'email': self.email})
        if email_find:
            return 2
        return 0

    def __repr__(self):
        return self.username

    def verify_password(self):
        """
        验证密码
        :return: 0：密码和用户名匹配， 1：密码错误， 2：用户名不存在
        """
        result = self.db.find_one({'email': self.email})
        if result:
            if check_password_hash(result.get('password'), self.password):
                return 0
            return 1
        return 2


class temp(UserMixin):
    is_active = True
    is_anonymous = False
    is_authenticated = True

    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.username
