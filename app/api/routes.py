# -*- coding: utf-8 -*-
"""
    :author: KevinLiao
    :time: 2020/12/17
    :contact: cooltut@hotmail.com
"""
from sqlalchemy import func
from app.api import bp
from app.models import Quotation


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
