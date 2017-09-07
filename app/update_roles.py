#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-7
# Author: LXD
# 在数据库中更新用户角色用，注意与models中对用的部分保持一致性

from pymongo import MongoClient
import logging
logging.basicConfig(level=logging.INFO)


class Role(object):
    conn = MongoClient().LinBlogsDB.Role

    def __init__(self, name, permissions, default):
        self.name = name
        self.default = default
        self.permissions = permissions

    def add_role(self):
        collection = {
            'name': self.name,
            'default': self.default,
            'permissions': self.permissions
        }
        self.conn.insert(collection)


class Permission(object):
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


def insert_roles():
    roles = {
        'User': (Permission.FOLLOW |
                 Permission.COMMENT |
                 Permission.WRITE_ARTICLES, True),
        'Moderator': (Permission.FOLLOW |
                      Permission.COMMENT |
                      Permission.WRITE_ARTICLES |
                      Permission.MODERATE_COMMENTS, False),
        'Administrator': (0xff, False)
    }
    conn = MongoClient().LinBlogsDB.Role
    for r in roles:
        role = conn.find_one({'name': r})
        if role is None:
            logging.info('insert {}, {}, {}'.format(r, roles[r][0], roles[r][1]))
            new_role = Role(name=r, permissions=roles[r][0], default=roles[r][1])
            new_role.add_role()
        else:
            logging.info('update {}, {}, {}'.format(r, roles[r][0], roles[r][1]))
            conn.update({'name': r}, {'$set': {'permissions': roles[r][0]}})
            conn.update({'name': r}, {'$set': {'default': roles[r][1]}})


if __name__ == '__main__':
    insert_roles()
