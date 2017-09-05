#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-9-5
# Author: LXD

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views