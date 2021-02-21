import csv
import praw

with open("../shh.txt", "r") as secret:
    secrets = secret.readlines()
reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=secrets[1],
                     username="Zokalyx",
                     password=secrets[0].strip(),
                     user_agent="theconfluenceBOT")

pb = []  # List containing all the csv data
pro = open("posts.csv", "r", newline="", encoding="utf-8")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        pb.append(row)
pro.close()

last_time = float(pb[-1][1])
aux = []

sub = reddit.subreddit("TheConfluence")
posts = sub.new(limit=None)
for post in posts:
    if post.created_utc <= last_time:
        break
    print(post.title)
    aux.append([post.id, post.created_utc, post.title, post.author])

tosave = pb + aux[::-1]
proby = open("posts.csv", "w", newline="", encoding="utf-8")  # Write the data
with proby:
    writer = csv.writer(proby)
    for row in tosave:
        writer.writerow(row)
proby.close()

