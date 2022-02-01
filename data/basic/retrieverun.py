import praw
import re
from os import environ
from dotenv import load_dotenv
import logging
from typing import Tuple

LOGGER = logging.getLogger(__name__)

def startsWithNumber(line: str) -> bool:
    """
        Returns if some text has an integer in its beginning
    """
    pattern = re.compile("\d+.*")
    return pattern.match(line)


def cycleWhileNumber(lines: list[str], startIndex: int) -> Tuple[list[Tuple[int, str]], int]:
    """
        Returns a list of consecutive lines that contain a number at
        the beginning, starting from the specified index

        Also returns the end index
    """
    saved = []
    index = startIndex
    maxIndex = len(lines)

    while index < maxIndex:
        line = lines[index]
        # Ignore empty lines
        if line == "":
            index += 1
            continue
        # Stop when line does not start with a number
        if not startsWithNumber(line):
            break
        index += 1
        # Save second word (1st is number, 2nd is name, 3rd might be something random)
        # EG: 36 luri7555 cake
        # Also, underscores are always prefixed by a backslash, replace them
        number = int(line.split()[0])
        try:
            username = line.split()[1].replace("\\", "")
        except IndexError as e:
            LOGGER.error(f"The following line couldn't be parsed:\n{line}")

        saved.append((number, username))

    return saved, index


def parseRun(text: str) -> Tuple[list[Tuple[int, str]], list[Tuple[int, str]]]:
    """
        Parses the text corresponding to a Run Post and returns
        a list of usernames and their flair numbers corresponding
        to departures and arrivals
    """

    lines = [line.strip() for line in text.split("\n")]

    # Find "departures" line
    pattern = re.compile("\**departures:?\**", re.IGNORECASE)
    index = -1
    for i, line in enumerate(lines):
        if pattern.match(line):
            index = i + 1
            break

    # Error checking
    if index == -1:
        raise Exception("Post couldn't be parsed")

    # Save departures
    departures, index = cycleWhileNumber(lines, index)

    # Save arrivals
    index += 1
    arrivals, index = cycleWhileNumber(lines, index)

    return departures, arrivals


load_dotenv()

reddit = praw.Reddit(client_id=environ["ZOKA_ID"],
                     client_secret=environ["ZOKA_TOKEN"],
                     username="Zokalyx",
                     password=environ["ZOKA_PASS"],
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
week = int(title_arr[1][0:-2]) + 7
with open("../week.txt", "w") as wk:
    wk.write(str(week))
print(f"week {week}")

deps, arrs = parseRun(text)

print(deps)
print(arrs)

arr_num = arrs[0][0] - 1
print(f"\nInsert users manually - currently, first user in arrivals is {arrs[0]}:\n")
username = input(f"{arr_num}: ")
while username:
    arrs.insert(0, (arr_num, username))
    arr_num -= 1

with open("../departures/{}.txt".format(week), "w") as departures:
    for dep in deps:
        departures.write(f"{dep[0]} {dep[1]}")
        if dep != deps[-1]:
            departures.write("\n\n")

with open("../arrivals/{}.txt".format(week), "w") as arrivals:
    for arr in arrs:
        arrivals.write(f"{arr[0]} {arr[1]}")
        if arr != arrs[-1]:
            arrivals.write("\n\n")





