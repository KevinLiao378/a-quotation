# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from flask import Flask, request, session, url_for
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, helpers as admin_helpers
from flask_babelex import Babel

from app.admin import MyHomeView, MyModelView, UserModelView, UserRoleModelView

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
    from app.models import Game, Hero, Quotation, User, Role

    _admin = Admin(
        app,
        name=u'后台管理系统',
        base_template='admin/my_master.html',
        index_view=MyHomeView(),
        template_mode='bootstrap3'
    )

    _admin.add_view(MyModelView(Game, db.session, name=u'游戏'))
    _admin.add_view(MyModelView(Hero, db.session, name=u'英雄角色'))
    _admin.add_view(MyModelView(Quotation, db.session, name=u'语录'))
    _admin.add_view(UserModelView(User, db.session, name=u'用户管理'))
    _admin.add_view(UserRoleModelView(Role, db.session, name=u'用户角色管理'))

    # 创建权限控制实例
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # 定义一个上下文处理器，用于将 flask-admin 的模板上下文合并到 flask-security 视图。
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=_admin.base_template,
            admin_view=_admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

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
