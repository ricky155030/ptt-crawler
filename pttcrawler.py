import re
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup
from post import Post

class PTTCrawler(object):

    def __init__(self, board_name):
        self.board_name = board_name

    def get_posts_url(self, start, end):
        self.post_urls = list()

        for index in range(start, end+1):
            resp = requests.get(
                url="http://www.ptt.cc/bbs/{}/index{}.html".format(self.board_name, index),
                cookies={"over18": "1"}
            )
            soup = BeautifulSoup(resp.text)
            for tag in soup.find_all("div", "r-ent"):
                try:
                    postfix = tag.find('a').attrs.get('href').split('/')
                    ### ex: M.1432098950.A.EC7.html
                    self.post_urls.append(postfix[3])
                except:
                    pass

        return self.post_urls

    def _get_soup(self, link):
        resp = requests.get(url=link, cookies={"over18": "1"})
        return BeautifulSoup(resp.text)

    def parse_all_posts(self, author=True, title=True, date=True, contents=True, messages=True, reply=True, images=True):
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

                # ip
                # try:
                #     ip = soup.find(text=re.compile("※ 發信站:"))
                #     ip = re.search("[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*",str(ip)).group()
                # except:
                #     ip = "ip is not find"

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

                ### TODO: repair push_*** may be None value
                if messages or reply:
                    messages = list()
                    for tag in soup.find_all("div","push"):
                        d = dict()
                        push_tag = tag.find("span","push-tag").string.replace(' ', '')
                        push_userid = tag.find("span","push-userid").string.replace(' ', '')
                        push_content = tag.find("span","push-content").string.replace(' ', '').replace('\n', '').replace('\t', '')
                        push_ipdatetime = tag.find("span","push-ipdatetime").string.replace('\n', '')

                        d.setdefault('狀態', push_tag)
                        d.setdefault('留言者', push_userid)
                        d.setdefault('留言內容', push_content)
                        d.setdefault('留言時間', push_ipdatetime)

                        messages.append(d)

                        if push_tag == '推':
                            post.good += 1
                        elif push_tag == '噓':
                            post.bad += 1
                        else:
                            post.normal += 1
            except:
                ### There are some fields missing in the html
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
                return int(re.findall('index(.*?).html',tag.attrs.get('href'))[0])

if __name__ == "__main__":
    p = PTTCrawler("Beauty")
    anchor = p.get_index_max()
    p.get_posts_url(anchor-5, anchor)
    all_posts = p.parse_all_posts(author=False, contents=False)

    for i in all_posts:
        if i.score > 20:
            print("%3s %10s %s" % (i.score, i.date, i.title))
