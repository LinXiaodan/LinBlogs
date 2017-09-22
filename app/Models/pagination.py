#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-15
# Author: LXD

from pymongo import MongoClient, DESCENDING
import math
import logging
logging.basicConfig(level=logging.INFO)


class Paginate(object):
    db = MongoClient().get_database('LinBlogsDB')

    def __init__(self, collection_name, page=1, per_page=3):
        self.collection = self.db.get_collection(collection_name)
        self.per_page = per_page

        articles = self.collection.find().sort('issuing_time', DESCENDING)
        self.page_num = int(math.ceil(1.0*articles.count()/per_page))

        if page >= self.page_num:
            self.page = self.page_num
        elif page > 0:
            self.page = page
        else:
            self.page = 1

        if self.page > 1:
            self.has_prev = True
        else:
            self.has_prev = False

        if self.page < self.page_num:
            self.has_next = True
        else:
            self.has_next = False

        current_num = articles.count() - per_page * (self.page - 1)
        if current_num > per_page:
            current_num = per_page
        self.items = []
        for i in range(current_num):
            self.items.append(articles[per_page * (self.page - 1) + i])

    def iter_pages(self, left_edge=2, left_current=2, right_current=2, right_edge=2):
        record = 0
        for i in range(1, self.page_num+1):
            if i <= left_edge \
                    or self.page - left_current <= i <= self.page + right_current \
                    or i > self.page_num - right_edge:
                if record + 1 != i:
                    yield None
                yield i
                record = i


if __name__ == '__main__':
    pagination = Paginate(collection_name='Article')
    print pagination.page_num
    for p in pagination.iter_pages():
        print p