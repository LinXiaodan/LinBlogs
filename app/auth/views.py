#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-5
# Author: LXD

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User, temp, verify_password
from forms import LoginForm
from pymongo import MongoClient


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = MongoClient().LinBlogsDB.User.find_one({'email': form.email.data})

        if user:
            if verify_password(user.get('password'), form.password.data):
                new_user = temp(user_id=user.get('_id'), username=user.get('username'), email=user.get('email'),
                                password=user.get('password'))
                login_user(new_user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.index'))

            flash('Invalid password')

        flash('Invalid username')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register')
def register():
    return render_template('index.html')