#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-5
# Author: LXD

from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, temp, verify_password
from forms import LoginForm, RegisterForm
from pymongo import MongoClient
from ..email import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bson import ObjectId
import logging
logging.basicConfig(level=logging.INFO)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        # current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    logging.info(current_user.is_anonymous)
    logging.info(current_user.confirmed)
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = MongoClient().LinBlogsDB.User.find_one({'email': form.email.data})

        if user:
            if verify_password(user.get('password'), form.password.data):
                new_user = temp(user_id=user.get('_id'), username=user.get('username'), email=user.get('email'),
                                password=user.get('password'), confirmed=user.get('confirmed'), role=user.get('role'))
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


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        logging.info('validate register')
        new_user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        user = new_user.add_user()
        user_temp = temp(user_id=user.get('_id'), username=user.get('username'), email=user.get('email'),
                         password=user.get('password'), confirmed=False, role=user.get('role'))
        token = user_temp.generate_confirmation_token()
        send_email(user_temp.email, 'Confirm Your Account', 'auth/email/confirm', user=user_temp, token=token)
        flash('A confirmation email has been send to you by email')
        return redirect(url_for('auth.login'))
    logging.info('not validate register')
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
def confirm(token):
    logging.info('start confirm')
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return redirect(url_for('main.index'))
    user_id = data.get('confirm')
    user = MongoClient().LinBlogsDB.User.find_one({'_id': ObjectId(user_id)})
    if user:
        if user.get('confirmed'):
            logging.info('has confirmed')
            flash('The account is already confirmed')
        else:
            logging.info('confirm success')
            MongoClient().LinBlogsDB.User.update({'_id': ObjectId(user_id)}, {'$set': {'confirmed': True}})
            flash('You have confirmed your account. Thanks!')
    else:
        logging.info('confirm account not found')
        flash('The confirmation link is invalid or has expired.')
    logging.info('end confirm')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirm_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been send to you by email')
    return redirect(url_for('main.index'))
