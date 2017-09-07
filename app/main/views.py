#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from datetime import datetime
from flask import render_template, session, redirect, url_for
from forms import NameForm
from flask_login import login_required
from ..decorators import admin_required, permission_required
from ..models import Permission

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


@main.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return 'For administrators!'


@main.route('/moderators')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return 'For comment moderators!'
