import csv
import praw
from os import environ
from dotenv import load_dotenv

print("Updating posts and time machine data")

load_dotenv()
reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=environ["ZOKA_TOKEN"],
                     username="Zokalyx",
                     password=environ["ZOKA_PASS"],
                     user_agent="theconfluenceBOT")

pb = []  # List containing all the csv data of posts
pro = open("posts.csv", "r", newline="", encoding="utf-8")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        pb.append(row)
pro.close()

tm = []  # Contains all data of time machine
names = []
pro = open("timemachine.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        tm.append(row)
        names.append(row[0])
pro.close()

newones = []  # Array for new members
pro = open("../basic/probyuser.csv")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        newones.append(row[0])
pro.close()

for person in newones:
    if person not in names:
        tm.append([person, "noposts", 0, "nocomments", 0, ""])
        names.append(person)

last_time = float(pb[-1][1])
aux = []

sub = reddit.subreddit("TheConfluence")
posts = sub.new(limit=200)
for post in posts:
    print(post.title)
    if post.created_utc > last_time:
        aux.append([post.id, post.created_utc, post.title, post.author])

    if post.author.name:
        if post.author.name in names:
            imp_row = tm[names.index(post.author.name)]
            if imp_row[1] == "noposts" or post.created_utc < float(imp_row[2]):
                tm[names.index(post.author.name)][1] = post.id
                tm[names.index(post.author.name)][2] = post.created_utc

    comments = post.comments
    comments.replace_more(limit=None)
    for comment in comments.list():
        if comment.author:
            if comment.author.name in names:
                imp_row = tm[names.index(comment.author.name)]
                if imp_row[3] == "nocomments" or comment.created_utc < float(imp_row[4]):
                    tm[names.index(comment.author.name)][3] = comment.id
                    tm[names.index(comment.author.name)][4] = comment.created_utc
                    tm[names.index(comment.author.name)][5] = post.id

tosave = pb + aux[::-1]
proby = open("posts.csv", "w", newline="", encoding="utf-8")  # Write the data
with proby:
    writer = csv.writer(proby)
    for row in tosave:
        writer.writerow(row)
proby.close()

proby = open("timemachine.csv", "w", newline="")  # Write the data
with proby:
    writer = csv.writer(proby)
    for row in tm:
        writer.writerow(row)
proby.close()

print(tosave)
print(tm)

