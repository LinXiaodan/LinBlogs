#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from datetime import datetime
from flask import render_template, session, redirect, url_for
from forms import NameForm

from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    # return 'index page'
    # name = None
    # form = NameForm()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     form.name.data = ''
    return render_template('index.html', form={}, name='')