import praw
from os import environ
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=environ["ZOKA_TOKEN"],
                     username="Zokalyx",
                     password=environ["ZOKA_PASS"],
                     user_agent="theconfluenceBOT")

post = reddit.submission("mgrxct")
title = post.title
text = post.selftext

title_arr = title.split(" ")
week = int(title_arr[1]) + 6
with open("../week.txt", "w") as wk:
    wk.write(str(week))
print(f"week {week}")

text_arr = text.split("\n")
fix_text_arr = []
for i in text_arr:
    if i != "":
        fix_text_arr.append(i)

try:
    first_index = fix_text_arr.index("**Departures:**")
except:
    first_index = fix_text_arr.index("**Departures**")

try:
    second_index = fix_text_arr.index("**Arrivals:**")
except:
    second_index = fix_text_arr.index("**Arrivals**")

for i, el in enumerate(fix_text_arr[second_index+1:]):
    try:
        int(el.split(" ")[0])
    except:
        third_index = second_index + 1 + i
        break

deps = fix_text_arr[first_index + 1:second_index]
arrs = fix_text_arr[second_index + 1:]

deps = [dep.replace("\\", "") for dep in deps]
arrs = [arr.replace("\\", "") for arr in arrs]

with open("../departures/{}.txt".format(week), "w") as departures:
    for dep in deps:
        departures.write(dep)
        if dep != deps[-1]:
            departures.write("\n\n")

with open("../arrivals/{}.txt".format(week), "w") as arrivals:
    for arr in arrs:
        arrivals.write(arr)
        if arr != arrs[-1]:
            arrivals.write("\n\n")





