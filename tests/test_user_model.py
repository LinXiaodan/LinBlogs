#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-5
# Author: LXD

import unittest
from app.models import User
from pymongo import MongoClient
from app.update_roles import insert_roles
from app.models import Permission, AnonymousUser
from app import create_app


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_add_user(self):
        user1 = User(username='test_name1', email='test_email1', password='test_password')
        self.assertIsNotNone(user1.add_user())

    def test_password_salts_are_random(self):
        user = User(password='cat')
        user2 = User(password='cat')
        self.assertTrue(user.password != user2.password)

    def test_roles_and_permissions(self):
        insert_roles()
        u = User(email='john@example.com', password='cat', username='test_role_name1')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

    def tearDown(self):
        conn = MongoClient().LinBlogsDB.User
        conn.remove({'username': 'test_name1'})
        conn.remove({'username': 'test_name4'})
        self.app_context.pop()
