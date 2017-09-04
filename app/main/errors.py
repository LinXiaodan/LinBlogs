#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    # return '404', 400
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    # return '500', 500
    return render_template('500.html'), 500