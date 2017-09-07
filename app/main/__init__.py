#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)