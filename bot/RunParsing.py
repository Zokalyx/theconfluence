import re
import logging
from typing import Tuple

LOGGER = logging.getLogger(__name__)

def startsWithNumber(line: str) -> bool:
    """
        Returns if some text has an integer in its beginning
    """
    pattern = re.compile("\d+.*")
    return pattern.match(line)


def cycleWhileNumber(lines: list[str], startIndex: int) -> Tuple[list[str], int]:
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
        try:
            saved.append(line.split()[1].replace("\\", ""))
        except IndexError as e:
            LOGGER.error("The following line couldn't be parsed:")
            LOGGER.error(line)

        # TODO: Should this be saved?
        number = int(line.split()[0])

    return saved, index


def parseRun(text: str) -> Tuple[list[str], list[str]]:
    """
        Parses the text corresponding to a Run Post and returns
        a list of usernames corresponding to departures and arrivals
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


    



# Testing
# Function can successfully parse all "non-defective" posts so far.

from praw import Reddit
from os import environ
from dotenv import load_dotenv

load_dotenv()

reddit = Reddit(client_id=environ["ZOKA_ID"],
                client_secret=environ["ZOKA_TOKEN"],
                username="Zokalyx",
                password=environ["ZOKA_PASS"],
                user_agent="theconfluenceBOT")

# Check all correctly formatted posts
redditor = reddit.redditor("theconfluencer")
posts = redditor.submissions.new(limit=1000)
for post in posts:
    # These are the bad posts - most of them are "empty"
    if "run" in post.title.lower() and "85" not in post.title and "84" not in post.title and "80" not in post.title and "delay" not in post.title and "protocol" not in post.title and "[removed]" not in post.selftext and " 8th" not in post.title and "27/4/2020" not in post.title and "sod" not in post.title:
        parseRun(post.selftext)

# Test specific arrivals and departures
post = reddit.submission("sdjs2q")
deps, arrs = parseRun(post.selftext)
print(deps)
print(arrs)