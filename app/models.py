#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask_login import UserMixin, AnonymousUserMixin
from bson import ObjectId
from . import login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import logging
logging.basicConfig(level=logging.INFO)


def verify_password(user_password, password):
    return check_password_hash(user_password, password)


@login_manager.user_loader
def load_user(user_id):
    user = MongoClient().LinBlogsDB.User.find_one({'_id': ObjectId(user_id)})
    return temp(user_id=user_id, username=user.get('username'), email=user.get('email'), password=user.get('password'),
                confirmed=user.get('confirmed'), role=user.get('role'))


class User(object):
    conn = MongoClient().LinBlogsDB.User

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = generate_password_hash(kwargs.get('password'))

        if self.email == current_app.config['LINBLOGS_ADMIN']:
            self.role = MongoClient().LinBlogsDB.Role.find_one({'permissions': 0xff})
        else:
            self.role = MongoClient().LinBlogsDB.Role.find_one({'default': True})

    def add_user(self):
        collection = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'confirmed': False,
            'role': self.role
        }
        self.conn.insert(collection)
        return self.conn.find_one({'email': self.email})

    def __repr__(self):
        return self.username


class temp(UserMixin):
    is_active = True
    is_anonymous = False
    is_authenticated = True
    conn = MongoClient().LinBlogsDB.User

    def __init__(self, user_id, username, email, password, confirmed, role):
        self.id = str(user_id)
        self.username = username
        self.email = email
        self.password = password
        self.confirmed = confirmed
        self.role = role

    def get_id(self):
        return self.id

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        user = self.conn.find_one({'_id': self.id})
        if user:
            if user.get('confirmed'):
                return False
            self.conn.update({'_id': self.id}, {'$set': {'confirmed': True}})
            return True
        else:
            return False

    def can(self, permissions):
        return self.role is not None and (self.role['permissions'] & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return self.username


class Role(object):
    conn = MongoClient().LinBlogsDB.Role

    def __init__(self, name, default, permissions):
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


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
