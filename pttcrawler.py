#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import pytz
import requests
sys.path.append('/home/hungwei/project/ptt-beauty-img-retriever/')
import storage
import logging
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Disable module logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

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

<<<<<<< HEAD

=======
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


class PTTCrawler(object):
>>>>>>> 893977686f50835d4dd39f2331e09699c5265199
    def __init__(self, board_name):
        self.board_name = board_name

    def get_posts_url(self, start, end, score, include_newest=True):
        self.post_urls = list()

        # Get url from index start to end
        for index in range(start, end+1):
            resp = requests.get(
                url="http://www.ptt.cc/bbs/{}/index{}.html".format(self.board_name, index),
                cookies={"over18": "1"}
            )
            soup = BeautifulSoup(resp.text)
            for tag in soup.find_all("div", "r-ent"):
                try:
                    flag = tag.find('span', class_='hl').text.replace('爆', '100')
                    if int(flag) >= score:
                        # print("{} {}".format(tag.find('span', class_='hl').text, tag.find('a').text))
                        # ex: M.1432098950.A.EC7.html
                        postfix = tag.find('a').attrs.get('href').split('/')
                        self.post_urls.append(postfix[3])
                except AttributeError:
                    # Some post may not have flag text (ex: deleted post)
                    pass
                except ValueError:
                    # Some flag fail at int conversion (ex: X1, XX)
                    pass

        # Get url from newest index
        if include_newest:
            resp = requests.get(
                url='http://www.ptt.cc/bbs/{}/index.html'.
                    format(self.board_name),
                cookies={'over18': '1'}
            )
            soup = BeautifulSoup(resp.text)
            for tag in soup.find('div', 'r-list-container').children:
                try:
                    # As read r-list-sep (fix buttom posts) then break
                    if tag.attrs.get('class')[0] == 'r-list-sep':
                        break
                    else:
                        flag = tag.find('span', class_='hl').text.replace('爆', '100')
                        if int(flag) >= score:
                            # print("{} {}".format(tag.find('span', class_='hl').text, tag.find('a').text))
                            postfix = tag.find('a').attrs.get('href').split('/')
                            self.post_urls.append(postfix[3])
                except:
                    pass

        return self.post_urls

    def _get_soup(self, link):
        resp = requests.get(url=link, cookies={"over18": "1"})
        return BeautifulSoup(resp.text)

    def parse_all_posts(self, author=True, title=True, date=True, contents=True, messages=True,
                        reply=True, images=True, ip=False):
        try:
            if self.post_urls is None:
                raise Exception("You must run get_posts_url first")
        except Exception as err:
            print(err)
            sys.exit(1)

        post_objects = list()
        for url in self.post_urls:
            soup = self._get_soup("http://www.ptt.cc/bbs/{}/{}".format(self.board_name, url))
            post = Post(url)

            try:
                article_meta = soup.find_all('span', class_="article-meta-value")
                if author:
                    post.author = article_meta[0].contents[0]

                if title:
                    post.title = article_meta[2].contents[0]

                if date:
                    post.date = article_meta[3].contents[0]

                # TODO: ip
                if ip:
                    pass

                if contents:
                    a = str(soup.find(id="main-container").contents[1])
                    a = a.split("</div>")
                    a = a[4].split("<span class=\"f2\">※ 發信站: 批踢踢實業坊(ptt.cc),")
                    post.contents = a[0].replace(' ', '').replace('\n', '').replace('\t', '')

                if images:
                    a = soup.find_all('img')
                    imgs = list()
                    for i in a:
                        imgs.append(i.attrs.get('src'))
                    post.images = imgs

                # TODO: There are some push_content lost due to hyperlink in the content
                if messages or reply:
                    # messages = list()
                    for tag in soup.find_all("div", "push"):
                        # d = dict()
                        push_tag = tag.find("span", "push-tag").\
                            string.replace(' ', '')

                        # d.setdefault('狀態', push_tag)
                        # d.setdefault('留言者', push_userid)
                        # d.setdefault('留言內容', push_content)
                        # d.setdefault('留言時間', push_ipdatetime)

                        # messages.append(d)

                        if push_tag == '推':
                            post.good += 1
                        elif push_tag == '噓':
                            post.bad += 1
                        else:
                            post.normal += 1

                    # post.messages = messages
            except:
                pass

            post_objects.append(post)

        return post_objects

    def get_index_max(self):
        resp = requests.get(
            url="http://www.ptt.cc/bbs/{}/index.html".format(self.board_name),
            cookies={"over18": "1"}
        )
        soup = BeautifulSoup(resp.text)
        for tag in soup.find_all("a", "wide"):
            if tag.contents[0] == '‹ 上頁':
                return int(re.findall('index(.*?).html', tag.attrs.get('href'))[0])

    def save_post(self, post):
        db = storage.Storage()
        data = {
            'title'  : post.title,
            'author' : post.author,
            'images' : ','.join(post.images),
            'good'   : post.good,
            'bad'    : post.bad,
            'normal' : post.normal,
            'date'   : post.date
        }

        db.insert_update('posts', data)

if __name__ == "__main__":
    # Test: Run this program directly
    #       Show posts (score > 10) of first page in beauty board
    p = PTTCrawler("Beauty")
    anchor = p.get_index_max()
    p.get_posts_url(anchor-30, anchor, 10)
    all_posts = p.parse_all_posts(author=True, contents=False)

    for i in all_posts:
        p.save_post(i)
        # print("%3s %10s %s %s" % (i.score, i.date, i.title, i.images))
