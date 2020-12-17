# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from flask import Flask, request, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel


db = SQLAlchemy()
migrate = Migrate()
babel = Babel()


@babel.localeselector
def get_locale():
    """
    国际化支持
    :return:
    """
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'zh_CN')


def create_app(config_cls):
    """
    创建 Flask 实例
    :param config_cls: 配置类
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config_cls)

    db.init_app(app)
    migrate.init_app(app, db)

    babel.init_app(app)

    # 创建后台管理模块
    from app.models import Game, Hero, Quotation
    _admin = Admin(app, name=u'后台管理系统', template_mode='bootstrap3')
    _admin.add_view(ModelView(Game, db.session, name=u'游戏'))
    _admin.add_view(ModelView(Hero, db.session, name=u'英雄角色'))
    _admin.add_view(ModelView(Quotation, db.session, name=u'语录'))

    # 注册错误处理模块蓝图
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # 注册主模块蓝图
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # 注册 api 接口模块蓝图
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
