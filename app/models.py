# -*- coding: utf-8 -*-
"""
    数据模型模块

    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from hashlib import md5
from flask_security import RoleMixin, UserMixin
from app import db


class Game(db.Model):
    """
    游戏表
    """
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    heroes = db.relationship('Hero', backref='game_obj', lazy='dynamic')

    def __repr__(self):
        return '<Game {}>'.format(self.name)


class Hero(db.Model):
    """
    英雄角色表
    """
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    quotations = db.relationship('Quotation', backref='hero_obj', lazy='dynamic')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))

    def __repr__(self):
        return '<Hero {}>'.format(self.name)


class Quotation(db.Model):
    """
    英雄角色语录表
    """
    __tablename__ = 'quotations'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    audio_url = db.Column(db.String(200))
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))

    def __repr__(self):
        return '<Quotation {}>'.format(self.content)


# 定义用户-角色多对多关系表
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    """
    用户角色表
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model, UserMixin):
    """
        用户表
        """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def avatar(self, size):
        """
        使用 gravatar 服务展示头像
        :param size: 头像大小
        :return:
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __str__(self):
        return self.email

    def __repr__(self):
        return '<User {}>'.format(self.email)
