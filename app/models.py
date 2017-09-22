#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from flask_login import UserMixin, AnonymousUserMixin, current_user
from bson import ObjectId
from . import login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import bleach
from markdown import markdown
import logging
logging.basicConfig(level=logging.INFO)


def verify_password(user_password, password):
    return check_password_hash(user_password, password)


@login_manager.user_loader
def load_user(user_id):
    user = MongoClient().LinBlogsDB.User.find_one({'_id': ObjectId(user_id)})
    return temp(user_id=user_id, username=user.get('username'), email=user.get('email'), password=user.get('password'),
                confirmed=user.get('confirmed'), role=user.get('role'), location=user.get('location'),
                about_me=user.get('about_me'), member_since=user.get('member_since'), last_seen=user.get('last_seen'),
                name=user.get('name'))


class User(object):
    conn = MongoClient().LinBlogsDB.User

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = generate_password_hash(kwargs.get('password'))

        if self.email == current_app.config['LINBLOGS_ADMIN']:
            self.role = MongoClient().LinBlogsDB.Role.find_one({'permissions': 0xff}).get('name')
        else:
            self.role = MongoClient().LinBlogsDB.Role.find_one({'default': True}).get('name')

    def add_user(self):
        collection = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'confirmed': False,
            'role': self.role,
            'location': '',
            'about_me': '',
            'member_since': datetime.now(),
            'last_seen': datetime.now(),
            'name': ''
        }
        self.conn.insert(collection)
        return collection

    def __repr__(self):
        return self.username


class temp(UserMixin):
    is_active = True
    is_anonymous = False
    is_authenticated = True
    conn = MongoClient().LinBlogsDB.User

    def __init__(self, user_id, username, email, password, confirmed, role, location, about_me, member_since,
                 last_seen, name):
        self.id = str(user_id)
        self.username = username
        self.email = email
        self.password = password
        self.confirmed = confirmed
        role_coll = MongoClient().LinBlogsDB.Role.find_one({'name': role})
        self.role = Role(name=role, permissions=role_coll.get('permissions'), default=role_coll.get('default'))
        self.location = location
        self.about_me = about_me
        self.member_since = member_since
        self.last_seen = last_seen
        self.name = name

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
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.now()
        self.conn.update({'email': self.email}, {'$set': {'last_seen': self.last_seen}})

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


class Article(object):
    def __init__(self, body):
        self.body = body
        self.body_html = self.get_body_html()

    def get_body_html(self):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong',
                        'ul', 'h1', 'h2', 'h3', 'p']
        body_html = bleach.linkify(bleach.clean(markdown(self.body, output_format='html'), tags=allowed_tags, strip=True))

        return body_html

    def add_article(self):
        new_article = {
            'user_id': current_user.id,
            'username': current_user.username,
            'body': self.body,
            'body_html': self.body_html,
            'issuing_time': datetime.now()
        }
        MongoClient().LinBlogsDB.Article.insert(new_article)
        return new_article
