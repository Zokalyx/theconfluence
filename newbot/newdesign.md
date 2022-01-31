# New bot design

With the power of databases, the bot could be significantly improved.
These are my ideas as to how to implement the new bot.

## Schemas

The bot would continuously check comments and posts from the Confluence (as streams) and save them in the database.

Tables would consist of:

### Submissions

- Database ID
- Submission ID
- Author ID [Foreign]
- Name **(What is this? I didn't understand the [docs](https://praw.readthedocs.io/en/latest/code_overview/models/submission.html#praw.models.Submission.fullname))**
- Title
- Body
- URL **(can be shortened if necessary, eg: redd.it/haucpf. If this is "too" shortened, a regular URL can omit the post title, eg: https://www.reddit.com/comments/haucpf)**
- Creation date
- Database insertion date

### Comments

- Database ID
- Comment ID
- Submission (Post) ID [Foreign]
- Author ID [Foreign]
- Body
- Parent comment/post ID
- URL **(Example: https://www.reddit.com/comments/haucpf/_/fv5lwph/?context=3. `context` is the amount of parent comments to show | Currently not in DB)**
- Creation date
- Database insertion date

### Redditors

- Database ID
- User ID
- Username
- Database insertion date
- URL **(Currently not in DB)**
- Last activity date **(Currently not in DB)**
- Oldest activity date **(Currently not in DB)**
- Oldest comment ID [Foreign] **(Currently not in DB)**
- Oldest post ID [Foreign] **(Currently not in DB)**
- Member status **(Currently not in DB)**
- Flair number **(Currently not in DB)**

## Arrivals

### Relevant files: [`redditorqueue.py`](https://github.com/Zokalyx/theconfluence/blob/main/newbot/redditorqueue.py)

Following the [algorithm](https://github.com/Zokalyx/theconfluence/blob/main/docs/theconfluenceBOT.md), the bot would have a **queue** of 200 redditors in memory, adding a new one (and popping another one) every 1 minute. This way, whenever the bot is called for its duty, it will readily return 200 redditors. With this frequency, every redditor in the list would have been picked in the last 3 hours or so. This frequency can be adjusted if necessary.

To reduce performance as much as possible, this can be scheduled to start 24h before a run is supposed to happen (leaving some margin in case u/theconfluencer decides to do the run early).

Even when the bot is called, redditors in the queue don't have to be marked as "members" in the database. This should be done later, read [updating the database](#updating-the-database).

## Departures

The bot should always keep track of what was the last run post (`lastrun`). Whenever the bot is called by u/theconfluencer, the following should happen ("pythonic pseudocode"):

```py
last_run_date = lastrun.date()

departures = []

for redditor in redditors:
    # Only focus on current members
    # This would be done with SQL
    if not redditor.is_member:
        continue

    # If last activity of redditor was before the last run post,
    # that means that they were must be kicked.
    # But don't remove their member status,
    # u/theconfluencer has the last word
    if redditor.last_activity_date > last_run_date:
        departures.append(redditor)

# This would be posted
print(departures)
```

No database updates should have happend by now, because the ultimate source of modifications are posts by `u/theconfluencer`.

## Updating the database

While the bot is continually scanning for posts, it will find the one corresponding to the new run.

- When this happens, save that post as the new `lastrun`.
- Scrape the post for the list of departures and arrivals.
- Update the database, removing the membership of those in departures.
- Update the database, giving the membership to those in arrivaly. Possibly create new entries in the database if user did not exist.
- Update the flair numbers of every user (arrivals is easy, just use the numbers in the post; it is for existing users that some math has to be done).

Additionally, the bot might also update the flair numbers, add and remove users from the sub. This should, at least for some time, be an optional feature until it is well tested and accepted by u/theconfluencer.

## Calling the bot

The bot should only accept calls from whitelisted members. This should be the order of events.

- Bot is messaged by a whitelisted user.
- Bot posts the following:
  - Summary: contains retention, departures and arrivals.
  - Detailed arrivals: contains the original post or comment the redditor was selected from. This should also contain a few extra randoms in case u/theconfluencer needs to replace some user for any reason.
- u/theconfluencer posts the weekly run post.
- Bot posts the new flair numbers for the convenience of `u/theconfluencer`
- If a new or the original DM or a comment posted on this last post contains some special keyword, make the bot update the flairs. Also add the option to add and remove users from the subreddit.

## Note

I have a `posts.csv` file containing many old posts, going back to the start of the subreddit. These have been obtained by using the technique of scanning up to 1000 posts from individual users of the subreddit (so I can't guarantee I have them all, because there's probably at least one user that has more than 1000 posts since their oldest post in the sub). But I can send it if it's useful.

If this technique is going to be used, the full list of members can be used - they can be obtained by scraping u/theconfluencer's posts or by using `probyuser.csv` (probably better).
