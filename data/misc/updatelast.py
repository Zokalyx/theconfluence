import csv
import praw
from os import environ as env

with open("../broken.txt", "r") as b:
    broken = len(b.read().split("\n"))

w = open("../week.txt", "r")
week = int(w.readline()) # = (Run [1-5]; Run + 1 [6-10]; Run + 2 [11+])
w.close()

p = open("../arrivals/" + str(week) + ".txt", "r") # Get population
for last_line in p:
    pass
p.close()
space = last_line.find(" ")
pop = int(last_line[0:space])
# pop = 162

leaders = []

pro = open("../basic/pro.csv", "r", newline="")
with pro:
    reader = csv.reader(pro)
    for i in range(pop):
        ppl = next(reader)
        leaders.append(ppl[len(ppl)-1])
pro.close()

text = ""
for i in range(len(leaders)):
    text += (str(i+1) + " " + leaders[i])
    if i != len(leaders) - 1:
        text += "\n\n"

print("Updating 'Last' post")

reddit = praw.Reddit(client_id="0S1WpGMeuyOQkg",
                     client_secret=env["BOT_TOKEN"],
                     username="theconfluenceBOT",
                     password=env["BOT_PASS"],
                     user_agent="theconfluenceBOT")
reddit.validate_on_submit = True
profile = reddit.subreddit("U_theconfluenceBOT")

for post in profile.new(limit=10):
    if "Last" in post.title:
        post.delete()
        break

profile.submit("Last (" + str(week - broken) + ")", text)

print("Done")
