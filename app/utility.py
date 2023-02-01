import requests as rq
import datetime as dt
import time

import app
from app.const import TOKEN, VERSION


def clear_link(link: str) -> str:
    link = link.strip()
    link = link.split('/')
    return link[-1]


def vk_send_request(method_name: str, add_params: dict):
    response = rq.get(url=f"https://api.vk.com/method/{method_name}",
                      params={
                                 'access_token': TOKEN,
                                 'v': VERSION
                             } | add_params).json()
    if 'response' in response:
        return response['response']
    return response['error']['error_msg']


def vk_formalize(posts):
    posts_list = []
    for posts in posts:
        x = {'link': f"https://vk.com/wall{posts['owner_id']}_{posts['id']}",
             'date': dt.datetime.fromtimestamp(posts['date']),  # '7': posts['text'],
             'likes': posts['likes']['count'], 'comments': posts['comments']['count'],
             'reposts': posts['reposts']['count'], 'views': posts['views']['count']}
        posts_list.append(x)
    return posts_list


def vk_get_from_groups(link_list, period):
    x = link_list.split(',')
    for group in x:
        screen_name = clear_link(group)
        id = app.Group.get_id(screen_name)
        wall = app.Wall(id)
        wall.get_posts_by_date(period)
        x.append(wall.posts)
    y = [vk_formalize(i) for i in x]
    return y
