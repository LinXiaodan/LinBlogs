#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-15
# Author: LXD

from pymongo import MongoClient, DESCENDING
from ..models import Article
from datetime import datetime


class ArticleModel(object):
    db = MongoClient().get_database('LinBlogsDB')
    collection = db.get_collection('Article')

    @staticmethod
    def query_article(item=None):
        return ArticleModel.collection.find(item).sort('issuing_time', DESCENDING)

    @staticmethod
    def update_article(article_id, body):
        update_item = {
            'body': body,
            'body_html': Article(body).body_html,
            'issuing_time': datetime.now()
        }
        ArticleModel.collection.update({'_id': article_id}, {'$set': update_item})