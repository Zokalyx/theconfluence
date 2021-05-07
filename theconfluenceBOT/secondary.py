import praw
from praw.models import MoreComments
from prawcore.exceptions import Forbidden
import random
import time
import math
from os import environ as env

reddit = praw.Reddit(client_id="0S1WpGMeuyOQkg",
                     client_secret=env["BOT_TOKEN"],
                     username="theconfluenceBOT",
                     password=env["BOT_PASS"],
                     user_agent="The Confluence Bot")
botAccounts = ["AutoModerator"]

def get_amount(amount):
    randoms = []
    count = 0
    reached_count = False
    while not reached_count:
        try:
            res = random_redditor()
        except Forbidden:
            print("403, continuing")
            continue
        if res[0] not in botAccounts:  #and res[0] not in reference_list:
            randoms.append(res)
            count += 1
            print(res[0])
            print(str(round(count / amount * 100)) + "%")
            if count == amount:
                reached_count = True

    return randoms


def random_redditor():
    ran = random.randint(0, 9)
    allow_op = False

    if ran < 8:
        # 80% chance of random subreddit
        sub = reddit.random_subreddit(nsfw=False)
        ran2 = random.randint(0, 1)
        if ran2 == 0:
            posts = sub.hot(limit=10)
        else:
            posts = sub.new(limit=10)

    elif ran == 8:
        # 10% chance of r/popular
        sub = reddit.subreddit("popular")
        posts = sub.new(limit=10)

    else:
        # 10% chance of r/all
        sub = reddit.subreddit("all")
        posts = sub.hot(limit=10)
        ran2 = random.randint(0, 3)
        if ran2 == 0:
            allow_op = True

    post_list = []
    for post in posts:
        post_list.append(post)

    max_post = len(post_list)
    if max_post > 10:
        max_post = 10

    ran = random.randrange(max_post)
    post = post_list[ran]

    if allow_op:
        commenter = post.author
        is_op = True
    else:
        result = get_random_commenter(post)
        commenter = result[0]
        is_op = result[1]

    if commenter:
        return [commenter.name, post.subreddit.display_name, post.id, sub.display_name, is_op]
    else:
        random_redditor()


def get_random_commenter(post):
    com_list = []
    for com in post.comments:
        if isinstance(com, MoreComments) or not com.author:
            continue
        com_list.append(com)

    max_com = len(com_list)
    if max_com > 20:
        max_com = 20

    # Defaults to OP when there are no comments
    if max_com == 0:
        commenter = post.author
        is_op = True
    else:
        ran = random.randrange(max_com)
        commenter = com_list[ran].author
        is_op = False

    return [commenter, is_op]


def obtain_random_text(starting, amount, extra):
    names = get_amount(amount + extra)

    details = False
    text = ""
    for i in range(amount):
        u = names[i]
        text += str(starting + i) + " " + str(u[0])
        if details:
            text += " r/" + str(u[1]) + " [Post](https://redd.it/" + str(u[2]) + ")"
            if u[4]:
                text += " (OP)"
        if u != names[-1]:
            text += "\n\n"

    details = True
    text2 = ""
    for i in range(amount):
        u = names[i]
        text2 += str(starting + i) + " " + str(u[0])
        if details:
            text2 += " r/" + str(u[1]) + " [Post](https://redd.it/" + str(u[2]) + ")"
            if u[4]:
                text2 += " (OP)"
        text2 += "\n\n"

    text2 += "\n\n**Extra random users if you need to add or replace some:**\n\n"

    for i in range(amount, amount + extra):
        u = names[i]
        text2 += str(u[0])
        if details:
            text2 += " r/" + str(u[1]) + " [Post](https://redd.it/" + str(u[2]) + ")"
            if u[4]:
                text2 += " (OP)"
        if u != names[-1]:
            text2 += "\n\n"

    return [text, text2]


we_need = 100
starting = 100
newbs = obtain_random_text(starting, we_need, 10)

print(newbs)
with open("newbs.txt", "w") as n:
    n.write(newbs)