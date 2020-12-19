# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/19
    :contact: cooltut@hotmail.com
"""
import os


def init_app(app):
    @app.cli.command("create_su")
    def create_su():
        """
        设置管理员账户
        :return:
        """
        from flask_security.utils import hash_password
        from app.models import User, Role
        admin_email = os.environ.get('admin_email') or None
        admin_password = os.environ.get('admin_password') or None

        su = User.query.filter(User.roles.any(name='superuser')).first()

        # 如果数据库中不存在管理员账户，并且主机设置了管理员账户环境变量，则插入管理员账户
        if su is None and admin_email is not None and admin_password is not None:
            from app import db
            security = app.extensions['security']
            user_role = Role(name='user')
            super_user_role = Role(name='superuser')
            db.session.add(user_role)
            db.session.add(super_user_role)
            db.session.commit()

            su_user = security.datastore.create_user(
                email=admin_email,
                password=hash_password(admin_password),
                roles=[user_role, super_user_role]
            )
            db.session.commit()
            print("success!")
