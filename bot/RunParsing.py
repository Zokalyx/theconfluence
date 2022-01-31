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
        if not startsWithNumber(line):
            break
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

        index += 1

    return saved, index


def parseRun(text: str) -> Tuple[list[str], list[str]]:
    """
        Parses the text corresponding to a Run Post and returns
        a list of usernames corresponding to departures and arrivals
    """

    lines = [line.strip() for line in text.split("\n\n")]

    index = lines.index("**Departures**") + 1

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

from praw import Reddit
from os import environ
from dotenv import load_dotenv

load_dotenv()

reddit = Reddit(client_id=environ["ZOKA_ID"],
                client_secret=environ["ZOKA_TOKEN"],
                username="Zokalyx",
                password=environ["ZOKA_PASS"],
                user_agent="theconfluenceBOT")

post = reddit.submission("s8546z")

deps, arrs = parseRun(post.selftext)

print("DEPARTURES")
print(deps)
print("\nARRIVALS")
print(arrs)