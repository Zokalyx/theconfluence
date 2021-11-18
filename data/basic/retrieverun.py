import praw
import re

with open("../shh.txt", "r") as secret:
    secrets = secret.readlines()

reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                     client_secret=secrets[1],
                     username="Zokalyx",
                     password=secrets[0].strip(),
                     user_agent="theconfluenceBOT")

sub = reddit.subreddit("TheConfluence")
runs = sub.hot(limit=5)
for run in runs:
    if run.stickied:
        if "Run" in run.title or "Run!" in run.title or "run" in run.title or "run!" in run.title:
            title = run.title
            text = run.selftext
            break
else:
    print("Last run not found!")
    exit(2)

print(title)

title_arr = title.split(" ")
week = int(title_arr[1][0:-2]) + 6
with open("../week.txt", "w") as wk:
    wk.write(str(week))
print(f"week {week}")

text_arr = text.split("\n")
fix_text_arr = []
for i in text_arr:
    if i != "":
        fix_text_arr.append(i)


def find_word(arr, word):
    p = re.compile(r"\w*\*\*" + word + ":*" + r"\*\*\w*", re.IGNORECASE)
    for a in arr:
        if p.search(a):
            print(a)
            return arr.index(a)


first_index = find_word(fix_text_arr, "Departures")

second_index = find_word(fix_text_arr, "Arrivals")

for i, el in enumerate(fix_text_arr[second_index+1:]):
    try:
        int(el.split(" ")[0])
    except:
        print(i, el)
        third_index = second_index + 1 + i
        break

deps = fix_text_arr[first_index + 1:second_index]
arrs = fix_text_arr[second_index + 1:third_index]

print(first_index, second_index, third_index)

deps = [dep.replace("\\", "").strip() for dep in deps]
arrs = [arr.replace("\\", "").strip() for arr in arrs]

print(deps)
print(arrs)

arr_num = int(arrs[0].split()[0]) - 1
print(f"\nInsert users manually - currently, first user in arrivals is {arrs[0]}:\n")
username = input(f"{arr_num}: ")
while username:
    arrs.insert(0, [arr_num, username])
    arr_num -= 1

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





