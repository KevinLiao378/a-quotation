# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from app import create_app, db, cli
from app.models import Game, Hero, Quotation
from config import Config

app = create_app(Config)
cli.init_app(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Game': Game, 'Hero': Hero, 'Quotation': Quotation}
