# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


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
