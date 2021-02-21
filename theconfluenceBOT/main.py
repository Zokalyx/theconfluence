import praw
from praw.models import MoreComments
import random
import time
import math
from os import environ as env

botAccounts = ["AutoModerator"]
reddit = praw.Reddit(client_id="0S1WpGMeuyOQkg",
                     client_secret=env["BOT_TOKEN"],
                     username="theconfluenceBOT",
                     password=env["BOT_PASS"],
                     user_agent="theconfluenceBOT")

while True:
    found_new_message = False

    for unread in reddit.inbox.unread(limit=1):
        author = unread.author
        unread.mark_read()
        found_new_message = True

    if found_new_message:
        if author.name not in ["Zokalyx", "MoscaMye", "theconfluencer"]:
            continue
    else:
        continue

#   -------------------------------------------- Sending initial message ----------------------------------------------

    author.message("Working on it", "Message received, I'm processing the data. I'll message you again once I'm done!")
    print("Sending 1st Message to " + author.name)

#     ------------------------------------------- Get last run's users -------------------------------------------

    # reddit = ZOKALYX'S ACCOUNT
    reddit = praw.Reddit(client_id="xskzciRXmoU-JA",
                         client_secret=env["ZOKA_TOKEN"],
                         username="Zokalyx",
                         password=env["ZOKA_PASS"],
                         user_agent="theconfluenceBOT")

    conbot = reddit.subreddit("U_theconfluenceBOT")
    newest = conbot.new(limit=10)
    for post in newest:
        if "Last" in post.title:
            auxlastrundata = post.selftext.split("\n\n")
            lastrundata = []
            lastruncopy = []
            for entry in auxlastrundata:
                lastrundata.append([entry.split()[0], entry.split()[1]])
                lastruncopy.append([entry.split()[0], entry.split()[1]])
            lastpop = len(lastrundata)


            break

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
    runs = sub.hot(limit=5)
    posts = sub.new(limit=500)
    for run in runs:
        if run.stickied:
            if "Run" in run.title or "Run!" in run.title:
                print(run.title)
                last_run_start = run.created_utc

                string = run.title

                string_arr = string.split()

                if "Run" in string_arr:
                    index = string_arr.index("Run") - 1
                elif "Run!" in string_arr:
                    index = string_arr.index("Run!") - 1

                lastrun = string_arr[index][:len(string_arr[index]) - 2]

                break

    for post in posts:
        if post.created_utc > smm:

            print(post.title)
            print(str(math.trunc(10 * ((s - post.created_utc) / (s - smm) * 100)) / 10) + "%")

            if post.created_utc > last_run_start:

                """
                if post.author == "yo-whatupmofo":
                    ind = reference_list.index("Or-Your-Money-Back")
                    departures[ind][1] = False
                """

                if post.author in reference_list:
                    ind = reference_list.index(post.author)
                    departures[ind][1] = False

            comments = post.comments
            comments.replace_more(limit=None)

            for comment in comments.list():

                if comment.created_utc > last_run_start:

                    """
                    if comment.author == "yo-whatupmofo":
                        ind = reference_list.index("Or-Your-Money-Back")
                        departures[ind][1] = False
                    """

                    if comment.author in reference_list:
                        ind = reference_list.index(comment.author)
                        departures[ind][1] = False

    # Logic
    for n in reversed(departures):
        if n[1]:
            lastrundata.pop(int(n[0])-1)
        else:
            lastruncopy.pop(int(n[0])-1)

#  ------------------------------------------- Random redditor selection -------------------------------------------
# Main


    def get_amount(amount):

        randoms = []
        count = 0
        reached_count = False
        while not reached_count:
            res = random_redditor()
            if res[0] not in botAccounts and res[0] not in reference_list:
                randoms.append(res)
                count += 1
                print(res[0])
                print(str(round(count / amount * 100)) + "%")
                if count == amount:
                    reached_count = True

        return randoms


    def random_redditor():

        ran = random.randint(0, 9)
        allow_op = False

        if ran < 8:
            # 80% chance of random subreddit
            sub = reddit.random_subreddit(nsfw=False)
            ran2 = random.randint(0, 1)
            if ran2 == 0:
                posts = sub.hot(limit=10)
            else:
                posts = sub.new(limit=10)

        elif ran == 8:
            # 10% chance of r/popular
            sub = reddit.subreddit("popular")
            posts = sub.new(limit=10)

        else:
            # 10% chance of r/all
            sub = reddit.subreddit("all")
            posts = sub.hot(limit=10)
            ran2 = random.randint(0,3)
            if ran2 == 0:
                allow_op = True

        post_list = []
        for post in posts:
            post_list.append(post)

        max_post = len(post_list)
        if max_post > 10:
            max_post = 10

        ran = random.randrange(max_post)
        post = post_list[ran]

        if allow_op:
            commenter = post.author
            is_op = True
        else:
            result = get_random_commenter(post)
            commenter = result[0]
            is_op = result[1]

        if commenter:
            return [commenter.name, post.subreddit.display_name, post.id, sub.display_name, is_op]
        else:
            random_redditor()


    def get_random_commenter(post):

        com_list = []
        for com in post.comments:
            if isinstance(com, MoreComments) or not com.author:
                continue
            com_list.append(com)

        max_com = len(com_list)
        if max_com > 20:
            max_com = 20

        # Defaults to OP when there are no comments
        if max_com == 0:
            commenter = post.author
            is_op = True
        else:
            ran = random.randrange(max_com)
            commenter = com_list[ran].author
            is_op = False

        return [commenter, is_op]


    def obtain_random_text(starting, amount, extra):

        names = get_amount(amount + extra)

        details = False
        text = ""
        for i in range(amount):
            u = names[i]
            text += str(starting + i) + " " + str(u[0])
            if details:
                text += " r/" + str(u[1]) + " [Post](https://redd.it/" + str(u[2]) + ")"
                if u[4]:
                    text += " (OP)"
            if u != names[-1]:
                text += "\n\n"

        details = True
        text2 = ""
        for i in range(amount):
            u = names[i]
            text2 += str(starting + i) + " " + str(u[0])
            if details:
                text2 += " r/" + str(u[1]) + " [Post](https://redd.it/" + str(u[2]) + ")"
                if u[4]:
                    text2 += " (OP)"
            text2 += "\n\n"

        text2 += "\n\n**Extra random users if you need to add or replace some:**\n\n"

        for i in range(amount, amount + extra):
            u = names[i]
            text2 += str(u[0])
            if details:
                text2 += " r/" + str(u[1]) + " [Post](https://redd.it/" + str(u[2]) + ")"
                if u[4]:
                    text2 += " (OP)"
            if u != names[-1]:
                text2 += "\n\n"

        return [text, text2]


    we_need = lastpop - len(lastrundata)
    starting = len(lastrundata) + 1
    newbs = obtain_random_text(starting, we_need, 10)

# ------------------------------------------ Creating text posts ---------------------------------------------------

    reddit = None

    summary_text = "**Departures:**\n\n"
    for user in lastruncopy:
        summary_text += str(user[0]) + " " + str(user[1]) + "\n\n"
    summary_text += "**Arrivals:**\n\n"
    summary_text += newbs[0]

    detailed_text = newbs[1]

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
                         user_agent="theconfluenceBOT")
    reddit.validate_on_submit = True
    profile = reddit.subreddit("U_theconfluenceBOT")

    reddit.submission("ks2m4w").mod.sticky(False)

    for post in profile.new(limit=10):
        if "Run " + str(newrun) in post.title:
            post.delete()
        elif "summary" in post.title and post.stickied:
            post.mod.sticky(False)

# ----------------------------------------- Posting Data -----------------------------------------------------------

    print("Posting submissions")
    profile.submit("Run " + str(newrun) + " detailed arrivals + extra randoms", detailed_text)
    profile.submit("Run " + str(newrun) + " new flairs for old members", new_flairs)
    to_pin = profile.submit("Run " + str(newrun) + " summary - " + str(retention) + "% retention", summary_text)

    reddit.submission("ks2m4w").mod.sticky(True)
    to_pin.mod.sticky(True)

# -------------------------------------------- Sending final message ----------------------------------------------

    author.message("Results ready", "I have finished processing the data, go to my profile page to see the results."
                                    " See you next time :)")
    print("Sending 2nd Message to " + author.name)

