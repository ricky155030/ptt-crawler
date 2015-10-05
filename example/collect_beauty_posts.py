#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pttcrawler
import storage


hostname = ''
username = ''
password = ''
dbname = ''
table = ''

database = storage.Storage(hostname, username, password, dbname)

def save_post(post):
    data = {
        'title'  : post.title,
        'author' : post.author,
        'images' : ','.join(post.images),
        'good'   : post.good,
        'bad'    : post.bad,
        'normal' : post.normal,
        'date'   : post.date
    }

    database.insert_update(table, data)

if __name__ == "__main__":
    crawler = pttcrawler.PTTCrawler("Beauty")
    anchor = crawler.get_index_max()
    # parse 10 pages with condition: push > 10
    crawler.get_posts_url(anchor-10, anchor, 10)
    all_posts = crawler.parse_all_posts(author=True, contents=False)

    for post in all_posts:
        if len(post.images) != 0 and post.title.find("公告") == -1:
            save_post(post)
