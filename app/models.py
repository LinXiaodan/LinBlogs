#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient


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

    def verify_password(self, password):
        user = self.db.find_one({'username': self.username})
        if user:
            password_hash = user['password']
            return check_password_hash(password_hash, password)
        else:
            return False