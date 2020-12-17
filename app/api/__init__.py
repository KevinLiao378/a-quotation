# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import routes
