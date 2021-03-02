import praw
import time
import csv
import math
from pathlib import Path

s = time.time()  # time
smm = s - 2592000  # time minus one month
smm = s - 1296000 # time minus two weeks
smm = s - 1.5*1296000 # time minus three weeks

names = []
bools = []
links = []
times = []
wk = 0
with open("../basic/pro.csv", "r") as pro:
    reader = csv.reader(pro)
    for row in reader:
        if not wk:
            wk = len(row)
        names.append(row[-1])
        bools.append(False)
        links.append("")
        times.append(0)

with open("../shh.txt", "r") as secret:
    secrets = secret.readlines()

reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=secrets[1],
                     username="Zokalyx",
                     password=secrets[0].strip(),
                     user_agent="theconfluenceBOT")

last_run_start = 0
sub = reddit.subreddit("TheConfluence")
runs = sub.hot(limit=5)
posts = sub.new(limit=300)

for run in runs:
    if run.stickied:
        if "Run" in run.title or "Run!" in run.title or "run" in run.title or "run!" in run.title:
            print(run.title)
            last_run_start = run.created_utc
            break
else:
    print("Last run not found!")
    exit(2)

for post in posts:

    if post.created_utc > smm:

        print(post.title)
        print(str(math.trunc(10 * ((s - post.created_utc) / (s - smm) * 100)) / 10) + "%")

        if post.created_utc > last_run_start:
            """
            if post.author == "yo-whatupmofo":
                ind = names.index("Or-Your-Money-Back")
                if not bools[ind]:
                    links[ind] = "reddit.com" + post.permalink
                    times[ind] = (s - post.created_utc)/86400
                bools[ind] = True
            """

            if post.author in names:
                ind = names.index(post.author)
                if not bools[ind]:
                    links[ind] = "reddit.com" + post.permalink
                    times[ind] = (s - post.created_utc)/86400
                bools[ind] = True

        comments = post.comments
        comments.replace_more(limit=None)

        for comment in comments.list():

            if comment.created_utc > last_run_start:

                """
                if comment.author == "yo-whatupmofo":
                    ind = names.index("Or-Your-Money-Back")
                    if not bools[ind]:
                        links[ind] = "reddit.com" + post.permalink
                        times[ind] = (s - post.created_utc) / 86400
                    bools[ind] = True
                """

                if comment.author in names:
                    ind = names.index(comment.author)
                    if not bools[ind]:
                        links[ind] = "reddit.com" + post.permalink + comment.id
                        times[ind] = (s - comment.created_utc)/86400
                    bools[ind] = True

    else:

        break

com = zip(names, bools, links, times)

with open("commented.csv", "w", newline="") as commented:
    writer = csv.writer(commented)
    writer.writerows(com)

with open("../../website/leaderboard/wk.txt", "w") as wek:
    wek.write(str(wk - 1))
