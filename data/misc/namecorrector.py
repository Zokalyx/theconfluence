import csv
import praw

with open("../shh.txt", "r") as secret:
    secrets = secret.readlines()
reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=secrets[1],
                     username="Zokalyx",
                     password=secrets[0].strip(),
                     user_agent="theconfluenceBOT")

names = []
pro = open("../basic/probyuser.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for row in reader:
        names.append(row[0])
pro.close()

print(names)

for name in names:
    try:
        user = reddit.redditor(name)
        user.id
        if name != user.name:
            print(name + " vs " + user.name + " in Reddit")
    except:
        print("404 for user " + name)
