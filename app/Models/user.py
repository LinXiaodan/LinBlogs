#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-9
# Author: LXD

from pymongo import MongoClient


class UserModel(object):
    db = MongoClient().get_database('LinBlogsDB')
    collection = db.get_collection('User')

    @staticmethod
    def query_user(item):
        return UserModel.collection.find_one(item)

    @staticmethod
    def update_user(find_item, set_item):
        update_result = UserModel.collection.update(find_item, {'$set': set_item})
        return update_result['updatedExisting']

    @staticmethod
    def insert_user(insert_item):
        UserModel.collection.insert(insert_item)

# if __name__ == '__main__':
#     print UserModel.update_user({'username': 'linxiaodan'},
#                           {'about_me': 'about me update', 'name': 'new linxiaodan'})
#     print UserModel.update_user({'username': 'linlinlin'},
#                                 {'about_me': 'linxiaodan'})
#     print UserModel.update_user({'username': 'linxiaodan'},
#                                 {'nameadd': 'linxiaodan'})