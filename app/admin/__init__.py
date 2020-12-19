# -*- coding: utf-8 -*-
"""
    后台管理视图

    :author: KevinLiao
    :time: 2020/12/18
    :contact: cooltut@hotmail.com
"""
from flask import url_for, redirect, request, abort
from flask_admin import AdminIndexView, expose
from flask_admin.contrib import sqla
from flask_security import current_user


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
        return self.render('admin/index.html')


class MyModelView(sqla.ModelView):
    # 不能删除操作
    can_delete = False
    """
    自定义后台管理视图，进行权限控制
    """
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('user')
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


class MySuperUserModelView(sqla.ModelView):
    """
    自定义后台管理视图，进行权限控制
    """
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser')
                )


class UserModelView(MySuperUserModelView):
    # 不显示密码项
    column_exclude_list = ['password', ]


class UserRoleModelView(MySuperUserModelView):
    # 不能删除操作
    can_delete = False
