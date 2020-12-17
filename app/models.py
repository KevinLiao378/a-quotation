# -*- coding: utf-8 -*-
"""
    数据模型模块

    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
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
