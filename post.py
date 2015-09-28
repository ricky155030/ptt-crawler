#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: post.py
Author: hungwei kao
Email: hungwei.kao@gmail.com
Github: https://github.com/ricky155030
Description: Class Post
"""

from datetime import datetime
import pytz

class Post(object):

    def __init__(self, url):
        self.__url = url
        self.__good = 0
        self.__bad = 0
        self.__normal = 0
        self.__images = list()
        self.__title = str()
        self.__messages = list()
        self.__date = datetime(2015, 1, 1, 0, 0, 0).replace(tzinfo=pytz.timezone('Asia/Taipei'))
        self.__contents = str()
        self.__author = str()

    @property
    def images(self):
        return self.__images

    @images.setter
    def images(self, value):
        self.__images = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def messages(self):
        return self.__messages

    @messages.setter
    def messages(self, value):
        self.__messages = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = datetime.strptime(value, "%a %b %d %H:%M:%S %Y").replace(tzinfo=pytz.timezone('Asia/Taipei'))

    @property
    def good(self):
        return self.__good

    @good.setter
    def good(self, value):
        self.__good = value

    @property
    def bad(self):
        return self.__bad

    @bad.setter
    def bad(self, value):
        self.__bad = value

    @property
    def normal(self):
        return self.__normal

    @normal.setter
    def normal(self, value):
        self.__normal = value

    @property
    def all(self):
        return self.normal + self.good + self.bad

    @property
    def score(self):
        return self.good - self.bad

    @property
    def contents(self):
        return self.__contents

    @contents.setter
    def contents(self, value):
        self.__contents = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value
