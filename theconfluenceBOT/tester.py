import praw
from praw.models import MoreComments
from prawcore.exceptions import Forbidden
import random
import time
import math
from os import environ as env

botAccounts = ["AutoModerator"]
reddit = praw.Reddit(client_id="0S1WpGMeuyOQkg",
                     client_secret=env["BOT_TOKEN"],
                     username="theconfluenceBOT",
                     password=env["BOT_PASS"],
                     user_agent="The Confluence Bot")

while True:

    found_new_message = False

    for unread in reddit.inbox.unread(limit=1):
        author = unread.author
        unread.mark_read()
        found_new_message = True

    if found_new_message:
        if author.name != "Zokalyx":
            continue
    else:
        continue

#   -------------------------------------------- Sending initial message ----------------------------------------------

    # author.message("[TEST] Working on it", "I'm checking for actual departures")
    print("Sending 1st Message to " + author.name)

    error_occured = False

    while True:

        try:

        #     ------------------------------------------- Get last run's users -------------------------------------------

            # assert error_occured

            # reddit = ZOKALYX'S ACCOUNT
            reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                                client_secret=env["ZOKA_TOKEN"],
                                username="Zokalyx",
                                password=env["ZOKA_PASS"],
                                user_agent="The Confluence Bot")

            conbot = reddit.subreddit("U_theconfluenceBOT")
            newest = conbot.new(limit=10)
            for post in newest:
                if "Last" in post.title:
                    # auxlastrundata = post.selftext.split("\n\n")
                    with open("results.txt") as f:
                        auxlastrundata = f.read().splitlines()
                    lastrundata = []
                    lastruncopy = []
                    for entry in auxlastrundata:
                        lastrundata.append([entry.split()[0], entry.split()[1]])
                        lastruncopy.append([entry.split()[0], entry.split()[1]])
                    lastpop = len(lastrundata)


                    break

            print(lastrundata)

        #    ------------------------------------------- Departure calculator -------------------------------------------

            departures = []
            depar_text = ""
            reference_list = []
            for row in lastrundata:
                reference_list.append(row[1])
                departures.append([row[0], True])

            s = time.time()  # time
            smm = s - 1.5*1296000  # time minus three weeks
            last_run_start = 0
            sub = reddit.subreddit("TheConfluence")
            # runs = sub.hot(limit=5)
            posts = sub.new(limit=500)

            runs = [reddit.submission(id="pz5258")]

            for run in runs:
                if run.stickied or True:
                    if "Run" in run.title or "Run!" in run.title or "run" in run.title or "run!" in run.title:
                        print(run.title)
                        last_run_start = run.created_utc

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

                        lastrun = string_arr[index][:len(string_arr[index]) - 2]

                        break

            top_limit_run = reddit.submission(id="q2jf11")
            top_time = top_limit_run.created_utc

            for post in posts:
                if post.created_utc > top_time:
                    continue
                elif post.created_utc > smm:

                    print(post.title)
                    print(str(math.trunc(10 * ((top_time - post.created_utc) / (top_time - smm) * 100)) / 10) + "%")

                    if post.created_utc > last_run_start and post.created_utc < top_time:

                        if post.author in reference_list:
                            ind = reference_list.index(post.author)
                            departures[ind][1] = False

                    comments = post.comments
                    comments.replace_more(limit=None)

                    for comment in comments.list():

                        if comment.created_utc > last_run_start  and post.created_utc < top_time:

                            if comment.author in reference_list:
                                ind = reference_list.index(comment.author)
                                departures[ind][1] = False
                else:
                    break

            # Logic
            for n in reversed(departures):
                if n[1]:
                    lastrundata.pop(int(n[0])-1)
                else:
                    lastruncopy.pop(int(n[0])-1)


        # ------------------------------------------ Creating text posts ---------------------------------------------------

            reddit = None

            summary_text = "**Departures:**\n\n"
            for user in lastruncopy:
                summary_text += str(user[0]) + " " + str(user[1]) + "\n\n"

            retention = round(len(lastrundata) / lastpop * 10000) / 100

            newrun = int(lastrun) + 1

            new_flairs = ""
            for old in lastrundata:
                old_no = int(old[0])
                new_no = lastrundata.index(old) + 1
                diff = old_no - new_no
                new_flairs += str(old_no) + " → " + str(new_no) + " " + old[1]
                if diff == 0:
                    extra_text = " (=)"
                else:
                    extra_text = " (-" + str(diff) + ")"
                new_flairs += extra_text
                if old != lastrundata[-1]:
                    new_flairs += "\n\n"

        # ----------------------------------------- Deleting duplicates -----------------------------------------------------

            reddit = praw.Reddit(client_id="0S1WpGMeuyOQkg",
                                client_secret=env["BOT_TOKEN"],
                                username="theconfluenceBOT",
                                password=env["BOT_PASS"],
                                user_agent="The Confluence Bot")
            reddit.validate_on_submit = True
            profile = reddit.subreddit("U_theconfluenceBOT")

        # -------------------------------------------- Sending final message ----------------------------------------------

            author.message("Results ready", summary_text)
            print("Sending 2nd Message to " + author.name)

            break

        except Exception as e:
            if error_occured:
                print("Two errors in a row: Stopping")
                # author.message("Can't fix it", "Something went wrong again, I'm stopping now. Sorry!")
                print("Sending 2nd error message to " + author.name)
                break
            else:
                error_occured = True
                print("Trying again")
                # author.message("Oops...", "Something went wrong, I'm trying again.")
                print("Sending 1st error message to " + author.name)
            print("Error:", e)

