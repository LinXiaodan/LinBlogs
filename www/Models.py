#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-30
# Author: LXD

import pymongo


class User(object):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        conn = pymongo.MongoClient(port=27017)
        self.db = conn.LinBlogsDB.User

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
        else:
            return result

    def find_user(self):
        """
        通过邮箱和名字进行查找
        :return: mongo中有相同的名字返回1，有相同的邮箱返回2，否则返回0
        """
        name_find = self.db.find_one({'username': self.username})
        if name_find:
            return 1
        email_find = self.db.find_one({'email': self.email})
        if email_find:
            return 2
        return 0

if __name__ == '__main__':
    user = User(username='aaa', email='bbbb', password='c')
    print user.add_user()