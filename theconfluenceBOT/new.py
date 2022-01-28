import sys
import praw
from praw.models import MoreComments

import random
import time
import math
from datetime import datetime
from os import environ as env

BLACKLIST = [
    "AutoModerator"
]
WHITELIST = [
    "Zokalyx",
    "MoscaMye",
    "theconfluencer"
]
EXTRA_RANDOMS = 10

DEBUG = False


def main():

    # Login to BOT's account
    try:
        reddit = login_as("theconfluenceBOT")
        print("Logged in as theconfluenceBOT!")
    except Exception as e:
        print(e)
        # This prevents the script to call reddit.inbox.unread(limit=1) because reddit is undefined
        sys.exit("Bot couldn't Login. Terminate Script")

    while True:
        # Read inbox and filter
        for unread in reddit.inbox.unread(limit=1):
            author = unread.author
            unread.mark_read()

            # Filter
            if author.name not in WHITELIST:
                break

            # Send first message
            print("Sending 1st Message to", author.name)
            if not DEBUG:
                author.message("Working on it", "Message received, I'm processing the data. I'll message you again once I'm done!")
            status_text = ""

            # Calculate departures
            try:
                summary_dep, detailed_dep, retention, newrun, starting, arrs, r_list = departures()
            except Exception as e:
                print(e.with_traceback())
                summary_dep = "There was an error getting departures.\n"
                detailed_dep = "There was an error getting departures.\n"
                retention = "?"
                newrun = "?"
                starting = 0
                arrs = 100
                r_list = []
                status_text += "There was an issue getting departures :(\n"

            # Calculate arrivals
            try:
                summary_arr, detailed_arr = arrivals(reddit, starting, arrs, r_list)
            except Exception as e:
                print(e)
                summary_arr = "There was an error getting arrivals.\n\n"
                detailed_arr = "There was an error getting arrivals.\n\n"
                if status_text == "":
                    status_text += "There was an issue getting arrivals :(\n"
                else:
                    print("Sending total failure message to", author.name)
                    if not DEBUG:
                        author.message("Oops...", "There was some problem and I couldn't get departures or arrivals. Sorry!")
                    break

            # Create summary text
            summary = "**Departures:**\n\n" + summary_dep + "**Arrivals:**\n\n" + summary_arr

            # Only proceed if DEBUG is disabled
            if DEBUG:
                print("DEBUG mode is on, will not post - printing summary instead:")
                print(summary)
                break

            # Post results
            print("Posting results")
            try:
                post_results(reddit, newrun, retention, summary, detailed_arr, detailed_dep)
            except Exception:
                status_text += "There was an error posting results, so here's the results:\n" + summary

            # Send final status
            status_text += "Results are posted in my profile. See you next time :)"
            print("Sending final status to", author.name)
            print(status_text)
            author.message("Results ready", status_text)


def departures():
    """
    Calculates departures by comparing times of comments and posts to the previous
    (stickied) run post. Also calculates retention and the new run number.
    See https://i.imgur.com/P3BTMKJ.jpeg for a visual description of the process.
    """

    print("Getting departures...")

    # Log in with Zokalyx's account
    try:
        reddit = login_as("Zokalyx")
        print("Logged in as Zokalyx!")
    except Exception as e:
        print(e)
        # Prevents the use of an undefined reddit object
        sys.exit("Zokalyx login in departures failed.")

    # Get departures
    ref_list, departures, remaining, lastrun, lastpop = get_departures(reddit)

    # Get texts
    summary = get_departures_text(departures)
    detailed = get_new_flairs_text(remaining)

    # Calculate data
    newrun = str(int(lastrun) + 1)
    retention = str(round(len(remaining) / lastpop * 10000) / 100)
    starting = len(remaining) + 1
    arrs = 200 - starting + 1

    print()
    print("New Run:", newrun)
    print("Retention:", retention)
    print("Remaining Users:", starting - 1)
    print()

    return summary, detailed, retention, newrun, starting, arrs, ref_list


def get_departures(reddit):
    """
    Returns a list of departures
    """

    # Get times
    s = time.time()  # Current time
    smm = s - 1.5 * 1296000  # Current time minus three weeks

    # Find last run post
    sub = reddit.subreddit("TheConfluence")
    runs = sub.hot(limit=5)
    for run in runs:
        if run.stickied:
            if "Run" in run.title or "Run!" in run.title or "run" in run.title or "run!" in run.title:
                print(run.title)
                last_run_start = run.created_utc
                print("Comparing against:", datetime.utcfromtimestamp(last_run_start).strftime('%Y-%m-%d %H:%M:%S'))

                # Parse title
                string = run.title
                string_arr = string.split()

                if "Run" in string_arr:
                    index = string_arr.index("Run") - 1
                elif "Run!" in string_arr:
                    index = string_arr.index("Run!") - 1
                elif "run" in string_arr:
                    index = string_arr.index("run") - 1
                elif "run!" in string_arr:
                    index = string_arr.index("run!") - 1
                
                lastrun_sub = string_arr[index][:len(string_arr[index]) - 2]

                break

    # Find LAST post
    bot_profile = reddit.subreddit("U_theconfluenceBOT")
    newest = bot_profile.new(limit=10)
    for post in newest:
        if "Last" in post.title:
            lastrun_bot = post.title.split("(")[1].split(")")[0]
            auxlastrundata = post.selftext.split("\n\n")
            lastrundata = []
            lastruncopy = []
            for entry in auxlastrundata:
                lastrundata.append([entry.split()[0], entry.split()[1]])
                lastruncopy.append([entry.split()[0], entry.split()[1]])
            lastpop = len(lastrundata)

    # Check if runs are the same
    if lastrun_sub != lastrun_bot:
        raise Exception("There is a mismatch between run numbers")

    # Process posts
    departures = []  # Contains numbers and a boolean
    reference_list = []  # Contains names
    for row in lastrundata:
        reference_list.append(row[1])
        departures.append([row[0], True])

    posts = sub.new(limit=500)
    for post in posts:

        # Stop after having gone over 3 weeks
        if post.created_utc < smm:
            break

        # Log
        print(post.title, str(math.trunc(10 * ((s - post.created_utc) / (s - smm) * 100)) / 10), "%")

        # Remove author from departures if it was posted after the last run post
        if post.created_utc > last_run_start:
            if post.author in reference_list:
                ind = reference_list.index(post.author)
                departures[ind][1] = False

        comments = post.comments
        comments.replace_more(limit=None)

        # Remove author from departures if it was posted after the last run post
        for comment in comments.list():
            if comment.created_utc > last_run_start:
                if comment.author in reference_list:
                    ind = reference_list.index(comment.author)
                    departures[ind][1] = False

    # Logic
    for n in reversed(departures):
        if n[1]:
            lastrundata.pop(int(n[0]) - 1)  # Keeps the remaining users
        else:
            lastruncopy.pop(int(n[0]) - 1)  # Keeps the departing users

    return reference_list, lastruncopy, lastrundata, lastrun_sub, lastpop


def get_new_flairs_text(remaining):
    """
    Returns text containing new flairs for old users
    """
    text = ""
    for user in remaining:
        old_number = int(user[0])
        new_number = remaining.index(user) + 1
        diff = old_number - new_number
        text += f"{old_number} → {new_number} {user[1]}"
        if diff == 0:
            text += " (=)"
        else:
            text += f" (-{diff})"
        text += "\n\n"
    return text


def get_departures_text(departures):
    """
    Returns text containing departing users
    """
    text = ""
    for user in departures:
        text += f"{user[0]} {user[1]}\n\n"
    return text
     

def arrivals(reddit, starting, amount, current_members):
    """
    Returns formatted text of random redditors that are selected algorithmically.
    See https://i.imgur.com/lWHrfAN.jpeg for a visual description of the process.
    """

    print("Getting arrivals...")
    randoms = get_randoms(reddit, amount, current_members)
    extras = get_randoms(reddit, 10, current_members)

    summary = get_arrivals_text(randoms, starting, False)
    detailed = get_arrivals_text(randoms, starting, True, extras)

    return summary, detailed


def get_arrivals_text(randoms, starting, with_detail, extras=None):
    """
    Returns formatted text of random redditors
    """

    text = ""
    for i, rand in enumerate(randoms):
        if with_detail:
            if starting:
                text += f"{starting + i} "
            text += f"{rand['name']} r/{rand['sub']} [Post](https://redd.it/{rand['post-id']})"
            if rand["is-OP"]:
                text += " (OP)"
        else:
            if starting:
                text += f"{starting + i} "
            text += f"{rand['name']}"
        text += "\n\n"

    if with_detail:
        text += "**Extra rand users if you need to add or replace some:**\n\n"
        for i, rand in enumerate(extras):
            text += f"{rand['name']} r/{rand['sub']} [Post](https://redd.it/{rand['post-id']})"
            if rand["is-OP"]:
                text += " (OP)"
            text += "\n\n"

    return text


def get_randoms(reddit, amount, current_members):
    """
    Returns a list of random redditors
    """

    count = 0
    randoms = []

    while count < amount:

        # Get redditor
        try:
            redditor = get_random_redditor(reddit, current_members)
        except Exception as e:
            print(e)
            continue

        # Add
        randoms.append(redditor)
        count += 1
        print(redditor["name"], str(round(count / amount * 100)), "%")

    return randoms


def get_random_redditor(reddit, current_members):
    """
    Returns a random, filtered redditor following the algorithm.
    """

    # Random posts from which to choose
    try:
        sub_name, posts = get_random_posts(reddit)
    except Exception as e:
        raise e

    # If sub is r/all, 25% chance of directly adding OP
    if sub_name == "all":
        rand = random.randint(0, 3)
        allow_OP = rand == 0
    else:
        allow_OP = False

    # Convert to list to know length of it (might not be 10)
    posts = list(posts)

    # Continue if no posts to pick from
    if len(posts) == 0:
        raise Exception("No posts in sub")

    # Pick random post
    post = random.choice(posts)

    # Pick commenter, or OP
    if allow_OP:
        redditor = post.author
        is_OP = True
    else:
        redditor, is_OP = get_random_commenter(post)

    # Filter
    if not redditor:
        raise Exception("Redditor account deleted (probably)")
    if redditor.name in BLACKLIST or redditor.name in current_members:
        raise Exception("Redditor in blacklist or already in the confluence")

    return {
        "name": redditor.name,
        "sub": post.subreddit.display_name,
        "post-id": post.id,
        "origin": sub_name,
        "is-OP": is_OP
    }


def get_random_commenter(post):
    """
    Gets an random commenter from a post
    """

    # Get comment list
    comment_list = []
    for comment in post.comments:
        # Only look for valid comments (user not deleted, or actual comment)
        if isinstance(comment, MoreComments) or not comment.author:
            continue
        comment_list.append(comment)

    # Only look for first 20 comments
    max_com = len(comment_list)
    if max_com > 20:
        max_com = 20

    # Default to OP if there are no comments
    if max_com == 0:
        return post.author, True
    # Otherwise pick random comment
    return random.choice(comment_list[0:max_com]).author, False


def get_random_posts(reddit):
    """
    Returns a random subreddit according to the algorithm
    """

    sub = None
    rand = random.randint(0, 9)
    
    # 80% chance of random subreddit
    if rand < 8:
        sub = reddit.random_subreddit(nsfw=False)
    # 10% chance of r/popular
    elif rand < 9:
        sub = reddit.subreddit("popular")
    # 10% chance of r/all
    elif rand < 10:
        sub = reddit.subreddit("all")

    if sub is not None:
        hot_or_new = random.randint(0, 1)
        # 50-50 chance of sorting by new or hot
        if hot_or_new == 0:
            return sub.display_name, sub.hot(limit=10)
        else:
            return sub.display_name, sub.new(limit=10)
    raise Exception("Sub couldn't be read")


def login_as(username):
    """
    Returns the reddit instance corresponding to the user.
    Only allows `Zokalyx` and `theconfluenceBOT`.
    """
    if username == "theconfluenceBOT":
        return praw.Reddit(
            client_id="0S1WpGMeuyOQkg",
            client_secret=env["BOT_TOKEN"],
            username="theconfluenceBOT",
            password=env["BOT_PASS"],
            user_agent="The Confluence Bot"
        )
    elif username == "Zokalyx":
        return praw.Reddit(
            client_id="xskzciRXmoU-JA",
            client_secret=env["ZOKA_TOKEN"],
            username="Zokalyx",
            password=env["ZOKA_PASS"],
            user_agent="The Confluence Bot"
        )
    else:
        print("Unknown user!")
        raise Exception("unknown user error")


def post_results(reddit, run, ret, summary, d_arr, d_dep):
    """
    Posts results to theconfluenceBOT's profile page.
    """

    # Setup
    reddit.validate_on_submit = True
    profile = reddit.subreddit("U_theconfluenceBOT")
    faq = reddit.submission("ks2m4w")

    # Remove duplicates
    posts = profile.new(limit=10)
    for post in posts:
        if f"Run {run}" in post.title:
            post.delete()
        elif post.stickied and "summary" in post.title:
            post.mod.sticky(False)

    # Unpin FAQ
    faq.mod.sticky(False)

    # Post
    profile.submit(f"Run {run} arrivals", d_arr)
    profile.submit(f"Run {run} flairs", d_dep)
    to_pin = profile.submit(f"Run {run} summary - {ret}% retention", summary)

    # Pin FAQ and summary
    faq.mod.sticky(True)
    to_pin.mod.sticky(True)


if __name__ == "__main__":
    main()


# TESTS
def login_test():
    print(login_as("Zokalyx"))
    print(login_as("theconfluenceBOT"))
    print(login_as("asd"))
