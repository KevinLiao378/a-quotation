# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from flask import request
from sqlalchemy import func
from app.api import bp
from app.models import Quotation
from app.util.wallpaper import get_wallpaper_by_tag


@bp.route('/quotation', methods=['GET'])
def get_a_quotation():
    """
    随机获取一条语录返回
    :return:
    """
    q = Quotation.query.order_by(func.random()).first()
    if q:
        result = {
            'content': q.content,
            'author': q.hero_obj.name,
            'source': q.hero_obj.game_obj.name
        }
        return result
    else:
        return {}


@bp.route('/wallpaper', methods=['GET'])
def get_a_wallpaper():
    tag_name = request.args.get("tag")
    if tag_name:
        return get_wallpaper_by_tag(tag_name)
    else:
        return {}
