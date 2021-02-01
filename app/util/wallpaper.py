# -*- coding: utf-8 -*-
"""
    在线壁纸API，详见https://wallhaven.cc/help/api
    :author: KevinLiao
    :time: 2021/02/01
    :contact: cooltut@hotmail.com
"""
import urllib.request
import json
import random
from xeger import Xeger

HOST = "https://wallhaven.cc/api/v1/search"


def get_wallpaper_by_tag(tag_name):
    """
    根据类别获取随机壁纸
    :param tag_name: 类别，如 dota2
    :return: 随机一张壁纸
    """
    # 随机种子
    seed = Xeger().xeger(r'[a-zA-Z0-9]{6}')
    # 拼接请求Url及参数
    url = "{}?q={}&sorting=random&seed={}".format(HOST, tag_name, seed)
    # 发起请求
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.141 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    res_body = response.read()
    # json解析结果
    content = json.loads(res_body.decode('utf-8'))
    # 取出结果列表
    wallpaper_list = content['data']

    result_one = None
    if wallpaper_list:
        # 从列表中随机取一个
        length = len(wallpaper_list)
        pos = random.randint(1, length)
        result_one = wallpaper_list[pos]
    return result_one
