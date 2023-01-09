#!/usr/bin/python3
# -*- coding: utf-8 -*-

from app import utility as ut
import time


class Group:
    group_id: int
    screen_name: str
    name: str
    members_count: [int, str]
    members: list

    def __init__(self, group_id: int):
        self.group_id = group_id
        response = ut.vk_send_request('groups.getById', {
            'group_id': self.group_id,
            'fields': 'members_count'
        })
        print(response)
        response = response[0]
        self.screen_name = response['screen_name']
        self.name = response['name']
        if 'members_count' in response:
            self.members_count = response['members_count']
        else:
            self.members_count = 'no access to members'
        self.members = []

    def __str__(self):
        return f'Name: {self.name}\n' \
               f'ID: {self.group_id}\n'\
               f'Short adress: {self.screen_name}\n' \
               f'Members count: {self.members_count}'

    def __repr__(self):
        return (f'"group_id": {self.group_id}, '
                f'"name": "{self.name}", '
                f'"screen_name": "{self.screen_name}", '
                f'"members_count": {self.members_count}')

    def __call__(self, *args, **kwargs):
        return self.group_id

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    @staticmethod
    def get_id(screen_name: str):
        group_id = ut.vk_send_request(method_name='utils.resolveScreenName', add_params={
            'screen_name': screen_name
        })
        return group_id['object_id']

    def get_members(self, get_all: bool = True, count: int = 1000, offset: int = 0):
        if self.members_count is str:
            return self.members_count
        while self.members_count != len(self.members):
            try:
                ids = ut.vk_send_request(method_name='groups.getMembers',
                                         add_params={'group_id': self.group_id,
                                                     'offset': offset,
                                                     'count': count
                                                     })['items']
                offset += count
                self.members.extend(ids)
            except KeyError:
                time.sleep(0.5)
        return self.members


class Wall:
    owner_id: int
    posts: list

    def __init__(self, owner_id):
        owner_id: [Group, int]
        if type(owner_id) is Group:
            self.owner_id = Group.__getattribute__(owner_id, Group.group_id)
        self.owner_id = owner_id
        self.posts = []

    def __call__(self, *args, **kwargs):
        return self.owner_id

    def __str__(self):
        return f'Owner id: {self.owner_id}\n' \
               f'Posts per year: {len(self.posts)}'

    def __repr__(self):
        pass

    def get_posts_by_amount(self, count: int = 20, offset: int = 0):

        posts = []
        while count != len(posts):
            posts = ut.vk_send_request('wall.get', {'owner_id': -self.owner_id,
                                                    'count': count,
                                                    'offset': offset
                                                    })['items']
        return ut.vk_formalize(posts, self.owner_id)

    def get_posts_by_date(self, period: tuple):
        count = 100
        offset = 0
        start_date = time.mktime(min(period).timetuple())
        end_date = time.mktime(max(period).timetuple())
        min_date = start_date + 1
        raw_posts = []
        while min_date > start_date:
            try:
                posts = ut.vk_send_request('wall.get', {'owner_id': -self.owner_id,
                                                        'count': count,
                                                        'offset': offset
                                                        })['items']
                timestamps = [post['date'] for post in posts if not ('is_pinned' in post)]
                min_date = min(timestamps)
                raw_posts.extend(posts)
                offset += count
            except KeyError:
                time.sleep(0.5)
        self.posts = [post for post in raw_posts
                      if start_date < post['date'] < end_date]
