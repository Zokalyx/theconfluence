import csv
import praw

with open("../shh.txt", "r") as secret:
    secrets = secret.readlines()
reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=secrets[1],
                     username="Zokalyx",
                     password=secrets[0].strip(),
                     user_agent="theconfluenceBOT")

posts = []  # List containing all the post data (important = id)
lol = open("posts.csv", "r", newline="", encoding="utf-8")
with lol:
    reader = csv.reader(lol)
    for row in reader:
        posts.append(row)

pb = []  # List containing all the csv data
names = []
pro = open("../basic/probyuser.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        #         [ NAME ,   POSTID , POSTIME, COMMENTID, COMMENTTIME, COMMENTPOSTID]
        pb.append([row[0], "noposts",    0,   "nocomments",    0,           ""])
        names.append(row[0])
pro.close()

for post in posts:
    actual_post = reddit.submission(post[0])
    print(actual_post.title)
    print((actual_post.created_utc - 1583809200) / 604800 / 50 * 100)
    if actual_post.author.name:
        if actual_post.author.name in names:
            imp_row = pb[names.index(actual_post.author.name)]
            if imp_row[1] == "noposts" or actual_post.created_utc < imp_row[2]:
                pb[names.index(actual_post.author.name)][1] = actual_post.id
                pb[names.index(actual_post.author.name)][2] = actual_post.created_utc

    comments = actual_post.comments
    comments.replace_more(limit=None)
    for comment in comments.list():
        if comment.author:
            if comment.author.name in names:
                imp_row = pb[names.index(comment.author.name)]
                if imp_row[3] == "nocomments" or comment.created_utc < imp_row[4]:
                    pb[names.index(comment.author.name)][3] = comment.id
                    pb[names.index(comment.author.name)][4] = comment.created_utc
                    pb[names.index(comment.author.name)][5] = actual_post.id

print(pb)

proby = open("timemachine.csv", "w", newline="", encoding="utf-8")  # Write the data
with proby:
    writer = csv.writer(proby)
    for row in pb:
        writer.writerow(row)
proby.close()
