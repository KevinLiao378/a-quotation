# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from app.main import bp
from flask import render_template


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
