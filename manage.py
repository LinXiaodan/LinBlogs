#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-31
# Author: LXD

import os
from app import create_app
from flask_script import Manager, Shell
from flask import url_for

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command("run", )

if __name__ == '__main__':
    manager.run()