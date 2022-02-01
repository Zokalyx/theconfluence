import DbHandler
import praw
import logging
from datetime import datetime
from praw.models import Redditor
from os import environ
from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)

load_dotenv()

db = DbHandler.DbHandler()
"""
reddit = praw.Reddit(
    client_id=environ["ZOKA_ID"],
    client_secret=environ["ZOKA_TOKEN"],
    username="Zokalyx",
    password=environ["ZOKA_PASS"],
    user_agent="theconfluenceBOT"
)
"""
lastRunTime = datetime(2022, 1, 31)

def remind() -> None:
    """
        Reminds all subscribed users to post or comment if they havent't
        participated in the subreddit since the last run started

        TODO: Not final.
    """
    
    # TODO: Implement reminder filter here, and also just select members
    query = "SELECT redditId, name FROM redditors WHERE name = 'Zokalyx'"
    redditIds = db.fetchAll(query, ())

    for (redditId, name) in redditIds:
        
        # Get latest comment time
        query = "SELECT createdUtc FROM comments WHERE authorId = %s ORDER BY createdUtc DESC LIMIT 1"
        lastCommentTime = db.fetchAll(query, (redditId,))

        # Get latest post time
        query = "SELECT createdUtc FROM submissions WHERE authorId = %s ORDER BY createdUtc DESC LIMIT 1"
        lastPostTime = db.fetchAll(query, (redditId,))

        # Entries might be null
        noTime = False
        # User never interacted
        if not lastCommentTime and not lastPostTime:
            noTime = True
        # User posted but didn't comment
        elif not lastCommentTime and lastPostTime:
            lastTime = lastPostTime[0][0]
        # User commented but didn't post
        elif lastCommentTime and not lastPostTime:
            lastTime = lastCommentTime[0][0]
        # User commented and posted, pick latest
        else:
            lastTime = max(lastCommentTime[0][0], lastPostTime[0][0])

        reminder = False

        # No interactions ever
        if noTime:
            reminder = True
        # Else compare times
        elif lastTime < lastRunTime:
            reminder = True

        # Send reminder
        if reminder:
            LOGGER.info(f"Sending reminder to {name}")
            # redditor: Redditor = reddit.redditor(redditId)
            # redditor.message("Friendly reminder", "You haven't posted or commented in The Confluence since the last run started.\n\nReply with \"stop\" to stop receiving reminders.")

remind()