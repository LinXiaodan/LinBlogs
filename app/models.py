#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask_login import UserMixin, current_user
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
                confirmed=user.get('confirmed'))


class User(object):
    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = generate_password_hash(kwargs.get('password'))
        self.db = MongoClient().LinBlogsDB.User

    def add_user(self):
        collection = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'confirmed': False
        }
        self.db.insert(collection)
        return self.db.find_one({'email': self.email})

    def __repr__(self):
        return self.username


class temp(UserMixin):
    is_active = True
    is_anonymous = False
    is_authenticated = True

    def __init__(self, user_id, username, email, password, confirmed):
        self.id = str(user_id)
        self.username = username
        self.email = email
        self.password = password
        self.db = MongoClient().LinBlogsDB.User
        self.confirmed = confirmed

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
        user = self.db.find_one({'_id': self.id})
        if user:
            if user.get('confirmed'):
                return False
            self.db.update({'_id': self.id}, {'$set': {'confirmed': True}})
            return True
        else:
            return False

    def __repr__(self):
        return self.username