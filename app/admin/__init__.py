# -*- coding: utf-8 -*-
"""
    后台管理视图

    :author: KevinLiao
    :time: 2020/12/18
    :contact: cooltut@hotmail.com
"""
import pyexcel
from flask import url_for, redirect, request, abort, flash
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib import sqla
from flask_security import current_user
import flask_excel as excel


class MyHomeView(AdminIndexView):
    """
        自定义后台管理主页视图，进行权限控制
        """

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
                )

    def _handle_view(self, name, **kwargs):
        """
        重写内置 _handle_view，以便重定向到登录页。
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # 无权访问
                abort(403)
            else:
                # 重定向到登录页
                return redirect(url_for('security.login', next=request.url))

    @expose('/')
    def index(self):
        from app.models import Game
        options = []
        games = Game.query.all()
        if games:
            for game in games:
                options.append(game.name)
        return self.render('admin/index.html', options=options)


class DataManageView(BaseView):
    """
    数据导入、导出管理
    """

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
                )

    def _handle_view(self, name, **kwargs):
        """
        重写内置 _handle_view，以便重定向到登录页。
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # 无权访问
                abort(403)
            else:
                # 重定向到登录页
                return redirect(url_for('security.login', next=request.url))

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if request.method == 'POST':
            from app.models import Game, Hero, Quotation
            from app import db

            def hero_init_func(row):
                select_game_name = request.form.get('game_select')
                g = Game.query.filter_by(name=select_game_name).first()
                hero = Hero(name=row['name'], game_id=g.id)
                return hero

            def quotation_init_func(row):
                hero = Hero.query.filter_by(name=row['hero_name']).first()
                quotation = Quotation(content=row['content'], audio_url=row['audio_url'], hero_id=hero.id)
                return quotation

            request.save_book_to_database(
                field_name='file', session=db.session,
                tables=[Hero, Quotation],
                initializers=[hero_init_func, quotation_init_func]
            )
            flash("导入成功！", 'success')
            return redirect(url_for('manage.index'))
        else:
            from app.models import Game
            options = []
            games = Game.query.all()
            if games:
                for game in games:
                    options.append(game.name)
            return self.render('admin/manage.html', options=options)

    @expose('/export')
    def export(self):
        """
        Excel 模板下载
        :return:
        """
        excel_data = {
            'heroes': [
                ['name']
            ],
            'quotations': [
                ['content', 'audio_url', 'hero_name']
            ]
        }
        book = pyexcel.get_book(bookdict=excel_data)
        return excel.make_response(book, file_type='xls',
                                   file_name='data_template')


class MySuperUserModelView(sqla.ModelView):
    """
    自定义后台管理视图，进行权限控制
    """
    # 可以创建
    can_create = True
    # 可以编辑
    can_edit = True
    # 可以删除
    can_delete = True
    # 可以导出
    can_export = True
    # 显示查看详情视图
    can_view_details = True
    # 弹出框形式展示创建功能
    create_modal = True
    # 弹出框形式展示编辑功能
    edit_modal = True

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
                )

    def _handle_view(self, name, **kwargs):
        """
        重写内置 _handle_view，以便重定向到登录页。
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # 无权访问
                abort(403)
            else:
                # 重定向到登录页
                return redirect(url_for('security.login', next=request.url))


class UserModelView(MySuperUserModelView):
    # 不显示密码项
    column_exclude_list = ['password', ]
