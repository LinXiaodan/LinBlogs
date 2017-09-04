#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    # 路由及错误页面
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
