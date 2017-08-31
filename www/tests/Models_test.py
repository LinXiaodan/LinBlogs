#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-30
# Author: LXD

from www.Models import User
import unittest


class TestModel(unittest.TestCase):

    def test_add_user(self):
        user1 = User(username='name1', email='123@11.com', password='aaaaaa')
        user2 = User(username='name2', email='1234@11.com', password='aaaaaa')
        user3 = User(username='name1', email='1111@11.com', password='aa220@kdo')
        user4 = User(username='name4', email='123@11.com', password='dikdo$%%%')
        user5 = User(username='name2', email='1234@11.com', password='aaaaaa')
        self.assertEqual(user1.add_user(), 0)
        self.assertEqual(user2.add_user(), 0)
        self.assertEqual(user3.add_user(), 1)
        self.assertEqual(user4.add_user(), 2)
        self.assertEqual(user5.add_user(), 1)