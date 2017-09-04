#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')