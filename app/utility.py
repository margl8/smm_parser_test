import requests as rq
import datetime as dt
from app.const import TOKEN, VERSION


def clear_link(link: str):
    link = link.strip()
    link = link.split('/')
    return link[-1::]


def vk_send_request(method_name: str, add_params: dict):
    response = rq.get(url=f"https://api.vk.com/method/{method_name}",
                      params={
                                 'access_token': TOKEN,
                                 'v': VERSION
                             } | add_params).json()
    return response['response']


def vk_formalize(posts, id):
    posts_list = []
    for posts in posts:
        x = {'link': f"https://vk.com/wall-{id}_{posts['id']}",
             'date': dt.datetime.fromtimestamp(posts['date']),  # '7': posts['text'],
             'likes': posts['likes']['count'], 'comments': posts['comments']['count'],
             'reposts': posts['reposts']['count'], 'views': posts['views']['count']}
        posts_list.append(x)
    return posts_list

