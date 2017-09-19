#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-15
# Author: LXD

from pymongo import MongoClient, DESCENDING


class ArticleModel(object):
    db = MongoClient().get_database('LinBlogsDB')
    collection = db.get_collection('Article')

    @staticmethod
    def query_article(item=None):
        return ArticleModel.collection.find(item).sort('issuing_time', DESCENDING)

    @staticmethod
    def paginate(item=None, page=1, per_page=5):
        """返回按照分页得到的文章"""
        if page == 1:
            return ArticleModel.collection.find(item).\
                sort('issuing_time', DESCENDING).\
                limit(per_page)

        return ArticleModel.collection.find(item).\
            sort('issuing_time', DESCENDING).\
            skip(per_page*(page-1)).\
            limit(per_page)