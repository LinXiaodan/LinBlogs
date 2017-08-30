#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 17-8-29
# Author: LXD

from flask import Flask, request, render_template, url_for
import time

UPLOAD_FOLDER = 'path/uploads/'

app = Flask(__name__)


@app.route('/')
def index():
    summary = 'test'
    blogs = [
        dict(id='1', name='name1', summary=summary, created_at=time.time()-120),
        dict(id='2', name='name2', summary=summary, created_at=time.time()-3000),
        dict(id='3', name='name3', summary=summary, created_at=time.time()-7200)
    ]
    return render_template('blogs.html', blogs=blogs)


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return 'register success'


@app.route('/api/register', methods=['POST'])
def api_register():
    return 'success'

if __name__ == '__main__':
    app.run(port=8080)