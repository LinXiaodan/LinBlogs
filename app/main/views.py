#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash, request
from forms import NameForm, EditProfileForm, EditProfileAdminForm
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import Permission, temp
from bson import ObjectId
from ..Models.user import UserModel

from . import main
from pymongo import MongoClient
import logging
logging.basicConfig(level=logging.INFO)


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


@main.route('/edit-profile-admin', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin():

    user_id = request.args.get('user_id')
    user = UserModel.query_user({'_id': ObjectId(user_id)})
    if user is None:
        abort(404)

    form = EditProfileAdminForm()
    if form.validate_on_submit():
        new_user = {
            'email': form.email.data,
            'username': form.username.data,
            'confirmed': form.confirmed.data,
            'role': form.role.data,
            'name': form.name.data,
            'location': form.location.data,
            'about_me': form.about_me.data,
        }
        if UserModel.query_user({'email': new_user['email']}):
            UserModel.update_user({'email': new_user['email']}, new_user)
            flash('The profile of {} has been updated.'.format(new_user['email']))
        else:
            UserModel.insert_user(new_user)
            flash('The profile of {} has been added.'.format(new_user['email']))
        return redirect(url_for('.user', username=new_user['username']))

    form.email.data = user.get('email')
    form.username.data = user.get('username')
    form.confirmed.data = user.get('confirmed')
    form.role.data = user.get('role')
    form.name.data = user.get('name')
    form.location.data = user.get('location')
    form.about_me.data = user.get('about_me')
    return render_template('edit_profile.html', form=form)


