#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-5
# Author: LXD

import unittest
from app.models import User
from pymongo import MongoClient


class UserModelTestCase(unittest.TestCase):

    def test_add_user(self):
        coll = MongoClient().LinBlogsDB.User
        coll.remove({'username': 'test_name1'})
        coll.remove({'username': 'test_name4'})
        user1 = User(username='test_name1', email='test_email1', password='test_password')
        user2 = User(username='test_name1', email='test_email2', password='test_password')
        user3 = User(username='test_name3', email='test_email1', password='test_password')
        user4 = User(username='test_name4', email='test_email4', password='test_password')
        self.assertEqual(user1.add_user(), 0)
        self.assertEqual(user2.add_user(), 1)
        self.assertEqual(user3.add_user(), 2)
        self.assertEqual(user4.add_user(), 0)

    def test_password_verification(self):
        user = User(password='cat')
        self.assertTrue(user.verify_password('cat'))
        self.assertFalse(user.verify_password('dog'))

    def test_password_salts_are_random(self):
        user = User(password='cat')
        user2 = User(password='cat')
        self.assertTrue(user.password != user2.password)