#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash
from forms import NameForm, EditProfileForm
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import Permission, temp
from .. import moment

from . import main
from pymongo import MongoClient


@main.route('/', methods=['GET', 'POST'])
def index():
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


@main.route('/user/<username>')
def user(username):
    user = MongoClient().LinBlogsDB.User.find_one({'username': username})
    if user:
        user_temp = temp(user_id=user.get('_id'), username=user.get('username'), email=user.get('email'),
                         password=user.get('password'), confirmed=False, role=user.get('role'),
                         location=user.get('location'), about_me=user.get('about_me'),
                         member_since=user.get('member_since'), last_seen=user.get('last_seen'), name=user.get('name'))
        return render_template('user.html', user=user_temp)

    abort(404)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        MongoClient().LinBlogsDB.User.update(
            {'username': current_user.username},
            {'$set': {'name': form.name.data, 'location': form.location.data, 'about_me': form.about_me.data}})
        flash('Your profile has been update.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)